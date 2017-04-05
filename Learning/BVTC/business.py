import common


class Business(common.Common):
    """A entity that produces a product"""
    def __init__(self, name, product):
        super().__init__()
        self.name = name
        self.product = product
        self.departments = []
        self.motto = None


class BVTC(Business):
    def __init__(self):
        super().__init__("Boston Valley Terra Cotta", "Architectural Terracotta")
        self.motto = "To make the best friggin' tc on the market!"
