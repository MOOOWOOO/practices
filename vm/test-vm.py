#!/usr/bin/env python3
# coding: utf-8

import nose
from nose import with_setup

import vm
from vm import vm_main


def setup():
    vm.RUNNING = True
    vm.STACK_BOTTOM = 0
    vm.STACK_LENGTH = 10
    vm.STACK = [None] * vm.STACK_LENGTH
    vm.PROGRAM = list()

    vm.ip = 0  # instruction pointer
    vm.sp = -1  # stack pointer


@with_setup(setup)
def test_vm_main_no_hlt():
    PROG = [
        'PUSH', 100,
    ]

    res = vm_main(PROG=PROG)
    print('test_vm_main_no_hlt: ', res)

    assert res[0] is True


@with_setup(setup)
def test_vm_main_add_not_a_number():
    PROG = [
        'PUSH', 1,
        'PUSH', 'ABC',
        'ADD',
    ]

    res = vm_main(PROG=PROG)
    print('test_vm_main_add_not_a_number: ', res)

    assert res[0] is False
    assert isinstance(res[1], str)


@with_setup(setup)
def test_vm_main_hlt_at_line():
    PROG = [
        'PUSH', 1,
        'HLT',
        'PUSH', 2,
    ]

    res = vm_main(PROG=PROG)
    print('test_vm_main_hlt_at_line: ', res)

    assert res[0] is True
    assert res[2][0] == 1 and res[2][1] is None


@with_setup(setup)
def test_vm_main_pop_null_stack():
    PROG = [
        'POP'
    ]

    res = vm_main(PROG=PROG)
    print('test_vm_main_pop_null_stack: ', res)

    assert res[0] is False


@with_setup(setup)
def test_vm_main_push_out_of_stack():
    PROG = ['PUSH', 1, ] * (vm.STACK_LENGTH + 1)

    res = vm_main(PROG=PROG)
    print('test_vm_main_push_out_of_stack: ', res)

    assert res[0] is False
    assert isinstance(res[1], str)
    assert res[2] == [1] * 10


@with_setup(setup)
def test_vm_main_push_to_full_pop_to_empty():
    PROG = ['PUSH', 1, ] * vm.STACK_LENGTH
    for i in range(vm.STACK_LENGTH):
        PROG.append('POP')

    res = vm_main(PROG=PROG)
    print('test_vm_main_push_to_full_pop_to_empty: ', res)

    assert res[0] is True
    assert res[2] == [1] * vm.STACK_LENGTH
    assert vm.sp == -1


if __name__ == '__main__':
    nose.runmodule()
