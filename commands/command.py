#!/usr/bin/env python
# coding: utf-8

'''
load REG MEM
store REG MEM
四则/逻辑/比较
jump
'''

base_commands_dict = {
    'load': 'load data from mem to reg',
    'save': 'save data from reg to mem',
    'add':  '任意直接数/寄存器 + 任意直接数/寄存器，结果存入寄存器ra',
    'sub':  '任意直接数/寄存器 - 任意直接数/寄存器，结果存入寄存器ra',
    'mul':  '任意直接数/寄存器 * 任意直接数/寄存器，结果存入寄存器ra',
    'div':  '任意直接数/寄存器 / 任意直接数/寄存器，结果存入寄存器ra',
    'and':  '任意直接数/寄存器 & 任意直接数/寄存器，结果存入寄存器rb',
    'or':   '任意直接数/寄存器 | 任意直接数/寄存器，结果存入寄存器rb',
    'not':  '! 任意直接数/寄存器，结果存入寄存器rb',
    'cmp':  '比较，结果存入寄存器rc',
    'jmp':  '直接跳转，目标地址取自寄存器rd',
    'jpe':  '= 条件跳转，条件取自寄存器rc，目标地址取自寄存器rd',
    'jpl':  '< 条件跳转，条件取自寄存器rc，目标地址取自寄存器rd',
    'jpg':  '> 条件跳转，条件取自寄存器rc，目标地址取自寄存器rd',
}

registers_dict = {
    'RA': 'A 寄存器',
    'RB': 'B 寄存器',
    'RC': 'C 寄存器',
    'RD': 'D 寄存器',
    'SP': '栈指针',
    'IP': '指令指针',
    'ZF': '0位标志',
    'SF': '符号标志',
    'OF': '溢出标志',
}

registers = [
    'ra', 'rb', 'rc', 'rd',
    'sp', 'ip',
    'zf', 'sf', 'of',
]

prog_bc_map = {
    'define': 'load',
    'tag':    'save',
    '+':      'add',
    '-':      'sub',
    '*':      'mul',
    '/':      'div',
    '&':      'and',
    '|':      'or',
    '!':      'not',
    'if':     {
        '=':  'not jpe',
        '!=': 'jpe',
        '<':  'jpg',
        '<=': 'not jpl',
        '>':  'jpl',
        '>=': 'not jpg',
    },
    'goto':   'jmp',
    '=':      'cmp',
    '!=':     'cmp',
    '<':      'cmp',
    '<=':     'cmp',
    '>':      'cmp',
    '>=':     'cmp',
}

bc_oper_reg_map = {
    'add': 'ra',
    'sub': 'ra',
    'mul': 'ra',
    'div': 'ra',
    'and': 'rb',
    'or':  'rb',
    'not': 'rb',
    'jmp': 'ip',
    'jpe': 'ip',
    'jpl': 'ip',
    'jpg': 'ip',
}

bc_mc_map = {
    'load': '00000000',
    'save': '00000001',
    'add':  '00000010',
    'sub':  '00000011',
    'mul':  '00000100',
    'div':  '00000101',
    'and':  '00000110',
    'or':   '00000111',
    'not':  '00001000',
    'cmp':  '00001001',
    'jmp':  '00001010',
    'jpe':  '00001011',
    'jpl':  '00001100',
    'jpg':  '00001101',
}

registers_mc_map = {
    'ra': '10100000',
    'rb': '10110000',
    'rc': '11000000',
    'rd': '11010000',
    'sp': '11100000',
    'ip': '11110000',
    'zf': '00000001',
    'sf': '00000010',
    'of': '00000011',
}


enter_func = '''
save mem ra
save mem rb
save mem rc
save mem rd
save mem zf
save mem sf
save mem of
save mem sp
save mem ip
; mem-func2 怎么获取到？
load ip mem-func2
jmp
load ra mem
load rb mem
load rc mem
load rd mem
load zf mem
load sf mem
load of mem
load sp mem
'''

return_func = '''
load ip mem
; 跳过 enter_func 中 save mem ip 后剩余用于进入函数调用的步骤，即回到 load ra mem 一步
add ip 3
load ip ra
jmp
'''

high_level_prog = '''
[define a 1]
[define b 2]
[define c [+ a b]]
[if [> a b] a b]
'''

asm_prog = '''
; init prog
load ip 0

; [define a 1]
load ra 1

; [define b 2]
load rb 2

; [define c [+ a b]]
add ra rb rc
save rc 3(mem addr)

; [if [> a b] a b]
cmp ra rb rc
jpg ip+2
jpl ip+2

; output a or b
...
'''

mc_prog = '''
; init prog
0b00000000 0b11110000 0b00000000

; [define a 1]
0b00000000 0b10100000 0b00000001

; [define b 2]
0b00000000 0b10110000 0b00000010

; [define c [+ a b]]
0b00000010 0b10100000 0b10110000 0b11000000
0b00000001 0b11000000 0b00000011

; [if [> a b] a b]
0b00001001 0b10100000 0b10110000 0b11000000
0b00001101 0b00000010
0b00001100 0b00000010

; output a or b
...
'''