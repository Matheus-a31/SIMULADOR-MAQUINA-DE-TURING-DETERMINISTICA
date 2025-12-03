from State import State

class Machine: 
    def __init__(self, q: State, w: str, _range: int = 50):
        self.q = q
        self.w = w
        self.fita = []
        self.steps = 0
        
        # Configuração inicial da fita
        self.set_fita_space(_range)
        self.init_fita(w)

    def next_step(self):
        """Executa APENAS UMA transição. Retorna (True, msg) se continuar, (False, msg) se parar."""
        
        # Proteção contra estado nulo
        if self.q is None:
            return False, "ERRO: Estado atual é None."

        # Se já chegou no final antes de tentar o passo
        if self.q.isFinal:
            return False, "ACEITO: A máquina já está em estado final."

        char_atual = self.fita[self.current]
        transicao = self.q.transition(char_atual)

        if transicao is not None:
            edge = transicao.getEdge()
            qNext = transicao.getState()
            
            
            self.fita[self.current] = edge.getWriteC()

            
            direction = edge.getDirection()
            if direction == 'D':
                self.current += 1
            elif direction == 'E':
                self.current -= 1
            
            
            self.q = qNext
            self.steps += 1
            
            
            if self.q.isFinal:
                # Retorna False para parar o loop na interface, mas avisa que aceitou
                return False, f"Leu '{char_atual}' -> Foi para {qNext.getName()} (FINAL) -> ACEITO!"
            
        
            return True, f"Leu '{char_atual}' -> Escreveu '{edge.getWriteC()}' -> Moveu {direction} -> Foi para {qNext.getName()}"
        else:
            # Não tem transição (Travou/Rejeitou)
            return False, f"TRAVOU: Sem transição em {self.q.getName()} lendo '{char_atual}'"

    def get_tape_snapshot(self, window_size=21):
        start = self.current - (window_size // 2)
        end = self.current + (window_size // 2) + 1
        
        snapshot = []
        for i in range(start, end):
            if 0 <= i < len(self.fita):
                val = self.fita[i]
                snapshot.append(val if val is not None else "_")
            else:
                snapshot.append("_")
        return snapshot

    def init_fita(self, w):
        idx = self.current
        for a in list(w):
            self.fita[idx] = a
            idx += 1

    def set_fita_space(self, _range):
        self.range = _range
        self.fita = [None] * (self.range * 4)
        self.current = self.range