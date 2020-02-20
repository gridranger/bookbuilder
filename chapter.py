from slugify import slugify


class Chapter(object):
    def __init__(self, node_name, level, content=""):
        self.node_name = node_name
        self.level = level
        self.content = "# {1}\n".format(level+1, node_name.capitalize()) if not content else content
        self.body = True if content else False

    @property
    def slug_name(self):
        return slugify(self.node_name, separator="_")

    @property
    def xhtml_name(self):
        return "{}.xhtml".format(self.slug_name)

    def __eq__(self, other):
        try:
            if self.node_name == other.node_name and self.level == other.level and self.content == other.content:
                return True
        except AttributeError:
            return False
        return False