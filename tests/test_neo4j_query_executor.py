"""
Test suite for Neo4j Query Executor - Interactive Development + Automated Confidence Processing

This test suite follows evaluation-first development principles:
- Tests define success criteria before implementation
- Tests must FAIL initially to prove they test the right functionality
- Implementation serves the tests, not vice versa
"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class TestEvalCommandInfrastructure(unittest.TestCase):
    """Test the /eval command infrastructure (Part 1)"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.commands_dir = Path(self.temp_dir) / ".claude" / "commands"
        self.evals_dir = Path(self.temp_dir) / "evals"

        # Create directory structure
        self.commands_dir.mkdir(parents=True)
        self.evals_dir.mkdir(parents=True)

        # Create test folders
        for folder in ["todo", "review", "passed", "failed", "blocked"]:
            (self.evals_dir / folder).mkdir()

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_eval_command_file_exists(self):
        """Test that the /eval command file exists with correct structure"""
        # Check in the real project directory, not test temp dir
        real_commands_dir = Path(__file__).parent.parent / ".claude" / "commands"
        eval_command_file = real_commands_dir / "eval.md"

        # Should exist
        self.assertTrue(eval_command_file.exists(), "eval.md command file should exist")

        # Should have proper frontmatter
        content = eval_command_file.read_text()
        self.assertIn("description: Develop Cypher query for evaluation test", content)
        self.assertIn("arguments: test_number", content)

        # Should have workflow documentation
        self.assertIn("Opens EVAL-NN test file", content)
        self.assertIn("interactive query development", content)

    def test_eval_command_discovers_test_files(self):
        """Test that eval command can discover test files by ID"""
        # Create test files in different folders
        test_file_1 = self.evals_dir / "todo" / "EVAL-05.md"
        test_file_2 = self.evals_dir / "review" / "EVAL-42.md"

        test_file_1.write_text("# EVAL-05: Test content")
        test_file_2.write_text("# EVAL-42: Another test")

        # This will FAIL initially - implementation needed
        from scripts.neo4j_query_executor import find_evaluation_test

        # Should find exact matches
        found_05 = find_evaluation_test("05", self.evals_dir)
        self.assertEqual(found_05, test_file_1)

        found_42 = find_evaluation_test("42", self.evals_dir)
        self.assertEqual(found_42, test_file_2)

        # Should handle EVAL- prefix
        found_eval_05 = find_evaluation_test("EVAL-05", self.evals_dir)
        self.assertEqual(found_eval_05, test_file_1)

    def test_eval_command_aborts_on_multiple_matches(self):
        """Test that eval command aborts if multiple test files found"""
        # Create duplicate test files (should never happen in practice)
        test_file_1 = self.evals_dir / "todo" / "EVAL-05.md"
        test_file_2 = self.evals_dir / "review" / "EVAL-05.md"

        test_file_1.write_text("# EVAL-05: Test content")
        test_file_2.write_text("# EVAL-05: Duplicate test")

        # This will FAIL initially - implementation needed
        from scripts.neo4j_query_executor import find_evaluation_test

        with self.assertRaises(ValueError) as context:
            find_evaluation_test("05", self.evals_dir)

        self.assertIn("Multiple test files found", str(context.exception))

    def test_eval_command_loads_business_context(self):
        """Test that eval command loads business context from evaluation_tests.md"""
        # Create evaluation_tests.md with sample data
        eval_tests_content = """
| Test# | Theme | Prompt | Expected Response | Search Category |
|-------|-------|--------|-------------------|-----------------|
| EVAL-05 | Identity | Find person named John | Person records | People |
| EVAL-42 | Communication | Phone call analysis | Call records | Communications |
        """

        (self.evals_dir / "evaluation_tests.md").write_text(eval_tests_content)

        # This will FAIL initially - implementation needed
        from scripts.neo4j_query_executor import load_business_context

        context_05 = load_business_context("05", self.evals_dir)
        self.assertEqual(context_05["theme"], "Identity")
        self.assertEqual(context_05["prompt"], "Find person named John")
        self.assertEqual(context_05["expected_response"], "Person records")

        context_42 = load_business_context("42", self.evals_dir)
        self.assertEqual(context_42["theme"], "Communication")
        self.assertEqual(context_42["prompt"], "Phone call analysis")


class TestConfidenceProcessor(unittest.TestCase):
    """Test the automated confidence processor (Part 2)"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.evals_dir = Path(self.temp_dir) / "evals"

        # Create directory structure
        for folder in ["todo", "review", "passed", "failed", "blocked"]:
            (self.evals_dir / folder).mkdir(parents=True)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_confidence_processor_parses_new_format(self):
        """Test that confidence processor parses new simple format"""
        # Create test file with new confidence format
        test_file = self.evals_dir / "review" / "EVAL-05.md"
        test_content = """
# EVAL-05: Test Query

## Implementation

### Query
```cypher
MATCH (p:Person) WHERE p.name = "John" RETURN p
```

## Confidence Assessment

**Query Results**: Found 3 person records
**Business Question**: "Find person named John"
**Assessment**: Does this correctly answer the business question?

✅ **Y** = 80% confidence (auto-promotes to PASSED)

**Confidence**: 80% → Auto-promote to PASSED
        """
        test_file.write_text(test_content)

        # This will FAIL initially - implementation needed
        from scripts.neo4j_query_executor import ConfidenceProcessor

        processor = ConfidenceProcessor(self.evals_dir)
        confidence_data = processor.parse_confidence_section(test_file)

        self.assertIsNotNone(confidence_data)
        self.assertEqual(confidence_data["percentage"], 80)
        self.assertEqual(confidence_data["action"], "Auto-promote to PASSED")

    def test_confidence_processor_ignores_legacy_format(self):
        """Test that confidence processor ignores complex legacy calculations"""
        # Create test file with legacy confidence format
        test_file = self.evals_dir / "review" / "EVAL-42.md"
        test_content = """
# EVAL-42: Legacy Test

## Confidence Calculation

Expected: [count: 12, score: 5.37]
Actual:   [count: 12, score: 5.37]

Confidence = (count_accuracy × 0.7) + (score_similarity × 0.3)
           = (12/12 × 0.7) + (5.37/5.37 × 0.3)
           = 100% → Auto-promote to PASSED
        """
        test_file.write_text(test_content)

        # This will FAIL initially - implementation needed
        from scripts.neo4j_query_executor import ConfidenceProcessor

        processor = ConfidenceProcessor(self.evals_dir)
        confidence_data = processor.parse_confidence_section(test_file)

        # Should ignore legacy format
        self.assertIsNone(confidence_data)

    def test_confidence_processor_auto_promotes_high_confidence(self):
        """Test that confidence processor auto-promotes tests with ≥80% confidence"""
        # Create test file with 80% confidence
        test_file = self.evals_dir / "review" / "EVAL-05.md"
        test_content = """
# EVAL-05: High Confidence Test

**Confidence**: 80% → Auto-promote to PASSED
        """
        test_file.write_text(test_content)

        # This will FAIL initially - implementation needed
        from scripts.neo4j_query_executor import ConfidenceProcessor

        processor = ConfidenceProcessor(self.evals_dir)

        # Mock the harness transition method
        with patch.object(processor, "transition_test") as mock_transition:
            results = processor.process_existing_confidence(test_id="05")

            # Should call transition to PASSED
            mock_transition.assert_called_once()
            args = mock_transition.call_args
            self.assertEqual(args[0][2], "PASSED")  # Target state

            # Should report promotion
            self.assertEqual(results["promoted_count"], 1)
            self.assertEqual(results["failed_count"], 0)

    def test_confidence_processor_auto_fails_low_confidence(self):
        """Test that confidence processor auto-fails tests with ≤30% confidence"""
        # Create test file with 30% confidence
        test_file = self.evals_dir / "review" / "EVAL-42.md"
        test_content = """
# EVAL-42: Low Confidence Test

**Confidence**: 30% → Auto-fail to FAILED
        """
        test_file.write_text(test_content)

        # This will FAIL initially - implementation needed
        from scripts.neo4j_query_executor import ConfidenceProcessor

        processor = ConfidenceProcessor(self.evals_dir)

        # Mock the harness transition method
        with patch.object(processor, "transition_test") as mock_transition:
            results = processor.process_existing_confidence(test_id="42")

            # Should call transition to FAILED
            mock_transition.assert_called_once()
            args = mock_transition.call_args
            self.assertEqual(args[0][2], "FAILED")  # Target state

            # Should report failure
            self.assertEqual(results["promoted_count"], 0)
            self.assertEqual(results["failed_count"], 1)

    def test_confidence_processor_leaves_medium_confidence_in_review(self):
        """Test that confidence processor leaves medium confidence tests in REVIEW"""
        # Create test file with 50% confidence
        test_file = self.evals_dir / "review" / "EVAL-33.md"
        test_content = """
# EVAL-33: Medium Confidence Test

**Confidence**: 50% → Stay in REVIEW
        """
        test_file.write_text(test_content)

        # This will FAIL initially - implementation needed
        from scripts.neo4j_query_executor import ConfidenceProcessor

        processor = ConfidenceProcessor(self.evals_dir)

        # Mock the harness transition method
        with patch.object(processor, "transition_test") as mock_transition:
            results = processor.process_existing_confidence(test_id="33")

            # Should NOT call transition - stays in REVIEW
            mock_transition.assert_not_called()

            # Should report no promotions or failures
            self.assertEqual(results["promoted_count"], 0)
            self.assertEqual(results["failed_count"], 0)

    def test_confidence_processor_batch_mode(self):
        """Test that confidence processor handles batch mode correctly"""
        # Create multiple test files with different confidence levels
        test_files = [
            ("EVAL-01.md", "**Confidence**: 85% → Auto-promote to PASSED"),
            ("EVAL-02.md", "**Confidence**: 25% → Auto-fail to FAILED"),
            ("EVAL-03.md", "**Confidence**: 50% → Stay in REVIEW"),
            ("EVAL-04.md", "No confidence section"),
        ]

        for filename, content in test_files:
            test_file = self.evals_dir / "review" / filename
            test_file.write_text(f"# {filename.replace('.md', '')}\n\n{content}")

        # This will FAIL initially - implementation needed
        from scripts.neo4j_query_executor import ConfidenceProcessor

        processor = ConfidenceProcessor(self.evals_dir)

        # Mock the harness transition method
        with patch.object(processor, "transition_test") as mock_transition:
            results = processor.process_existing_confidence(batch=True)

            # Should have 2 transitions (1 promote, 1 fail)
            self.assertEqual(mock_transition.call_count, 2)

            # Should report correct counts
            self.assertEqual(results["promoted_count"], 1)
            self.assertEqual(results["failed_count"], 1)
            self.assertEqual(results["skipped_count"], 2)  # Medium confidence + no confidence


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = Path(self.temp_dir)

        # Create full project structure
        self.commands_dir = self.project_dir / ".claude" / "commands"
        self.evals_dir = self.project_dir / "evals"
        self.scripts_dir = self.project_dir / "scripts" / "python"

        for directory in [self.commands_dir, self.evals_dir, self.scripts_dir]:
            directory.mkdir(parents=True)

        # Create eval folders
        for folder in ["todo", "review", "passed", "failed", "blocked"]:
            (self.evals_dir / folder).mkdir()

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow from /eval command to auto-promotion"""
        # This test will FAIL initially - proves complete integration

        # Step 1: Create test file with placeholder
        test_file = self.evals_dir / "todo" / "EVAL-05.md"
        test_content = """
# EVAL-05: Find Person Named John

## Implementation

### Query
```cypher
// TODO: Implement Cypher query
```
        """
        test_file.write_text(test_content)

        # Step 2: Simulate /eval command workflow
        from scripts.neo4j_query_executor import EvalCommand

        eval_command = EvalCommand(self.project_dir)

        # Mock MCP interaction
        with patch.object(eval_command, "interactive_query_development") as mock_mcp:
            mock_mcp.return_value = {
                "query": "MATCH (p:Person) WHERE p.name = 'John' RETURN p",
                "confidence": 80,
                "assessment": "Y",
            }

            # Run eval command
            eval_command.run("05")

            # Should update file with query and confidence
            updated_content = test_file.read_text()
            self.assertIn("MATCH (p:Person) WHERE p.name = 'John' RETURN p", updated_content)
            self.assertIn("**Confidence**: 80% → Auto-promote to PASSED", updated_content)

        # Step 3: Run confidence processor
        from scripts.neo4j_query_executor import ConfidenceProcessor

        processor = ConfidenceProcessor(self.evals_dir)

        # Mock harness transition
        with patch.object(processor, "transition_test") as mock_transition:
            results = processor.process_existing_confidence(test_id="05")

            # Should auto-promote to PASSED
            mock_transition.assert_called_once()
            args = mock_transition.call_args
            self.assertEqual(args[0][2], "PASSED")

            # Should report successful promotion
            self.assertEqual(results["promoted_count"], 1)


if __name__ == "__main__":
    unittest.main()
