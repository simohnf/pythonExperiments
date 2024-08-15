# https://www.geeksforgeeks.org/heaps-algorithm-for-generating-permutations/
# Python program to print all permutations using
# Heap's algorithm
# Generating permutation using Heap Algorithm
def heapPermutation(a, size):
    # if size becomes 1 then prints the obtained
    # permutation
    if size == 1:
        print(a)
        return

    for i in range(size):
        heapPermutation(a, size-1)
        
        # if size is odd, swap 0th i.e (first)
        # and (size-1)th i.e (last) element
        # else If size is even, swap ith
        # and (size-1)th i.e (last) element
        if size & 1:
            a[0], a[size-1] = a[size-1], a[0]
        else:
            a[i], a[size-1] = a[size-1], a[i]

def heapPerm(a, mem, size = -1):
    if size == -1:
        size = len(a)
    # if size becomes 1 then prints the obtained
    # permutation
    elif size == 1:
        mem+=a
        print(a)
        return

    for i in range(size):
        heapPerm(a, mem, size-1)
        
        # if size is odd, swap 0th i.e (first)
        # and (size-1)th i.e (last) element
        # else If size is even, swap ith
        # and (size-1)th i.e (last) element
        if size & 1:
            a[0], a[size-1] = a[size-1], a[0]
        else:
            a[i], a[size-1] = a[size-1], a[i]

# Driver code
a = [1, 2, 3]
n = len(a)
heapPermutation(a, n)

# This code is contributed by ankush_953
# This code was cleaned up to by more pythonic by glubs9
