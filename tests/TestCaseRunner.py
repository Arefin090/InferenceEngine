import unittest
import subprocess

class TestKnowledgeBase(unittest.TestCase):
    def run_test_case(self, test_file, expected_output, method):
        result = subprocess.run(["python", "main.py", test_file, method], capture_output=True, text=True)
        output = result.stdout.strip()
        test_result = output.split("\n")[-1]
        self.assertEqual(test_result, expected_output, f"Test {test_file}: Expected {expected_output}, but got {test_result}")

    def test_forward_chaining(self):
        test_cases = [
            ("test_cases/test1.txt", "YES: 1"),
            ("test_cases/test2.txt", "NO"),
            ("test_cases/test3.txt", "YES: 1"),
            ("test_cases/test4.txt", "NO"),
            ("test_cases/test5.txt", "YES: 1"),
            ("test_cases/test6.txt", "YES: 1"),
            ("test_cases/test7.txt", "YES: 1"),
            ("test_cases/test8.txt", "YES: 1"),
        ]
        for test_file, expected_output in test_cases:
            with self.subTest(test_file=test_file, expected_output=expected_output):
                self.run_test_case(test_file, expected_output, "FC")

    def test_backward_chaining(self):
        test_cases = [
            ("test_cases/test1.txt", "YES: 1"),
            ("test_cases/test2.txt", "NO"),
            ("test_cases/test3.txt", "YES: 1"),
            ("test_cases/test4.txt", "NO"),
            ("test_cases/test5.txt", "YES: 1"),
            ("test_cases/test6.txt", "YES: 1"),
            ("test_cases/test7.txt", "YES: 1"),
            ("test_cases/test8.txt", "YES: 1"),
        ]
        for test_file, expected_output in test_cases:
            with self.subTest(test_file=test_file, expected_output=expected_output):
                self.run_test_case(test_file, expected_output, "BC")

if __name__ == '__main__':
    unittest.main()
