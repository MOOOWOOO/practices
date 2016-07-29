#!/usr/bin/env python3
# coding: utf-8
from commands import prog_bc_map
from commands import registers


def translater_main(prog):
    asm = trans_prog_to_asm(prog=prog)
    # mc = trans_asm_to_mc(asm)
    # return True, asm, mc
    return asm


def trans_prog_to_asm(prog):
    asm = ''
    prog_length = len(prog)
    for i in range(prog_length):
        item = prog[i]
        item_type = type(item)
        if item_type == list:
            sub_prog = item
            res = trans_prog_to_asm(sub_prog)
            if res[0]:
                asm += res[3]
            else:
                return res
        elif item_type == str:
            if item in prog_bc_map:
                asm += '{bc} '.format(bc=prog_bc_map[item])
            elif item in registers:
                asm += '{registers} '.format(registers=item)
            else:
                return False, prog, i, ''
        else:
            # don't translate DEC TO BIN here
            asm += '{num} '.format(num=item)

    return True, prog, prog_length, asm


def trans_asm_to_mc(asm):
    bin = ''
    return True, asm, bin


if __name__ == '__main__':
    prog0 = ['define', 'ra', 1]
    prog1 = ['define', 'rb', 2]
    prog2 = ['define', 'rc', ['+', 'ra', 'rb']]
    for prog in [prog0, prog1, prog2]:
        print(translater_main(prog))
