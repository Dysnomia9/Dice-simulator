import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import time
from datetime import datetime
import json
from dice_simulator import DiceSimulator
from graph_manager import GraphManager

class SimuladorDados:
    def __init__(self, root):
        self.root = root
        self.simulator = DiceSimulator()
        self.setup_window()
        self.setup_colors()
        self.create_widgets()
        self.simulacion_activa = False
        self.configuraciones_guardadas = {}
        
    def setup_window(self):
        """Configurar ventana principal"""
        self.root.title(" Simulador de Dados Avanzado - Análisis Probabilístico")
        self.root.geometry("1300x850")
        self.root.minsize(1300, 850)
        
        # Icono de la aplicación (si existe)
        try:
            self.root.iconbitmap("dice_icon.ico")
        except:
            pass
        
        # Centrar ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configurar protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """Manejar el cierre de la aplicación"""
        if self.simulacion_activa:
            if messagebox.askokcancel("Simulación en progreso", 
                                    "Hay una simulación en progreso. ¿Estás seguro de que quieres cerrar la aplicación?"):
                self.root.destroy()
        else:
            if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
                self.root.destroy()
        
    def setup_colors(self):
        """Definir esquema de colores mejorado"""
        self.colores = {
            'bg_principal': '#ECF0F1',
            'bg_frame': '#FFFFFF',
            'bg_boton': '#3498DB',
            'bg_boton_hover': '#2980B9',
            'bg_boton_peligro': '#E74C3C',
            'bg_boton_exito': '#27AE60',
            'bg_boton_info': '#F39C12',
            'texto_principal': '#2C3E50',
            'texto_secundario': '#7F8C8D',
            'acento': '#27AE60',
            'borde': '#BDC3C7',
            'warning': '#F39C12',
            'success': '#27AE60',
            'error': '#E74C3C'
        }
        
        self.root.configure(bg=self.colores['bg_principal'])
           
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colores['bg_principal'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título principal
        title_frame = tk.Frame(main_frame, bg=self.colores['bg_principal'])
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(title_frame, 
                              text="🎲 SIMULADOR DE DADOS - ANÁLISIS PROBABILÍSTICO",
                              font=('Arial', 18, 'bold'),
                              bg=self.colores['bg_principal'],
                              fg=self.colores['texto_principal'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Explora las probabilidades teóricas vs experimentales",
                                 font=('Arial', 11),
                                 bg=self.colores['bg_principal'],
                                 fg=self.colores['texto_secundario'])
        subtitle_label.pack()
        
        # Frame de controles
        self.create_control_frame(main_frame)
        
        # Notebook para las pestañas
        self.create_notebook(main_frame)
        
    def create_control_frame(self, parent):
        """Frame de controles de simulación"""
        control_frame = tk.LabelFrame(parent, 
                                     text=" 🎯 Controles de Simulación ",
                                     font=('Arial', 12, 'bold'),
                                     bg=self.colores['bg_frame'],
                                     fg=self.colores['texto_principal'],
                                     relief=tk.RIDGE,
                                     bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Frame interno para organizar controles
        inner_frame = tk.Frame(control_frame, bg=self.colores['bg_frame'])
        inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Frame izquierdo - Configuración
        left_frame = tk.Frame(inner_frame, bg=self.colores['bg_frame'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Número de lanzamientos
        tk.Label(left_frame, text="Número de lanzamientos:",
                font=('Arial', 10, 'bold'),
                bg=self.colores['bg_frame'],
                fg=self.colores['texto_principal']).grid(row=0, column=0, sticky='w', pady=2)
        
        self.entry_lanzamientos = tk.Entry(left_frame, font=('Arial', 10), width=15)
        self.entry_lanzamientos.insert(0, "10000")
        self.entry_lanzamientos.grid(row=0, column=1, padx=(5, 0), pady=2)
        
        # Número de dados
        tk.Label(left_frame, text="Número de dados:",
                font=('Arial', 10, 'bold'),
                bg=self.colores['bg_frame'],
                fg=self.colores['texto_principal']).grid(row=1, column=0, sticky='w', pady=2)
        
        self.combo_dados = ttk.Combobox(left_frame, values=[1, 2, 3], state='readonly', width=12)
        self.combo_dados.set(3)
        self.combo_dados.grid(row=1, column=1, padx=(5, 0), pady=2)
        
        # Frame derecho - Botones
        right_frame = tk.Frame(inner_frame, bg=self.colores['bg_frame'])
        right_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Botón simular
        self.btn_simular = tk.Button(right_frame, 
                                    text="🎲 SIMULAR",
                                    font=('Arial', 11, 'bold'),
                                    bg=self.colores['bg_boton'],
                                    fg='white',
                                    relief=tk.RAISED,
                                    bd=3,
                                    padx=20,
                                    pady=8,
                                    command=self.iniciar_simulacion)
        self.btn_simular.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón limpiar
        self.btn_limpiar = tk.Button(right_frame,
                                    text="🗑️ LIMPIAR",
                                    font=('Arial', 11, 'bold'),
                                    bg=self.colores['bg_boton_peligro'],
                                    fg='white',
                                    relief=tk.RAISED,
                                    bd=3,
                                    padx=20,
                                    pady=8,
                                    command=self.limpiar_todo)
        self.btn_limpiar.pack(side=tk.LEFT)
        
        # Barra de progreso
        self.progress_frame = tk.Frame(control_frame, bg=self.colores['bg_frame'])
        self.progress_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.progress_var = tk.StringVar()
        self.progress_label = tk.Label(self.progress_frame,
                                      textvariable=self.progress_var,
                                      font=('Arial', 9),
                                      bg=self.colores['bg_frame'],
                                      fg=self.colores['texto_secundario'])
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, 
                                           mode='indeterminate',
                                           length=400)
        self.progress_bar.pack(pady=5)
        
    def create_notebook(self, parent):
        """Crear notebook con pestañas"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de Gráficos
        self.graph_frame = tk.Frame(self.notebook, bg=self.colores['bg_frame'])
        self.notebook.add(self.graph_frame, text=" Gráficos Visuales")
        
        # Pestaña de Análisis
        self.analysis_frame = tk.Frame(self.notebook, bg=self.colores['bg_frame'])
        self.notebook.add(self.analysis_frame, text=" Análisis Detallado")
        
        # Inicializar gráficos
        self.graph_manager = GraphManager(self.graph_frame, self.colores)
        
        # Crear área de texto para análisis
        self.create_analysis_area()
        
    def create_analysis_area(self):
        """Crear área de análisis de texto"""
        # Título del análisis
        title_label = tk.Label(self.analysis_frame,
                              text=" ANÁLISIS ESTADÍSTICO DETALLADO",
                              font=('Arial', 14, 'bold'),
                              bg=self.colores['bg_frame'],
                              fg=self.colores['texto_principal'])
        title_label.pack(pady=10)
        
        # Área de texto con scroll
        self.text_analysis = scrolledtext.ScrolledText(
            self.analysis_frame,
            font=('Consolas', 10),
            bg='#FAFAFA',
            fg=self.colores['texto_principal'],
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            bd=2
        )
        self.text_analysis.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Mensaje inicial
        mensaje_inicial = """
 SIMULADOR DE DADOS - ANÁLISIS PROBABILÍSTICO
═══════════════════════════════════════════════

¡Bienvenido al simulador de dados!

Este simulador te permite:
• Analizar probabilidades con 1, 2 o 3 dados
• Comparar resultados experimentales vs teóricos  
• Visualizar distribuciones mediante gráficos
• Estudiar la Ley de los Grandes Números

 INSTRUCCIONES:
1. Selecciona el número de lanzamientos
2. Elige cuántos dados simular (1, 2 o 3)
3. Haz clic en "SIMULAR" para ejecutar
4. Revisa los gráficos y análisis detallado

 CONCEPTOS CLAVE:
• Con más lanzamientos, los resultados experimentales se acercan a los teóricos
• La probabilidad de sacar 6 en un dado es 1/6 ≈ 0.1667
• Para múltiples dados, analizamos cuántos 6 aparecen por lanzamiento

¡Comienza tu simulación para ver estos conceptos en acción!
        """
        
        self.text_analysis.insert(tk.END, mensaje_inicial)
        self.text_analysis.config(state=tk.DISABLED)
        
    def iniciar_simulacion(self):
        """Iniciar simulación en hilo separado"""
        if self.simulacion_activa:
            return
            
        try:
            lanzamientos = int(self.entry_lanzamientos.get())
            if lanzamientos <= 0:
                raise ValueError("El número debe ser positivo")
            if lanzamientos > 1000000:
                if not messagebox.askyesno("Confirmación", 
                                         f"¿Estás seguro de simular {lanzamientos:,} lanzamientos?\n"
                                         "Esto podría tomar un tiempo considerable."):
                    return
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido de lanzamientos")
            return
            
        num_dados = int(self.combo_dados.get())
        
        # Deshabilitar botón y mostrar progreso
        self.simulacion_activa = True
        self.btn_simular.config(state='disabled')
        self.progress_bar.start()
        self.progress_var.set(f"Simulando {lanzamientos:,} lanzamientos con {num_dados} dado(s)...")
        
        # Ejecutar simulación en hilo separado
        thread = threading.Thread(target=self.ejecutar_simulacion, 
                                args=(lanzamientos, num_dados))
        thread.daemon = True
        thread.start()
        
    def ejecutar_simulacion(self, lanzamientos, num_dados):
        """Ejecutar simulación en hilo separado"""
        try:
            start_time = time.time()
            
            # Realizar simulación
            self.simulator.simular_dados(lanzamientos, num_dados)
            
            end_time = time.time()
            tiempo_transcurrido = end_time - start_time
            
            # Actualizar interfaz en hilo principal
            self.root.after(0, self.finalizar_simulacion, tiempo_transcurrido)
            
        except Exception as e:
            self.root.after(0, self.error_simulacion, str(e))
            
    def finalizar_simulacion(self, tiempo_transcurrido):
        """Finalizar simulación y actualizar interfaz"""
        self.simulacion_activa = False
        self.btn_simular.config(state='normal')
        self.progress_bar.stop()
        self.progress_var.set(f"Simulación completada en {tiempo_transcurrido:.2f} segundos")
        
        # Actualizar gráficos
        self.graph_manager.update_graphs(self.simulator)
        
        # Actualizar análisis
        self.actualizar_analisis()
        
        # Mensaje de éxito
        messagebox.showinfo("Éxito", 
                           f"Simulación completada exitosamente!\n"
                           f"Tiempo: {tiempo_transcurrido:.2f} segundos")
        
    def error_simulacion(self, error_msg):
        """Manejar errores en la simulación"""
        self.simulacion_activa = False
        self.btn_simular.config(state='normal')
        self.progress_bar.stop()
        self.progress_var.set("Error en la simulación")
        messagebox.showerror("Error", f"Error durante la simulación:\n{error_msg}")
        
    def actualizar_analisis(self):
        """Actualizar el análisis de texto"""
        self.text_analysis.config(state=tk.NORMAL)
        self.text_analysis.delete(1.0, tk.END)
        
        # Encabezado
        texto = "🎲 ANÁLISIS ESTADÍSTICO DETALLADO\n"
        texto += "═" * 80 + "\n\n"
        
        # Análisis por tipo de dados
        texto += self.simulator.analizar_un_dado()
        texto += self.simulator.analizar_dos_dados()
        texto += self.simulator.analizar_tres_dados()
        
        # Resumen general
        if any([self.simulator.resultados_1_dado, 
                self.simulator.resultados_2_dados, 
                self.simulator.resultados_3_dados]):
            texto += " RESUMEN GENERAL\n"
            texto += "─" * 60 + "\n"
            
            total_lanzamientos = sum(self.simulator.total_lanzamientos.values())
            texto += f"Total de lanzamientos realizados: {total_lanzamientos:,}\n"
            
            for tipo, total in self.simulator.total_lanzamientos.items():
                if total > 0:
                    tipo_texto = {"1": "1 dado", "2": "2 dados", "3": "3 dados"}[tipo]
                    texto += f"• {tipo_texto}: {total:,} lanzamientos\n"
            
        self.text_analysis.insert(tk.END, texto)
        self.text_analysis.config(state=tk.DISABLED)
        
    def limpiar_todo(self):
        """Limpiar todos los resultados"""
        if messagebox.askyesno("Confirmación", "¿Estás seguro de limpiar todos los datos?"):
            self.simulator.limpiar_resultados()
            self.graph_manager.clear_all_graphs()
            
            # Restaurar texto inicial
            self.text_analysis.config(state=tk.NORMAL)
            self.text_analysis.delete(1.0, tk.END)
            
            mensaje_inicial = """
 DATOS LIMPIADOS EXITOSAMENTE
═══════════════════════════════

Todos los resultados han sido eliminados.
¡Listo para una nueva simulación!

Configura los parámetros y haz clic en "SIMULAR" para comenzar.
            """
            
            self.text_analysis.insert(tk.END, mensaje_inicial)
            self.text_analysis.config(state=tk.DISABLED)
            
            self.progress_var.set("Datos limpiados - Listo para nueva simulación")
            
            messagebox.showinfo("Éxito", "Todos los datos han sido limpiados exitosamente")