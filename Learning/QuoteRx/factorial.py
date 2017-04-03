"""
Learning how to call a recursive function in python.

This module simply recreates the factorial 
algorithm via a recursive function call. 
"""


def factorial(number):
    if number <= 1:
        print(number)
        return 1
    else:
        result = number * factorial(number - 1)
        print(result)
        return result

def main():
    factorial(5)

if __name__ == "__main__":
    main()
