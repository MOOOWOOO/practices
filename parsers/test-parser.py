#!/usr/bin/env python
# coding: utf-8

import nose

from parsers import parser_main


def test_lexer_1_op_2_elements():
    print()
    PROG = '[+ 1 2]'
    res = parser_main(PROG)
    print('test_lexer_1_op_2_elements: ', res)
    assert res[0] is True
    assert type(res[2]) is list


def test_lexer_multi_op_mulit_elements():
    print()
    PROG = '[+ 1 [/ 9 8] [] ]'
    res = parser_main(PROG)
    print('test_lexer_multi_op_mulit_elements: ', res)

    assert res[0] is True
    assert type(res[2]) is list


def test_lexer_start_end_not_match():
    print()
    PROG1 = '[+ 1 [/ 9 8] [] ]]'
    PROG2 = '[+ 1 [/ 9 8] [] '
    PROG3 = '[[+ 1 [/ 9 8] [] ]'
    PROG4 = '+ 1 [/ 9 8] [] ]'
    res1 = parser_main(PROG1)
    print('test_lexer_start_end_not_match 1: ', res1)
    assert res1[0] is True
    assert type(res1[2]) is list

    res2 = parser_main(PROG2)
    print('test_lexer_start_end_not_match 2: ', res2)
    assert res2[0] is True
    assert type(res2[2]) is list

    res3 = parser_main(PROG3)
    print('test_lexer_start_end_not_match 3: ', res3)
    assert res3[0] is True
    assert type(res3[2]) is list

    res4 = parser_main(PROG4)
    print('test_lexer_start_end_not_match 4: ', res4)
    assert res4[0] is True
    assert type(res4[2]) is list


def test_parser_1_op_2_elements():
    print()
    l = ['[', '-', 23, 45, ']']
    res = parser_main(l)
    print('test_parser_1_op_2_elements: ', res)
    assert res[0] is True


def test_parser_multi_op_mulit_elements():
    print()
    l = ['[', '+', 12, '[', '-', 23, 45, ']', '[', '-', 23, 45, ']', ']']
    res = parser_main(l)
    print('test_parser_multi_op_mulit_elements: ', res)
    assert res[0] is True


def test_parser_without_start_end():
    print()
    l1 = ['-', 23, 45]
    l2 = ['+', 12, ['-', 23, 45]]
    l3 = ['+', 12, ['-', 23, 45], ['-', 23, 45, ]]
    res1 = parser_main(l1)
    print('test_parser_without_start_end 1:', res1)
    assert res1[0] is True

    res2 = parser_main(l2)
    print('test_parser_without_start_end 2:', res2)
    assert res2[0] is True

    res3 = parser_main(l3)
    print('test_parser_without_start_end 3:', res3)
    assert res3[0] is True


def test_parser_start_end_not_match():
    print()
    l1 = ['[', '-', 23, 45]
    l2 = ['-', 23, 45, ']']
    l3 = ['[', '-', 23, 45, ']', ']']
    l4 = ['[', '[', '-', 23, 45, ']']
    l5 = ['[', '-', 23, 45, ']', '[']
    l6 = [']', '[', '-', 23, 45, ']']
    res1 = parser_main(l1)
    print('test_parser_start_end_not_match 1:', res1)
    assert res1[0] is True

    res2 = parser_main(l2)
    print('test_parser_start_end_not_match 2:', res2)
    assert res2[0] is True

    res3 = parser_main(l3)
    print('test_parser_start_end_not_match 3:', res3)
    assert res3[0] is True

    res4 = parser_main(l4)
    print('test_parser_start_end_not_match 4:', res4)
    assert res4[0] is True

    res5 = parser_main(l5)
    print('test_parser_start_end_not_match 5:', res5)
    assert res5[0] is True

    res6 = parser_main(l6)
    print('test_parser_start_end_not_match 6:', res6)
    assert res6[0] is True


if __name__ == '__main__':
    nose.runmodule()
