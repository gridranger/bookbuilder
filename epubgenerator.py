from os import makedirs
from os.path import dirname, realpath
from shutil import copyfile, rmtree
from navpointgenerator import NavPointGenerator


class EpubGenerator(object):
    def __init__(self, output_file_path_without_extension, metadata, html_content):
        self._output_file_path_without_extension = output_file_path_without_extension
        self._metadata = metadata
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
        self._nav_points = self._generate_nav_points(self._html_content)
        self._create_table_of_contents()
        self._create_metadata()

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

    def _generate_nav_points(self, content):
        nav_point_generator = NavPointGenerator(content, self._templates["navpoint"])
        return nav_point_generator.get_nav_points()

    def _create_content_page(self, raw_content):
        pass
        # title = ""
        # text = ""
        # for line in raw_content:
        #     if line.startswith("# ") and title == "":
        #         title = line.replace("# ", "")
        #     elif line.startswith("# "):
        #         raise RuntimeError("More than one title defined in a chapter!")
        #     elif line.startswith("András:") or line.startswith("Erika:"):
        #         line = line.replace(": ", " üzenete:</span><br/>")
        #         text += """  <p class="msn"><span style="color: grey;">{}</p>\n""".format(line)
        #     else:
        #         text += "  <p>{}</p>\n".format(line)
        # content_page = self._templates["content"]
        # content_page = content_page.format(title=title, text=text)
        # return content_page