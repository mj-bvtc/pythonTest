import common
import business


class Employee(common.Common):
    """A worker in a business"""
    def __init__(self, first, last, dob):
        super().__init__()
        self.first = first
        self.last = last
        self.dob = dob
        self.business = None
        self.pay = None
        self.department = None
        self.start_date = None
        self.ssn = None

    @property
    def full_name(self):
        name = f"{self.first} {self.last}"
        return name


class BvtcEmployee(Employee):
    def __init__(self, first, last, dob):
        super().__init__(first, last, dob)
        self.business = business.BVTC


def main():
    bv = business.BVTC()
    mk = BvtcEmployee("Matthew", "Kurdsley", 19851221)
    mk.business = bv
    print(mk.full_name)
    mk.first = "Jane"
    print(mk.full_name)
    mk.ssn = 123456789
    print(mk.business.motto)

if __name__ == "__main__":
    main()
