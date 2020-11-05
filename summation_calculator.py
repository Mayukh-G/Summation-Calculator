# Author : Mayukh Gautam
# Calculator that returns the value of a summation, very limited, only works with definite sums
# How to use located at the bottom


# Starts from 1
def sum(pattern, summed_var, summed_to_var_with_equal):
    summed_to_var_with_equal = split(summed_to_var_with_equal)

    summed_to_var = summed_to_var_with_equal[0]
    summed_to_value = int(find_num(summed_to_var_with_equal, 1, False))

    total = 0
    for i in range(summed_to_value):
        total += operate(equation=pattern,
                         summed_var=summed_var,
                         summed_var_val=i+1,
                         summed_to_var=summed_to_var,
                         summed_to_var_val=summed_to_value)
    return total


def operate(equation, summed_var, summed_var_val, summed_to_var, summed_to_var_val):
    # This list will function like a coordinate system
    # list of lists
    # Older elements have priority over older ones
    # To accomplish this the list is flipped after being created
    # element format : [start_index, end_index]
    priority_list = []
    equation = equation.replace(summed_var, str(summed_var_val))
    equation = equation.replace(summed_to_var, str(summed_to_var_val))

    while equation.find("(") >= 0:
        start = equation.find("(")
        end = equation.rfind(")")
        priority_list.append([start, end])
        equation = split(equation)
        equation[start] = "O"
        equation[end] = "C"
        equation = join(equation)

    priority_list.reverse()
    if len(priority_list) != 0:
        for coords in priority_list:
            len_of_backet = coords[1] - coords[0] - 1
            to_replace = equation[coords[0]:len_of_backet+2]
            sub_equation = equation[coords[0]+1:len_of_backet+1]
            sub_equation = add(divide(multiply(sub_equation)))
            equation = equation.replace(to_replace, sub_equation)
    return float(add(divide(multiply(equation))))


def multiply(eq):
    if eq.find("*") >= 0:
        eq = eq.replace("-", "m")
        while eq.find("*") >= 0:
            pre_replacement_str = ""
            mult_index = eq.find("*")
            v1 = find_num(eq, mult_index, bool_is_left=True)
            pre_replacement_str += v1

            pre_replacement_str += "*"

            v2 = find_num(eq, mult_index, bool_is_left=False)
            pre_replacement_str += v2

            v1 = v1.replace("m", "-")
            v2 = v2.replace("m", "-")
            ans = str(float(v1) * float(v2))
            eq = eq.replace(pre_replacement_str, ans, 1)

    eq = eq.replace("m", "-")
    return eq


def divide(eq):
    if eq.find("/") >= 0:
        eq = eq.replace("-", "m")
        while eq.find("/") >= 0:
            pre_replacement_str = ""
            mult_index = eq.find("/")
            v1 = find_num(eq, mult_index, bool_is_left=True)
            pre_replacement_str += v1

            pre_replacement_str += "/"

            v2 = find_num(eq, mult_index, bool_is_left=False)
            pre_replacement_str += v2

            v1 = v1.replace("m", "-")
            v2 = v2.replace("m", "-")
            ans = str(float(v1) / float(v2))
            eq = eq.replace(pre_replacement_str, ans, 1)

    eq = eq.replace("m", "-")
    return eq


def subtract(eq):
    """
    Should never in theory be called buy itself.
    Use add(eq) instead
    """
    if eq[0] == "-":
        eq = eq.replace("-", "m", 1)
    if eq.find("-") >= 0:
        while eq.find("-") >= 0:
            pre_replacement_str = ""
            mult_index = eq.find("-")
            v1 = find_num(eq, mult_index, bool_is_left=True)
            pre_replacement_str += v1
            v1 = v1.replace("m", "-")

            pre_replacement_str += "-"

            v2 = find_num(eq, mult_index, bool_is_left=False)
            pre_replacement_str += v2
            v2 = v2.replace("m", "-")

            ans = str(float(v1) - float(v2))
            eq = eq.replace(pre_replacement_str, ans, 1)
            if float(ans) < 0:
                eq = eq.replace("-", "m", 1)

    eq = eq.replace("m", "-")
    return eq


def add(eq):
    if eq.find("+-") >= 0 or eq.find("-+") >= 0:
        eq = eq.replace("+-", "-")
        eq = eq.replace("-+", "-")
        eq = subtract(eq)
    eq = subtract(eq)
    if eq.find("+") >= 0:
        while eq.find("+") >= 0:
            pre_replacement_str = ""
            mult_index = eq.find("+")
            v1 = find_num(eq, mult_index, bool_is_left=True)
            pre_replacement_str += v1
            v1 = v1.replace("m", "-")

            pre_replacement_str += "+"

            v2 = find_num(eq, mult_index, bool_is_left=False)
            pre_replacement_str += v2
            v2 = v2.replace("m", "-")

            ans = str(float(v1) + float(v2))
            eq = eq.replace(pre_replacement_str, ans, 1)
            if float(ans) < 0:
                eq = eq.replace("-", "m", 1)

    eq = eq.replace("m", "-")
    return eq


def split(string):
    return [char for char in string]


def join(list_char):
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
        num_s = split(num_s)
        num_s.reverse()

    else:
        for x in range(len(eq)-index_of_operator-1):
            if is_char_num(eq[index_of_operator + x + 1]):
                num_s += eq[index_of_operator + x + 1]
            else:
                break

    return join(num_s)


def is_char_num(char):
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "m"]
    for num in nums:
        if char == num:
            return True
    return False


# HOW TO USE:
# For {param} pattern:
#   Enter a string that represents your equation :
#       Implicit multiplication is not recognized
#       No whitespace characters present
#       Power is represented by '^' (Does not Work Yet)
# For {param} summed_var:
#   Enter the character with which you want to represent the variable that will be summed to:
#       Must NOT be 'm'
#       Must be a single character
#       Must be consistent with {param} pattern
# For {param} summed_to_var_with_equal:
#   Enter a string containing the variable you will use to represent the end value, an equal sign, and the end value:
#   Example : "j=10"
#   Variable must NOT be "m"
#   No whitespace characters present
#   End value must be a positive integer

summation = sum(pattern="(n*7+i)+n*i", summed_var="i", summed_to_var_with_equal="n=100")
print(summation)
