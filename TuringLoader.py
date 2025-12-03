from State import State

class TuringLoader:
    def __init__(self, filename):
        self.filename = filename
        self.states = {} 
        self.start_state = None
        self.w = ""

    def get_or_create_state(self, name):
        """Retorna o estado se já existe, ou cria um novo se não."""
        name = name.strip()
        if name not in self.states:
            self.states[name] = State(name)
        return self.states[name]

    def load(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            
            if not line or line.startswith('#'):
                continue

            if line.startswith('fita'):
                self.w = line.split()[1]
                continue

            if line.startswith('init'):
                state_name = line.split()[1]
                self.start_state = self.get_or_create_state(state_name)
                continue

            if line.startswith('accept'):
                final_names = line.split()[1].split(',') 
                for fn in final_names:
                    s = self.get_or_create_state(fn)
                    s.setFinal()
                continue

            # Lê transições: origem, leu, destino, escreveu, direcao
            # Ex: qp,_,qx,X,<
            if ',' in line:
                parts = line.split(',')
                if len(parts) == 5:
                    src_name = parts[0].strip()
                    read_char = parts[1].strip()
                    dest_name = parts[2].strip()
                    write_char = parts[3].strip()
                    direction_symbol = parts[4].strip()

                    # Conversão de símbolos do TXT para o Python
                    # _ vira None (vazio)
                    # > vira 'D'
                    # < vira 'E'
                    
                    final_read = None if read_char == '_' else read_char
                    final_write = None if write_char == '_' else write_char
                    
                    final_dir = 'D'
                    if direction_symbol == '<':
                        final_dir = 'E'
                    elif direction_symbol == '>':
                        final_dir = 'D'
                    else:
                        final_dir = direction_symbol # Fallback se já estiver escrito D ou E

                    # Cria a transição
                    src_state = self.get_or_create_state(src_name)
                    dest_state = self.get_or_create_state(dest_name)
                    
                    src_state.addTransition(dest_state, final_read, final_write, final_dir)

        return self.start_state, self.w