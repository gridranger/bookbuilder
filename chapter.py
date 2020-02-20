class Chapter(object):
    def __init__(self, node_name, level, content=""):
        self.node_name = node_name
        self.level = level
        self.content = "<h{0}>{1}</h{0}>".format(level+1, node_name.capitalize()) if not content else content

    def __eq__(self, other):
        try:
            if self.node_name == other.node_name and self.level == other.level and self.content == other.content:
                return True
        except AttributeError:
            return False
        return False