import re


ids = ["B6", "B7", "B123", "B12-1"]

ex_string = "Jessica is 15 years old, and Daniel is 27 years old."


for id in ids:
    pat = r"[A-Za-z]{1,3}[1-9][]"
    find = re.findall(pat, id)
    print(find)




ages = re.findall(r"\d{1,3}", ex_string)
names = re.findall(r"[A-Z][a-z]*", ex_string)

age_dict = {}

for index, name in enumerate(names):
    print(index, name)
    age_dict[name] = ages[index]

print(age_dict)
