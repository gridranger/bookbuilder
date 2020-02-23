from json import load
from os import getcwd, listdir
from os.path import isdir, join, splitext
from re import compile as re_compile, MULTILINE
from markdown2 import Markdown
from chapter import Chapter
from epubgenerator import EpubGenerator


class BookBuilder(object):
    def __init__(self, input_folder_path, output_file_path_without_extension):
        self._input_folder_path = self._clean_folder_path(input_folder_path)
        self._output_file_path_without_extension = output_file_path_without_extension
        self._markdown_converter = Markdown(extras={"smarty-pants": True})

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
        metadata = self._read_metadata()
        self._demote_headings(content)
        self._convert_content_to_html(content)
        self._post_html_custom_formattings(content)
        EpubGenerator(self._output_file_path_without_extension, metadata, content).generate()

    def _process_folder(self, folder_path, level=0):
        exclusions = ["meta"]
        content = []
        folder_content = listdir(folder_path)
        for node_name in folder_content:
            if node_name in exclusions:
                continue
            full_path_to_item = join(folder_path, node_name)
            if isdir(full_path_to_item):
                if not any(subnode_name.endswith(".md") for subnode_name in listdir(full_path_to_item)):
                    continue
                content.append(Chapter(node_name, level))
                folder_content = self._process_folder(full_path_to_item, level=level + 1)
                content += folder_content
            else:
                file_content = self._process_file(full_path_to_item)
                if file_content:
                    file_name_without_extension = splitext(node_name)[0]
                    content.append(Chapter(file_name_without_extension, level, file_content))
        return content

    @staticmethod
    def _process_file(full_path_to_item):
        extension = splitext(full_path_to_item)[1]
        if extension != ".md":
            return ""
        with open(full_path_to_item, encoding='utf-8') as file_handler:
            file_content = file_handler.read()
            file_content = file_content.replace("\ufeff", "")
        return file_content

    def _read_metadata(self):
        with open("{}/.metadata.json".format(self._input_folder_path), encoding='utf-8') as file_handler:
            raw_metadata = load(file_handler)
        return raw_metadata

    def _demote_headings(self, content):
        pattern = re_compile("^(#)", MULTILINE)
        for chapter in content:
            demotion_level = chapter.level + 1
            chapter.content = pattern.sub(demotion_level*"#", chapter.content)

    def _convert_content_to_html(self, content):
        for chapter in content:
            chapter.content = self._markdown_converter.convert(chapter.content)

    def _post_html_custom_formattings(self, content):
        for chapter in content:
            # General Hungarian
            chapter.content = chapter.content.replace("&#8220;", "&#8222;")  # Hungarian quotation mark
            # custom format could be put here
