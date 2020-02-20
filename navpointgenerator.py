# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'


class NavPointGenerator(object):
    def __init__(self, chapter_list, navpoint_template):
        self._content = chapter_list
        self._template = navpoint_template
        self._closing_cursor = "\n{cursor}"
        self._nav_points = "{cursor}"
        self._actual_depth = 0

    def get_nav_points(self):
        for index, chapter in enumerate(self._content):
            self._actual_depth = chapter.level
            cursor = self._get_inner_cursor_placeholder_value(index)
            nav_point = self._template.format(nav_id=chapter.slug_name, order_number=index, nav_name=chapter.node_name,
                                              file_name=chapter.xhtml_name, spacing=(chapter.level + 1) * 4 * " ",
                                              cursor=cursor)
            new_mid_cursor_should_be_added = self._check_if_new_mid_cursor_is_required(index)
            if new_mid_cursor_should_be_added:
                nav_point += self._closing_cursor
            self._nav_points = self._nav_points.format(cursor=nav_point)
            self._create_closing_cursor_if_there_is_none(index)
        return self._nav_points

    def _get_inner_cursor_placeholder_value(self, index):
        try:
            if self._content[index + 1].level > self._actual_depth:
                cursor = self._closing_cursor
            else:
                cursor = ""
        except IndexError:
            cursor = ""
        return cursor

    def _check_if_new_mid_cursor_is_required(self, index):
        new_mid_cursor_should_be_added = False
        try:
            if self._content[index + 1].level == self._actual_depth:
                new_mid_cursor_should_be_added = True
        except IndexError:
            pass
        return new_mid_cursor_should_be_added

    def _create_closing_cursor_if_there_is_none(self, index):
        try:
            if self._content[index + 1] and "{cursor}" not in self._nav_points:
                self._nav_points += self._closing_cursor
        except IndexError:
            pass
