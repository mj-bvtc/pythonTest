import uuid
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Node:
    """Basic connection point"""
    def __init__(self, name):
        self.name = name
        self.connections = []
        self.id = uuid.uuid4()
        self.is_node = None
        self.is_hub = None

    def add_connections(self, *connections):
        for connection in connections:
            self.connections.append(connection)
        return

    def calc_is_node(self):
        if self.connections:
            self.is_node = True
        else:
            self.is_node = False
        return

    def calc_is_hub(self):
        if self.connections.__len__() > 1:
            self.is_hub = True
        else:
            self.is_hub = False
        return
    
    
class Line:
    """Connects two nodes"""
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.id = uuid.uuid4()
        a.add_connections(b)
        b.add_connections(a)
        a.calc_is_node()
        b.calc_is_node()
        a.calc_is_hub()
        b.calc_is_hub()


def main():
    a = Node("a")
    b = Node("b")
    c = Node("c")
    d = Node("d")
    line = Line(a,b)
    line_2 = Line(a,c)
    line_3 = Line(a,d)

    print(list(x.id for x in a.connections))
    print(list(x.id for x in b.connections))

    print(a.is_node)
    print(a.is_hub)
    print(b.is_hub)
    print("Script done!")

if __name__ == "__main__":
    main()

