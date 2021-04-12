from sudoku import Sudoku, Celula

def main():

    sudoku = cria_sudoku()

    print( '---------- Antes -------------')
    print(sudoku)
    sudoku.resolve()        

    print( '---------- Depois -------------')
    print(sudoku)
    
    sudoku.print_status()

def cria_cel( sudoku, x, y, val):
    cel = Celula(x, y )
    cel.possibilidades = [val]
    sudoku.sudoku[x][y] = cel

def cria_sudoku():
    texto =  '*91*7**7*'
    texto += '2*4******'
    texto += '*5*3*****'
    texto += '1***2***8'
    texto += '**76*32**'
    texto += '9***5***3'
    texto += '*****7*3*'
    texto += '******9*6'
    texto += '*6**1*57*'

    s = Sudoku()

    for i in range(9):
        for j in range(9):
            cel = Celula(i, j )
            pos = i * 9 + j
            valor = texto[ pos: pos + 1 ]

            if valor != '*':
                cel.possibilidades = []
                cel.val = int(valor)

            s.sudoku[i][j] = cel
    
    return s

if __name__ == "__main__":
    main()