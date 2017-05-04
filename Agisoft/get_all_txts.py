import PhotoScan
import os
import itertools

doc = PhotoScan.app.document


def get_folder(chunk):
    file = chunk.cameras[0].photo.path
    path = os.path.dirname(file)
    return path


def get_txt_files(folder_path):
    texts = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            path = os.path.join(folder_path, file)
            texts.append(path)
    return texts


def get_folders():
    folders = []
    for chunk in doc.chunks:
        folder = get_folder(chunk)
        folders.append(folder)
    return folders


def get_all_txt_files():
    texts = []
    for folder in get_folders():
        texts.append(get_txt_files(folder))
    join_list = list(itertools.chain.from_iterable(texts))
    return join_list

texts = get_all_txt_files()
for text in texts:
    print(text)

file = open(r"C:\Users\mkreidler\Desktop\agifolders.txt", "w")
for path in texts:
    file.write(path)
    file.write("\n")
print("done")
