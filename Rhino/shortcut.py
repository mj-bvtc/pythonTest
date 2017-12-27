import os, winshell
from win32com.client import Dispatch
import os.path

desktop = winshell.desktop()
path = os.path.join(desktop, "purty.lnk")
target = r"C:\Program Files (x86)\Windows Media Player\wmplayer.exe"
wDir = r"C:\Program Files (x86)\Windows Media Player"
icon = r"C:\Users\mkreidler\Documents\Hopstarter-Mac-Folders-Documents.ico"

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = icon
shortcut.save()
