#!/usr/bin/env python
# coding: utf-8

tokens = ['[', '+', 12, '[', '-', 23, 45, ']', ']']

def first_token(token_list):
    ts = token_list
    token = ts[0]
    del ts[0]
    if token == '[':
        exp = []
        while ts[0] != ']':
            t = first_token(ts)
            exp.append(t)
        # 循环结束, 删除末尾的 ']'
        del ts[0]
        return exp
    else:
        # token 需要 process_token / parsed_token
        return token


def pop_list(stack):
    l = []
    while stack[-1] != '[':
        l.append(stack.pop(-1))
    stack.pop(-1)
    l.reverse()
    return l

def parsed_ast(token_list):
    l = []
    i = 0
    while i < len(token_list):
        token = token_list[i]
        i += 1
        if token == ']':
            list_token = pop_list(l)
            l.append(list_token)
        else:
            l.append(token)
    return l


tokens1 = ['[', '+', 12, '[', '-', 23, 45, ']', ']']
tokens2 = ['[', '+', 12, '[', '-', 23, 45, ']', ']']
res_1 = parsed_ast(tokens1+tokens2)
print('stack parse', res_1)

expected_ast = ['+', 12, ['-', 23, 45]]
ast = first_token(tokens)
print(ast)
assert ast == expected_ast
