from os import getcwd
from unittest import TestCase
from bookbuilder import BookBuilder


class TestBookBuilder(TestCase):
    def setUp(self):
        self.b = BookBuilder("sample/input", "sample/output/test_book")
        self.sample_structure = {"Part 1": {"chapter 1": "# My first chapter\n\nLorem ipsum...\n",
                                            "chapter 2": "# My second chapter\n\nLorem ipsum...\n"},
                                 "Part 2": {"chapter 3": "# My third chapter\n\nLorem ipsum...\n"}}

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
        expected_result = self.sample_structure
        self.assertEqual(expected_result, result)

    def test__convert_content_to_html(self):
        result = self.b._convert_content_to_html(self.sample_structure)
        expected_result = {"Part 1": {"chapter 1": "<h1>My first chapter</h1>\n\n<p>Lorem ipsum...</p>\n",
                                      "chapter 2": "<h1>My second chapter</h1>\n\n<p>Lorem ipsum...</p>\n"},
                           "Part 2": {"chapter 3": "<h1>My third chapter</h1>\n\n<p>Lorem ipsum...</p>\n"}}
        self.assertEqual(expected_result, result)
