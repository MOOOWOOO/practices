#!/usr/bin/env python
# coding: utf-8

running = True


def push_value():
    global ip
    global PROGRAM
    global STACK
    global sp

    sp += 1
    ip += 1

    STACK[sp] = PROGRAM[ip]


def pop_value():
    global STACK
    global sp
    val = STACK[sp]
    STACK.remove(STACK[sp])
    sp -= 1

    print(val)

    return val


def add():
    global STACK
    global sp
    val_1 = STACK[sp]
    sp -= 1

    val_2 = STACK[sp]
    sp -= 1

    val = val_1 + val_2
    sp += 1

    STACK[sp] = val



def set_value():
    global ip
    global PROGRAM
    global OPERATOR
    global ERROR_MSG

    ip += 1
    reg = PROGRAM[ip]

    if reg in OPERATOR['REG']:
        pass
    else:
        return ERROR_MSG['REG_ERROR']

    ip += 1
    val = PROGRAM[ip]
    if type(val) in [int, float]:
        OPERATOR[reg] = val
    else:
        return ERROR_MSG['NUMBER_ERROR']


def mov():
    global ip
    global PROGRAM
    global OPERATOR
    global ERROR_MSG

    ip += 1
    reg_1 = PROGRAM[ip]

    if reg_1 in OPERATOR['REG']:
        pass
    else:
        return ERROR_MSG['REG_ERROR']

    ip += 1
    reg_2 = PROGRAM[ip]
    if reg_2 in OPERATOR['REG'] or type(reg_2) in [int, float]:
        reg_1 = reg_2
    else:
        return '{0}\nor\n{1}'.format(ERROR_MSG['REG_ERROR'], ERROR_MSG['NUMBER_ERROR'])


def hlt():
    global running
    running = False


ERROR_MSG = {
    'REG_ERROR': '*** registers error: need registers',
    'NUMBER_ERROR': '*** number error: need numbers',
    'STACK_ERROR': '*** stack error: need stack'
}

REGISTERS = {
    'A': list(),
    'B': list(),
    'C': list(),
    'D': list(),
    'SP': list(),
    'PC': list(),
    'NUM': list(),
}

# PROGRAM = list()
PROGRAM = [
    'PUSH', 1,
    'PUSH', 2,
    'ADD',
    'POP',
    'HLT'
]

STACK = [-1]*100

ip = 0  # instruction pointer
sp = -1  # stack pointer

OPERATOR = {
    'PUSH': push_value,
    'POP': pop_value,
    'ADD': add,
    'SET': set_value,
    'MOV': mov,
    'HLT': hlt,
    'REG': {
        'REG_A': REGISTERS['A'],
        'REG_B': REGISTERS['B'],
        'REG_C': REGISTERS['C'],
        'REG_D': REGISTERS['D'],
        'REG_SP': REGISTERS['SP'],
        'REG_PC': REGISTERS['PC'],
    },
}


def main():
    global running
    global OPERATOR
    global ip
    global REGISTERS
    global PROGRAM

    program_lenght = len(PROGRAM)
    result=None
    while running and ip <= program_lenght:
        if PROGRAM[ip] in OPERATOR:
            op = PROGRAM[ip]
            result=OPERATOR[op]()
        else:
            # this branch will never been reached.
            REGISTERS['A'] = PROGRAM[ip]

        ip += 1
    global STACK
    return result


if __name__ == '__main__':
    print(main())
