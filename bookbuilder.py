from os import getcwd, listdir
from os.path import isdir, join, splitext
from markdown2 import Markdown


class BookBuilder(object):
    def __init__(self, input_folder_path, output_file_path_without_extension):
        self._input_folder_path = self._clean_folder_path(input_folder_path)
        self._markdown_converter = Markdown()

    @staticmethod
    def _clean_folder_path(input_folder_path):
        folder_name_is_starting_with_root = input_folder_path[0] in ["/", "\\"]
        folder_name_is_starting_with_drive_letter = input_folder_path[1] in [":", "/"] and input_folder_path[0] != "."
        folder_name_is_relative = not (folder_name_is_starting_with_drive_letter or folder_name_is_starting_with_root)
        if folder_name_is_relative:
            input_folder_path = join(getcwd(), input_folder_path)
        input_folder_path = input_folder_path.replace("\\", "/")
        return input_folder_path

    def convert(self):
        content = self._process_folder(self._input_folder_path)
        html_content = self._convert_content_to_html(content)

    def _process_folder(self, folder_path):
        content = {}
        folder_content = listdir(folder_path)
        for node_name in folder_content:
            full_path_to_item = join(folder_path, node_name)
            if isdir(full_path_to_item):
                folder_content = self._process_folder(full_path_to_item)
                if folder_content:
                    content[node_name] = folder_content
            else:
                file_content = self._process_file(full_path_to_item)
                if file_content:
                    file_name_without_extension = splitext(node_name)[0]
                    content[file_name_without_extension] = file_content
        return content

    @staticmethod
    def _process_file(full_path_to_item):
        extension = splitext(full_path_to_item)[1]
        if extension != ".md":
            return ""
        with open(full_path_to_item) as file_handler:
            file_content = file_handler.read()
        return file_content

    def _convert_content_to_html(self, content):
        html_content = {}
        try:
            for key, value in content.items():
                html_content[key] = self._convert_content_to_html(value)
        except AttributeError:
            return self._markdown_converter.convert(content)
        return html_content
