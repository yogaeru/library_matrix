from setsmatrix import SetMatrix as sm
import collections
import random
import numpy as np

def generate_num():
    row_num = [random.randint(100, 10000) for _ in range(10)]
    return row_num

def obe(matrix) -> "sm" :
    n = len(matrix)
    mat = matrix.copy()  # Supaya matrix asli tidak berubah
    det = 1

    for i in range(n):
        # Cari pivot bukan nol
        # print("mat ii", mat[i][i])
        if mat[i][i] == 0:
            for j in range(i + 1, n):
                # print("mat ji 1", mat[j][i])
                if mat[j][i] != 0:
                    # print("Ini mat", mat[i], mat[j])
                    mat[i], mat[j] = mat[j], mat[i]
                    det *= -1  # Tanda determinan berubah kalau tukar baris
                    break
            else:
                return 0  # Semua pivot nol → determinan 0

        # Eliminasi ke bawah
        for j in range(i + 1, n):
            # print(f"mat ji {mat[j][i]} dan ii {mat[i][i]}")
            # print(mat[j][i], mat[i][i])
            ratio = mat[j][i] / mat[i][i]
            # print("ini ratio", ratio)
            for k in range(n):
                # print("ini mat jk", mat[j][k])
                mat[j][k] -= ratio * mat[i][k]

    # Ambil hasil kali diagonal
    for i in range(n):
        det *= mat[i][i]
    
    print(sm.matrix(mat))
    return sm.matrix(mat)


def determinant(matrix):
    n = len(matrix)
    mat = matrix.copy()  # Copy biar matrix asli gak berubah
    swap_count = 0
    sm.printMatrix(sm.matrix(mat))
    for i in range(n):
        # Pivoting: tukar baris kalau pivot = 0
        if mat[i][i] == 0:
            for k in range(i + 1, n):
                if mat[k][i] != 0:
                    mat[i], mat[k] = mat[k], mat[i]
                    swap_count += 1
                    break
            else:
                # print(sm.matrix(mat))
                return 0  # Semua elemen di kolom i = 0 → determinan = 0

        for j in range(i + 1, n):
            ratio = mat[j][i] / mat[i][i]
            for k in range(i, n):
                mat[j][k] -= ratio * mat[i][k]

    # Hasil akhirnya: mat jadi bentuk segitiga atas
    print(sm.matrix(mat))
    det = 1
    for i in range(n):
        det *= mat[i][i]

    # Koreksi tanda jika ada pertukaran baris
    if swap_count % 2 == 1:
        det *= -1

    return det


def main() -> None:
    nim = [
        [2,4,0,4,1,3,0,1,0,4]
    ]
    
    for i in range(9):
        nim.append(generate_num())
    # Contoh penggunaan
    matrix = [
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
    
    E = [
        [3,2, -1],
        [2, -2, 4],
        [-1, 1/2, -1]
    ]

    mtr2 = sm.matrix(nim)
    mtr = np.array(nim)
    # det = determinant(nim)
    sm.printMatrix(mtr2)
    inv = sm.matrix(nim).adj.inv()
    print(inv)
    sm.printMatrix(inv, mode="frc")
    
    # print(type(mtr2.gauss.det()))

    # print(det)
    print(np.linalg.det(mtr))
    
    
if __name__ == "__main__":
    main()

