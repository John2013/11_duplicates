import sys
from collections import defaultdict
from os.path import isdir, realpath, getsize, join
from os import walk


def get_duplicates(path):
    duplicates_dict = defaultdict(set)
    for files_dir, _, files_names in walk(path):
        for file_name in files_names:
            path = realpath(join(files_dir, file_name))
            file_size = getsize(path)
            duplicate_key = "{} ({} б)".format(file_name, file_size)
            duplicates_dict[duplicate_key].add(path)

    for duplicates_dict_key in list(duplicates_dict):
        if len(duplicates_dict[duplicates_dict_key]) < 2:
            del duplicates_dict[duplicates_dict_key]

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

    duplicates_dict = get_duplicates(dirpath)
    print('Дубликаты:')
    show_duplicates(duplicates_dict)
