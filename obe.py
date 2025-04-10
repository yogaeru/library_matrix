from setsmatrix import SetMatrix as sm
import collections

def obe(matrix) -> "sm" :
    n = len(matrix)
    mat = matrix.copy()  # Supaya matrix asli tidak berubah
    det = 1

    for i in range(n):
        # Cari pivot bukan nol
        print("mat ii", mat[i][i])
        if mat[i][i] == 0:
            for j in range(i + 1, n):
                print("mat ji 1", mat[j][i])
                if mat[j][i] != 0:
                    print("Ini mat", mat[i], mat[j])
                    mat[i], mat[j] = mat[j], mat[i]
                    det *= -1  # Tanda determinan berubah kalau tukar baris
                    break
            else:
                return 0  # Semua pivot nol → determinan 0

        # Eliminasi ke bawah
        for j in range(i + 1, n):
            print(f"mat ji {mat[j][i]} dan ii {mat[i][i]}")
            # print(mat[j][i], mat[i][i])
            ratio = mat[j][i] / mat[i][i]
            print("ini ratio", ratio)
            for k in range(n):
                print("ini mat jk", mat[j][k])
                mat[j][k] -= ratio * mat[i][k]

    # Ambil hasil kali diagonal
    for i in range(n):
        det *= mat[i][i]
    
    print(mat)
    return round(det)


def main() -> None:
    
    # Contoh penggunaan
    matrix = [
        [1, 2, 3],
        [2, 3, 1],
        [3, 2, 2]
    ]
    
    print("ini sm det", sm.kof.det(pMatrix=sm.matrix(matrix)))

    obe(matrix)
    
if __name__ == "__main__":
    main()

