import tkinter as tk
from model.desenho import Desenho
from view.interface import Interface
from controllers.controlador import Controlador

if __name__ == "__main__":
    root = tk.Tk()
    
    meu_desenho = Desenho()
    minha_interface = Interface(root)
    meu_controlador = Controlador(meu_desenho, minha_interface)
    
    root.mainloop()