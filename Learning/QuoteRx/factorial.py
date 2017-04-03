"""Learning how to call a recursive function in python"""

def factorial(number):
    if number <= 1:
        print(number)
        return 1
    else:
        result = number * factorial(number - 1)
        print(result)
        return result

factorial(100)
