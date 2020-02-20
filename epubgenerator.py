from os import makedirs
from os.path import dirname, realpath
from shutil import copyfile, rmtree
from uuid import uuid1
from zipfile import ZipFile
from navpointgenerator import NavPointGenerator


class EpubGenerator(object):
    def __init__(self, output_file_path_without_extension, metadata, html_content):
        self._output_file_path = "{}.epub".format(output_file_path_without_extension)
        self._metadata = metadata
        self._metadata["uuid"] = uuid1()
        self._html_content = html_content
        self._templates_folder = "{}/templates".format(dirname(realpath(__file__)))
        self._workspace_folder = "{}/ws".format(dirname(output_file_path_without_extension))
        self._book_file_paths = []
        self._chapter_file_names = []
        self._hidden_nav_counter = 0
        self._nav_points = ""
        self._templates = {}

    @property
    def _nav_counter(self):
        value = self._hidden_nav_counter
        self._hidden_nav_counter += 1
        return value

    def generate(self):
        self._load_templates()
        self._create_workspace()
        self._create_title_page()
        self._create_content_pages(self._html_content)
        self._create_nav_points()
        self._create_table_of_contents()
        self._create_metadata()
        self._compress_workspace()
        self._remove_workspace()

    def _load_templates(self):
        templates = ["content", "metadata", "navpoint", "title", "toc.ncx"]
        for template in templates:
            with open("{}/{}.html".format(self._templates_folder, template)) as file_handler:
                self._templates[template] = file_handler.read()

    def _create_workspace(self):
        self._create_folders()
        self._create_mimetype_file()
        self._create_css()
        self._create_container_xml()

    def _create_folders(self):
        makedirs(self._workspace_folder, exist_ok=True)
        makedirs("{}/META-INF".format(self._workspace_folder), exist_ok=True)
        makedirs("{}/OEBPS".format(self._workspace_folder), exist_ok=True)

    def _create_mimetype_file(self):
        file_path = "{}/mimetype".format(self._workspace_folder)
        with open(file_path, "w") as file_handler:
            file_handler.write("application/epub+zip")
        self._book_file_paths.append(file_path)

    def _create_css(self):
        file_name = "stylesheet.css"
        file_path = "{}/OEBPS/{}".format(self._workspace_folder, file_name)
        copyfile("{}/{}".format(self._templates_folder, file_name), file_path)
        self._book_file_paths.append(file_path)

    def _create_container_xml(self):
        file_name = "container.xml"
        file_path = "{}/META-INF/{}".format(self._workspace_folder, file_name)
        copyfile("{}/{}".format(self._templates_folder, file_name), file_path)
        self._book_file_paths.append(file_path)

    def _create_title_page(self):
        file_path = "{}/OEBPS/title.xhtml".format(self._workspace_folder)
        title_page  = self._templates["title"]
        title_page = title_page.format(title=self._metadata["title"], author=self._metadata["author"])
        with open(file_path, "w", encoding='utf-8') as file_handler:
            file_handler.write(title_page)
        self._book_file_paths.append(file_path)

    def _create_content_pages(self, content):
        for chapter in content:
            file_path = "{}/OEBPS/{}".format(self._workspace_folder, chapter.xhtml_name)
            with open(file_path, "w", encoding='utf-8') as file_handler:
                file_handler.write(chapter.content)

    def _create_nav_points(self):
        nav_point_generator = NavPointGenerator(self._html_content, self._templates["navpoint"])
        self._nav_points = nav_point_generator.get_nav_points()

    def _create_metadata(self):
        file_path = "{}/OEBPS/metadata.opf".format(self._workspace_folder)
        manifest = []
        spine = []
        text_reference = ""
        for chapter in self._html_content:
            new_manifest_line = """    <item id="{}" href="{}" media-type="application/xhtml+xml" />"""
            manifest.append(new_manifest_line.format(chapter.slug_name, chapter.xhtml_name))
            new_spine_line = """    <itemref idref="{}" />"""
            spine.append(new_spine_line.format(chapter.slug_name))
            if not text_reference and chapter.body:
                text_reference = """<reference type="text" title="{}" href="{}"/>""".format(chapter.node_name,
                                                                                            chapter.xhtml_name)
        metadata = self._templates["metadata"]
        metadata = metadata.format(title=self._metadata["title"], author=self._metadata["author"],
                                   uuid=self._metadata["uuid"], language=self._metadata["language"],
                                   manifest="\n".join(manifest), spine="\n".join(spine), text_reference=text_reference)
        with open(file_path, "w", encoding='utf-8') as file_handler:
            file_handler.write(metadata)
        self._book_file_paths.append(file_path)

    def _create_table_of_contents(self):
        file_path = "{}/OEBPS/toc.ncx".format(self._workspace_folder)
        toc = self._templates["toc.ncx"]
        toc = toc.format(uuid=self._metadata["uuid"],
                         title=self._metadata["title"],
                         nav_map=self._nav_points)
        with open(file_path, "w", encoding='utf-8') as file_handler:
            file_handler.write(toc)
        self._book_file_paths.append(file_path)

    def _compress_workspace(self):
        file_list = []
        file_list += self._book_file_paths
        for chapter_file_name in self._chapter_file_names:
            file_list.append("{}/OEBPS/{}".format(self._workspace_folder, chapter_file_name))
        with ZipFile(self._output_file_path, 'w') as file_handler:
            for file_path in file_list:
                file_handler.write(file_path, file_path.replace(self._workspace_folder, ""))

    def _remove_workspace(self):
        rmtree(self._workspace_folder)