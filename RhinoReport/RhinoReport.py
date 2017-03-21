import os
import collections
import HiddenFiles

target = r"V:\Projects\Miscericordia University\_Field Work Folder Template (Do Not Delete)\Agi-Renders"
count_global = collections.Counter()        # built-in counting object, used globally
print(f"This is the target path that will be walked: {target}\n")


# walk the tree of the specified target path
for root, dirs, files in os.walk(target):

    # remove hidden files, .psx extensions, and directories that end in .files
    files[:] = [f for f in files if not HiddenFiles.is_hidden(os.path.join(root, f))
                or f.endswith(".psx")]
    dirs[:] = [d for d in dirs if not d.endswith(".files")]

    # only concerned with areas that contain files
    if files:
        count = collections.Counter()   # instantiate local counter
        new_root = root.replace(target+"\\", "")
        print(f"Relative path {new_root} contains: ")

        # search and count file extensions
        for file in files:
            name, ext = os.path.splitext(file)
            count[ext] += 1         # increment local count
            count_global[ext] += 1  # increment global count
            # print(file)            # if interested, uncomment this to see files
        print(count)

    print("\n")                     # create a visual space between directories

# print global counts
print("Global counts: ")
print(count_global)
