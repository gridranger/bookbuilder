from sys import argv
from bookbuilder import BookBuilder

b = BookBuilder(argv[1], argv[2])
b.convert()
