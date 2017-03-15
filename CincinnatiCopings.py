def separate(item_list, width_a, width_b):
    """Function to split objects into lists"""

    list_a = []
    list_b = []
    list_c = []

    for item in item_list:

        delta_a = abs(width_a - item)
        delta_b = abs(width_b - item)

        if delta_a == delta_b:
            list_c.append(item)
        else:
            if delta_a > delta_b:
                list_b.append(item)
            else:
                list_a.append(item)

    return list_a, list_b, list_c


def main():
    num_list = [12, 14, 15, 12.23, 14.15, 13, 8, 12.89, 13.39]
    width_a = 12
    width_b = 14
    print(separate(num_list, width_a, width_b))


if __name__ == "__main__":
    main()