fruits = ["apple", "banana", "orange"]
citrus = ["orange"]

def split(group, items):
    for item in items:
        if item not in group:
            print "Error: '{}' not in {}".format(item, group)
            return 
    b = [x for x in group if x not in items]
    for thing in items:
        group.remove(thing)


split(fruits, citrus)
print fruits
print citrus



