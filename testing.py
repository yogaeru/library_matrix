from setsmatrix import SetMatrix as sm
import numpy as np
import random


def generate_matrix(nim: list):
    matrix = [
        nim,

    ]

    for i in range(9):
        row = [random.randint(500, 10000) for _ in range(10)]
        matrix.append(row)

    return matrix




def main() -> None:
    A = sm.matrix([
        [1,1,1],
        [2,-1,3],
        [1,2,-1]
    ])
    
    adjoin = A.adjoin()
    print(adjoin)
    print(adjoin.T)
    
    
if __name__ == "__main__":
    main()
