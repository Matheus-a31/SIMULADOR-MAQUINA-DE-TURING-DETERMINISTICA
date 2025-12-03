class Edge:
    # read_c: Caractere lido na fita
    # write_c: Caractere a ser escrito na fita
    # direction: 'D' (Direita) ou 'E' (Esquerda)
    def __init__(self, read_c: str, write_c: str, direction: str):
        self.read_c = read_c
        self.write_c = write_c
        self.direction = direction

    def getReadC(self): return self.read_c
    def getWriteC(self): return self.write_c
    def getDirection(self): return self.direction

    @staticmethod
    def instance(read_c: str, write_c: str, direction: str):
        return Edge(read_c, write_c, direction)

    def equals(self, o):
        if isinstance(o, Edge):
            # Para identificar a transição, basta comparar o caractere de leitura
            return Edge.testAB(self.read_c, o.getReadC())
        return False

    def __repr__(self):
        return f'[{self.read_c}/{self.write_c}, {self.direction}]'

    @staticmethod
    def testAB(a, b):
        return a == b