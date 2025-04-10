import numpy as np
from fractions import Fraction as frc
from tabulate import tabulate
from rich import print
from abc import ABC, abstractmethod


# class kofaktor:
#     pass

class SetMatrix:
    def __new__(cls, matrix):
        raise TypeError("Tidak bisa membuat objek baru secara langsung")
    
    def __init__(self, matrix):
        # self.det_kofaktor = kofaktor()
        self.__matrix = matrix
    
    @classmethod
    def matrix(cls, matrix) -> object:
        instance = super().__new__(cls)
        instance.__init__(matrix)
        return instance
        # return cls(matrix)

    @staticmethod
    def printMatrix(*matrix) -> None:
        matrix_container = []
        max_row = max(len(m) for m in matrix)
        min_row = min(len(m) for m in matrix)
        # print(max_row, min_row)
        
        for mtr in matrix:
            row, col= len(mtr), len(mtr[0])
            new_matrix = []

            for i in range(max_row):
                new_data = []
                for j in range(col):
                    formatted_num = str(frc(mtr[i][j]).limit_denominator(100)) if i < row else "px"
                    new_data.append(formatted_num)
                new_matrix.append(new_data)
            
            table_matrix = tabulate(new_matrix, tablefmt="grid").split("\n") #membuat table matrix dengan tabulate
            ws = " " * (len(table_matrix[0]) - 6) #untuk membuat whitespace sepanjang kolom matrix
            table_matrix.insert(0, "[bold green1]Matrix[/bold green1]" + ws if len(mtr)>=3 else "[bold green1]Minor[/bold green1]" + ws + " ")
            matrix_container.append(table_matrix) #menambahkan table matrix yang sudah dibuat ke container


        len_coantiner, len_matrix = len(matrix_container), len(matrix_container[0])

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


    @staticmethod
    def get_Minor(matrix, row, col):
        if len(matrix) <= 1:
            print("[bold red] Can't get minor for matrix!! [/bold red]")
            return
        matrix = np.array(matrix)
        minor = np.delete(matrix, row, axis=0)
        minor = np.delete(minor, col, axis=1)
        minor = minor.tolist()
        return minor


    @staticmethod
    def det_kofaktor(matrix, depth=0) -> float:
        len_matrix = len(matrix)
        
        if len_matrix == 1:
            return tabulate(matrix, tablefmt="grid")
        if len_matrix == 2:
            det = (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])
            return det
        
        if len_matrix > 2:
            container_minor = []
            container_text = []
            print(f"[bold cyan2]Matrix yang sedang dihitung: {depth} [/bold cyan2]") if depth > 0 else None
            SetMatrix.printMatrix(matrix) if depth == 0 and len_matrix!=3 or len_matrix == 4 else None
            print() if depth == 0 else None
            container_minor.append(matrix) if len_matrix == 3 else None

        
        container_result = [
            [],
            []
        ]
        det_result = 0
        
        for i in range(len_matrix):
            matrix_minor = SetMatrix.get_Minor(matrix, 0, i)
            container_minor.append(matrix_minor) if len_matrix > 2 else None
            
            cofactor = ((-1)** i) * matrix[0][i]
            det_minor = SetMatrix.det_kofaktor(matrix_minor, depth+1)
            result = cofactor * det_minor
            det_result+=result
            
            if depth == 0:
                container_result[0].append(det_result)
                container_result[1].append(result)
            if depth!=0 or depth == 0 and len_matrix == 3:
                rsltText = f"[yellow1]({cofactor} * {det_minor})= {result} [/yellow1]" 
                container_text.append(rsltText) if len_matrix == 3 else print(rsltText)
                
        # diluar loop
        if len_matrix == 3:
            SetMatrix.printMatrix(*container_minor) if container_minor else None 
            for i, result in enumerate(container_text):
                print(f"{i+1}. {result} ")
            print(f"[green1]Determinan minor saat ini = {det_result} [/green1]\n")
        if depth == 0:
            print("[bold dark_slate_gray2]<========== DETERMINAN AKHIR =========>[/bold dark_slate_gray2]")
            for i in range (len(container_result)):
                answer = ""
                for j, result in enumerate(container_result[i]):
                    temp = f"({matrix[0][j]} * {result})" if i == 0 else f"({result})"
                    answer+= temp + " + " if j!=len(container_result[i]) - 1 else temp
                print(f"[bold yellow1]{answer}[/bold yellow1]")
            print(f"[bold dark_orange]Hasil Akhir = {det_result}[/bold dark_orange]") 

        return det_result


    @staticmethod
    def inv_adjoin(matrix)->list[float]:
        len_matrix = len(matrix)
        
        container_matrix = []
        matrix_adjoin = []
        
        even = lambda num: num%2==0
        
        for i in range(len_matrix):
            row_data = []
            row = i+1
            print(f"even row {row} {even(row)}")
            for j in range(len_matrix):
                col = j+1
                print("even col",col ,even(col))
                matrix_minor = SetMatrix.get_Minor(matrix, i, j)
                det_minor = str(frc(SetMatrix.det_kofaktor(matrix_minor) * (-1) if not even(row) and even(col) or even(row) and not even(col)
                                    else SetMatrix.det_kofaktor(matrix_minor)))
                # print("ini fungsi", SetMatrix.det_kofaktor(matrix_minor))
                print(f"Ini det minor {det_minor}")
                row_data.append(det_minor)
            matrix_adjoin.append(row_data)

        print(matrix_adjoin)
        

A = [
    [2, 8, -1, -2, 9],
    [4, 16, -2, -4, -18],
    [1, 2, 3, 4, 5],
    [4, -2, 1, 2, 1]

]
sm = SetMatrix.matrix(A)
det = sm.det_kofaktor(A)

# B = [
#     [1, 2, 3, 4],
#     [5, 6, 7, 8],
#     [9, 10, 11, 12],
#     [13, 14, 15, 16]
# ]

# sm.printMatrix(B, A)