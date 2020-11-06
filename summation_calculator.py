# Author : Mayukh Gautam
# Calculator that returns the value of a summation, very limited, only works with definite sums
# How to use located at the bottom

# TODO :
#  Make really large numbers work, those displayed with xeX
#  Make special functions work ex: sin and cos
#  Make special values recognized ex: pi, e


# Starts from 1
def do_sum(pattern, summed_var, summed_to_var_with_equal):
    """
    Separates String where necessary and adding accumulates total

    :param pattern: String that represents the equation
    :param summed_var: Character representing the variable that is being increased each call
    :param summed_to_var_with_equal: Character representing variable that is being summed to
    :return: Float answer to sum
    """
    summed_to_var_with_equal = split(summed_to_var_with_equal)

    summed_to_var = summed_to_var_with_equal[0]
    summed_to_value = int(find_num(summed_to_var_with_equal, 1, bool_is_left=False))

    total = 0
    for i in range(summed_to_value):
        total += operate(equation=pattern,
                         summed_var=summed_var,
                         summed_var_val=i+1,
                         summed_to_var=summed_to_var,
                         summed_to_var_val=summed_to_value)
    return total


def operate(equation, summed_var, summed_var_val, summed_to_var, summed_to_var_val):
    """
    Establishes bracket priority in equations and starts the operation chain by calling start_and_power(eq), passes
    equation as arg

    :param equation: String representing equation
    :param summed_var: Character representing the variable that is being increased each call
    :param summed_var_val: Int value of the variable being increased
    :param summed_to_var: Character representing variable that is being summed to
    :param summed_to_var_val: Int value of the variable that is being summed to
    :return: A Float which has the same value as the equation which is passed in
    """
    # This list will function like a coordinate system
    # Older elements have priority over newer ones
    # To accomplish this the list is flipped after being created
    # element format : [start_index, end_index]
    priority_list = []
    original = equation
    equation = equation.replace(summed_var, str(summed_var_val))
    equation = equation.replace(summed_to_var, str(summed_to_var_val))

    while equation.find("(") >= 0 or equation.find(")") >= 0:
        start = equation.find("(")
        end = equation.rfind(")")
        if start == -1 or end == -1:
            raise SyntaxError(f"Incomplete Brackets in equation : {original}")
        elif end - start == -1:
            raise SyntaxError(f"Empty Brackets in equation : {original}")
        priority_list.append([start, end])
        equation = split(equation)
        equation[start] = "@"
        equation[end] = "#"
        equation = join(equation)

    priority_list.reverse()
    if len(priority_list) != 0:
        for coords in priority_list:
            if (len(equation) - coords[1] - 1) == 0:
                to_replace = equation[coords[0]:]
            else:
                to_replace = equation[coords[0]: -(len(equation) - coords[1] - 1)]
            if (len(equation) - coords[1]) == 0:
                sub_equation = equation[coords[0] + 1:]
            else:
                sub_equation = equation[coords[0]+1: -(len(equation) - coords[1])]
            sub_equation = start_and_power(eq=sub_equation)
            equation = equation.replace(to_replace, sub_equation)
    return float(start_and_power(eq=equation))


def multiply(eq):
    """
    Finds numbers in a string, finds all the '*' operators and performs all divisions
    Calls divide(eq) and passes modified string as arg
    Is called by start_and_power(eq)
    Should never in theory be called by itself.
    Use start_and_power(eq) instead

    :param eq: equation as a string, only numbers no variables
    :type eq: String
    :returns: Final modified string after all operations were executed
    """
    if eq.find("*") >= 0:
        eq = eq.replace("-", "$")
        while eq.find("*") >= 0:
            pre_replacement_str = ""
            mult_index = eq.find("*")
            v1 = find_num(eq, mult_index, bool_is_left=True)
            pre_replacement_str += v1

            pre_replacement_str += "*"

            v2 = find_num(eq, mult_index, bool_is_left=False)
            pre_replacement_str += v2

            v1 = v1.replace("$", "-")
            v2 = v2.replace("$", "-")
            ans = str(float(v1) * float(v2))
            eq = eq.replace(pre_replacement_str, ans, 1)

    eq = eq.replace("$", "-")
    return divide(eq)


def divide(eq):
    """
    Finds numbers in a string, finds all the '/' operators and performs all divisions
    Calls add(eq) and passes modified string as arg
    Is called by multiply(eq)
    Should never in theory be called by itself.
    Use start_and_power(eq) instead

    :param eq: equation as a string, only numbers no variables
    :type eq: String
    :returns: Final modified string after all operations were executed
    """
    if eq.find("/") >= 0:
        eq = eq.replace("-", "$")
        while eq.find("/") >= 0:
            pre_replacement_str = ""
            mult_index = eq.find("/")
            v1 = find_num(eq, mult_index, bool_is_left=True)
            pre_replacement_str += v1

            pre_replacement_str += "/"

            v2 = find_num(eq, mult_index, bool_is_left=False)
            pre_replacement_str += v2

            v1 = v1.replace("$", "-")
            v2 = v2.replace("$", "-")
            ans = str(float(v1) / float(v2))
            eq = eq.replace(pre_replacement_str, ans, 1)

    eq = eq.replace("$", "-")
    return add(eq)


def subtract(eq):
    """
    Finds numbers in a string, finds all the '-' operators and performs all subtraction
    Is called by add(eq)
    Should never in theory be called by itself.
    Use start_and_power(eq) instead

    :param eq: equation as a string, only numbers no variables
    :type eq: String
    :return eq: Modified string, after all subtractions have been executed
    """
    if eq[0] == "-":
        eq = eq.replace("-", "$", 1)
    if eq.find("-") >= 0:
        while eq.find("-") >= 0:
            pre_replacement_str = ""
            mult_index = eq.find("-")
            v1 = find_num(eq, mult_index, bool_is_left=True)
            pre_replacement_str += v1
            v1 = v1.replace("$", "-")

            pre_replacement_str += "-"

            v2 = find_num(eq, mult_index, bool_is_left=False)
            pre_replacement_str += v2
            v2 = v2.replace("$", "-")

            ans = str(float(v1) - float(v2))
            eq = eq.replace(pre_replacement_str, ans, 1)
            if float(ans) < 0:
                eq = eq.replace("-", "$", 1)

    eq = eq.replace("$", "-")
    return eq


def add(eq):
    """
        Finds numbers in a string, finds all the '+' and '+-' or '-+' operators and performs all additions
        Calls subtract(eq) with eq as arg and sets eq to the return value before adding
        Is called by divide(eq)
        Should never in theory be called by itself
        Use start_and_power(eq) instead

        :param eq: equation as a string, only numbers no variables
        :type eq: String
        :returns: Final modified string after all operations were executed
    """
    if eq.find("+-") >= 0 or eq.find("-+") >= 0:
        eq = eq.replace("+-", "-")
        eq = eq.replace("-+", "-")
    eq = subtract(eq)
    if eq.find("+") >= 0:
        while eq.find("+") >= 0:
            pre_replacement_str = ""
            mult_index = eq.find("+")
            v1 = find_num(eq, mult_index, bool_is_left=True)
            pre_replacement_str += v1
            v1 = v1.replace("$", "-")

            pre_replacement_str += "+"

            v2 = find_num(eq, mult_index, bool_is_left=False)
            pre_replacement_str += v2
            v2 = v2.replace("$", "-")

            ans = str(float(v1) + float(v2))
            eq = eq.replace(pre_replacement_str, ans, 1)

    eq = eq.replace("$", "-")
    return eq


def start_and_power(eq):
    """
        Finds numbers in a string, finds all the '^' operators and performs all power operations
        Starting point for operations
        Calls multiply(eq) and passes modified string as arg

        :param eq: equation as a string, only numbers no variables
        :type eq: String
        :returns: Final modified string after all operations were executed
    """
    if eq.find("^") >= 0:
        eq = eq.replace("-", "$")
        while eq.find("^") >= 0:
            pre_replacement_str = ""
            mult_index = eq.find("^")
            v1 = find_num(eq, mult_index, bool_is_left=True)
            pre_replacement_str += v1
            v1 = v1.replace("$", "-")

            pre_replacement_str += "^"

            v2 = find_num(eq, mult_index, bool_is_left=False)
            pre_replacement_str += v2
            v2 = v2.replace("$", "-")

            ans = str(pow(float(v1), float(v2)))
            eq = eq.replace(pre_replacement_str, ans, 1)

    eq = eq.replace("$", "-")
    return multiply(eq)


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
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "$"]
    for num in nums:
        if char == num:
            return True
    return False


# HOW TO USE:
# For {param} pattern:
#   Enter a string that represents your equation :
#       *Implicit multiplication is not recognized
#       *No whitespace characters present
#       *Power is represented by '^'
#       *To represent a negative number's power, use this format (-x^y).
#       *To exclude the negative use this format, -(x^y)
# For {param} summed_var:
#   Enter the character with which you want to represent the variable that will be summed to:
#       Must be a single character
#       Must be consistent with {param} pattern
# For {param} summed_to_var_with_equal:
#   Enter a string containing the variable you will use to represent the end value, an equal sign, and the end value:
#   Example : "j=10"
#   No whitespace characters present
#   End value must be a positive integer

summation = do_sum(pattern="(i/n)()*2^i", summed_var="i", summed_to_var_with_equal="n=2")
print(summation)
