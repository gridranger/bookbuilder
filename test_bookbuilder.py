from os import getcwd
from unittest import TestCase
from bookbuilder import BookBuilder
from chapter import Chapter


class TestBookBuilder(TestCase):
    def setUp(self):
        self.b = BookBuilder("sample/input", "sample/output/test_book")
        self.sample_flat_structure = [Chapter("Part 1", 0, "# Part 2"),
                                      Chapter("chapter 1", 1, "# My firs chapter\n\nLorem ipsum...\n"),
                                      Chapter("chapter 2", 1, "# My second chapter\n\nLorem ipsum...\n"),
                                      Chapter("Part 2", 0, "# Part 2"),
                                      Chapter("chapter 3", 1, "# My third chapter\n\nLorem ipsum...\n")]

    def test__clean_folder_path(self):
        test_set = [
            {"input": "sample/input", "output": "{}/{}".format(getcwd(), "sample/input").replace("\\", "/")},
            {"input": "./sample/input", "output": "{}/{}".format(getcwd(), "./sample/input").replace("\\", "/")},
            {"input": "/sample/input", "output": "/sample/input"},
            {"input": "\\sample\\input", "output": "/sample/input"},
            {"input": "c:\\sample\\input", "output": "c:/sample/input"},
            {"input": "c/sample/input", "output": "c/sample/input"}
        ]
        for case in test_set:
            expected_result = case["output"]
            result = self.b._clean_folder_path(case["input"])
            self.assertEqual(expected_result, result)

    def test__process_folder(self):
        path = "sample/input"
        result = self.b._process_folder(path)
        expected_result = self.sample_flat_structure
        self.assertTrue(expected_result[i] == result[i] for i in range(len(result)))

    def test__convert_content_to_html(self):
        self.b._convert_content_to_html(self.sample_flat_structure)
        expected_result = [Chapter("Part 1", 0, "<h1>Part 2</h1>"),
                           Chapter("chapter 1", 1, "<h1>My firs chapter</h1>\n\n<p>Lorem ipsum...</p>\n"),
                           Chapter("chapter 2", 1, "<h1>My second chapter</h1>\n\n<p>Lorem ipsum...</p>\n"),
                           Chapter("Part 2", 0, "<h1>Part 2</h1>"),
                           Chapter("chapter 3", 1, "<h1>My third chapter</h1>\n\n<p>Lorem ipsum...</p>\n")]
        self.assertTrue(expected_result[i] == self.sample_flat_structure[i] for i in range(len(self.sample_flat_structure)))
