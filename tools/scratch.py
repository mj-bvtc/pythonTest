import re

test = "BK29 -- broken TbR colOR"

pat = r"--(\s*[a-z0-9\s]*)"

result = re.findall(pat, test)

print(result)


pat2 = r"broken|tbr|color"
r2 = re.findall(pat2, test, re.IGNORECASE)


print(r2)
