#import PhotoScan
import csv
import re
import os


class Report:
    def __init__(self):
        self.my_dict = {}
        self.paths = []
        self.save_location = None
        self.save_name = None

    def add_paths(self, *paths):
        for path in paths:
            self.paths.append(path)
            return

    def set_location(self, path):
        self.save_location = path
        return path

    def set_name(self, name):
        self.save_name = name
        return name

    def run(self, location, name):
        self.set_location(location)
        self.set_name(name)
        for path in self.paths:
            self.read_text(path)
            self.export_csv()

    def read_text(self, path):
        file = open(path, "r")
        count = 0
        for line in file:
            if line.strip() == '':
                continue
            else:
                key = in_quotes(line)
                value = find_float(line)
                if key and value:
                    set_kv(self.my_dict, key[0], value[0])
                if re.search("User:", line):
                    user = re.sub("User:", "", line.strip())
                    set_kv(self.my_dict, "user@computer", user)
                if re.search("Project", line):
                    path = re.sub("Project file path:", "", line.strip())
                    set_kv(self.my_dict, "path", path)
                if re.search("Chunk:", line):
                    chunk = re.sub("Chunk:", "", line.strip())
                    set_kv(self.my_dict, "chunk", chunk)
                if count == 0:
                    set_kv(self.my_dict, "date/time", line.rstrip())
                count += 1

    def export_csv(self):
        name = self.save_name
        file = os.path.join(self.save_location, name)
        if os.path.exists(file):
            # this is adding rows to doc
            with open(file, 'a', newline="\n", encoding="utf8") as csv_file:
                w = csv.DictWriter(csv_file, self.my_dict.keys())
                w.writerow(self.my_dict)
        else:
            # this is the first entry in file
            with open(file, 'w', newline="\n", encoding="utf8") as csv_file:
                w = csv.DictWriter(csv_file, self.my_dict.keys())
                w.writeheader()
                w.writerow(self.my_dict)


def read_text(path):
    file = open(path, "r")
    count = 0
    for line in file:
        if line.strip() == '':
            continue
        else:
            key = in_quotes(line)
            value = find_float(line)
            if key and value:
                set_kv(my_dict, key[0], value[0])
            if re.search("User:", line):
                user = re.sub("User:", "", line.strip())
                set_kv(my_dict, "user@computer", user)
            if re.search("Project", line):
                path = re.sub("Project file path:", "", line.strip())
                set_kv(my_dict, "path", path)
            if re.search("Chunk:", line):
                chunk = re.sub("Chunk:", "", line.strip())
                set_kv(my_dict, "chunk", chunk)
            if count == 0:
                set_kv(my_dict, "date/time", line.rstrip())
            count += 1


def in_quotes(line):
    result = re.findall(r"'(\w+)'", line)
    return result


def find_float(line):
    result = re.findall("\d+\.\d+", line)
    return result


def set_kv(dict, k, v):
    dict[k] = v
    return dict


def export_csv(folder_path):
    name = "report.csv"
    file = os.path.join(folder_path, name)
    if os.path.exists(file):
        # this is adding rows to doc
        with open(file, 'a', newline="\n", encoding="utf8") as csv_file:
            w = csv.DictWriter(csv_file, my_dict.keys())
            w.writerow(my_dict)
    else:
        # this is the first entry in file
        with open(file, 'w', newline="\n", encoding="utf8") as csv_file:
            w = csv.DictWriter(csv_file, my_dict.keys())
            w.writeheader()
            w.writerow(my_dict)

paths = []
file = open(r"C:\Users\mkreidler\Desktop\agifolders.txt", 'r')
for line in file:
    paths.append(line.replace("\n", ""))
    #print(line)


r = Report()
r.paths = paths
r.run(r"C:\Users\mkreidler\Desktop", "CompiledReports.csv")
