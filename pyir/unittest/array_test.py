#!/usr/bin/env python3

from pyir.utils import array

def same_array(nums1, nums2):
    if len(nums1) != len(nums2):
        return False
    for x, y in zip(nums1, nums2):
        if x != y:
            return False
    return True

def array_check(nums1, nums2):
    if not same_array(nums1, nums2):
        print(f"output: {nums1}")
        print(f"expect: {nums2}")
        print("Not the same")
        quit()



def adv_test():
    row0 = array.Array(int)
    row0.append(1)
    row0.append(2)
    row0.append(3)

    row1 = array.Array(int)
    row1.append(4)
    row1.append(4)
    row1.append(4)

    matrix = array.Array(array.Array)
    matrix.append(row0)
    matrix.append(row1)

    print(matrix)


def simple_test():
    nums = array.Array(int)
    nums.append(1)
    nums.append(2)
    nums.append(3)
    x = nums.pop()
    if x != 3:
        print("Error x should be 3")
        quit()
    array_check(nums, [1, 2])

    try:
        nums.append("hello")
    except TypeError:
        print("Yes, the type is checked")

    nums[0] = 2
    nums[1] = 3
    nums.append(5)
    array_check(nums, [2,3,5])

    try:
        nums[3] = 1
    except IndexError:
        print("Yes, the index is checked")

    print(f"PASS: {nums}")
    for num in nums:
        print(num)

    strings = array.Array(str)
    strings.append("hello")
    strings.append("world")
    print(strings)


if __name__ == "__main__":
    simple_test()
