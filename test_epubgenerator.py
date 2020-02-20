# -*- coding: utf-8 -*-
from os.path import exists
from shutil import rmtree
from unittest import TestCase
from chapter import Chapter
from epubgenerator import EpubGenerator

__author__ = 'Bárdos Dávid'


class TestEpubGenerator(TestCase):
    def setUp(self):
        if exists("sample/output/ws"):
            rmtree("sample/output/ws")
        metadata = {"source": "https://github.com/gridranger/bookbuilder/sample", "title": "Best Sample Book Ever",
                    "author": "Famous Author", "language": "hun", "rights": "© 2020"}
        html_content = [Chapter("Part 1", 0, ""),
                        Chapter("chapter 1", 1, "<h1>My firs chapter</h1>\n\n<p>Lorem ipsum...</p>\n"),
                        Chapter("chapter 2", 1, "<h1>My second chapter</h1>\n\n<p>Lorem ipsum...</p>\n"),
                        Chapter("Part 2", 0, ""),
                        Chapter("chapter 3", 1, "<h1>My third chapter</h1>\n\n<p>Lorem ipsum...</p>\n")]
        self.e = EpubGenerator("sample/output/unit_test", metadata, html_content)

    def test__load_templates(self):
        self.e._load_templates()
        expected_result = ["content", "metadata", "navpoint", "title", "toc.ncx"]
        self.assertEqual(expected_result, list(self.e._templates.keys()))

    def test__create_folders(self):
        self.e._create_folders()
        self.assertTrue(exists("sample/output/ws/META-INF"))
        self.assertTrue(exists("sample/output/ws/OEBPS"))

    def test__create_mimetype_file(self):
        expected_path = "sample/output/ws/mimetype"
        expected_content = "application/epub+zip"
        self.e._create_folders()
        self.e._create_mimetype_file()
        self.assertTrue(exists(expected_path))
        with open(expected_path) as file_handler:
            self.assertEqual(expected_content, file_handler.read())

    def test__create_css(self):
        expected_path = "sample/output/ws/OEBPS/stylesheet.css"
        self.e._create_folders()
        self.e._create_css()
        with open(expected_path) as file_handler:
            self.assertTrue("p.book_title" in file_handler.read())

    def test__create_container_xml(self):
        expected_path = "sample/output/ws/META-INF/container.xml"
        self.e._create_folders()
        self.e._create_container_xml()
        with open(expected_path) as file_handler:
            self.assertTrue("OEBPS/metadata.opf" in file_handler.read())

    def test__create_title_page(self):
        expected_path = "sample/output/ws/OEBPS/title.xhtml"
        self.e._load_templates()
        self.e._create_folders()
        self.e._create_title_page()
        with open(expected_path) as file_handler:
            self.assertTrue("Famous Author" in file_handler.read())

    def test__create_content_pages(self):
        self.e._load_templates()
        self.e._create_folders()
        self.e._create_content_pages()
        with open("sample/output/ws/OEBPS/chapter_3.xhtml") as file_handler:
            self.assertTrue("<p>Lorem ipsum...</p>" in file_handler.read())

    def test__create_nav_points(self):
        expected_result = """    <navPoint id="part_1" playOrder="0">
        <navLabel><text>Part 1</text></navLabel><content src="part_1.xhtml"/>
        <navPoint id="chapter_1" playOrder="1">
            <navLabel><text>chapter 1</text></navLabel><content src="chapter_1.xhtml"/>
        </navPoint>
        <navPoint id="chapter_2" playOrder="2">
            <navLabel><text>chapter 2</text></navLabel><content src="chapter_2.xhtml"/>
        </navPoint>
    </navPoint>
    <navPoint id="part_2" playOrder="3">
        <navLabel><text>Part 2</text></navLabel><content src="part_2.xhtml"/>
        <navPoint id="chapter_3" playOrder="4">
            <navLabel><text>chapter 3</text></navLabel><content src="chapter_3.xhtml"/>
        </navPoint>
    </navPoint>"""
        self.e._load_templates()
        self.e._create_nav_points()
        self.assertEqual(expected_result, self.e._nav_points)

    def test__create_metadata(self):
        self.e._metadata["uuid"] = "dummy"
        self.e._load_templates()
        self.e._create_folders()
        self.e._create_metadata()
        expected_result = """<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>Best Sample Book Ever</dc:title>
    <dc:creator opf:role="aut">Famous Author</dc:creator>
    <dc:identifier opf:scheme="uuid" id="uuid_id">dummy</dc:identifier>
    <dc:language>hun</dc:language>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
    <item id="style" href="stylesheet.css" media-type="text/css" />
    <item id="title" href="title.xhtml" media-type="application/xhtml+xml" />
    <item id="part_1" href="part_1.xhtml" media-type="application/xhtml+xml" />
    <item id="chapter_1" href="chapter_1.xhtml" media-type="application/xhtml+xml" />
    <item id="chapter_2" href="chapter_2.xhtml" media-type="application/xhtml+xml" />
    <item id="part_2" href="part_2.xhtml" media-type="application/xhtml+xml" />
    <item id="chapter_3" href="chapter_3.xhtml" media-type="application/xhtml+xml" />
  </manifest>
  <spine toc="ncx">
    <itemref idref="title" />
    <itemref idref="part_1" />
    <itemref idref="chapter_1" />
    <itemref idref="chapter_2" />
    <itemref idref="part_2" />
    <itemref idref="chapter_3" />
  </spine>
  <guide>
    <reference type="cover" title="title" href="title.xhtml"/>
    <reference type="text" title="chapter 1" href="chapter_1.xhtml"/>
  </guide>
</package>
"""
        with open("sample/output/ws/OEBPS/metadata.opf") as file_handler:
            self.assertEqual(expected_result, file_handler.read())

    def test__create_table_of_contents(self):
        self.e._load_templates()
        self.e._create_folders()
        self.e._create_nav_points()
        self.e._create_table_of_contents()

    def test__compress_workspace(self):
        self.e._create_workspace()
        self.e._compress_workspace()
        self.assertTrue(exists("sample/output/unit_test.epub"))

    def test__remove_workspace(self):
        self.e._create_workspace()
        self.e._remove_workspace()
        self.assertFalse(exists("sample/output/ws"))
