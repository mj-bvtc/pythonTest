import win32api, win32con


def is_hidden(path):
    """
    Takes a path and determines whether
    that file or folder is hidden

    input: path to file/folder
    returns: boolean
    """
    attribute = win32api.GetFileAttributes(path)
    even_odd = attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    return bool(even_odd)


