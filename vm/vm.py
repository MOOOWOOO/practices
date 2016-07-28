#!/usr/bin/env python
# coding: utf-8

RUNNING = True
STACK_BOTTOM = 0
STACK_LENGTH = 10
STACK = [None] * STACK_LENGTH
PROGRAM = list()

ip = 0  # instruction pointer
sp = -1  # stack pointer

ERROR_MSG = {
    'NEED_REGISTER': '*** registers error: need registers',
    'NEED_NUMBER': '*** number error: need numbers',
    'NEED_STACK': '*** stack error: need stack',
    'NULL_STACK': '*** stack error: stack is empty',
    'FULL_STACK': '*** stack error: stack overflow',
}

DATA_STYLE = {
    'NUM': [int, float, ],
    'STR': [str, ],
    'SET': [set, list, dict],
}


def push_value():
    global ip
    global PROGRAM
    global STACK
    global sp

    sp += 1
    if sp >= len(STACK):
        return False, ERROR_MSG['FULL_STACK']
    ip += 1

    STACK[sp] = PROGRAM[ip]

    return True, STACK[sp]


def pop_value():
    global STACK
    global sp

    if sp < STACK_BOTTOM:
        return False, ERROR_MSG['NULL_STACK']

    val = STACK[sp]
    sp -= 1

    return True, val


def add():
    global STACK
    global sp
    val_1 = STACK[sp]
    sp -= 1

    if type(val_1) not in DATA_STYLE['NUM']:
        return False, ERROR_MSG['NEED_NUMBER']

    val_2 = STACK[sp]
    sp -= 1

    if type(val_2) not in DATA_STYLE['NUM']:
        return False, ERROR_MSG['NEED_NUMBER']

    val = val_1 + val_2
    sp += 1

    STACK[sp] = val
    return True, STACK[sp]


def set_value():
    global ip
    global PROGRAM
    global OPERATOR

    ip += 1
    reg = PROGRAM[ip]

    if reg in OPERATOR['REGISTERS']:
        pass
    else:
        return False, ERROR_MSG['NEED_REGISTER']

    ip += 1
    val = PROGRAM[ip]
    if type(val) in [int, float]:
        OPERATOR[reg] = val
        return True, OPERATOR[reg]
    else:
        return False, ERROR_MSG['NEED_NUMBER']


def mov():
    global ip
    global PROGRAM
    global OPERATOR

    ip += 1
    reg_1 = PROGRAM[ip]

    if reg_1 in OPERATOR['REGISTERS']:
        pass
    else:
        return False, ERROR_MSG['NEED_REGISTER']

    ip += 1
    reg_2 = PROGRAM[ip]
    if reg_2 in OPERATOR['REGISTERS'] or type(reg_2) in [int, float]:
        reg_1 = reg_2
        return True, reg_1
    else:
        return False, '{0}\nor\n{1}'.format(ERROR_MSG['NEED_REGISTER'], ERROR_MSG['NEED_NUMBER'])


def hlt():
    global RUNNING
    RUNNING = False
    return True, RUNNING


OPERATOR = {
    'PUSH': push_value,
    'POP': pop_value,
    'ADD': add,
    'SET': set_value,
    'MOV': mov,
    'HLT': hlt,
    'REGISTERS': {
        'A': 0,
        'B': 0,
        'C': 0,
        'D': 0,
        'SP': 0,
        'PC': 0,
    },
}


def vm_main(PROG):
    global OPERATOR
    global ip
    global PROGRAM

    PROGRAM = PROG

    program_length = len(PROGRAM)
    result = None
    data = None
    while RUNNING and ip < program_length:
        op = PROGRAM[ip]
        result, data = OPERATOR[op]()
        if result:
            ip += 1
        else:
            data = '{msg}\nbroken on line {ip}.'.format(msg=data, ip=ip)
            break

    global STACK
    return result, data, STACK


if __name__ == '__main__':
    PROGRAM = [
        'PUSH', 1,
        'PUSH', 2,
        'ADD',
        'POP',
        'HLT'
    ]
    print(vm_main(PROGRAM))
