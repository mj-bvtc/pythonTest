
result = map(lambda x: x%2==0, [1,2,3,4,5,6,77])
print(list(result))

result = filter(lambda x: x%3!=0, [1,2,3,4,5,6,77])
print(list(result))
