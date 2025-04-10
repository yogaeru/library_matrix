from setsmatrix import SetMatrix as sm
import time
from setsmatrix import adjoin as adj
import numpy as np
import random

def generate_num() :
    row_num = [random.randint(100, 10000) for _ in range(10)]
    return row_num


def main() -> None:
    
    
    matrix = [
        [2,4,0,4,1,3,0,1,0,4]
    ]

    # Array 2D 3x3
    E = [
        [3,2, -1],
        [2, -2, 4],
        [-1, 1/2, -1]
    ]
    
    matrix2 = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
    [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
    [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
    [71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
    [81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
    [91, 92, 93, 94, 95, 96, 97, 98, 99, 100],
    ]
    
    C = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25]
    ]

    for i in range(9):
        matrix.append(generate_num())
        
    noa = sm.matrix(C)
    mtr1 = np.array(matrix)
    mtr = sm.matrix(matrix)
    mtr2 = sm.matrix(E)
    start = time.time()
    noa.kof.det(opt="print")
    
    
    end = time.time()
    print(f"\nWaktu eksekusi: {end - start:.4f} detik")
    
if __name__ == "__main__":
    main()
    # print(generate_num())