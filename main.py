from sys import argv
from bookbuilder import BookBuilder


try:
    b = BookBuilder(argv[1], argv[2])
except IndexError:
    print("Please run it as 'python main.py input_folder_path output_file_path'.")
    exit(1)
b.convert()
