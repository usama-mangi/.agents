#!/usr/bin/env python3
"""Tests for memory-skill graph.py — behavior, not implementation."""

import json
import os
import subprocess
import sys
import tempfile
import unittest

GRAPH = os.path.join(os.path.dirname(__file__), "..", "scripts", "graph.py")


def run_graph(*args, workdir=None):
    if workdir:
        cmd = [sys.executable, GRAPH, "--dir", workdir, *args]
    else:
        cmd = [sys.executable, GRAPH, *args]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=workdir)
    return r


def init_store(d):
    run_graph("init", workdir=d)


class TestGraphBasics(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        init_store(self.d)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.d, ignore_errors=True)

    def test_init_creates_empty_store(self):
        r = run_graph("get", "--keyword", "nothing", workdir=self.d)
        self.assertIn(r.returncode, (0, 1))
        with open(os.path.join(self.d, "memory-graph.json")) as f:
            data = json.load(f)
        self.assertEqual(data["entities"], {})
        self.assertEqual(data["relations"], [])

    def test_add_and_get_entity(self):
        r = run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "Joint Embedding Predictive Architecture.", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        r = run_graph("get", "--entity", "JEPA", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        obj = json.loads(r.stdout)
        self.assertEqual(obj["entity"], "JEPA")
        self.assertEqual(obj["entityType"], "ML/AI")
        self.assertEqual(len(obj["observations"]), 1)
        self.assertEqual(obj["observations"][0]["text"], "Joint Embedding Predictive Architecture.")

    def test_add_duplicate_fails(self):
        run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "x", workdir=self.d)
        r = run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "y", workdir=self.d)
        self.assertNotEqual(r.returncode, 0)

    def test_get_keyword_finds_entity(self):
        run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "Joint Embedding Predictive Architecture.", workdir=self.d)
        r = run_graph("get", "--keyword", "JEPA", workdir=self.d)
        obj = json.loads(r.stdout)
        self.assertTrue(any(e["entity"] == "JEPA" for e in obj["entities"]))

    def test_update_append_adds_observation(self):
        run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "First.", workdir=self.d)
        r = run_graph("update", "--entity", "JEPA", "--text", "Second.", "--append", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        r = run_graph("get", "--entity", "JEPA", workdir=self.d)
        obj = json.loads(r.stdout)
        texts = [o["text"] for o in obj["observations"]]
        self.assertIn("First.", texts)
        self.assertIn("Second.", texts)

    def test_update_replace_observations(self):
        run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "First.", workdir=self.d)
        r = run_graph("update", "--entity", "JEPA", "--text", "Replaced.", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        r = run_graph("get", "--entity", "JEPA", workdir=self.d)
        obj = json.loads(r.stdout)
        texts = [o["text"] for o in obj["observations"]]
        self.assertEqual(texts, ["Replaced."])

    def test_relate_and_get_relations(self):
        run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "x", workdir=self.d)
        run_graph("add", "--entity", "EBM", "--type", "Mathematics", "--text", "y", workdir=self.d)
        r = run_graph("relate", "--from", "JEPA", "--to", "EBM", "--type", "builds-on", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        r = run_graph("get", "--entity", "JEPA", workdir=self.d)
        obj = json.loads(r.stdout)
        self.assertTrue(any(rel["type"] == "builds-on" for rel in obj["relations"]))

    def test_remove_entity_clears_relations(self):
        run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "x", workdir=self.d)
        run_graph("add", "--entity", "EBM", "--type", "Mathematics", "--text", "y", workdir=self.d)
        run_graph("relate", "--from", "JEPA", "--to", "EBM", "--type", "builds-on", workdir=self.d)
        r = run_graph("remove", "--entity", "JEPA", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        r = run_graph("get", "--entity", "EBM", workdir=self.d)
        obj = json.loads(r.stdout)
        self.assertEqual([rel for rel in obj["relations"] if rel["from"] == "JEPA"], [])

    def test_list_returns_entities(self):
        run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "x", workdir=self.d)
        r = run_graph("list", workdir=self.d)
        self.assertIn("JEPA", r.stdout)


class TestEnrichment(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        init_store(self.d)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.d, ignore_errors=True)

    def test_add_with_source_confidence(self):
        r = run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "x", "--source", "test.md", "--confidence", "high", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        r = run_graph("get", "--entity", "JEPA", workdir=self.d)
        obj = json.loads(r.stdout)
        obs = obj["observations"][0]
        self.assertEqual(obs["source"], "test.md")
        self.assertEqual(obs["confidence"], "high")

    def test_update_append_with_source_confidence(self):
        run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "x", workdir=self.d)
        r = run_graph("update", "--entity", "JEPA", "--text", "y", "--append", "--source", "test.md", "--confidence", "medium", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        r = run_graph("get", "--entity", "JEPA", workdir=self.d)
        obj = json.loads(r.stdout)
        self.assertEqual(len(obj["observations"]), 2)
        self.assertEqual(obj["observations"][1]["source"], "test.md")
        self.assertEqual(obj["observations"][1]["confidence"], "medium")


class TestTraverse(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        init_store(self.d)
        run_graph("add", "--entity", "A", "--type", "ML/AI", "--text", "a", workdir=self.d)
        run_graph("add", "--entity", "B", "--type", "ML/AI", "--text", "b", workdir=self.d)
        run_graph("add", "--entity", "C", "--type", "ML/AI", "--text", "c", workdir=self.d)
        run_graph("relate", "--from", "A", "--to", "B", "--type", "builds-on", workdir=self.d)
        run_graph("relate", "--from", "B", "--to", "C", "--type", "similar-to", workdir=self.d)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.d, ignore_errors=True)

    def test_traverse_depth_1(self):
        r = run_graph("traverse", "--entity", "A", "--depth", "1", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        obj = json.loads(r.stdout)
        names = {n["entity"] for n in obj["neighborhood"]}
        self.assertIn("B", names)
        self.assertNotIn("C", names)

    def test_traverse_depth_2(self):
        r = run_graph("traverse", "--entity", "A", "--depth", "2", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        obj = json.loads(r.stdout)
        names = {n["entity"] for n in obj["neighborhood"]}
        self.assertIn("B", names)
        self.assertIn("C", names)

    def test_traverse_depth_0(self):
        r = run_graph("traverse", "--entity", "A", "--depth", "0", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        obj = json.loads(r.stdout)
        names = {n["entity"] for n in obj["neighborhood"]}
        self.assertNotIn("B", names)
        self.assertIn("A", names)


class TestCheck(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        init_store(self.d)
        run_graph("add", "--entity", "A", "--type", "Career", "--text", "ATS rejects 75% of resumes.", "--source", "x", workdir=self.d)
        run_graph("add", "--entity", "B", "--type", "Career", "--text", "ATS rejection rate is a myth.", "--source", "y", workdir=self.d)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.d, ignore_errors=True)

    def test_check_finds_contradiction(self):
        r = run_graph("check", "--entity", "A", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        obj = json.loads(r.stdout)
        self.assertTrue(len(obj["contradictions"]) > 0)

    def test_check_no_contradiction(self):
        r = run_graph("check", "--entity", "A", workdir=self.d)
        # Even if it finds a contradiction in B, check on A should surface it
        self.assertIn("contradictions", r.stdout)


class TestSuggest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        init_store(self.d)
        run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "x", workdir=self.d)
        run_graph("add", "--entity", "EBM", "--type", "ML/AI", "--text", "y", workdir=self.d)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.d, ignore_errors=True)

    def test_suggest_returns_candidates(self):
        r = run_graph("suggest", "--entity", "JEPA", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        obj = json.loads(r.stdout)
        self.assertIn("suggestions", obj)
        if obj["suggestions"]:
            self.assertIn("to", obj["suggestions"][0])
            self.assertIn("reason", obj["suggestions"][0])


class TestSynthesize(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        init_store(self.d)
        run_graph("add", "--entity", "JEPA", "--type", "ML/AI", "--text", "Joint Embedding Predictive Architecture.", workdir=self.d)
        run_graph("add", "--entity", "EBM", "--type", "Mathematics", "--text", "Energy-Based Models.", workdir=self.d)
        run_graph("relate", "--from", "JEPA", "--to", "EBM", "--type", "builds-on", workdir=self.d)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.d, ignore_errors=True)

    def test_synthesize_returns_summary(self):
        r = run_graph("synthesize", "--entity", "JEPA", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        obj = json.loads(r.stdout)
        self.assertIn("summary", obj)
        self.assertTrue(len(obj["summary"]) > 0)


class TestStale(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        init_store(self.d)
        run_graph("add", "--entity", "JEPA", "--type", "Career", "--text", "x", workdir=self.d)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.d, ignore_errors=True)

    def test_stale_returns_list(self):
        r = run_graph("stale", "--days", "0", workdir=self.d)
        self.assertEqual(r.returncode, 0)
        obj = json.loads(r.stdout)
        self.assertIn("stale", obj)


if __name__ == "__main__":
    unittest.main(verbosity=2)
