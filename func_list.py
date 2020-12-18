# Author : Mayukh Gautam
# Functions for summation calculator

def to_list(string):
    return [char for char in string]


def list_to_string(list_char):
    string = ""
    for char in list_char:
        string += char
    return string


def find_num(eq, index_of_operator, bool_is_left):
    num_s = ""
    if bool_is_left:
        for x in range(index_of_operator):
            if is_char_num(eq[index_of_operator - x - 1]):
                num_s += eq[index_of_operator - x - 1]
            else:
                break
        num_s = to_list(num_s)
        num_s.reverse()

    else:
        for x in range(len(eq) - index_of_operator - 1):
            if is_char_num(eq[index_of_operator + x + 1]):
                num_s += eq[index_of_operator + x + 1]
            else:
                break

    return list_to_string(num_s)


NUMS = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "$", "%", "&", ">"}


def is_char_num(char):
    # non number chars aside for '.' are replacement characters
    # $ = -, % = e+, & = e-, > = inf
    return char in NUMS


def deserialize(eq):
    eq = eq.replace("$", "-")
    eq = eq.replace("%", "e+")
    eq = eq.replace("&", "e-")
    eq = eq.replace(">", "inf")
    return eq


def serialize(eq):
    eq = eq.replace("-", "$")
    eq = eq.replace("e+", "%")
    eq = eq.replace("e-", "&")
    eq = eq.replace("inf", ">")
    return eq
