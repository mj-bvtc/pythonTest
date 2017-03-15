class Book(object):
    """This is a book object"""
    count_global = 0

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.numPages = None
        self.isbn = None
        Book.count_global += 1
        self.count_local = Book.count_global


def happy():
    tree = 8


def main():
    b1 = Book("Mary Had a Little Lamb", "John Smith")
    b2 = Book("ex", "aly b")
    print(b1.title)
    print(b1.author)
    print(b1.__dict__)
    print(Book.count_global)
    print(b2.count_local)
    print(b1.count_local)
    if hasattr(b1, "title"):
        print("Attribute exists")
    else:
        print("Attribute does not exist")

    if "b2" in locals():
        print(3)
    if "tree" in globals():
        print(5)
    if "tree" in locals():
        print(6)
    if "tree" in vars():
        print(4)

if __name__ == "__main__":
    main()
