import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime
from collections import Counter
import numpy as np

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
        self.colores = {
            'bg_principal': '#23272e',     
            'bg_secundario': "#24363D",     
            'bg_frame': "#ffffff",          
            'bg_card': "#79bcff",           
            'bg_accent': '#4f8cff',        
            'bg_boton_primary': '#4f8cff',  
            'bg_boton_hover': '#357ae8',    
            'bg_boton_danger': '#e74c3c',  
            'bg_boton_success': '#27ae60',  
            'bg_boton_warning': '#f1c40f', 
            'texto_principal': '#23272e',   
            'texto_secundario': '#4f5b6e',
            'texto_accent': "#5588e7"   
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

        style.configure('Accent.TButton',
            font=('Segoe UI', 11, 'bold'),
            background=self.colores['bg_boton_primary'],
            foreground=self.colores['texto_principal'],
            borderwidth=0,
            focusthickness=3,
            focuscolor=self.colores['bg_boton_hover'],
            padding=10
        )
        style.map('Accent.TButton',
            background=[('active', self.colores['bg_boton_hover']), ('pressed', self.colores['bg_boton_success'])]
        )

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


        controls_frame = tk.Frame(input_container, bg=self.colores['bg_frame'])
        controls_frame.pack(pady=0)
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)

        tk.Label(controls_frame, text="Número de lanzamientos:", font=('Segoe UI', 9, 'bold'),
                 bg=self.colores['bg_frame'], fg=self.colores['texto_principal']).grid(row=0, column=0, sticky='e', padx=5, pady=3)
        self.entry_lanzamientos = tk.Entry(controls_frame, font=('Segoe UI', 10), width=15,
                                           bg="#ffffff", fg=self.colores['texto_principal'],
                                           insertbackground=self.colores['texto_principal'])
        self.entry_lanzamientos.insert(0, "10000")
        self.entry_lanzamientos.grid(row=0, column=1, sticky='w', padx=5, pady=3)

        tk.Label(controls_frame, text="Número de dados:", font=('Segoe UI', 9, 'bold'),
                 bg=self.colores['bg_frame'], fg=self.colores['texto_principal']).grid(row=1, column=0, sticky='e', padx=5, pady=3)
        self.combo_dados = ttk.Combobox(controls_frame, values=[1, 2, 3], state='readonly', width=12)
        self.combo_dados.set(3)
        self.combo_dados.grid(row=1, column=1, sticky='w', padx=5, pady=3)

        # Contenido del panel derecho (Acciones)
        tk.Label(right_panel, text="ACCIONES", font=('Segoe UI', 10, 'bold'),
                 bg=self.colores['bg_frame'], fg=self.colores['texto_principal']).pack(pady=8)
        button_container = tk.Frame(right_panel, bg=self.colores['bg_frame'])
        button_container.pack(padx=15, pady=(0, 15))
        self.btn_simular = ttk.Button(button_container, text="SIMULAR", style='Accent.TButton', command=self.iniciar_simulacion)
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
        """Crear el notebook con pestañas para gráficos, análisis y tablas."""
        notebook_container = tk.Frame(parent, bg=self.colores['bg_principal'])
        notebook_container.grid(row=2, column=0, sticky='nsew')
        notebook_container.grid_rowconfigure(0, weight=1)
        notebook_container.grid_columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(notebook_container, style='Custom.TNotebook')
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # Frame con scroll para los gráficos
        self.graph_outer = tk.Frame(self.notebook, bg=self.colores['bg_principal'])
        self.graph_outer.grid(row=0, column=0, sticky='nsew')
        self.graph_outer.grid_rowconfigure(0, weight=1)
        self.graph_outer.grid_columnconfigure(0, weight=1)

        # Canvas con scrollbar
        self.graph_canvas = tk.Canvas(self.graph_outer, bg=self.colores['bg_principal'], 
                                    highlightthickness=0)
        self.graph_canvas.grid(row=0, column=0, sticky='nsew')

        # Scrollbar vertical
        v_scroll = tk.Scrollbar(self.graph_outer, orient='vertical', 
                             command=self.graph_canvas.yview)
        v_scroll.grid(row=0, column=1, sticky='ns')
        
        # Configurar el canvas para usar el scrollbar
        self.graph_canvas.configure(yscrollcommand=v_scroll.set)

        # Frame real donde van los gráficos
        self.graph_frame = tk.Frame(self.graph_canvas, bg=self.colores['bg_secundario'])
        self.graph_frame.grid(row=0, column=0, sticky='nsew')

        # Crear ventana dentro del canvas
        self.graph_window_id = self.graph_canvas.create_window(
            (0, 0), 
            window=self.graph_frame, 
            anchor='nw'
        )

        # Configurar eventos para el canvas de gráficos
        self._setup_graph_scroll_events()

        # Añadir pestañas al notebook
        self.notebook.add(self.graph_outer, text="RESULTADOS GRÁFICOS")


        # Pestaña de Análisis
        self.analysis_frame = tk.Frame(self.notebook, bg=self.colores['bg_secundario'])
        self.notebook.add(self.analysis_frame, text="ANÁLISIS DETALLADO")
        
        # Nueva pestaña de Tablas
        self.tables_frame = tk.Frame(self.notebook, bg=self.colores['bg_secundario'])
        self.notebook.add(self.tables_frame, text="TABLAS DE FRECUENCIA")
        
        # Inicializar componentes
        self.graph_manager = GraphManager(self.graph_frame, self.colores)
        self.create_analysis_area()
        self.create_frequency_tables()

    def _limit_graph_width(self, event):
        """Ajusta el ancho del frame interno al del canvas."""
        if hasattr(self, 'graph_window_id'):
            width = event.width
            if width > 1: 
                self.graph_canvas.itemconfig(self.graph_window_id, width=width)

                self.graph_canvas.configure(scrollregion=self.graph_canvas.bbox("all"))

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
        self.actualizar_tablas_mejoradas()  # Nueva llamada
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
            
            # Limpiar tablas
            if hasattr(self, 'tables'):
                for tree in self.tables.values():
                    for item in tree.get_children():
                        tree.delete(item)
                        
            self.status_var.set("Listo para simular.")


    def _setup_graph_scroll_events(self):
        """Configurar eventos de scroll para el canvas de gráficos."""
        def _on_frame_configure(event):
            """Actualizar scrollregion cuando cambia el tamaño del frame interno."""
            bbox = self.graph_frame.bbox("all")
            min_height = max(self.graph_canvas.winfo_height(), self.graph_frame.winfo_reqheight())
            self.graph_canvas.configure(
                scrollregion=(
                    bbox[0], bbox[1], bbox[2], max(bbox[3], min_height * 2)
                )
            )
            canvas_width = self.graph_canvas.winfo_width()
            if canvas_width > 1:
                self.graph_canvas.itemconfig(
                    self.graph_window_id,
                    width=canvas_width,
                    height=max(bbox[3], min_height * 2)
                )

        def _on_canvas_configure(event):
            """Ajustar el tamaño de la ventana interna cuando cambia el tamaño del canvas."""
            width = event.width
            height = event.height
            if width > 1 and height > 1:
                content_height = max(height * 2, self.graph_frame.winfo_reqheight())
                self.graph_canvas.itemconfig(
                    self.graph_window_id,
                    width=width,
                    height=content_height
                )
                self.graph_canvas.configure(scrollregion=(0, 0, width, content_height))

        def _on_mousewheel(event):
            """Manejar el evento de scroll del mouse."""
            self.graph_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Vincular eventos
        self.graph_frame.bind("<Configure>", _on_frame_configure)
        self.graph_canvas.bind('<Configure>', _on_canvas_configure)
        self.graph_canvas.bind('<Enter>', 
                              lambda e: self.graph_canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.graph_canvas.bind('<Leave>', 
                              lambda e: self.graph_canvas.unbind_all("<MouseWheel>"))

    def create_frequency_tables(self):
        """Crear tablas de frecuencias con análisis estadístico y scroll."""
        # Frame contenedor principal (ya existe como self.tables_frame)
        for widget in self.tables_frame.winfo_children():
            widget.destroy()  # Limpia si ya existe

        # Canvas y Scrollbar para las tablas
        canvas_frame = tk.Frame(self.tables_frame, bg=self.colores['bg_principal'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tables_canvas = tk.Canvas(canvas_frame, bg=self.colores['bg_principal'], highlightthickness=0)
        self.tables_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tables_v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.tables_canvas.yview)
        self.tables_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tables_canvas.configure(yscrollcommand=self.tables_v_scrollbar.set)

        # Frame interno scrollable
        self.tables_scrollable_frame = tk.Frame(self.tables_canvas, bg=self.colores['bg_principal'])
        self.tables_canvas.create_window((0, 0), window=self.tables_scrollable_frame, anchor="nw")

        # Ajustar el scrollregion cuando cambie el tamaño del frame interno
        def on_frame_configure(event):
            self.tables_canvas.configure(scrollregion=self.tables_canvas.bbox("all"))
        self.tables_scrollable_frame.bind("<Configure>", on_frame_configure)

        # Diccionario para almacenar las tablas
        self.tables = {}

        # Crear las diferentes tablas
        self.tables['resumen'] = self._create_table_section(
            "RESUMEN GENERAL",
            ["Parámetro", "Valor", "Descripción"],
            height=6,
            parent=self.tables_scrollable_frame
        )
        self.tables['distribucion'] = self._create_table_section(
            "DISTRIBUCIÓN DE SEISES",
            ["Seises", "Frecuencia", "Porcentaje", "Prob. Exp.", "Prob. Teórica"],
            height=7,
            parent=self.tables_scrollable_frame
        )
        self.tables['frecuencias'] = self._create_table_section(
            "FRECUENCIAS POR CARA",
            ["Cara", "Frecuencia", "Porcentaje", "Esperado", "Diferencia"],
            height=7,
            parent=self.tables_scrollable_frame
        )

        # Configurar eventos de scroll
        self._setup_tables_scroll_events()

    def _create_table_section(self, title, columns, height=6, parent=None):
        """Crear una sección de tabla con título."""
        if parent is None:
            parent = self.tables_frame
        frame = tk.Frame(parent, bg=self.colores['bg_secundario'])
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Título de la sección
        tk.Label(frame, 
                 text=title,
                 font=('Segoe UI', 12, 'bold'),
                 bg=self.colores['bg_secundario'],
                 fg='white').pack(pady=5)
        
        # Crear y configurar tabla
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=height, style="Custom.Treeview")
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, minwidth=100, width=150)
        
        tree.pack(fill=tk.X, padx=5, pady=5)
        return tree

    def _setup_tables_scroll_events(self):
        """Configurar eventos de scroll para las tablas."""
        def _on_mousewheel(event):
            self.tables_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.tables_canvas.bind('<Enter>', lambda e: self.tables_canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.tables_canvas.bind('<Leave>', lambda e: self.tables_canvas.unbind_all("<MouseWheel>"))
        self.tables_canvas.bind('<Enter>', lambda e: self.tables_canvas.bind_all("<Shift-MouseWheel>", _on_mousewheel))
        self.tables_canvas.bind('<Leave>', lambda e: self.tables_canvas.unbind_all("<Shift-MouseWheel>"))

    def actualizar_tablas_mejoradas(self):
        """Actualizar todas las tablas con los resultados actuales."""
        if not hasattr(self, 'tables'):
            return

        num_dados = int(self.combo_dados.get())
        resultados = getattr(self.simulator, f'resultados_{num_dados}_dado' + ('s' if num_dados > 1 else ''), [])

        if not resultados:
            return

        # Limpiar tablas existentes
        for tree in self.tables.values():
            for item in tree.get_children():
                tree.delete(item)

        # Actualizar tabla de resumen
        total = len(resultados)
        if num_dados == 1:
            media = sum(resultados) / total if total > 0 else 0
            self.tables['resumen'].insert('', tk.END, values=(
                "Total lanzamientos", f"{total:,}", "Número de experimentos"
            ))
            self.tables['resumen'].insert('', tk.END, values=(
                "Media de caras", f"{media:.4f}", "Promedio de la cara obtenida"
            ))

            # Tabla de distribución: SOLO 0 o 1 seis
            seises = sum(1 for x in resultados if x == 6)
            no_seises = total - seises
            prob_teoricas = self.simulator.calcular_probabilidades_teoricas(1)
            # 0 seises
            self.tables['distribucion'].insert('', tk.END, values=(
                "0",
                f"{no_seises:,}",
                f"{(no_seises / total * 100):.2f}%",
                f"{no_seises / total:.4f}",
                f"{5/6:.4f}"
            ))
            # 1 seis
            self.tables['distribucion'].insert('', tk.END, values=(
                "1",
                f"{seises:,}",
                f"{(seises / total * 100):.2f}%",
                f"{seises / total:.4f}",
                f"{1/6:.4f}"
            ))

            # Tabla de frecuencias: frecuencia de cada cara
            contador = Counter(resultados)
            esperado = total / 6 if total > 0 else 0
            for cara in range(1, 7):
                freq = contador.get(cara, 0)
                porcentaje = (freq / total * 100) if total > 0 else 0
                diferencia = freq - esperado
                self.tables['frecuencias'].insert('', tk.END, values=(
                    str(cara),
                    f"{freq:,}",
                    f"{porcentaje:.2f}%",
                    f"{esperado:.1f}",
                    f"{diferencia:+.1f}"
                ))
        else:
            media = sum(resultados) / total if total > 0 else 0
            self.tables['resumen'].insert('', tk.END, values=(
                "Total lanzamientos", f"{total:,}", "Número de experimentos"
            ))
            self.tables['resumen'].insert('', tk.END, values=(
                "Media de seises", f"{media:.4f}", "Promedio por lanzamiento"
            ))

            # Actualizar tabla de distribución
            contador = Counter(resultados)
            prob_teoricas = self.simulator.calcular_probabilidades_teoricas(num_dados)
            for i in range(num_dados + 1):
                freq = contador.get(i, 0)
                porcentaje = (freq / total * 100) if total > 0 else 0
                prob_exp = freq / total if total > 0 else 0
                prob_teo = prob_teoricas.get(f"{i}_seises", 0)
                self.tables['distribucion'].insert('', tk.END, values=(
                    str(i),
                    f"{freq:,}",
                    f"{porcentaje:.2f}%",
                    f"{prob_exp:.4f}",
                    f"{prob_teo:.4f}"
                ))

            if hasattr(self.simulator, 'resultados_detallados'):
                detalles = self.simulator.resultados_detallados.get(str(num_dados), [])
                caras_contador = Counter()
                for detalle in detalles:
                    if isinstance(detalle, dict) and 'dados' in detalle:
                        if isinstance(detalle['dados'], list):
                            for cara in detalle['dados']:
                                caras_contador[cara] += 1
                        else:
                            caras_contador[detalle['dados']] += 1
                    else:
                        caras_contador[detalle] += 1

                total_caras = sum(caras_contador.values())
                esperado = total_caras / 6 if total_caras > 0 else 0

                for cara in range(1, 7):
                    freq = caras_contador.get(cara, 0)
                    porcentaje = (freq / total_caras * 100) if total_caras > 0 else 0
                    diferencia = freq - esperado

                    self.tables['frecuencias'].insert('', tk.END, values=(
                        str(cara),
                        f"{freq:,}",
                        f"{porcentaje:.2f}%",
                        f"{esperado:.1f}",
                        f"{diferencia:+.1f}"
                    ))