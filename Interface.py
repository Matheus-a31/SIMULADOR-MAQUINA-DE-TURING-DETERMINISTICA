import tkinter as tk
from tkinter import filedialog, messagebox
from TuringLoader import TuringLoader
from Machine import Machine
import os

class TuringGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        self.machine = None
        self.is_running = False
        
        self.speed = 2000 
        
        
        frame_top = tk.Frame(root, bg="#ddd", pady=10, padx=10)
        frame_top.pack(fill=tk.X)

        self.btn_load = tk.Button(frame_top, text="📂 Carregar input.txt", command=self.load_file, 
                                  bg="#4a90e2", fg="white", font=("Arial", 11, "bold"), relief=tk.FLAT)
        self.btn_load.pack(side=tk.LEFT, padx=10)

        self.lbl_file = tk.Label(frame_top, text="Nenhum arquivo carregado", bg="#ddd", font=("Arial", 10, "italic"))
        self.lbl_file.pack(side=tk.LEFT)

       
        frame_tape_container = tk.Frame(root, bg="white", pady=20)
        frame_tape_container.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(frame_tape_container, text="FITA:", bg="white", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10)

        self.canvas_tape = tk.Canvas(frame_tape_container, height=80, bg="white", highlightthickness=0)
        self.canvas_tape.pack(fill=tk.X, padx=10)

      
        frame_info = tk.Frame(root, bg="#f0f0f0")
        frame_info.pack(pady=10)

        
        self.lbl_state = tk.Label(frame_info, text="AGUARDANDO...", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#555")
        self.lbl_state.pack()
        
        self.lbl_steps = tk.Label(frame_info, text="Passos: 0", font=("Arial", 12), bg="#f0f0f0", fg="#666")
        self.lbl_steps.pack()

        frame_log = tk.Frame(root, bg="#f0f0f0", padx=20)
        frame_log.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(frame_log, height=8, state=tk.DISABLED, bg="#e8e8e8", font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

        frame_controls = tk.Frame(root, bg="#ccc", pady=15)
        frame_controls.pack(side=tk.BOTTOM, fill=tk.X)

        self.btn_step = tk.Button(frame_controls, text="▶ Próximo Passo", command=self.step_once, 
                                  state=tk.DISABLED, font=("Arial", 12), width=15)
        self.btn_step.pack(side=tk.LEFT, padx=20)

        self.btn_run = tk.Button(frame_controls, text="⏩ Executar Tudo", command=self.toggle_run, 
                                 state=tk.DISABLED, font=("Arial", 12), width=15)
        self.btn_run.pack(side=tk.LEFT, padx=10)
        
        self.btn_reset = tk.Button(frame_controls, text="⟲ Reiniciar", command=self.reset_machine, 
                                   state=tk.DISABLED, font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", width=12)
        self.btn_reset.pack(side=tk.RIGHT, padx=20)

    def load_file(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[("Text files", "*.txt")])
        if filename:
            self.filename = filename
            self.lbl_file.config(text=os.path.basename(filename))
            self.reset_machine()

    def reset_machine(self):
        if not hasattr(self, 'filename'): return
        
        try:
            loader = TuringLoader(self.filename)
            initial_state, w = loader.load()
            
            if initial_state and w:
                self.machine = Machine(initial_state, w, 50)
                self.is_running = False
                self.btn_run.config(text="⏩ Executar Tudo")
                
                self.lbl_state.config(text=f"Estado: {initial_state.getName()}", fg="black")
                self.btn_step.config(state=tk.NORMAL)
                self.btn_run.config(state=tk.NORMAL)
                self.btn_reset.config(state=tk.NORMAL)
                
                self.log_text.config(state=tk.NORMAL)
                self.log_text.delete(1.0, tk.END)
                self.log_text.config(state=tk.DISABLED)
                
                self.update_ui()
                self.log(f"Arquivo '{os.path.basename(self.filename)}' carregado.")
            else:
                messagebox.showerror("Erro", "Arquivo inválido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao ler arquivo: {e}")

    def step_once(self):
        if not self.machine: return False
        
        continuar, msg = self.machine.next_step()
        self.log(msg)
        self.update_ui()

        if not continuar:
            self.is_running = False
            self.btn_run.config(text="⏩ Executar Tudo")
            
            if self.machine.q.isFinal:
                self.lbl_state.config(text=f"✅ ACEITO! ({self.machine.q.getName()})", fg="#27ae60")
                messagebox.showinfo("Resultado", f"A palavra foi ACEITA!\nEstado Final: {self.machine.q.getName()}")
            else:
                self.lbl_state.config(text=f"❌ REJEITADO ({self.machine.q.getName()})", fg="#c0392b")
                messagebox.showwarning("Resultado", "A palavra foi REJEITADA ou a máquina travou.")

        return continuar

    def toggle_run(self):
        if self.is_running:
            self.is_running = False
            self.btn_run.config(text="⏩ Executar Tudo")
        else:
            self.is_running = True
            self.btn_run.config(text="⏸ Pausar")
            self.run_loop()

    def run_loop(self):
        if self.is_running:
            continuar = self.step_once()
            if continuar:
                self.root.after(self.speed, self.run_loop)

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, ">> " + message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_ui(self):
        if not self.machine: return
        
        if not self.machine.q.isFinal and self.machine.steps > 0:
             self.lbl_state.config(text=f"Estado Atual: {self.machine.q.getName()}", fg="black")

        self.lbl_steps.config(text=f"Passos: {self.machine.steps}")
        self.draw_tape()

    def draw_tape(self):
        self.canvas_tape.delete("all")
        w_width = self.canvas_tape.winfo_width()
        if w_width < 100: w_width = 800
        
        center_x = w_width // 2
        cell_size = 40
        y = 10
        
        snapshot = self.machine.get_tape_snapshot(window_size=21)
        
        for i, char in enumerate(snapshot):
            x_pos = center_x + (i - 10) * cell_size
            is_head = (i == 10)
            
            fill_color = "#fffac8" if is_head else "white"
            outline_color = "#f39c12" if is_head else "#bbb"
            border_width = 3 if is_head else 1
            font_style = ("Courier", 14, "bold") if is_head else ("Courier", 12)

            self.canvas_tape.create_rectangle(x_pos, y, x_pos + cell_size, y + cell_size, 
                                              fill=fill_color, outline=outline_color, width=border_width)
            
            self.canvas_tape.create_text(x_pos + cell_size/2, y + cell_size/2, 
                                         text=char, font=font_style, fill="#333")
            
            if is_head:
                 self.canvas_tape.create_polygon(x_pos + cell_size/2, y + cell_size + 5, 
                                                 x_pos + cell_size/2 - 6, y + cell_size + 12,
                                                 x_pos + cell_size/2 + 6, y + cell_size + 12,
                                                 fill="#f39c12")

if __name__ == "__main__":
    root = tk.Tk()
    app = TuringGUI(root)
    root.mainloop()