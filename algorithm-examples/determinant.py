#https://www.geeksforgeeks.org/dsa/determinant-of-a-matrix/#
def getDet(A,n):
    temp = [0] *n
    total = 1
    det = 1

    for i in range(n):
        ind = i
        while ind < n and A[ind][i] == 0:
            ind += 1

        if ind == n:  
            # the determinant of matrix is zero
            continue

        if ind != i:
            for j in range(n):
                A[ind][j], A[i][j] = A[i][j], A[ind][j]
            # determinant sign changes when we shift rows
            det = det*int(pow(-1, ind-i))
        
        for j in range(n):
            temp[j] = A[i][j]
        
        for h in range(i+1, n):
            a1 = temp[i]     # value of diagonal element
            a2 = A[h][i]   # value of next row element

            for k in range(0, n):
                A[h][k] = (a1*A[h][k]) - (a2*temp[k])

            total = total * a1  # Det(kA)=kDet(A);
        
        # multiplying the diagonal elements to get determinant
    for i in range(0, n):
        det = det*A[i][i]

    return int(det/total)  # Det(kA)/k=Det(A);