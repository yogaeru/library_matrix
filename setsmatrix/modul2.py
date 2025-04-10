import numpy as np
from fractions import Fraction as frc
from tabulate import tabulate
from rich import print


class kofaktor:
    def __init__(self):
        pass
    
    
class SetMatrix:
    def __new__(cls, matrix):
        raise TypeError("Tidak bisa membuat objek baru secara langsung")
    
    def __init__(self, matrix):
        self.matrix = matrix
        self.kofaktor = kofaktor()
    
    def __str__(self):
        return tabulate(self.matrix, tablefmt="grid")
        

    @classmethod
    def matrix(cls, matrix):
        instance = super().__new__(cls)
        instance.__init__(matrix)
        return instance
    
    @staticmethod
    def printMatrix(*matrix) :
        matrix_container = []

        max_row = max(len(m.matrix) for m in matrix if isinstance(m, SetMatrix))
        min_row = min(len(m.matrix) for m in matrix if isinstance(m, SetMatrix))
        # print(max_row, min_row)
        
        for mtr in matrix:
            if not isinstance(mtr, SetMatrix) and not isinstance(mtr.matrix, (list, tuple)):
                raise TypeError("Matrix bukan atribut SetMatrix, tolong buat matrix dengan setsmatrix")
        
            row, col= len(mtr.matrix), len(mtr.matrix[0])
            new_matrix = []

            for i in range(max_row):
                new_data = []
                for j in range(col):
                    formatted_num = str(frc(mtr.matrix[i][j]).limit_denominator(100)) if i < row else "px"
                    new_data.append(formatted_num)
                new_matrix.append(new_data)
            
            table_matrix = tabulate(new_matrix, tablefmt="grid").split("\n") #membuat table matrix dengan tabulate
            ws = " " * (len(table_matrix[0]) - 6) #untuk membuat whitespace sepanjang kolom matrix
            table_matrix.insert(0, "[bold green1]Matrix[/bold green1]" + ws if len(mtr.matrix)>=3 else "[bold green1]Minor[/bold green1]" + ws + " ")
            matrix_container.append(table_matrix) #menambahkan table matrix yang sudah dibuat ke container


        len_coantiner, len_matrix = len(matrix_container), len(matrix_container[0])
        
        """Kondisi dimana setiap matrix memiliki ukuran yang berbeda"""
        if max_row!=min_row:
            # print (matrix_container)
            for i in range(len_coantiner):
                leng = len(matrix_container[i])
                # print("ini leng", leng)
                for j in range(leng):
                    # print("ini j ", j, end=" ")
                    if "px" in matrix_container[i][j]: #jika ada "px" maka ganti dengan whitespace
                        counter = sum([2 for _ in range(max_row-min_row)])
                        # print("ini count", counter)
                        row = len_matrix - counter
                        # print("ini row", row)
                        for k in range(row, leng):
                            matrix_container[i][k] = " "
                        break

        combined_table = ["    ".join(mtr) for mtr in zip(*matrix_container)]
        print(f"[bold]{"\n".join(combined_table)}[/bold]")


A = [
    [2, 4, 6, 2, 0],
    [2, 8, -1, -2, 9],
    [4, 16, -2, -4, -18],
    [1, 2, 3, 4, 5],
    [4, -2, 1, 2, 1]

]

mtr = SetMatrix.matrix(A)
# SetMatrix.printMatrix(A)
det = mtr.det_kofa
print(mtr)
