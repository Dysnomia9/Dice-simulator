import tkinter as tk
from main_window import SimuladorDados

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SimuladorDados(root)
        root.mainloop()
    except Exception as e:
        print(f"Ocurrió un error al iniciar la aplicación: {e}")
        import tkinter.messagebox
        tkinter.messagebox.showerror(
            "Error Crítico",
            f"No se pudo iniciar la aplicación.\n\nError: {e}"
        )