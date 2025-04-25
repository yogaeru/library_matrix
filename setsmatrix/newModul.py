import collections
from fractions import Fraction as frc
from tabulate import tabulate
from rich import print


"""
    <== FUNCTION HELPER ==>
"""
class helperWrapper:
    def __init__(self, matrix:"SetMatrix", fitur:str):
        self.__matrix = matrix
        self.__fitur_cls = fitur

    def __getattr__(self, attr):
        instance = object.__new__(self.__fitur_cls)
        instance.__init__(self.__matrix)
        # print("dari objek")
        return getattr(instance, attr)

"""
    <=== GAUSS ===>
"""
class Gauss:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Tidak bisa membuat instance dari class {cls.__name__}")
        
    def __init__(self, obj_mtr):
        self.__obj_mtr = obj_mtr

    def det(self, *, mtr:"SetMatrix" = None, mode:str = None) -> float:
        """
        Ini adalah method untuk menghitung determinan menggunakan metode eliminasi gauss
            <= Parameter =>
                - mtr:"Setmatrix" =  parameter matrix yang menerima tipe data "SetMatrix"
                - mode:str = mau pakai mode apa, ada print dan return(default)
                
            RETURN FLOAT
        """
        #instance akan meyimpan objek dari class SetMatrix
        instance = self.__obj_mtr if mtr == None else mtr
        if not isinstance(instance, SetMatrix):
            raise TypeError("Matrix harus berupa class SetMatrix")
        
        """
            Pada loop dibawah akan membuat copy dari matrix utama
            sehingga matrix utama tidak berubah
        """
        
        contianer_matrix = []
        matrix = [] #list untuk menyimpan matrix baru
        for row in instance.tolist:
            matrix.append(row.copy()) #pakai copy agar membuat alamat baru
        len_matrix = len(matrix) #mengambil panjang matrix
        
        swap_count = 0 #menampung jumlah pertukaran baris
        
        for pivot_row in range(len_matrix):
            SetMatrix.printMatrix(SetMatrix.matrix(matrix), type="frc", header=True) if mode == "print" else None
            
            contianer_result = [
                [],
                []
            ]
            
            pivot = matrix[pivot_row][pivot_row] #pivot saat ini
            
            if pivot == 0: #jika elemen pivot 0 maka ubah barisnya
                for row_bot in range(pivot_row + 1, len_matrix):
                    if matrix[row_bot][pivot_row] != 0:
                        matrix[pivot_row], matrix[row_bot] = matrix[row_bot], matrix[pivot_row]
                        swap_count+=1
                        break
                else:
                    # SetMatrix.printMatrix(SetMatrix.matrix(matrix))
                    # print(f"Semua elemen pada baris ke {i+1} sama dengan 0 -> determinan 0")
                    return 0
            count = 1
            for row_bot in range(pivot_row + 1, len_matrix):
            
                ratio = matrix[row_bot][pivot_row] / pivot
                for col in range(pivot_row, len_matrix):
                    result_text = f"[yellow1]{count}.  ({matrix[row_bot][col]:.1f}) - ({frc(ratio).limit_denominator(1000)}) * {matrix[pivot_row][col]:.1f}[/yellow1]"
                    matrix[row_bot][col] -= ratio * matrix[pivot_row][col]
                    contianer_result[0].append(result_text)
                    contianer_result[1].append(f"{frc(matrix[row_bot][col]).limit_denominator(1000)}")
                    count+=1
            count =1
            
            if mode == "print":
                for text, result in zip(*contianer_result):
                    print(f"{text} = {result}")
                print()
        #KELUAR LOOP
        """
            Jika ada perubahan maka determinan akan dikalikan dengan -1
                <= Nama Variabel =>
                - det = untuk menampung hasil determinan
                - swap_count = untuk menampung jumlah perubahan baris
                    - jika swapcount ganjil maka det akan negatif
                    - jika swapcount genap maka det akan positif

                Loop dibawah digunakan untuk mengalikan elemen diagonal matrix
        """
        det = -1 if swap_count % 2 != 0 else 1
        for i in range(len_matrix): #kalian elemen diagonaln untuk mendapatkan determinan
            det*=matrix[i][i]

        # print(SetMatrix.matrix(matrix)) if mode == "print" else None
        return float(f"{det:.1f}")
    
    
    
    
    """ METHOD UNTUK MENGHITUNG INVERSE DENGAN METODE GAUSS """
    def inv (self, *, mtr:"SetMatrix" = None, mode:str = None) -> "SetMatrix" :
        """
            Invers dengan metode Gauss-Jordan
            <= Parameter =>
                -mtr:"SetMatrix = objek dari class SetMatrix
                -mode:str = mode untuk menampilkan prosesnya atau tidak
        """
        
        instance = self.__obj_mtr if mtr == None else mtr
        if not isinstance(instance, SetMatrix):
            raise TypeError("Input instance harus objek dari class SetMatrix")
        
        matrix = instance.tolist
        len_matrix = len(matrix)
        identity = SetMatrix.identity(len_matrix)
        
        combined_matrix = [a + b for a,b in zip(matrix, identity)]
        # print(combined_matrix)
        SetMatrix.printMatrix(SetMatrix.matrix(combined_matrix), type="frc")
        
        for i in range(len_matrix):
            pivot = combined_matrix[i][i]
            container_result = [
                [],
                []
            ]
            
            if pivot == 0:
                for k in range(i+1, len_matrix):
                    if combined_matrix[k][i] != 0:
                        combined_matrix[i], combined_matrix[k] = combined_matrix[k], combined_matrix[i]
                        pivot = combined_matrix[i][i]
                        break
                else:
                    raise ValueError("Matrix tidak bisa diinvers (pivot nol di semua baris)")
            
            for col in range(len(combined_matrix[i])):
                result = str(frc(combined_matrix[i][col] / pivot).limit_denominator(100))
                result_text = f"[yellow1]{col+1}. {combined_matrix[i][col]:.2f} / ({pivot:.2f}) = {result} [/yellow1]"
                container_result[0].append(result_text)
                container_result[1].append(result)
                combined_matrix[i][col] /= pivot
                
                
                
            # combined_matrix[i] = [val / pivot for val in combined_matrix[i]]
            # for j in range(len_matrix):
            #     if j != i:
            #         factor = combined_matrix[j][i]
            #         combined_matrix[j] = [ a - factor * b for a, b in zip(combined_matrix[j], combined_matrix[i])]
            
            for row_elm in range(len_matrix):
                if row_elm !=i :
                    rasio = combined_matrix[row_elm][i]
                    for col in range(len(combined_matrix[row_elm])):
                        combined_matrix[row_elm][col] -= rasio * combined_matrix[i][col]
            
            sm_matrix = SetMatrix.matrix(combined_matrix)
            
            if mode == "print":
                half = len(container_result[0]) // 2
                left = container_result[0][:half]
                right = container_result[0][half:]
                
                for a, b in zip(left, right):
                    print(f"{a:<70}     {b:<40}")
                    # print(f"{" "*10}".join(result))
                    
            # for a, b in zip(*container_result):
            #     print(f"{a} = {b}")
            print(f"[bold dark_slate_gray1]Diperoleh baris {i+1} baru : [/bold dark_slate_gray1]")
            SetMatrix.printMatrix(SetMatrix.matrix([combined_matrix[i]]), type="frc")
            print()
            
            SetMatrix.printMatrix(sm_matrix, type="frc", header=True)
            print()
            

        inverse = SetMatrix.matrix([row[len_matrix:] for row in combined_matrix])
        print(f"[bold red1]<== INVERS ==>[/bold red1]")
        SetMatrix.printMatrix(inverse)
        # inverse = [list(map(float, row)) for row in inverse]
        return inverse
    

"""
    <=== ADJOIN ===>
"""
class adjoin:
    def __new__(cls, *agrs, **kwargs):
        raise TypeError(f"TIDAK BISA MEMBUAT INSTANCE DARI {cls}")


    def __init__(self, obj_matrix):
        self.__obj_matrix = obj_matrix
    
    def inv(self, *, mtr:"SetMatrix" = None) -> "SetMatrix":
        
        matrix = self.__obj_matrix if mtr == None else mtr
        
        if not isinstance(matrix, SetMatrix):
            raise TypeError("Parameter harus berupa SetMatrix")    
        
        container_matrix = []
        inv_matrix = []
        
        # print(matrix.adjoin().tolist)
        list_matrix = matrix.adjoin().T.tolist
        # print (list_matrix)
        len_matrix = len(list_matrix)
        det_matrix = 1 / matrix.gauss.det()
        # print(f"{det_matrix:.2f}")
        
        if det_matrix == 0:
            raise ValueError("Matrix dengan determinan 0 tidak bisa dicari inversnya")
        
        for i in range(len_matrix):
            row_data = []
            for j in range(len_matrix):
                data = list_matrix[i][j] * det_matrix
                row_data.append(data)
            inv_matrix.append(row_data)
            
        return SetMatrix.matrix(inv_matrix)


"""
    <=== KOFAKTOR ===>
"""
class kofaktor:
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError(f" TIDAK BISA MEMBUAT INSTANCE DARI {cls} ")
    #
    def __init__(self, obj_matrix):
        self.__obj_matrix = obj_matrix

    @property
    def getT(self):
        return self.__obj_matrix
    #
    @staticmethod
    def get_minor(matrix, row, col) -> "SetMatrix":
        if not isinstance(matrix, SetMatrix):
            raise ValueError(f"{matrix} BUKAN OBJEK DARI SetMatrix")
        
        if len(matrix.tolist) <=1:
            raise ValueError(" TIDAK BISA MENCARI MINOR DARI MATRIX 1X1 ")
    
        minor = []
        for baris in matrix.tolist:
            minor.append(baris.copy())
        
        """ Untuk menghapus baris matrix """
        minor.pop(row)
        
        """Loop untuk menghpaus kolom matrix"""
        for i in range(len(minor)):
            minor[i].pop(col)
        return SetMatrix.matrix(minor)
    
    """ METHOD UNTUK MENGHITUNG DETERMINAN KOFAKTOR """
    def det(self, *, pMatrix:"SetMatrix" = None , depth= 0, opt:str= None ) -> float:
        """
            --------------------
            #INFO NAMA VARIABEL#
            pMatrix:SetMatrix
                = matrix dari parameter
            depth:int, optional
                = tingkat ke dalam matrix (default = 0)
            opt:str, optinal = 
                = opsi untuk menampilkan informasi (default = none)
                
            +-----+
            RETURN
            det_result:float
        """
        
        instance = self.__obj_matrix if pMatrix ==  None else pMatrix

        if not isinstance(instance, SetMatrix):
            raise ValueError(f"{instance} BUKAN OBJEK DARI SetMatrix")
        
        matrix = instance.tolist
        len_matrix = len(matrix) #menentukan panjang matrix
        
        if len_matrix != len(matrix[0]):
            raise ValueError("BARIS DAN KOLOM MATRIX HARUS SAMA")

        if len_matrix == 1:
            return matrix[0][0]
        if len_matrix == 2:
            det = (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])
            return det
            

        if len_matrix > 2 :
            container_minor = []
            container_text = []
            print(f"[bold cyan2]Matrix yang sedang dihitung: {depth} [/bold cyan2]") if depth > 0 and opt == "print" else None
            SetMatrix.printMatrix(instance) if depth == 0 and len_matrix!=3 and opt == "print" or len_matrix == 4 and opt=="print"else None
            print() if depth == 0 and opt== "print" else None
            container_minor.append(instance) if len_matrix == 3 else None
        
        """CONTAINER UNTUK MENYIMPAN HASIL"""
        container_result = [
            [],
            []
        ]
        det_result:float = 0 #HASIL DETERMINANT
        
        for i in range(len_matrix):
            matrix_minor = kofaktor.get_minor(instance, 0, i)
            # print(type(matrix_minor))
            container_minor.append(matrix_minor) if len_matrix > 2 else None
            
            cofactor = ((-1)**i) * matrix[0][i]
            minor_determinant = self.det ( pMatrix=matrix_minor, depth= depth + 1, opt = opt )
            result = cofactor * minor_determinant
            det_result+=float(result)
            
            if depth == 0:
                container_result[0].append(minor_determinant)
                container_result[1].append(result)
            if depth != 0 or depth == 0 and len_matrix == 3:
                result_text = f"[yellow1]({cofactor:.2f} * {minor_determinant:.2f}) = {result:.2f} [/yellow1]"
                container_text.append(result_text)
        

        #KELUAR LOOP
        if len_matrix == 3 and opt == "print":
            SetMatrix.printMatrix(*container_minor) if container_minor else None
            
            """ 
                LOOP UNTUK PRINT HASIL DAN PROSESS PERHITUNGAN MINOR
            """
            for i, result in enumerate(container_text):
                print(f"{i+1}. {result}")
            print(f"[green1]Determinan minor saat ini = {det_result:.2f} [/green1]\n")

        if depth == 0 and opt == "print":
            print("[bold dark_slate_gray2]<========== DETERMINAN AKHIR =========>[/bold dark_slate_gray2]")
            for i in range(len(container_result)):
                answer = ""
                for j, result in enumerate(container_result[i]):
                    cofactor = ((-1)**j) * matrix[0][j]
                    temp = f"({cofactor:.1f} * {result:.1f})" if i==0 else f"({result:.1f})"
                    answer+= temp + " + " if j!=len(container_result[i]) -1 else temp
                    
                print(f"[bold yellow1]{answer}[/bold yellow1]")
            print(f"[bold dark_orange]Hasil Akhir = {det_result:.2f}[/bold dark_orange]") 
            
        return float(det_result)



"""   
    <=== CLASS SETMATRIX ===>
"""
class SetMatrix:
    kof:kofaktor = object.__new__(kofaktor)
    adj:adjoin = object.__new__(adjoin)
    gauss:Gauss = object.__new__(Gauss)

    __FITUR_MAP = {
        "kof": kofaktor,
        "adj" : adjoin,
        "gauss" : Gauss
    }
    
    def __new__(cls, matrix):
        raise TypeError("TIDAK BISA MEMBUAT OBJEK BARU SECARA LANGSUNG")
    
    def __init__(self, matrix):
        # print("instance berhasil dibuat")
        self.__matrix = matrix
    
    def __getattribute__(self, attr):
        fitur_map = super().__getattribute__("_SetMatrix__FITUR_MAP")
        if attr in fitur_map:
            raise AttributeError
        return super().__getattribute__(attr)
    
    def __getattr__(self, attr):
        if attr in self.__FITUR_MAP:
            return helperWrapper(self, self.__FITUR_MAP[attr])
        raise AttributeError(f"Tidak ada atribut {attr} dalam SetMatrix")
    
    def __str__(self) -> str:
        return tabulate(self.__matrix, tablefmt="grid", floatfmt=".1f")
    
    
    """ 
        <==== KUMPULAN PROPERTY CLASS ===>
    """
    @property
    def tolist(self):
        """GETTER UNTUK MENDAPATKAN MATRIX YANG PRIVATE"""
        return self.__matrix
        

    
    def adjoin(self, *, mode:str = None) -> "SetMatrix":
        matrix = SetMatrix.matrix(self.__matrix)
        inv_matrix = []
        even = lambda x: x%2==0
        isnum = lambda x: x.is_integer()
        
        container_matrix = [] if mode == "print" else None
        
        for i in range(len(matrix.tolist)):
            container_minor = []
            row_data = []
            for j in range(len(matrix.tolist)):
                matrix_minor = kofaktor.get_minor(matrix, i, j)
                container_minor.append(matrix_minor)
                
                det_matrix = matrix_minor.gauss.det()
                # row_data.append(det_matrix)
                
                data = det_matrix
                if not even(i) and even(j) or even(i) and not even(j):
                    data *= (-1)
                # if isnum(data):
                #     data = int(data)
                # # data = f"{da"
                row_data.append(float(data))
            container_minor.append(SetMatrix.matrix([row_data]))
            SetMatrix.printMatrix(*container_minor) if mode == "print" else None
            inv_matrix.append(row_data)
            
        # print(container_matrix)
        # SetMatrix.printMatrix(SetMatrix.matrix(inv_matrix)) if mode == "print" else None
        # print(inv_matrix)
        return SetMatrix.matrix(inv_matrix)
    
    @property
    def T(self):
        """GETTER UNTUK MENDAPATKAN TRANSPOS MATRIX"""
        transpose = self.__matrix
        transpose = [list(row) for row in zip(*transpose)]
        return SetMatrix.matrix(transpose)
    
    """METHOD UNTUK MEMBUAT OBJEK MATRIX """
    @classmethod
    def matrix(cls, matrix) -> object:
        instance: SetMatrix = super().__new__(cls)
        instance.__init__(matrix)
        return instance
    
    
    """
        <==== KUMPULAN METHOD DARI CLASS ===>
    """
    
    @staticmethod
    def identity(size:int):
        """MENYIAPKAN MATRIX IDENTITY"""
        matrix = [[0 for i in range(size)] for _ in range(size)]
        for i in range(size):
            matrix[i][i] = 1
            
        return matrix
    
    """METHOD UNTUK PRINT MATRIX DENGAN PARAMETER ARGS"""
    @staticmethod
    def printMatrix(*args, type:str = None, header:bool = False):
        """ 
            CEK APAKAH ARGUMEN YANG DIBERIKAN ADALAH OBJEK DARI SETMATRIX
        """
        for matrix in args:
            if not isinstance(matrix, list) and not isinstance(matrix, SetMatrix):
                raise ValueError(f"{matrix} bukan list atau tuple")
            if not isinstance(matrix, SetMatrix):
                raise ValueError(f"Matrix {matrix} bukan objek dari SetMatrix")

        ##
        """ CONTAINER UNTUK MENYIMPAN MATRIX """
        container_matrix = []
        
        """ MENENTUKAN JUMLAH MAKSIMAL DAN MINIMAL BARIS """
        max_row = max(len(m.tolist) for m in args)
        min_row = min(len(m.tolist) for m in args)

        """
            MENGAMBIL DATA MATRIX YANG ADA DI DALAM
            OBJEK SETMATRIX YANG AKAN DISIMPAN DALAM KONTAINER DAN
            MEMBUAT BARIS BARU DENGAN JUMLAH KOLOM YANG SAMA DENGAN JUMLAH MAKSIMAL BARIS
        """
        for matrix in args:
            row, col = len(matrix.tolist), len(matrix.tolist[0])
            new_matrix = [] #matrix baru yang sudah di format

            for i in range(max_row):
                row_data = [] #data baris baru
                for j in range (col):
                    if i < row:
                        value_matrix:float = float(matrix.tolist[i][j])
                        if type == "frc" :
                            if value_matrix.is_integer():
                                row_data.append(str(value_matrix))
                            else:
                                format_num = str(frc(value_matrix).limit_denominator(100))
                                row_data.append(format_num)
                        else:
                            format_num = f"{value_matrix:.4g}"
                            row_data.append(format_num)
                    else:
                        value_matrix = "px" #jika tidak ada data maka isi dengan px
                        row_data.append(value_matrix)
                new_matrix.append(row_data)
            # print(new_matrix)

            """
                MEMBUAT TABEL MATRIX DENGAN TABULATE YANG 
                KEMUDIAN DI SETOR KE CONTAINER MATRIX
            """
            if type == "frc":
                table_matrix = tabulate(new_matrix, tablefmt="grid", floatfmt=".1f").split("\n")
            else:
                table_matrix = tabulate(new_matrix, tablefmt="grid").split("\n")
            #membuat whitespace sepanjang jumlah elemen pada baris
            ws = " " * (len(table_matrix[0]) - 5) # -6 dari "matrix"
            
            """MENAMBAHKAN HEADER PADA TABEL MATRIX
            """
            if type != "com" and header:
                table_matrix.insert(0, "[bold green1]Matrix[/bold green1]" + ws + " " if len(matrix.tolist) >=3 
                                    else "[bold green1]Minor[/bold green1]" + ws) 
            container_matrix.append(table_matrix)

        #keluar loop
        """
            MENENTUKAN PANJANG CONTIANER MATRIX
        """
        len_container = len(container_matrix)
        
        """
            LOOP UNTUK MEMBUAT MANIPULASI TABEL MATRIX AGAR BISA
            DIPRINT WALAU UKURANNYA BERBEDA BEDA
        """
        # print(container_matrix)
        if max_row!=min_row: #jika tidak sama berarti ukuran matrix berbeda beda
            for i in range(len_container):
                leng = len(container_matrix[i]) #mengambil jumlah baris
                for j in range(leng):
                    if "px" in container_matrix[i][j]: #jika ada px berari itu adalah baris kosong
                    #     count = sum(2 for _ in range(max_row - min_row)) # +2 srtiap perbedaan baris
                    #     len_row = len_rowtr 
                        for k in range(j, leng):
                            container_matrix[i][k] = " " * len(container_matrix[i][1])
                        break
        
        if type == "com":
            # print(container_matrix[0][0])
            # print(len_col)
            
            for i in range (len_container):
                len_row = len(container_matrix[i])
                for j in range(len_row):
                    row = container_matrix[i][j]
                    row_list = list(row)
                    len_col = len(row_list)
                    # if j == 0 or j == len_row-1:
                    #     row_list[len_col-1]= "-"
                    if i == 0:
                        row_list[len_col-1] = "|" if j != 0 and j != len_row-1 else row_list[len_col-1]
                    if i != 0:
                        row_list[0] = ""
                    row = ''.join(row_list)
                    container_matrix[i][j] = row
            

        # print([row for row in zip(*container_matrix)])
        # print(container_matrix)
        """ PRINT MATRIX """
        combined_table = ["".join(row_matrix) for row_matrix in zip(*container_matrix)] if type == "com" else ["  ".join(row_matrix) for row_matrix in zip(*container_matrix)]
        combined_table = "\n".join(combined_table)
        print(f"[bold]{combined_table}[bold]")



"""UNIT TESTING"""
def main() -> None:
    A = [
        [2, 4, 6, 2, 0],
        [2, 8, -1, -2, 9],
        [4, 16, -2, -4, -18],
        [1, 2, 3, 4, 5],
        [4, -2, 1, 2, 1]
    ]

    B = [
        [1, 2, 4,6],
        [11, 2, 8 ,3],
        [-2, -2, 6, 2],
        [1, 1, 8, -3],
    ]
    
    E = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]


    
if __name__ == "__main__":
    main()