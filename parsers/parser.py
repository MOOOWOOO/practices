#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python3
# coding: utf-8

class Operator(object):
    def __init__(self):
        self.start = '['
        self.end = ']'
        self.add = '+'
        self.subtract = '-'
        self.multiply = '*'
        self.divide = '/'
        self.space = ' '

        self.operator = [
            self.start, self.end,
            self.add, self.subtract,
            self.multiply, self.divide,
        ]
        self.number = [
            '0', '1', '2', '3', '4',
            '5', '6', '7', '8', '9',
        ]
        self.split = [
            self.space
        ]

    def is_operator(self, item):
        if item in self.operator:
            return True
        else:
            return False

    def is_number(self, item):
        if item in self.number:
            return True
        else:
            return False

    def is_split(self, item):
        if item in self.split:
            return True
        else:
            return False


OPERATOR = Operator()


def parser_main(obj):
    obj_type = type(obj)
    if obj_type == list:
        result = parser_array_to_str(obj)
    elif obj_type == str:
        result = parser_str_to_array(obj)
    else:
        return False, 'please input an array or a string'

    return True, obj, result


def parser_array_to_str(array):
    string = ''
    for item in array:
        string += '{item} '.format(item=item)

    string = string.strip()

    if string.startswith(OPERATOR.start):
        pass
    else:
        string = '{start} {string}'.format(string=string, start=OPERATOR.start)

    if string.endswith(']'):
        pass
    else:
        string = '{string} {end}'.format(string=string, end=OPERATOR.end)

    return True, string


def parser_str_to_array(string):
    array = []
    number = []
    string = string.strip()
    for item in string:
        if OPERATOR.is_operator(item=item):
            push_number(array=array, number=number)
            array.append(item)
        elif OPERATOR.is_number(item=item):
            number.append(item)
        elif OPERATOR.is_split(item):
            push_number(array=array, number=number)
        else:
            return False, 'unknow mark'

    if array[0] == OPERATOR.start:
        pass
    else:
        array.insert(0, OPERATOR.start)

    if array[len(array) - 1] == OPERATOR.end:
        pass
    else:
        array.append(OPERATOR.end)

    return True, array


def push_number(array, number):
    number_length = len(number)
    if number_length:
        num = 0
        for n in range(number_length):
            num += int(number[n]) * 10 ** (number_length - n - 1)
        array.append(num)
        number.clear()
    else:
        pass


if __name__ == '__main__':
    print(parser_main(['[', '+', 12, '[', '-', 23, 45, ']', ']']))
    print(parser_main('[+ 12 [- 23 45]]'))
