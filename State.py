from Edge import Edge
from Transition import Transition

class State:
    def __init__(self, name: str):
        self.name = name
        self.isFinal = False
        self.transitions = []

    def getName(self): return self.name
    
    def setFinal(self): self.isFinal = True

    # modifiquei para aceitar write_c e direction
    def addTransition(self, state, read_c, write_c, direction):
        return self.addTransitions(state, Edge.instance(read_c, write_c, direction))

    def addTransitions(self, state, *edges):
        for edge in edges:
            transition = Transition(state, edge)
            if transition in self.transitions:
                continue
            self.transitions.append(transition)
        return self

    # Busca transição baseada no caractere lido
    def transition(self, char_lido):
        for t in self.transitions:
            e = t.getEdge()
            if e.getReadC() is None and char_lido is None:
                return t
            if e.getReadC() == char_lido:
                return t
        return None
    
    def equals(self, s):
        if isinstance(s, State):
            return s.getName() == self.getName()
        return False
    
    def hashCode(self):
        return hash(self.getName())