import sys
from collections import defaultdict
from os.path import isdir, realpath, getsize
from os import walk


def get_files_recursively(path):
    files_list = []

    for dir, ignored, files in walk(path):
        for file_name in files:
            path = realpath('{}/{}'.format(dir, file_name))
            files_list.append({
                'name': file_name,
                'path': path,
                'size': getsize(path)
            })

    return files_list


def are_duplicates(file1, file2):
    return file1['path'] != file2['path'] and file1['name'] == file2[
        'name'
    ] and file1['size'] == file2['size']


def get_duplicates(files_list):
    duplicates = defaultdict(set)

    for file1 in files_list:
        for file2 in files_list:
            if are_duplicates(file1, file2):
                duplicates[file1['name']].add(file1['path'])
                duplicates[file1['name']].add(file2['path'])

    return duplicates


def show_duplicates(duplicates):
    for name, files in duplicates.items():
        print('{}: '.format(name))
        for file in files:
            print('\t* {}'.format(file))
        print('')


if __name__ == '__main__':
    dirpath = ''
    if len(sys.argv) > 1 and isdir(sys.argv[1]):
        dirpath = sys.argv[1]
    else:
        exit('Ошибка: Отсутствует путь к папке или папка не найдена')

    files_list = get_files_recursively(dirpath)
    print('Дубликаты:')
    show_duplicates(get_duplicates(files_list))
