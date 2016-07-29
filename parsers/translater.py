#!/usr/bin/env python3
# coding: utf-8
from commands import bc_oper_reg_map
from commands import bc_mc_map
from commands import prog_bc_map
from commands import registers
from commands import registers_mc_map


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
                if item == 'if':
                    bc = prog_bc_map[item][prog[i + 1][0]]
                else:
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
    prog3 = ['if', ['>=', 'ra', 'rb'], 'ra', 'rb']
    res = []
    for prog in [prog0, prog1, prog2, prog3]:
        print(translater_main(prog))
    # print(translater_main(prog3))
