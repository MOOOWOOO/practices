#!/usr/bin/env python3
# coding: utf-8

def main(pic_arr1, pic_arr2):
    try:
        res1 = check_resolution(pic_arr1)
        res2 = check_resolution(pic_arr2)
    except Exception as e:
        print(e)
        return {'result': False, 'data': e}

    if res1 == res2:
        print(mix_pic(pic_arr1, pic_arr2, res1))
    else:
        return {'result': False, 'data': 'resolution is not the same'}


def mix_pic(pic_arr1, pic_arr2, res):
    mix_res = [[None] * res[0]] * res[1]
    for i in range(res[0]):
        for j in range(res[1]):
            mix_res[i][j] = pic_arr2[i][j] + pic_arr1[i][j]
    return mix_res


def check_resolution(pic_arr):
    lenght = len(pic_arr)
    if lenght > 0:
        width = len(pic_arr[0])
    else:
        raise Exception('pic is empty')
    return (lenght, width)


if __name__ == '__main__':
    main([[1] * 3] * 3, [[2] * 3] * 3)
