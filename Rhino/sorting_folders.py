import os
import subprocess


class AgiReport:
    def __init__(self, path):
        self.path = path
        self.scandir = os.scandir(self.path)
        self.files = set()
        self.rhinos = set()
        self.objs = set()
        self.dirs = set()
        self.empty_dirs = set()
        self.no_jpeg = set()
        self.jpegs = set()
        self.no_rhino = set()
        self.no_obj = set()

    def scan(self):
        """Recursively yield DirEntry objects for given directory."""

    def scn(path):
        for entry in path:
            print(entry.path)
            if entry.is_dir(follow_symlinks=False):
                if entry.path.endswith(".files"):  # skip Agisoft folders
                    print("skip 1")
                    continue
                if "embedded_files" in entry.path: # skip Agi folders
                    print("skip 2")
                    continue
                self.scan(entry.path)

                self.dirs.add(entry.path)
                print("dir added")
                if len(os.listdir(entry.path)) < 1:
                    self.empty_dirs.add(entry.path)
                    print("this dir empty")
                if entry.path.upper().endswith(".3DM"):
                    self.rhinos.add(entry.path)
                    print("rhino here")
                elif entry.path.upper().endswith(".OBJ"):
                    self.objs.add(entry.path)
                    print("obj here")

                if any(".JPG" in s.upper() for s in os.listdir(entry.path)):
                    self.jpegs.add(entry.path)
                    print("jpg here")
                else:
                    self.no_jpeg.add(entry.path)
                    print("no jpg here")
                if not any(".OBJ" in s.upper() for s in os.listdir(entry.path)):
                    self.no_obj.add(entry.path)
                    print("no obj")
                if not any(".3DM" in s.upper() for s in os.listdir(entry.path)):
                    self.no_rhino.add(entry.path)
                    print("no rhino")

    def any(self, ext, test_dir):
        if not any(ext.upper() in s.upper() for s in os.listdir(self.path)):
            print(f"{ext} not in {test_dir}")


def scan(input_path):
    rhinos = []
    objs = []
    dirs = []
    empty_dirs = set()
    no_jpeg = set()
    jpegs = set()
    no_rhino = set()
    no_obj = set()


    def scan_tree(input_path):
        """Recursively yield DirEntry objects for given directory."""

        for entry in os.scandir(input_path):
            if entry.is_dir(follow_symlinks=False):
                if entry.path.endswith(".files"):  # skip Agisoft folders
                    continue
                elif "embedded_files" in entry.path: # skip Agi folders
                    continue
                scan_tree(entry.path)

                dirs.append(entry.path)
                # print(entry.path)
                if len(os.listdir(entry.path)) < 1:
                    empty_dirs.add(entry.path)
                if entry.path.upper().endswith(".3DM"):
                    rhinos.append(entry.path)
                elif entry.path.upper().endswith(".OBJ"):
                    objs.append(entry.path)

                if any(".JPG" in s.upper() for s in os.listdir(entry.path)):
                    jpegs.add(entry.path)
                else:
                    no_jpeg.add(entry.path)
                if not any(".OBJ" in s.upper() for s in os.listdir(entry.path)):
                    no_obj.add(entry.path)
                if not any(".3DM" in s.upper() for s in os.listdir(entry.path)):
                    no_rhino.add(entry.path)


    scan_tree(input_path)
    return rhinos, objs, dirs, empty_dirs, no_jpeg


def open_in_explorer(path):
    subprocess.Popen(f'explorer "{path}"')


def experiments():

    path = r"V:\Projects\Moynihan Station Phase II\Field Work\Agi-Renders"

    return scan(path)

    # print(len(dirs)==len(set(dirs)))  # shows that no duplicate paths exist

    # print(f"Len of rhinos: {len(rhinos)}")
    # print(f"Len of objs: {len(objs)}")
    # print(f"Len of dirs: {len(dirs)}")


    # for d in dirs:
    #     if any(file.path.upper().endswith(".JPG") for file in os.scandir(d)):
    #         #print(d)
    #         pass
    #     else:
    #         print(f"NOT HEREEEEEEEEEEEEEEEEEEEEEEEE {d}")


def tree_walk():
    path = r"V:\Projects\Moynihan Station Phase II\Field Work\Agi-Renders"

    for root, dirs, files in os.walk(path):
        for file_ in files:
            print(os.path.join(root, file_))


path = r"V:\Projects\Moynihan Station Phase II\Field Work\Agi-Renders"
ar = AgiReport(path)
ar.scan(ar.path)

print(ar.dirs)
print(ar.rhinos)
print(ar.empty_dirs)
print(ar.jpegs)
print(ar.objs)
print(ar.no_obj)

