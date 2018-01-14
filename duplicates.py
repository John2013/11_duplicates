import sys
from collections import defaultdict
from os.path import isdir, realpath, getsize, join
from os import walk


def get_files_recursively(path):
    files_list = []

    for dir_, _, file_names in walk(path):
        for file_name in file_names:
            path = realpath(join(dir_, file_name))
            files_list.append({
                'name': file_name,
                'path': path,
                'size': getsize(path)
            })

    return files_list


def get_duplicates(files_list):
    duplicates_dict = defaultdict(set)

    for file in files_list:
        key = "{} ({} б)".format(file['name'], file['size'])
        duplicates_dict[key].add(file['path'])

    for key in list(duplicates_dict):
        if len(duplicates_dict[key]) < 2:
            del duplicates_dict[key]

    return duplicates_dict


def show_duplicates(duplicates):
    for name, file_paths in duplicates.items():
        print('{}: '.format(name))
        for file_path in file_paths:
            print('\t{}'.format(file_path))
        print('')


if __name__ == '__main__':
    if len(sys.argv) > 1 and isdir(sys.argv[1]):
        dirpath = sys.argv[1]
    else:
        exit('Ошибка: Отсутствует путь к папке или папка не найдена')

    files_list = get_files_recursively(dirpath)
    print('Дубликаты:')
    show_duplicates(get_duplicates(files_list))
