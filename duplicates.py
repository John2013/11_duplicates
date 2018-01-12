import sys
import re
from collections import defaultdict
from os.path import isdir, realpath
from os import scandir


def get_files_recursively(path):
    files_list = []

    for dir_item in scandir(path):
        if dir_item.is_dir() and not dir_item.name.startswith('.'):
            files_list += get_files_recursively(dir_item.path)
        elif dir_item.is_file:
            files_list.append(dir_item)

    return files_list


def are_duplicates(file1, file2):
    size_index = 6

    return \
        file1.name == file2.name and \
        file1.stat()[size_index] == file2.stat()[size_index]


def get_real_path(path):
    return re.sub(r'\\', '/', realpath(path))


def get_duplicates(files_list):
    duplicates = set()
    structed_duplicates = defaultdict(set)

    for file1 in files_list:
        if file1 in duplicates:
            continue
        for file2 in files_list:
            if file1.path == file2.path or file2 in duplicates:
                continue
            if are_duplicates(file1, file2):
                structed_duplicates[file1.name].add(get_real_path(file1.path))
                structed_duplicates[file1.name].add(get_real_path(file2.path))

    return structed_duplicates


def show_duplicates(duplicates):
    for name, files in duplicates.items():
        print(name + ": ")
        for file in files:
            print("\t* {}".format(file))
        print("")


if __name__ == '__main__':
    dirpath = ""
    if len(sys.argv) > 1 and isdir(sys.argv[1]):
        dirpath = sys.argv[1]
    else:
        exit("Ошибка: Отсутствует путь к папке или папка не найдена")

    files_list = get_files_recursively(dirpath)
    print("Дубликаты:")
    show_duplicates(get_duplicates(files_list))
