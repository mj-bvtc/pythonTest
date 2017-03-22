import re
from decimal import Decimal


def sci_note(num, exponent):
    return num * 10 ** exponent


def big_num_english(number):
    num_string = str(number)
    find = re.compile(r"^[^.]*")
    result = re.search(find, num_string).group(0)
    whole_num = str(result)
    num_digits = len(whole_num)
    magnitude = ['unit(s)', 'ten(s)', 'hundred(s)', 'thousand(s)', 'ten-thousand(s)', 'hundred-thousand(s)',
                 'million(s)', 'ten-million(s)', 'hundred-million(s)', 'billion(s)']
    if num_digits-1 > len(magnitude):
        return "really big number"
    else:
        return whole_num[0] + "." + whole_num[1] + " " +magnitude[num_digits - 1]


def big_num_estimate(number):
    num_string = str(number)
    find = re.compile(r"^[^.]*")
    result = re.search(find, num_string).group(0)
    whole_num = str(result)
    num_digits = len(whole_num)
    if 4 > num_digits > 0:
        return whole_num
    if 7 > num_digits > 3:
        return whole_num[0:(num_digits % 3)] + " thousand"
    if 10 > num_digits > 6:
        return whole_num[0:(num_digits % 3)] + " million"
    if 13 > num_digits > 9:
        return whole_num[0:(num_digits % 3)] + " billion"
    if num_digits >= 13:
        return "really big number"


def num_to_sci_note(number):
    sn = '%.2E' % Decimal(str(number))
    return sn


def main():
    print(num_to_sci_note("800.0000"))
    print(7.342e-10)


if __name__ == "__main__":
    main()
