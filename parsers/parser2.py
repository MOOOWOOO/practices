#!/usr/bin/env python
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
        self.dot = '.'

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
        result = parser_list_to_tree(obj)
    elif obj_type == str:
        result = lexer_str_to_list(obj)
    else:
        return False, 'please input an array or a string'

    return True, obj, result


def parser_array_to_str(array):
    return True


def lexer_str_to_list(string):
    array = []
    sub_array = []
    tmp_string = str()
    string_lenght = len(string)

    def push_tmp_string(array, tmp_string):
        if len(tmp_string):
            array.append(tmp_string)
            tmp_string = ''
        else:
            pass
        return array, tmp_string

    for item in range(string_lenght):
        char = string[item]
        if OPERATOR.is_split(char):
            array, tmp_string = push_tmp_string(array, tmp_string)
            sub_string = string[item + 1:]
            sub_array = lexer_str_to_list(string=sub_string)
            array.extend(sub_array)
            break
        else:
            if OPERATOR.is_operator(char):
                array, tmp_string = push_tmp_string(array, tmp_string)
                array.append(char)
            else:
                tmp_string += char

    return array


def parser_list_to_tree(array):
    array_length = len(array)
    tree = list()
    for number in range(array_length):
        item = array[number]
        if OPERATOR.is_operator(item=item):
            if item == OPERATOR.start:
                sub_array = array[number + 1:]
                item = parser_list_to_tree(sub_array)
                tree.append(item)
                break
            elif item == OPERATOR.end:
                break
            else:
                tree.append(item)
        else:
            if isinstance(item, str):
                if OPERATOR.dot in item:
                    item = float(item)
                else:
                    item = int(item)
            else:
                pass
            tree.append(item)
    return tree


if __name__ == '__main__':
    print(parser_main(['[', '+', '12', '[', '-', '2.3', '45', ']', ']']))
    print(parser_main('[+ 12 [ - 2.3 45 ]]'))
