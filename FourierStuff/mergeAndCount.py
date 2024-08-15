def merge( l1, l2, count = 0 ):
#     print(l1, l2)
    n1 = len(l1); n2 = len(l2) ; n = n1+n2; i = 0; j = 0; 
    out = []
    while i < n1 and j < n2:
        if l1[i]<=l2[j]:
            out.append(l1[i])
            i+=1
        else:
            out.append(l2[j])
            j+=1
            count += (n1 - i)
    while i < n1:
        out.append(l1[i])
        i+=1
    while j < n2:
        out.append(l2[j])
        j+=1
#     print("out", out )
    return [out, count]
    
def mergeSort( numbers, count = 0 ):
#     print("msINPUT", numbers, count)
    n = len(numbers)
    if n <= 1: return [ numbers, count ]
    hn = int(n/2)
    left = numbers[:hn]; right = numbers[hn:]
    res = mergeSort( left, count )
#     print( "left result", res )
    left = res[ 0 ]
    count = res[ 1 ]
    res = mergeSort( right, count )
#     print( "right result", res )
    right = res[ 0 ]
    count = res[ 1 ]
    return merge( left, right, count )