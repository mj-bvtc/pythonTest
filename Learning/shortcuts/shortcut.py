import os
import winshell
from win32com.client import Dispatch

desktop = winshell.desktop()
path = os.path.join(desktop, "Agibaby.lnk")
target = r"C:\Program Files\Agisoft\PhotoScan Pro\photoscan.exe"
wDir = r"C:\Program Files\Agisoft\PhotoScan Pro"
icon = r"C:\Program Files\Agisoft\PhotoScan Pro\photoscan.exe"

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = icon
shortcut.save()