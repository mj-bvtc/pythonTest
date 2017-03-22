import Pancake
import Plants.Flowers as Fl


class Company:
    """ This is a Company Class """

    pi = 3.14

    def __init__(self, co_id):
        self.id = co_id
        self.departmentObjects = []
        self.departmentNames = []
        self.address = None
        self.employees = []
        self.isProfitable = None

    def add_department(self, department):
        self.departmentObjects.append(department)  # class instance list
        self.departmentNames.append(department.id)  # list of department attribute/string names
        self.departmentNames.sort()  # gets all alphabetical-like

    def print_all_slogans(self):
        for dept in self.departmentObjects:
            print(dept.id + ": " + dept.slogan)
        print()

    def num_departments(self):
        num = len(self.departmentNames)
        print("There are {number} departments in {company} \n".format(number=str(num), company=self.id))


def main():
    bv = Company("Boston Valley")
    bv.isProfitable = False
    print(bv.id)
    p = Pancake.Pancake()
    print(p.size)
    if not bv.isProfitable:
        print("We're going down!")
    best_flower = Fl.Rose(46)
    print(best_flower.color)

if __name__ == "__main__":
    main()


