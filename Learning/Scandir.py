import os


def get_tree_size(path):
    try:
        """Return total size of files in given path and subdirs."""
        total = 0
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                total += get_tree_size(entry.path)
            else:
                total += entry.stat(follow_symlinks=False).st_size
        return total
    except FileNotFoundError:
        return total


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_size(path):
    return sizeof_fmt(get_tree_size(path))

path = "V:\\"
dirs = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
for dir in dirs:
    target = os.path.join(path, dir)
    size = get_tree_size(target)
    human = get_size(target)
    print(f"{dir},{size},{human}")



#size = sizeof_fmt(get_tree_size(path))
#print(size)
