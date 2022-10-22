import os
from re import search

def find_dirs(mas_dirs_find: list, find_str: str) -> list:
    mas_dirs_out = []
    for dir in mas_dirs_find:
        mas_dirs = [i for i in os.walk(dir)]
        for i in mas_dirs: # перебор os.walk в формате (путь, [список директорий в директории], файлы), ...
            for k in i[2]: # перебор файлов
                if search(find_str, k) or search(find_str.capitalize(), k): # поиск без учета регистра по файлам
                    path = f"{i[0]}\\{k}"
                    mas_dirs_out.append(path)
    return mas_dirs_out












