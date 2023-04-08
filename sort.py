import pathlib as pb
import re
import shutil
import sys



arg = pb.Path("{path}".format(path=sys.argv[1]))

folders = ['IMAGES', 'VIDEOS', 'AUDIO', 'ARCHIVES', 'DOCUMENTS', 'UNKNOWN FILE TYPE']
dict_of_known_fileformat = {(".png", ".jpg", ".jpeg", ".svg"): "IMAGES",
                            (".avi", ".mp4", ".mov", ".mkv"): "VIDEOS",
                            (".mp3", ".ogg", ".wav", ".amr"): "AUDIO",
                            (".gz", ".zip", ".tar"): "ARCHIVES",
                            (".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"): "DOCUMENTS"
                            }

dict_to_transliterate = {ord("а"): "a", ord("б"): "b", ord("в"): "v", ord("г"): "gh", ord("ґ"): "g", ord("д"): "d",
                         ord("е"): "e", ord("є"): "ye", ord("ж"): "zh", ord("з"): "z", ord("и"): "y", ord("і"): "i",
                         ord("ї"): "yi", ord("й"): "i", ord("к"): "k", ord("л"): "l", ord("м"): "m", ord("н"): "n",
                         ord("о"): "o", ord("п"): "p", ord("р"): "r", ord("c"): "s", ord("т"): "t", ord("у"): "u",
                         ord("Ф"): "f", ord("х"): "kh", ord("ц"): "ts", ord("ш"): "sh", ord("щ"): "sch", ord("ю"): "yu",
                         ord("я"): "ya", ord("ь"): "\'",

                         ord("А"): "A", ord("Б"): "B", ord("В"): "V", ord("Г"): "GH", ord("Ґ"): "G", ord("Д"): "D",
                         ord("Е"): "E", ord("Є"): "YE", ord("Ж"): "ZH", ord("З"): "Z", ord("И"): "Y", ord("І"): "I",
                         ord("Ї"): "YI", ord("Й"): "I", ord("К"): "K", ord("Л"): "L", ord("М"): "M", ord("Н"): "N",
                         ord("О"): "O", ord("П"): "P", ord("Р"): "R", ord("С"): "S", ord("Т"): "T", ord("У"): "U",
                         ord("Ф"): "F", ord("Х"): "KH", ord("Ц"): "TS", ord("Щ"): "SH", ord("Щ"): "SCH", ord("Ю"): "YU",
                         ord("Я"): "YA", ord("Ь"): "\'"
                         }
lisT_of_used_known_format = set()
lisT_of_used_unknown_format = set()


def normilize(text):
    text = text.translate(dict_to_transliterate)
    text = re.sub('[^a-zA-Z0-9_]', '_', text)
    return text


def copy_eror(file, dict_of_known_fileformat="UNKNOWN FILE TYPE", n=0, path=arg):
    try:
        file = file.rename(path / dict_of_known_fileformat / (normilize(file.stem) + f'{"_copy_" * n}' + file.suffix))
        return file
    except FileExistsError:
        n += 1
        copy_eror(file, dict_of_known_fileformat, n)


def sort_dir(file, path=arg):
    for key in dict_of_known_fileformat:
        if file.suffix in key:
            lisT_of_used_known_format.add(file.suffix)
            if file.parent == path / dict_of_known_fileformat[key]:
                copy_eror(file, dict_of_known_fileformat[key])
                return None
            copy_eror(file, dict_of_known_fileformat[key])
            return None
    lisT_of_used_unknown_format.add(file.suffix)
    copy_eror(file)


def unpack_file(path):
    for i in path.iterdir():
        if i.name == "ARCHIVES":
            continue
        elif i.is_dir():
            unpack_file(pb.Path(i))
        else:
            sort_dir(i)


def find_folder(folder_path, folder_name):
    path = pb.Path(folder_path) / folder_name
    if path.exists() and path.is_dir():
        return None
    else:
        path.mkdir()


def delete_empty_folder(path):
    for folder in path.iterdir():
        if folder.is_dir() and any(folder.iterdir()):
            delete_empty_folder(folder)
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()
        elif folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
        else:
            continue


for folder in folders:
    find_folder(arg, folder)

zip = []

unpack_file(arg)

for key, value in dict_of_known_fileformat.items():
    if value == "ARCHIVES":
        for i in key:
            zip.append(i)
        break

for i in (arg / "ARCHIVES").iterdir():
    if i.suffix in zip:
        shutil.unpack_archive(i, arg / "ARCHIVES" / i.stem)
        i.unlink()
delete_empty_folder(arg)
