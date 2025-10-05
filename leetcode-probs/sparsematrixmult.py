#"Convert" from https://www.youtube.com/watch?v=-JohvONOHTA&t=281s

from typing import List
import collections

class Solution:
    def multiply(self, mat1: List[List[int]], mat2: List[List[int]]) -> List[List[int]]:
        def convert(M):
            n = len(M)
            k = len(M[0])
            
            s = collections.defaultdict(collections.Counter)
            for i in range(n):
                for j in range(k):
                    if M[i][j] != 0:
                        s[i][j] = M[i][j]
            
            return s
    
        s1 = convert(mat1)
        s2 = convert(mat2)

        m, k, n = len(mat1), len(mat1[0]), len(mat2[0])
        result = [[0] * n for _ in range(m)]

        for a in s1:
            for b in s1[a]:
                if b in s2:
                    for c in s2[b]:
                        result[a][c] += s1[a][b] * s2[b][c]
        
        return result
