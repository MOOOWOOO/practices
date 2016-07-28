#!/usr/bin/env python
# coding: utf-8

commands = {
    'PUSH': '入栈',
    'POP': '出栈',
    'MOV': '寄存器TO栈/栈TO寄存器/寄存器TO寄存器/直接数TO寄存器',
    'ADD': '+',
    'SUB': '-',
    'MLT': '*',
    'DIV': '/',
    'AND': '&&',
    'OR': '||',
    'NOT': '!',
    'LOOP': '循环',
    'JMP': '跳转',
    'RTN': '返回',
    'CMP': '比较',
    'WAIT': '等待',
    'HLT': '停止',
}

commands_machine_code={
    'PUSH': 0B0000,
    'POP': 0B0001,
    'MOV': 0B0010,
    'ADD': 0B0011,
    'SUB': 0B0100,
    'MLT': 0B0101,
    'DIV': 0B0110,
    'AND': 0B0111,
    'OR': 0B1000,
    'NOT': 0B1001,
    'LOOP': 0B1010,
    'JMP': 0B1011,
    'RTN': 0B1100,
    'CMP': 0B1101,
    'WAIT': 0B1110,
    'HLT': 0B1111,
}

registers = {
    'ZF': 'ZERO FLAG',
    'TF': 'TYPE FLAG: REGISTER-0, STACK-1, NUMBER-2',
    'RA': 'REGISTER A',
    'RB': 'REGISTER B',
    'RC': 'REGISTER C',
    'RD': 'REGISTER D',
    'IP': 'INSTRUCTION POINTER',
    'SP': 'STACK POINTER',
}

registers_machine_code = {
    'RA': 0B0000,
    'RB': 0B0001,
    'RC': 0B0010,
    'RD': 0B0011,
    'IP': 0B0100,
    'SP': 0B0101,
    'ZF': 0B0110,
    'TF': 0B0111,
}

assembly_example = '''
    MOV RA 1
    MOV RB 2
    ADD
    PUSH RA
    HLT
'''

mc_example = '''
    0B0010 0B0000 0B0001
    0B0010 0B0001 0B0010
    0B0111
    0B0000 0B0000
    0B1111
'''
