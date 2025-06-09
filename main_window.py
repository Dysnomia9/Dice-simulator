import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime

from graph_manager import GraphManager
from dice_simulator import DiceSimulator


class SimuladorDados:
    def __init__(self, root):
        self.root = root
        self.simulator = DiceSimulator()
        self.setup_window()
        self.setup_colors()
        self.setup_styles()
        self.create_widgets()
        self.simulacion_activa = False

    def setup_window(self):
        """Configurar ventana principal."""
        self.root.title("Simulador de Dados Avanzado - Análisis Probabilístico")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Manejar el cierre de la aplicación."""
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.root.destroy()

    def setup_colors(self):
        """Definir esquema de colores."""
        self.colores = {
            'bg_principal': '#1a1a2e', 'bg_secundario': '#16213e',
            'bg_frame': '#0f3460', 'bg_card': '#e94560',
            'bg_accent': '#0f4c75', 'bg_boton_primary': '#e94560',
            'bg_boton_hover': '#d63447', 'bg_boton_danger': '#e74c3c',
            'bg_boton_success': '#27ae60', 'bg_boton_warning': '#f39c12',
            'texto_principal': '#ffffff', 'texto_secundario': '#bdc3c7',
            'texto_accent': '#e94560'
        }
        self.root.configure(bg=self.colores['bg_principal'])

    def setup_styles(self):
        """Configurar estilos personalizados para ttk."""
        style = ttk.Style()
        style.configure('Custom.TNotebook', background=self.colores['bg_principal'], borderwidth=0)
        style.configure('Custom.TNotebook.Tab',
                        background=self.colores['bg_accent'],
                        foreground=self.colores['texto_principal'],
                        borderwidth=1, padding=[15, 8], focuscolor='none')
        style.map('Custom.TNotebook.Tab',
                  background=[('selected', self.colores['bg_card']),
                              ('active', self.colores['bg_boton_hover'])])

    def create_widgets(self):
        """Crear todos los widgets de la interfaz."""
        main_frame = tk.Frame(self.root, bg=self.colores['bg_principal'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.create_header(main_frame)
        self.create_control_frame(main_frame)
        self.create_notebook(main_frame)

    def create_header(self, parent):
        """Crear el encabezado de la aplicación."""
        header_frame = tk.Frame(parent, bg=self.colores['bg_card'], relief=tk.RAISED, bd=2)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        tk.Label(header_frame, text="SIMULADOR DE DADOS PROBABILÍSTICO",
                 font=('Segoe UI', 18, 'bold'), bg=self.colores['bg_card'],
                 fg=self.colores['texto_principal']).pack(pady=10)
        tk.Label(header_frame, text="Análisis Estadístico Avanzado | Visualización de Probabilidades",
                 font=('Segoe UI', 10), bg=self.colores['bg_card'],
                 fg=self.colores['texto_secundario']).pack(pady=(0, 10))

    def create_control_frame(self, parent):
        """Crear el panel de control para la simulación."""
        control_outer = tk.Frame(parent, bg=self.colores['bg_secundario'], relief=tk.RAISED, bd=2)
        control_outer.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        control_frame = tk.Frame(control_outer, bg=self.colores['bg_secundario'])
        control_frame.pack(fill=tk.X, padx=10, pady=8)

        # Paneles internos
        left_panel = tk.Frame(control_frame, bg=self.colores['bg_frame'], relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        right_panel = tk.Frame(control_frame, bg=self.colores['bg_frame'], relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)

        # Contenido del panel izquierdo (Configuración)
        tk.Label(left_panel, text="CONFIGURACIÓN", font=('Segoe UI', 10, 'bold'),
                 bg=self.colores['bg_frame'], fg=self.colores['texto_principal']).pack(pady=8)
        input_container = tk.Frame(left_panel, bg=self.colores['bg_frame'])
        input_container.pack(padx=15, pady=(0, 15), fill=tk.X)
        tk.Label(input_container, text="Número de lanzamientos:", font=('Segoe UI', 9, 'bold'),
                 bg=self.colores['bg_frame'], fg=self.colores['texto_principal']).pack(anchor='w')
        self.entry_lanzamientos = tk.Entry(input_container, font=('Segoe UI', 10), width=15,
                                           bg='#2c3e50', fg=self.colores['texto_principal'],
                                           insertbackground=self.colores['texto_principal'])
        self.entry_lanzamientos.insert(0, "10000")
        self.entry_lanzamientos.pack(anchor='w', pady=(3, 8))
        tk.Label(input_container, text="Número de dados:", font=('Segoe UI', 9, 'bold'),
                 bg=self.colores['bg_frame'], fg=self.colores['texto_principal']).pack(anchor='w')
        self.combo_dados = ttk.Combobox(input_container, values=[1, 2, 3], state='readonly', width=12)
        self.combo_dados.set(3)
        self.combo_dados.pack(anchor='w', pady=(3, 0))

        # Contenido del panel derecho (Acciones)
        tk.Label(right_panel, text="ACCIONES", font=('Segoe UI', 10, 'bold'),
                 bg=self.colores['bg_frame'], fg=self.colores['texto_principal']).pack(pady=8)
        button_container = tk.Frame(right_panel, bg=self.colores['bg_frame'])
        button_container.pack(padx=15, pady=(0, 15))
        self.btn_simular = tk.Button(button_container, text="SIMULAR", font=('Segoe UI', 11, 'bold'),
                                     bg=self.colores['bg_boton_primary'], fg=self.colores['texto_principal'],
                                     activebackground=self.colores['bg_boton_hover'], bd=0, padx=25, pady=8,
                                     cursor='hand2', command=self.iniciar_simulacion)
        self.btn_simular.pack(pady=3)
        self.btn_limpiar = tk.Button(button_container, text="LIMPIAR", font=('Segoe UI', 10, 'bold'),
                                     bg=self.colores['bg_boton_danger'], fg=self.colores['texto_principal'],
                                     activebackground='#c0392b', bd=0, padx=20, pady=6,
                                     cursor='hand2', command=self.limpiar_todo)
        self.btn_limpiar.pack(pady=3)

        # Barra de estado
        self.status_var = tk.StringVar(value="Listo para simular")
        status_bar = tk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w',
                              bg=self.colores['bg_accent'], fg=self.colores['texto_principal'])
        status_bar.grid(row=3, column=0, sticky='ew', padx=10, pady=(5,0))

    def create_notebook(self, parent):
        """Crear el notebook con pestañas para gráficos y análisis."""
        notebook_container = tk.Frame(parent, bg=self.colores['bg_principal'])
        notebook_container.grid(row=2, column=0, sticky='nsew')
        notebook_container.grid_rowconfigure(0, weight=1)
        notebook_container.grid_columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(notebook_container, style='Custom.TNotebook')
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # Pestaña de Gráficos
        self.graph_frame = tk.Frame(self.notebook, bg=self.colores['bg_secundario'])
        self.notebook.add(self.graph_frame, text="GRÁFICOS VISUALES")
        
        # Configurar el grid del 'graph_frame' para que el contenido se expanda
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        # Pestaña de Análisis
        self.analysis_frame = tk.Frame(self.notebook, bg=self.colores['bg_secundario'])
        self.notebook.add(self.analysis_frame, text="ANÁLISIS DETALLADO")
        
        # Inicializar el gestor de gráficos (AHORA IMPORTADO DESDE graph_manager.py)
        self.graph_manager = GraphManager(self.graph_frame, self.colores)
        
        # Crear el área de texto para el análisis
        self.create_analysis_area()

    def create_analysis_area(self):
        """Crear el área de texto para mostrar los resultados del análisis."""
        self.analysis_frame.grid_rowconfigure(0, weight=1)
        self.analysis_frame.grid_columnconfigure(0, weight=1)
        self.text_analysis = scrolledtext.ScrolledText(
            self.analysis_frame, font=('Consolas', 10), bg=self.colores['bg_frame'],
            fg=self.colores['texto_principal'], wrap=tk.WORD, relief=tk.FLAT, bd=0
        )
        self.text_analysis.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.text_analysis.insert(tk.END, "Bienvenido al Simulador de Dados.\n\n"
                                           "Configure los parámetros y presione 'SIMULAR'.")
        self.text_analysis.config(state=tk.DISABLED)

    def iniciar_simulacion(self):
        """Validar entradas e iniciar la simulación en un hilo separado."""
        if self.simulacion_activa:
            return
        try:
            lanzamientos = int(self.entry_lanzamientos.get())
            if lanzamientos <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Número de lanzamientos inválido.")
            return

        num_dados = int(self.combo_dados.get())
        self.simulacion_activa = True
        self.btn_simular.config(state='disabled', text="PROCESANDO...")
        self.status_var.set(f"Simulando {lanzamientos:,} lanzamientos...")
        
        thread = threading.Thread(target=self.ejecutar_simulacion, args=(lanzamientos, num_dados))
        thread.daemon = True
        thread.start()

    def ejecutar_simulacion(self, lanzamientos, num_dados):
        """Lógica de la simulación que se ejecuta en el hilo."""
        self.simulator.simular_dados_vectorizado(lanzamientos, num_dados)
        self.root.after(0, self.finalizar_simulacion)

    def finalizar_simulacion(self):
        """Actualizar la GUI cuando la simulación termina."""
        self.graph_manager.update_graphs(self.simulator)
        self.actualizar_analisis()
        self.simulacion_activa = False
        self.btn_simular.config(state='normal', text="SIMULAR")
        self.status_var.set("Simulación completada.")
        self.notebook.select(0) # Cambiar a la pestaña de gráficos

    def actualizar_analisis(self):
        """Actualizar el widget de texto con los resultados del análisis."""
        self.text_analysis.config(state=tk.NORMAL)
        self.text_analysis.delete(1.0, tk.END)
        texto = f"ANÁLISIS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        texto += "═" * 80 + "\n\n"
        texto += self.simulator.analizar_un_dado()
        texto += self.simulator.analizar_dos_dados()
        texto += self.simulator.analizar_tres_dados()
        self.text_analysis.insert(tk.END, texto)
        self.text_analysis.config(state=tk.DISABLED)

    def limpiar_todo(self):
        """Limpiar todos los resultados y gráficos."""
        if messagebox.askyesno("Confirmar", "¿Limpiar todos los resultados?"):
            self.simulator.limpiar_resultados()
            self.graph_manager.clear_all_graphs()
            self.text_analysis.config(state=tk.NORMAL)
            self.text_analysis.delete(1.0, tk.END)
            self.text_analysis.insert(tk.END, "Resultados limpiados. Listo para nueva simulación.")
            self.text_analysis.config(state=tk.DISABLED)
            self.status_var.set("Listo para simular.")