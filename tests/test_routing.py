"""Routing v1 vignettes from system-design §7–8 and agents/*.md."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestrator.routing import classify, extract_signals, route  # noqa: E402


class RoutingVignettes(unittest.TestCase):
    def test_index_error_snippet_routes_debug(self):
        utterance = (
            "I get IndexError on this line:\n"
            "for i in range(len(a)+1):\n    print(a[i])"
        )
        decision = route(utterance)
        self.assertEqual(decision.mode, "debug")
        self.assertEqual(decision.classification, "debug")
        self.assertTrue(decision.signals.crash_language)

    def test_traceback_routes_debug(self):
        utterance = """Traceback (most recent call last):
  File "app.py", line 3, in <module>
    main()
ValueError: invalid"""
        decision = route(utterance)
        self.assertEqual(decision.mode, "debug")
        self.assertTrue(decision.signals.has_stack_trace)

    def test_theory_without_failure_routes_concept(self):
        decision = route("What is a deadlock?")
        self.assertEqual(decision.mode, "concept")
        self.assertEqual(decision.classification, "concept")

    def test_comparison_routes_concept(self):
        decision = route("Redis vs Memcached for caching?")
        self.assertEqual(decision.mode, "concept")

    def test_stuck_without_error_routes_mentor(self):
        decision = route("I'm stuck on how to approach this graph problem.")
        self.assertEqual(decision.mode, "mentor")
        self.assertEqual(decision.classification, "guided_work")

    def test_partial_code_approach_routes_mentor(self):
        decision = route(
            "Is this the right approach?\n```python\ndef two_sum(nums, target):\n    pass\n```"
        )
        self.assertEqual(decision.mode, "mentor")

    def test_theory_plus_traceback_prefers_debug(self):
        utterance = """What is a race condition? I also get this:
Traceback (most recent call last):
  File "worker.py", line 9
RuntimeError"""
        decision = route(utterance)
        self.assertEqual(decision.mode, "debug")
        self.assertEqual(decision.secondary, "concept")

    def test_pytest_failure_routes_debug(self):
        decision = route("FAILED tests/test_api.py::test_health - AssertionError")
        self.assertEqual(decision.mode, "debug")
        self.assertTrue(decision.signals.test_failure)

    def test_classify_meta(self):
        signals = extract_signals("How do I set hint level in deep tutor?")
        self.assertEqual(classify(signals), "meta")

    def test_named_exception_as_concept_stays_concept(self):
        decision = route("What is IndexError?")
        self.assertEqual(decision.mode, "concept")


if __name__ == "__main__":
    unittest.main()
