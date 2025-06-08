import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import Counter

from dice_simulator import DiceSimulator


class GraphManager:
    def __init__(self, parent_frame, colores):
        self.parent_frame = parent_frame
        self.colores = colores
        self.setup_matplotlib()
        self.create_graphs()

    def setup_matplotlib(self):
        """Configurar matplotlib con tema personalizado."""
        plt.style.use('default')
        plt.rcParams['figure.facecolor'] = '#ECF0F1'
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['text.color'] = '#2C3E50'
        plt.rcParams['axes.labelcolor'] = '#2C3E50'
        plt.rcParams['axes.edgecolor'] = '#2C3E50'
        plt.rcParams['xtick.color'] = '#2C3E50'
        plt.rcParams['ytick.color'] = '#2C3E50'
        plt.rcParams['font.size'] = 9

    def create_graphs(self):
        """Crear la figura y canvas para los gráficos."""
        # Frame contenedor principal
        self.container_frame = tk.Frame(self.parent_frame, bg=self.colores['bg_frame'])

        self.container_frame.grid(row=0, column=0, sticky='nsew')

        # Configurar el grid del frame contenedor para que se expanda
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)

        # Crear la figura de Matplotlib
        self.fig = Figure(figsize=(10, 7), dpi=80, facecolor='#ECF0F1')
        self.axes = self.fig.subplots(2, 2, gridspec_kw={
            'hspace': 0.4, 'wspace': 0.3, 'left': 0.08,
            'right': 0.95, 'top': 0.88, 'bottom': 0.12
        })
        self.fig.suptitle('Análisis Visual Completo de Resultados',
                         fontsize=14, fontweight='bold', color='#2C3E50')

        # Crear el canvas de Tkinter para Matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, self.container_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky='nsew')
        self.canvas_widget.configure(highlightthickness=0, bd=0)

        # Binds para redimensionamiento (sin cambios)
        self.parent_frame.bind('<Configure>', self.on_parent_configure)
        self.last_size = (0, 0)
        self.resize_job = None
        self.parent_frame.after(100, self.force_initial_resize)
        self.clear_all_graphs()

    def force_initial_resize(self):
        """Forzar redimensionamiento inicial."""
        try:
            self.parent_frame.update_idletasks()
            parent_width = self.parent_frame.winfo_width()
            parent_height = self.parent_frame.winfo_height()
            if parent_width > 1 and parent_height > 1:
                self.resize_figure(parent_width, parent_height)
        except:
            pass

    def on_parent_configure(self, event):
        """Manejar cambios en el frame padre."""
        width, height = event.width, event.height
        if width > 1 and height > 1:
            if self.resize_job:
                self.parent_frame.after_cancel(self.resize_job)
            self.resize_job = self.parent_frame.after(50, lambda: self.resize_figure(width, height))

    def resize_figure(self, width, height):
        """Redimensionar la figura según el tamaño del contenedor."""
        if abs(width - self.last_size[0]) < 10 and abs(height - self.last_size[1]) < 10:
            return
        self.last_size = (width, height)
        dpi = self.fig.dpi
        width_inch = max(6, (width - 10) / dpi)
        height_inch = max(4, (height - 10) / dpi)
        self.fig.set_size_inches(width_inch, height_inch, forward=True)
        self.canvas.draw_idle()

    def clear_all_graphs(self):
        """Limpiar todos los gráficos."""
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor('#FFFFFF')
            ax.grid(True, alpha=0.3, linestyle='--')
        self.canvas.draw()
        
    def update_graphs(self, simulator):
        self.clear_all_graphs()
        try:
            self.plot_single_die(simulator)
            self.plot_two_dice(simulator)
            self.plot_three_dice(simulator)
            self.plot_comparison(simulator)
            self.canvas.draw()
        except Exception as e:
            print(f"Error actualizando gráficos: {e}")

    def plot_single_die(self, simulator):
        ax = self.axes[0,0]
        if not simulator.resultados_1_dado:
            ax.text(0.5, 0.5, 'Sin datos para 1 dado', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('1 Dado - Sin datos')
            return
        contador = Counter(simulator.resultados_1_dado)
        valores = list(range(1, 7))
        frecuencias = [contador.get(i, 0) for i in valores]
        ax.bar(valores, frecuencias, color='#3498DB')
        ax.set_title(f'1 Dado - Distribución ({len(simulator.resultados_1_dado):,} lanzamientos)')
        ax.set_xlabel('Resultado')
        ax.set_ylabel('Frecuencia')
        ax.set_xticks(valores)

    def plot_two_dice(self, simulator):
        ax = self.axes[0,1]
        if not simulator.resultados_2_dados:
            ax.text(0.5, 0.5, 'Sin datos para 2 dados', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('2 Dados - Sin datos')
            return
        contador = Counter(simulator.resultados_2_dados)
        valores = list(range(3))
        frecuencias = [contador.get(i, 0) for i in valores]
        etiquetas = ['0 seises', '1 seis', '2 seises']
        ax.bar(etiquetas, frecuencias, color='#27AE60')
        ax.set_title(f'2 Dados - Número de 6s ({len(simulator.resultados_2_dados):,} lanzamientos)')
        ax.set_xlabel('Número de 6s')
        ax.set_ylabel('Frecuencia')

    def plot_three_dice(self, simulator):
        ax = self.axes[1,0]
        if not simulator.resultados_3_dados:
            ax.text(0.5, 0.5, 'Sin datos para 3 dados', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('3 Dados - Sin datos')
            return
        contador = Counter(simulator.resultados_3_dados)
        valores = list(range(4))
        frecuencias = [contador.get(i, 0) for i in valores]
        etiquetas = ['0 seises', '1 seis', '2 seises', '3 seises']
        ax.bar(etiquetas, frecuencias, color='#E74C3C')
        ax.set_title(f'3 Dados - Número de 6s ({len(simulator.resultados_3_dados):,} lanzamientos)')
        ax.set_xlabel('Número de 6s')
        ax.set_ylabel('Frecuencia')

    def plot_comparison(self, simulator):
        ax = self.axes[1,1]
        if simulator.resultados_3_dados:
            self._plot_dice_comparison(ax, 3, simulator)
        elif simulator.resultados_2_dados:
            self._plot_dice_comparison(ax, 2, simulator)
        elif simulator.resultados_1_dado:
            self._plot_dice_comparison(ax, 1, simulator)
        else:
            ax.text(0.5, 0.5, 'Sin datos para comparación', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Comparación - Sin datos')

    def _plot_dice_comparison(self, ax, num_dados, simulator):
        if num_dados == 1:
            resultados = simulator.resultados_1_dado
            total = len(resultados)
            prob_teoricas = simulator.calcular_probabilidades_teoricas(1)
            valores = list(range(1, 7))
            categorias = [f'Cara {i}' for i in valores]
            prob_exp = [Counter(resultados).get(i, 0) / total for i in valores]
            prob_teo = [prob_teoricas[f"sacar_{i}"] for i in valores]
        else:
            resultados = getattr(simulator, f'resultados_{num_dados}_dados')
            total = len(resultados)
            prob_teoricas = simulator.calcular_probabilidades_teoricas(num_dados)
            categorias = [f'{i} seises' for i in range(num_dados + 1)]
            prob_exp = [Counter(resultados).get(i, 0) / total for i in range(num_dados + 1)]
            prob_teo = [prob_teoricas[f"{i}_seises"] for i in range(num_dados + 1)]
        
        x = range(len(categorias))
        width = 0.35
        ax.bar([i - width/2 for i in x], prob_exp, width, label='Experimental', color='#F39C12')
        ax.bar([i + width/2 for i in x], prob_teo, width, label='Teórica', color='#9B59B6')
        ax.set_title(f'{num_dados} Dado(s) - Teórica vs. Experimental')
        ax.set_ylabel('Probabilidad')
        ax.set_xticks(x)
        ax.set_xticklabels(categorias, rotation=15, ha="right")
        ax.legend()


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
        # self.root.state('zoomed') # This line is causing the error. Comment it out.
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
        
        # ---> CORRECCIÓN CLAVE <---
        # Configurar el grid del 'graph_frame' para que el contenido (el canvas)
        # pueda expandirse correctamente.
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        # Pestaña de Análisis
        self.analysis_frame = tk.Frame(self.notebook, bg=self.colores['bg_secundario'])
        self.notebook.add(self.analysis_frame, text="ANÁLISIS DETALLADO")
        
        # Inicializar el gestor de gráficos
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