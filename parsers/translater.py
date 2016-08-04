#!/usr/bin/env python3
# coding: utf-8

from commands import bc_mc_map
from commands import bc_oper_reg_map
from commands import prog_bc_map
from commands import registers
from commands import registers_mc_map
from uuid import uuid1 as u1


def translater_main(prog):
    asm = trans_prog_to_asm(prog=prog)
    # mc = trans_asm_to_mc(asm[3])
    # return True, asm, mc
    return asm


def trans_prog_to_asm(prog):
    asm = ''
    prog_length = len(prog)
    sub_prog_length = 0
    for i in range(prog_length):
        item = prog[i]
        item_type = type(item)
        if item_type == list:
            sub_prog = item
            res = trans_prog_to_asm(sub_prog)
            sub_prog_length += res[2]
            if res[0]:
                sub_asm = res[3]
                oper = sub_asm.split()[0]
                asm = '{sub_asm} {asm}'.format(sub_asm=sub_asm, asm=asm)
                if oper in bc_oper_reg_map:
                    tmp_reg = bc_oper_reg_map[oper]
                    asm += '{reg} '.format(reg=tmp_reg)
                else:
                    pass
            else:
                return res
        elif item_type == str:
            if item in prog_bc_map:
                bc = prog_bc_map[item]
                asm += '{bc} '.format(bc=bc)
            elif item in registers:
                asm += '{registers} '.format(registers=item)
            else:
                return False, prog, i, ''
        else:
            # don't translate DEC TO BIN here
            asm += '{num} '.format(num=item)

    return True, prog, prog_length + sub_prog_length, asm.strip()


def rearrange_while(prog):
    prog_length = len(prog)
    new_prog = []
    tag = ''
    goto_time = 0

    for i in range(prog_length):
        item = prog[i]
        goto_time += 1
        if isinstance(item, str):
            if item == 'while':
                tag = u1().hex
                # tag = '12345678901234567890123456789012'
                new_prog.append(['tag', tag])
                new_prog.append('if')
            else:
                new_prog.append(item)
        elif isinstance(item, list):
            new_prog.append(rearrange_while(item))
        else:
            new_prog.append(item)

    if len(tag) == 32 and goto_time == 3:
        if isinstance(new_prog[-1], list):
            pass
        else:
            new_prog[-1] = [new_prog[-1]]
        new_prog[-1].append(['goto', tag])

    return new_prog


def rearrange_if(prog):
    prog_length = len(prog)
    new_prog = []
    continue_time = 0
    goto_time = 0

    for i in range(prog_length):
        goto_time += 1

        if continue_time:
            continue_time -= 1
            continue

        item = prog[i]

        if isinstance(item, str):
            if item == 'if':
                new_prog.append(prog[i + 1])
                new_prog.append(item)
                continue_time += 1
            else:
                new_prog.append(item)
        elif isinstance(item, list):
            new_prog.append(rearrange_if(item))
        else:
            new_prog.append(item)

    if goto_time == 4:
        tag = u1().hex
        # tag = '12345678901234567890123456789012'
        new_prog[-1] = [['tag', tag], new_prog[-1]]

    return new_prog


def trans_asm_to_mc(asm):
    asm_items = asm.split()
    mc = ''
    for item in asm_items:
        if item in bc_mc_map:
            mc += '{}\n'.format(bc_mc_map[item])
        elif item in registers_mc_map:
            mc += '{}\n'.format(registers_mc_map[item])
        else:
            num_bin = bin(int(item)).split('0b')[1]
            # check if num_bin is longer than register
            mc += '{:0>8s}\n'.format(num_bin)

    return True, asm, mc


if __name__ == '__main__':
    prog0 = ['define', 'ra', 1]
    prog1 = ['define', 'rb', 2]
    prog2 = ['define', 'rc', ['+', 'ra', 'rb']]

    prog3 = [
        'if', ['>=', 'ra', 'rb'],
        [
            'if', ['=', 10, 10],
            [
                '*', 'rd', 20
            ],
            [
                '/', 'rd', 20
            ]
        ],
        [
            'rb'
        ]
    ]

    res3 = [
        ['>=', 'ra', 'rb'],
        'if',
        [
            ['=', 10, 10],
            'if',
            ['*', 'rd', 20],
            [
                ['tag', 'ba4450e859ea11e69ea7000c29c59316'],
                ['/', 'rd', 20]]
        ],
        [
            ['tag', 'ba4450e959ea11e69ea7000c29c59316'],
            ['rb']
        ]
    ]

    prog4 = [
        'while', ['>', 'ra', 'rb'],
        [
            'while', ['>', 'rc', 'rd'],
            [
                ['load', 'ip', 'mem'],
                [
                    'while', ['<', 'ra', 10],
                    [
                        ['save', 'ra'],
                        ['load', 'ra', 'ip']
                    ]
                ]
            ]
        ]
    ]

    res4 = [
        ['tag', '12345678901234567890123456789012'],
        'if', ['>', 'ra', 'rb'],
        [
            ['tag', '12345678901234567890123456789012'],
            'if', ['>', 'rc', 'rd'],
            [
                ['load', 'ip', 'mem'],
                [
                    ['tag', '12345678901234567890123456789012'],
                    'if', ['<', 'ra', 10],
                    [
                        ['save', 'ra'],
                        ['load', 'ra', 'ip'],
                        ['goto', '12345678901234567890123456789012']
                    ]
                ],
                ['goto', '12345678901234567890123456789012']
            ],
            ['goto', '12345678901234567890123456789012']
        ]
    ]

    res5 = [
        ['tag', 'c09c08c0599511e682e33c46d8310838'],
        ['>', 'ra', 'rb'],
        'if',
        [
            ['tag', 'c09ca514599511e68de23c46d8310838'],
            ['>', 'rc', 'rd'],
            'if',
            [
                ['load', 'ip', 'mem'],
                [
                    ['tag', 'c09cb8a2599511e697cd3c46d8310838'],
                    ['<', 'ra', 10],
                    'if',
                    [
                        ['save', 'ra'],
                        ['load', 'ra', 'ip'],
                        ['goto', 'c09cb8a2599511e697cd3c46d8310838']
                    ]
                ],
                ['goto', 'c09ca514599511e68de23c46d8310838']
            ],
            ['goto', 'c09c08c0599511e682e33c46d8310838']
        ]
    ]

    for prog in [prog4, prog0, prog1, prog2, prog3]:
        print(translater_main(prog))
    print('\n\n\n')
    print('handle if:\n', rearrange_if(prog3))
    print('\n\n\n')
    print('handle while:\n', rearrange_while(prog4))
    print('\n\n\n')
    print('handle if after while:\n', rearrange_if(rearrange_while(prog4)))
