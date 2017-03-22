def logical_xor(bool_a, bool_b):
    return bool(bool_a) ^ bool(bool_b)


def not_equal(a, b):
    return a != b


def count_to_100():
    i = 0
    while i < 1000000:
        i += 1
        print(i)
    return True


def main():
    a = False
    b = True
    c = True
    print(b and a and count_to_100() and c)
#    print(a & count_to_100())

if __name__ == "__main__":
    main()
