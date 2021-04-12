class Sudoku:
    def __init__(self):
        self.sudoku = []
        for i in range(9):
            linha = []
            for j in range(9):
                linha.append( Celula( i, j))
            
            self.sudoku.append( linha)

    def resolve(self):
        iteration = 1
        mudanca = True
        while mudanca:
            mudanca = False

            for i in range(9):
                for j in range(9):

                    if iteration == 171 and i == 0 and j ==8:
                        a = 1
                
                    cel = self.sudoku[i][j]

                    if cel.node_consistency():
                        mudanca = True

                    if cel.arc_consistency( self.vizinhos_celula( cel )):
                        mudanca = True

                    #print(iteration, i,j,'------')
                    #print(self)
                    iteration += 1


    def vizinhos(self, x, y):
        linha = []
        for i in range(9):
            linha.append( self.sudoku[x][i])

        coluna = []
        for i in range(9):
            coluna.append( self.sudoku[i][y])

        quadro = []
        start = 3 * (x // 3)
        for i in range( start, start + 3):

            start_y = 3 * (y // 3)
            for j in range( start_y, start_y + 3):
                quadro.append( self.sudoku[i][j])

        return [ linha, coluna, quadro ]

    def vizinhos_celula(self, celula):
        x, y = celula.getXY()
        return self.vizinhos(x, y)

    def __str__(self):
        texto = ''
        for i in range(9):
            if i % 3 == 0:
                texto += '-------------\n'

            for j in range(9):

                if j % 3 == 0:
                    texto += '|'

                if self.sudoku[i][j] is None:
                    texto += '*'
                else:
                    texto += f'{self.sudoku[i][j]}'


            texto +='|\n'
        return texto
    
    def print_status(self):

        for i in range(9):
            for j in range(9):

                texto = f'[{i}] [{j}] '
                
                if self.sudoku[i][j] is not None:
                    texto += f' val: { self.sudoku[i][j].val }  { self.sudoku[i][j].possibilidades }'

                print( texto )

class Celula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.val = None
        self.possibilidades = [ 1,2,3,4,5,6,7,8,9]

    def __hash__(self):
        return hash((self.x, self.y, self.val, self.possibilidades))

    def __eq__(self, other):
        return (
            (self.x == other.x) and
            (self.y == other.y) and
            (self.val == other.val) and
            (self.possibilidades == other.possibilidades)
        )

    def __str__(self):
        
        if self.val is not None:
            return f'{self.val}'
        else:
            return '*'


    def getXY(self):
        return self.x, self.y

    def node_consistency(self):
        if self.val is not None:
            return False

        if len( self.possibilidades) == 1:
            self.val = self.possibilidades.pop( 0 )
            return True
    
    def arc_consistency(self, vizinhos ):

        mudanca = self.arc_consistency_simples(vizinhos)

        if self.arc_consistency_unico( vizinhos):
            mudanca = True

        if self.arc_consistency_par(vizinhos):
            mudanca = True

        return mudanca

    def arc_consistency_simples(self, vizinhos):
        mudanca = False

        if self.val is None:
            return False

        for conjunto in vizinhos:

            # solução simples
            for cel in conjunto:
                if ( cel is None or
                self == cel or
                cel.val is not None or
                self.val not in cel.possibilidades): 
                    continue
                
                cel.possibilidades.remove( self.val )
                mudanca = True

        return mudanca

    def arc_consistency_unico(self, vizinhos):
        # das minhas possibilidades, alguma é única nos vizinhos?
        if self.val is not None:
            return False

        valorMudar = None
        for val in self.possibilidades:

            for conjunto in vizinhos:

                valorMudar = val
                for cel in conjunto:
                    if ( self == cel ):
                        continue
                                        
                    if val in cel.possibilidades or cel.val == val:
                        valorMudar = None
                        break
        
                if valorMudar is not None:
                    self.val = valorMudar
                    self.possibilidades = []
                    return True


        return False

    def arc_consistency_par(self, vizinhos):

        if len(self.possibilidades) != 2:
            return False

        mudanca = False

        for conjunto in vizinhos:

            for cel in conjunto:
                if ( cel is None or
                self == cel or
                cel.val is not None or
                len(cel.possibilidades )!= 2 ):
                    continue
                
                if self.possibilidades == cel.possibilidades:
                    # remove todos os outros pares
                    for novo_cel in conjunto:
                        if novo_cel == self or novo_cel == cel:
                            continue

                        if self.possibilidades[0] in  novo_cel.possibilidades:
                            novo_cel.possibilidades.remove( self.possibilidades[0])
                            mudanca = True

                        if self.possibilidades[1] in  novo_cel.possibilidades:
                            novo_cel.possibilidades.remove( self.possibilidades[1])
                            mudanca = True


        return mudanca

