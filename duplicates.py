import sys
from collections import defaultdict
from os.path import isdir, realpath, getsize, join
from os import walk


def get_files(path):
    files_dict = defaultdict(list)

    for dir_path, _, file_names in walk(path):
        for file_name in file_names:
            path = realpath(join(dir_path, file_name))
            files_dict[
                '{} ({} б)'.format(file_name, getsize(path))
            ].append(path)

    return files_dict


def get_duplicates(files_dict):
    duplicates_dict = {}

    for dict_key, path_list in files_dict.items():
        path_list = set(path_list)
        if len(path_list) > 1:
            duplicates_dict[dict_key] = path_list

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

    files_dict = get_files(dirpath)
    print('Дубликаты:')
    show_duplicates(get_duplicates(files_dict))
