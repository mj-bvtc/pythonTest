import rhinoscriptsyntax as rs
import random
import time
import Rhino

obj = "7cd0c918-89ab-4481-92e7-47553185fd98"


def rand_color():
    r = lambda: random.randint(0,255)
    color = [r(),r(),r()]
    return color


def change():
    for i in range(200):
        color = rand_color()
        print color
        rs.ObjectColor(obj, color )
        time.sleep(.001)
        Rhino.RhinoApp.Wait()

def main():
    change()

if __name__ == "__main__":
    main()