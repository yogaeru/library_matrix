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
    <=== ADJOIN ===>
"""
class adjoin:
    def __new__(cls, *agrs, **kwargs):
        raise TypeError(f"TIDAK BISA MEMBUAT INSTANCE DARI {cls}")

    def __init__(self, obj_matrix):
        self.__obj_matrix = obj_matrix
    
    def inv(self, *, mtr:"SetMatrix" = None) -> "SetMatrix":
        
        matrix = self.__obj_matrix if mtr is None else mtr
        if not isinstance(matrix, SetMatrix):
            raise TypeError("Parameter harus berupa SetMatrix")    
        
        container_matrix = []
        inv_matrix = []
        
        print(matrix.adjoin.tolist)
        list_matrix = matrix.adjoin.tolist
        print (list_matrix)
        len_matrix = len(list_matrix)
        det_matrix = 1 / matrix.kof.det()
        print(f"{det_matrix:.2f}")
        
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

    __FITUR_MAP = {
        "kof": kofaktor,
        "adj" : adjoin
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
        
        container_matrix = [] #if mode == "print" else None
        
        for i in range(len(matrix.tolist)):
            container_minor = []
            row_data = []
            for j in range(len(matrix.tolist)):
                matrix_minor = kofaktor.get_minor(matrix, i, j)
                container_minor.append(matrix_minor)
                
                det_matrix = matrix_minor.kof.det()
                # row_data.append(det_matrix)
                
                data = det_matrix
                if not even(i) and even(j) or even(i) and not even(j):
                    data *= (-1)
                if isnum(data):
                    data = int(data)
                row_data.append(data)
            container_minor.append(SetMatrix.matrix([row_data]))
            SetMatrix.printMatrix(*container_minor)
            inv_matrix.append(row_data)
            
        # print(container_matrix)
        SetMatrix.printMatrix(SetMatrix.matrix(inv_matrix)) if mode == "print" else None
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
    
    """METHOD UNTUK PRINT MATRIX DENGAN PARAMETER ARGS"""
    @staticmethod
    def printMatrix(*args):
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
                        value_matrix = matrix.tolist[i][j]
                        if isinstance(value_matrix, (int) ) :
                            format_num = str(float(value_matrix))
                            row_data.append(format_num)
                        else:
                            format_num = str(frc(value_matrix).limit_denominator(100))
                            row_data.append(format_num)
                    else:
                        value_matrix = "px" #jika tidak ada data maka isi dengan px
                        row_data.append(value_matrix)
                new_matrix.append(row_data)

            """
                MEMBUAT TABEL MATRIX DENGAN TABULATE YANG 
                KEMUDIAN DI SETOR KE CONTAINER MATRIX
            """
            table_matrix = tabulate(new_matrix, tablefmt="grid", floatfmt=".1f").split("\n")
            #membuat whitespace sepanjang jumlah elemen pada baris
            ws = " " * (len(table_matrix[0]) - 5) # -6 dari "matrix"
            
            """MENAMBAHKAN HEADER PADA TABEL MATRIX
            """
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
        # print([row for row in zip(*container_matrix)])
        """ PRINT MATRIX """
        combined_table = ["   ".join(row_matrix) for row_matrix in zip(*container_matrix)]
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