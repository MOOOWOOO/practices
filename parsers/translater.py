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
                asm += '{sub_asm} '.format(sub_asm=sub_asm)
                if oper in bc_oper_reg_map:
                    tmp_reg = bc_oper_reg_map[oper]
                    asm += '{reg} '.format(reg=tmp_reg)
                else:
                    pass
            else:
                return res
        elif item_type == str:
            if item in prog_bc_map:
                if item == 'if':
                    bc = prog_bc_map[item][prog[i - 1][0]]
                else:
                    bc = prog_bc_map[item]
                asm += '{bc} '.format(bc=bc)
            elif item in registers:
                asm += '{registers} '.format(registers=item)
            else:
                asm += '{comment} '.format(comment=item)
        else:
            # don't translate DEC TO BIN here
            asm += '{num} '.format(num=item)

    return True, prog, prog_length + sub_prog_length, asm


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
        new_prog[-1] = [new_prog[-1], ['goto', tag]]

    return new_prog


def rearrange_if(prog):
    prog_length = len(prog)
    new_prog = []
    continue_time = 0
    goto_time = 0

    for i in range(prog_length):
        if goto_time:
            goto_time += 1

        if continue_time:
            continue_time -= 1
            continue

        item = prog[i]
        if isinstance(item, str):
            if item == 'if':
                goto_time += 1
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
            ['*', 'rd', 20],  # true
            ['/', 'rd', 20]  # false
        ],  # true
        ['rb']  # false
    ]

    res3 = [
        ['>=', 'ra', 'rb'],
        'if',
        [
            ['=', 10, 10],
            'if',
            ['*', 'rd', 20],  # true
            [
                ['tag', 'ba4450e859ea11e69ea7000c29c59316'],
                ['/', 'rd', 20]
            ]  # false
        ],  # true
        [
            ['tag', 'ba4450e959ea11e69ea7000c29c59316'],
            ['rb']
        ]  # false
    ]

    prog4 = [
        'if', ['>=', 'ra', 'rb'],
        [
            'while', ['=', 10, 10],
            [
                ['*', 'rd', 20],
                ['/', 'rd', 20]
            ],
        ],  # ture
        ['rb']  # false
    ]

    res4 = [
        ['>=', 'ra', 'rb'], 'if',
        [
            ['tag', '994b1f945a0c11e69ea7000c29c59316'], ['=', 10, 10], 'if',  # while
            [
                [
                    ['*', 'rd', 20], ['/', 'rd', 20]
                ],
                ['goto', '994b1f945a0c11e69ea7000c29c59316']
            ]  # loop body
        ],  # true
        [
            ['tag', '994b1f955a0c11e69ea7000c29c59316'],
            ['rb']
        ]  # false
    ]

    prog5 = [
        'while', ['>=', 'ra', 'rb'],
        [
            'if', ['=', 10, 10],
            ['*', 'rd', 20],
            ['/', 'rd', 20]
        ]
    ]

    res5 = [
        ['tag', '19a497745a0d11e69ea7000c29c59316'], ['>=', 'ra', 'rb'], 'if',  # while,
        [
            [
                ['=', 10, 10], 'if',
                ['*', 'rd', 20],  # true
                [
                    ['tag', '19a497755a0d11e69ea7000c29c59316'],
                    ['/', 'rd', 20]
                ]  # false
            ],
            ['goto', '19a497745a0d11e69ea7000c29c59316']
        ]  # loop body
    ]

    prog6 = [
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

    res6 = [
        ['tag', '6a98dbb45a0d11e69ea7000c29c59316'], ['>', 'ra', 'rb'], 'if',  # while
        [
            [
                ['tag', '6a98dbb55a0d11e69ea7000c29c59316'], ['>', 'rc', 'rd'], 'if',  # while
                [
                    [
                        ['load', 'ip', 'mem'],
                        [
                            ['tag', '6a98dbb65a0d11e69ea7000c29c59316'], ['<', 'ra', 10], 'if', # while
                            [
                                [
                                    ['save', 'ra'],
                                    ['load', 'ra', 'ip']
                                ],
                                ['goto', '6a98dbb65a0d11e69ea7000c29c59316']
                            ] # loop body
                        ]
                    ],
                    ['goto', '6a98dbb55a0d11e69ea7000c29c59316']
                ] # loop body
            ],
            ['goto', '6a98dbb45a0d11e69ea7000c29c59316']
        ] # loop body
    ]

    prog7 = [
        'while', ['>', 'ra', 'rb'],
        [
            'if', ['>', 'rc', 'rd'],
            [
                ['load', 'ip', 'mem'],
                [
                    'while', ['<', 'ra', 10],
                    [
                        ['save', 'ra'],
                        ['load', 'ra', 'ip']
                    ]
                ]
            ],
            [
                'if', ['!=', 'ra', 20],
                ['save', 'ip', 500],
                [
                    'while', ['<=', 10, 15],
                    ['load', 'ip', 'rd']
                ]
            ]
        ]
    ]

    res7 = [
        ['tag', '6a98dbb75a0d11e69ea7000c29c59316'], ['>', 'ra', 'rb'], 'if',  # while
        [
            [
                ['>', 'rc', 'rd'], 'if',
                [
                    ['load', 'ip', 'mem'],
                    [
                        ['tag', '6a98dbb85a0d11e69ea7000c29c59316'], ['<', 'ra', 10], 'if',
                        [
                            [
                                ['save', 'ra'],
                                ['load', 'ra', 'ip']
                            ],
                            ['goto', '6a98dbb85a0d11e69ea7000c29c59316']
                        ]  # loop body
                    ]
                ],  # true
                [
                    ['tag', '6a98dbbb5a0d11e69ea7000c29c59316'],
                    [
                        ['!=', 'ra', 20], 'if',
                        ['save', 'ip', 500],  # true
                        [
                            ['tag', '6a98dbba5a0d11e69ea7000c29c59316'],
                            [
                                ['tag', '6a98dbb95a0d11e69ea7000c29c59316'], ['<=', 10, 15], 'if',  # while
                                [
                                    ['load', 'ip', 'rd'],
                                    ['goto', '6a98dbb95a0d11e69ea7000c29c59316']
                                ]  # loop body
                            ]
                        ]  # false
                    ]
                ]  # false
            ],
            ['goto', '6a98dbb75a0d11e69ea7000c29c59316']
        ]  # loop body
    ]

    for prog in [prog0, prog1, prog2, prog3, prog4, prog5, prog6, prog7]:
        res_while = rearrange_while(prog)
        print('handle while:\n', res_while)
        print('\n\n\n')
        res_if = rearrange_if(res_while)
        print('handle if:\n', res_if)
        print('\n\n\n')
        print('handle if after while:\n', res_if)
        print('\n\n\n')
        print(translater_main(res_if))
        print('\n\n\n-------')
