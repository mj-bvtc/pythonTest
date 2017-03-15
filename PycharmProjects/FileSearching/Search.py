import os




def getRhino(_path, extensionList):
    count = 0
    for root, dirs, files in os.walk(_path):
        for file in files:
            ext = file.split(".")[-1]
            for et in extensionList:
                if ext.upper() == et.upper():
                    print(os.path.join(root, file))
                    count += 1
    print("There were {} results in {}".format(count, _path))



def main():
    path = r"V:\\"
    music = ["wav", "wma", "ogg", "mp3", "pcm", "aiff", "aac"]
    text = ["txt"]
    rhino = ["3dm"]
    getRhino(path, music)


if __name__ == "__main__":
    main()