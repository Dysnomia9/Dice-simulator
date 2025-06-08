import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from collections import Counter

class GraphManager:
    def __init__(self, parent_frame, colores):
        self.parent_frame = parent_frame
        self.colores = colores
        self.setup_matplotlib()
        self.create_graphs()
    
    def setup_matplotlib(self):
        """Configurar matplotlib con tema personalizado"""
        plt.style.use('default')
        # Configurar colores globales para matplotlib
        plt.rcParams['figure.facecolor'] = '#ECF0F1'
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['text.color'] = '#2C3E50'
        plt.rcParams['axes.labelcolor'] = '#2C3E50'
        plt.rcParams['axes.edgecolor'] = '#2C3E50'
        plt.rcParams['xtick.color'] = '#2C3E50'
        plt.rcParams['ytick.color'] = '#2C3E50'
        plt.rcParams['font.size'] = 9
    
    def create_graphs(self):
        """Crear la figura y canvas para los gráficos"""
        # Frame contenedor principal
        self.container_frame = tk.Frame(self.parent_frame, bg=self.colores['bg_frame'])
        
        # ---> INICIO DE LA MODIFICACIÓN <---
        # Cambiar de pack a grid para que respete la configuración del padre
        self.container_frame.grid(row=0, column=0, sticky='nsew') #
        # ---> FIN DE LA MODIFICACIÓN <---
        
        # Configurar el frame contenedor para que se expanda completamente
        self.container_frame.grid_rowconfigure(0, weight=1) #
        self.container_frame.grid_columnconfigure(0, weight=1) #
        
        # Crear figura con tamaño inicial más pequeño
        self.fig = Figure(figsize=(10, 7), dpi=80, facecolor='#ECF0F1') #
        
        # Crear subplots con espaciado optimizado
        self.axes = self.fig.subplots(2, 2, gridspec_kw={ #
            'hspace': 0.4, #
            'wspace': 0.3, #
            'left': 0.08, #
            'right': 0.95, #
            'top': 0.88, #
            'bottom': 0.12 #
        })
        
        # Título principal sin emojis
        self.fig.suptitle('Analisis Visual Completo de Resultados', #
                         fontsize=14, fontweight='bold', color='#2C3E50') #
        
        # Canvas para los gráficos
        self.canvas = FigureCanvasTkAgg(self.fig, self.container_frame) #
        self.canvas_widget = self.canvas.get_tk_widget() #
        
        # Configurar el canvas para llenar completamente el contenedor
        self.canvas_widget.grid(row=0, column=0, sticky='nsew', padx=0, pady=0) #
        self.canvas_widget.configure(highlightthickness=0, bd=0) #
        
        # Configurar eventos de redimensionamiento
        self.parent_frame.bind('<Configure>', self.on_parent_configure) #
        self.canvas_widget.bind('<Configure>', self.on_canvas_configure) #
        
        # Variables para controlar el redimensionamiento
        self.last_size = (0, 0) #
        self.resize_job = None #
        
        # Forzar actualización inicial después de un momento
        self.parent_frame.after(100, self.force_initial_resize) #
        
        # Inicializar gráficos vacíos
        self.clear_all_graphs() 
    
    def force_initial_resize(self):
        """Forzar redimensionamiento inicial"""
        try:
            self.parent_frame.update_idletasks()
            parent_width = self.parent_frame.winfo_width()
            parent_height = self.parent_frame.winfo_height()
            if parent_width > 1 and parent_height > 1:
                self.resize_figure(parent_width, parent_height)
        except:
            pass
    
    def on_parent_configure(self, event):
        """Manejar cambios en el frame padre"""
        if event.widget == self.parent_frame:
            width = event.width
            height = event.height
            if width > 1 and height > 1:
                self.schedule_resize(width, height)
    
    def on_canvas_configure(self, event):
        """Manejar cambios en el canvas"""
        if event.widget == self.canvas_widget:
            width = event.width
            height = event.height
            if width > 1 and height > 1:
                self.schedule_resize(width, height)
    
    def schedule_resize(self, width, height):
        """Programar redimensionamiento para evitar múltiples llamadas"""
        # Cancelar trabajo previo
        if self.resize_job:
            self.parent_frame.after_cancel(self.resize_job)
        
        # Programar nuevo redimensionamiento
        self.resize_job = self.parent_frame.after(50, lambda: self.resize_figure(width, height))
    
    def resize_figure(self, width, height):
        """Redimensionar la figura según el tamaño del contenedor"""
        try:
            # Evitar redimensionamientos innecesarios
            if abs(width - self.last_size[0]) < 10 and abs(height - self.last_size[1]) < 10:
                return
            
            self.last_size = (width, height)
            
            # Calcular tamaño óptimo en pulgadas
            dpi = self.fig.dpi
            
            # Usar prácticamente todo el espacio disponible
            width_inch = max(6, (width - 5) / dpi)
            height_inch = max(4, (height - 5) / dpi)
            
            # Limitar tamaños máximos para rendimiento
            width_inch = min(width_inch, 30)
            height_inch = min(height_inch, 25)
            
            # Ajustar proporción si es necesario
            aspect_ratio = width_inch / height_inch
            if aspect_ratio > 2.5:  # Muy ancho
                height_inch = width_inch / 2.0
            elif aspect_ratio < 0.7:  # Muy alto
                width_inch = height_inch * 1.0
            
            # Redimensionar la figura
            self.fig.set_size_inches(width_inch, height_inch, forward=False)
            
            # Ajustar espaciado dinámicamente
            self.adjust_subplot_spacing(width_inch, height_inch)
            
            # Actualizar canvas
            self.canvas.draw_idle()
            
            # Forzar actualización del widget
            self.canvas_widget.update_idletasks()
            
        except Exception as e:
            pass
        finally:
            self.resize_job = None
    
    def adjust_subplot_spacing(self, width_inch, height_inch):
        """Ajustar espaciado de subplots según el tamaño"""
        # Espaciado base
        base_hspace = 0.4
        base_wspace = 0.3
        base_left = 0.08
        base_right = 0.95
        base_top = 0.88
        base_bottom = 0.12
        
        # Ajustes según ancho
        if width_inch > 20:  # Pantalla muy ancha
            wspace = 0.15
            left = 0.04
            right = 0.98
        elif width_inch > 15:
            wspace = 0.20
            left = 0.06
            right = 0.96
        elif width_inch > 12:
            wspace = 0.25
            left = 0.07
            right = 0.95
        else:
            wspace = base_wspace
            left = base_left
            right = base_right
        
        # Ajustes según altura
        if height_inch > 15:  # Pantalla muy alta
            hspace = 0.25
            top = 0.92
            bottom = 0.08
        elif height_inch > 12:
            hspace = 0.30
            top = 0.90
            bottom = 0.10
        elif height_inch > 8:
            hspace = 0.35
            top = 0.88
            bottom = 0.12
        else:
            hspace = base_hspace
            top = base_top
            bottom = base_bottom
        
        # Aplicar ajustes
        self.fig.subplots_adjust(
            left=left,
            right=right,
            top=top,
            bottom=bottom,
            wspace=wspace,
            hspace=hspace
        )
    
    def clear_all_graphs(self):
        """Limpiar todos los gráficos"""
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor('#FFFFFF')
            ax.grid(True, alpha=0.3, linestyle='--')
        
        # Forzar redibujado
        self.canvas.draw()
    
    def update_graphs(self, simulator):
        """Actualizar todos los gráficos con los datos del simulador"""
        self.clear_all_graphs()
        
        try:
            # Gráfico 1: Distribución 1 dado
            self.plot_single_die(simulator)
            
            # Gráfico 2: Distribución 2 dados
            self.plot_two_dice(simulator)
            
            # Gráfico 3: Distribución 3 dados
            self.plot_three_dice(simulator)
            
            # Gráfico 4: Comparación teórica vs experimental
            self.plot_comparison(simulator)
            
            # Redibujado final
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error actualizando gráficos: {e}")
    
    def plot_single_die(self, simulator):
        """Gráfico para 1 dado"""
        if not simulator.resultados_1_dado:
            self.axes[0,0].text(0.5, 0.5, 'Sin datos\npara 1 dado', 
                               ha='center', va='center', transform=self.axes[0,0].transAxes,
                               fontsize=12, color='gray')
            self.axes[0,0].set_title('1 Dado - Sin datos')
            return
        
        contador = Counter(simulator.resultados_1_dado)
        valores = list(range(1, 7))
        frecuencias = [contador.get(i, 0) for i in valores]
        
        bars = self.axes[0,0].bar(valores, frecuencias, alpha=0.8, 
                                 color='#3498DB', edgecolor='#2C3E50', linewidth=1)
        
        # Añadir números en las barras
        max_freq = max(frecuencias) if frecuencias else 1
        for bar, freq in zip(bars, frecuencias):
            if freq > 0:
                height = bar.get_height()
                self.axes[0,0].text(bar.get_x() + bar.get_width()/2., height + max_freq*0.01,
                                   f'{freq:,}', ha='center', va='bottom', 
                                   fontweight='bold', fontsize=8)
        
        self.axes[0,0].set_title(f'1 Dado - Distribucion\n({len(simulator.resultados_1_dado):,} lanzamientos)', 
                                fontweight='bold')
        self.axes[0,0].set_xlabel('Resultado del dado', fontweight='bold')
        self.axes[0,0].set_ylabel('Frecuencia', fontweight='bold')
        self.axes[0,0].set_xticks(valores)
        self.axes[0,0].grid(True, alpha=0.3, linestyle='--')
    
    def plot_two_dice(self, simulator):
        """Gráfico para 2 dados"""
        if not simulator.resultados_2_dados:
            self.axes[0,1].text(0.5, 0.5, 'Sin datos\npara 2 dados', 
                               ha='center', va='center', transform=self.axes[0,1].transAxes,
                               fontsize=12, color='gray')
            self.axes[0,1].set_title('2 Dados - Sin datos')
            return
        
        contador = Counter(simulator.resultados_2_dados)
        valores = list(range(0, 3))
        frecuencias = [contador.get(i, 0) for i in valores]
        etiquetas = ['0 seises', '1 seis', '2 seises']
        
        bars = self.axes[0,1].bar(valores, frecuencias, alpha=0.8, 
                                 color='#27AE60', edgecolor='#2C3E50', linewidth=1)
        
        # Añadir números en las barras
        max_freq = max(frecuencias) if frecuencias else 1
        for bar, freq in zip(bars, frecuencias):
            if freq > 0:
                height = bar.get_height()
                self.axes[0,1].text(bar.get_x() + bar.get_width()/2., height + max_freq*0.01,
                                   f'{freq:,}', ha='center', va='bottom', 
                                   fontweight='bold', fontsize=8)
        
        self.axes[0,1].set_title(f'2 Dados - Numero de 6\n({len(simulator.resultados_2_dados):,} lanzamientos)', 
                                fontweight='bold')
        self.axes[0,1].set_xlabel('Numero de 6 por lanzamiento', fontweight='bold')
        self.axes[0,1].set_ylabel('Frecuencia', fontweight='bold')
        self.axes[0,1].set_xticks(valores)
        self.axes[0,1].set_xticklabels(etiquetas)
        self.axes[0,1].grid(True, alpha=0.3, linestyle='--')
    
    def plot_three_dice(self, simulator):
        """Gráfico para 3 dados"""
        if not simulator.resultados_3_dados:
            self.axes[1,0].text(0.5, 0.5, 'Sin datos\npara 3 dados', 
                               ha='center', va='center', transform=self.axes[1,0].transAxes,
                               fontsize=12, color='gray')
            self.axes[1,0].set_title('3 Dados - Sin datos')
            return
        
        contador = Counter(simulator.resultados_3_dados)
        valores = list(range(0, 4))
        frecuencias = [contador.get(i, 0) for i in valores]
        etiquetas = ['0 seises', '1 seis', '2 seises', '3 seises']
        
        bars = self.axes[1,0].bar(valores, frecuencias, alpha=0.8, 
                                 color='#E74C3C', edgecolor='#2C3E50', linewidth=1)
        
        # Añadir números en las barras
        max_freq = max(frecuencias) if frecuencias else 1
        for bar, freq in zip(bars, frecuencias):
            if freq > 0:
                height = bar.get_height()
                self.axes[1,0].text(bar.get_x() + bar.get_width()/2., height + max_freq*0.01,
                                   f'{freq:,}', ha='center', va='bottom', 
                                   fontweight='bold', fontsize=8)
        
        self.axes[1,0].set_title(f'3 Dados - Numero de 6\n({len(simulator.resultados_3_dados):,} lanzamientos)', 
                                fontweight='bold')
        self.axes[1,0].set_xlabel('Numero de 6 por lanzamiento', fontweight='bold')
        self.axes[1,0].set_ylabel('Frecuencia', fontweight='bold')
        self.axes[1,0].set_xticks(valores)
        self.axes[1,0].set_xticklabels(etiquetas)
        self.axes[1,0].grid(True, alpha=0.3, linestyle='--')
    
    def plot_comparison(self, simulator):
        """Gráfico de comparación teórica vs experimental"""
        # Usar datos de 3 dados si están disponibles, sino 2 dados, sino 1 dado
        if simulator.resultados_3_dados:
            self.plot_three_dice_comparison(simulator)
        elif simulator.resultados_2_dados:
            self.plot_two_dice_comparison(simulator)
        elif simulator.resultados_1_dado:
            self.plot_single_die_comparison(simulator)
        else:
            self.axes[1,1].text(0.5, 0.5, 'Sin datos\npara comparacion', 
                               ha='center', va='center', transform=self.axes[1,1].transAxes,
                               fontsize=12, color='gray')
            self.axes[1,1].set_title('Comparacion - Sin datos')
    
    def plot_three_dice_comparison(self, simulator):
        """Comparación para 3 dados"""
        contador = Counter(simulator.resultados_3_dados)
        total = len(simulator.resultados_3_dados)
        prob_teoricas = simulator.calcular_probabilidades_teoricas(3)
        
        categorias = ['0 seises', '1 seis', '2 seises', '3 seises']
        prob_exp = [contador.get(i, 0) / total for i in range(4)]
        prob_teo = [prob_teoricas[f"{i}_seises"] for i in range(4)]
        
        x = range(len(categorias))
        width = 0.35
        
        bars1 = self.axes[1,1].bar([i - width/2 for i in x], prob_exp, width, 
                                  label='Experimental', alpha=0.8, color='#F39C12',
                                  edgecolor='#2C3E50', linewidth=1)
        bars2 = self.axes[1,1].bar([i + width/2 for i in x], prob_teo, width, 
                                  label='Teorica', alpha=0.8, color='#9B59B6',
                                  edgecolor='#2C3E50', linewidth=1)
        
        # Añadir valores en las barras
        max_prob = max(max(prob_exp), max(prob_teo))
        for bars, probs in [(bars1, prob_exp), (bars2, prob_teo)]:
            for bar, prob in zip(bars, probs):
                if prob > 0:
                    height = bar.get_height()
                    self.axes[1,1].text(bar.get_x() + bar.get_width()/2., height + max_prob*0.02,
                                       f'{prob:.3f}', ha='center', va='bottom', 
                                       fontweight='bold', fontsize=7)
        
        self.axes[1,1].set_title('3 Dados - Teorica vs Experimental', fontweight='bold')
        self.axes[1,1].set_xlabel('Numero de 6 por lanzamiento', fontweight='bold')
        self.axes[1,1].set_ylabel('Probabilidad', fontweight='bold')
        self.axes[1,1].set_xticks(x)
        self.axes[1,1].set_xticklabels(categorias, rotation=0, ha='center')
        self.axes[1,1].legend(loc='upper right')
        self.axes[1,1].grid(True, alpha=0.3, linestyle='--')
    
    def plot_two_dice_comparison(self, simulator):
        """Comparación para 2 dados"""
        contador = Counter(simulator.resultados_2_dados)
        total = len(simulator.resultados_2_dados)
        prob_teoricas = simulator.calcular_probabilidades_teoricas(2)
        
        categorias = ['0 seises', '1 seis', '2 seises']
        prob_exp = [contador.get(i, 0) / total for i in range(3)]
        prob_teo = [prob_teoricas[f"{i}_seises"] for i in range(3)]
        
        x = range(len(categorias))
        width = 0.35
        
        bars1 = self.axes[1,1].bar([i - width/2 for i in x], prob_exp, width, 
                                  label='Experimental', alpha=0.8, color='#F39C12',
                                  edgecolor='#2C3E50', linewidth=1)
        bars2 = self.axes[1,1].bar([i + width/2 for i in x], prob_teo, width, 
                                  label='Teorica', alpha=0.8, color='#9B59B6',
                                  edgecolor='#2C3E50', linewidth=1)
        
        # Añadir valores en las barras
        max_prob = max(max(prob_exp), max(prob_teo))
        for bars, probs in [(bars1, prob_exp), (bars2, prob_teo)]:
            for bar, prob in zip(bars, probs):
                if prob > 0:
                    height = bar.get_height()
                    self.axes[1,1].text(bar.get_x() + bar.get_width()/2., height + max_prob*0.02,
                                       f'{prob:.3f}', ha='center', va='bottom', 
                                       fontweight='bold', fontsize=8)
        
        self.axes[1,1].set_title('2 Dados - Teorica vs Experimental', fontweight='bold')
        self.axes[1,1].set_xlabel('Numero de 6 por lanzamiento', fontweight='bold')
        self.axes[1,1].set_ylabel('Probabilidad', fontweight='bold')
        self.axes[1,1].set_xticks(x)
        self.axes[1,1].set_xticklabels(categorias)
        self.axes[1,1].legend(loc='upper right')
        self.axes[1,1].grid(True, alpha=0.3, linestyle='--')
    
    def plot_single_die_comparison(self, simulator):
        """Comparación para 1 dado"""
        contador = Counter(simulator.resultados_1_dado)
        total = len(simulator.resultados_1_dado)
        prob_teoricas = simulator.calcular_probabilidades_teoricas(1)
        
        valores = list(range(1, 7))
        prob_exp = [contador.get(i, 0) / total for i in valores]
        prob_teo = [prob_teoricas[f"sacar_{i}"] for i in valores]
        
        x = range(len(valores))
        width = 0.35
        
        bars1 = self.axes[1,1].bar([i - width/2 for i in x], prob_exp, width, 
                                  label='Experimental', alpha=0.8, color='#F39C12',
                                  edgecolor='#2C3E50', linewidth=1)
        bars2 = self.axes[1,1].bar([i + width/2 for i in x], prob_teo, width, 
                                  label='Teorica', alpha=0.8, color='#9B59B6',
                                  edgecolor='#2C3E50', linewidth=1)
        
        # Añadir valores en las barras
        max_prob = max(max(prob_exp), max(prob_teo))
        for bars, probs in [(bars1, prob_exp), (bars2, prob_teo)]:
            for bar, prob in zip(bars, probs):
                if prob > 0:
                    height = bar.get_height()
                    self.axes[1,1].text(bar.get_x() + bar.get_width()/2., height + max_prob*0.02,
                                       f'{prob:.3f}', ha='center', va='bottom', 
                                       fontweight='bold', fontsize=7)
        
        self.axes[1,1].set_title('1 Dado - Teorica vs Experimental', fontweight='bold')
        self.axes[1,1].set_xlabel('Resultado del dado', fontweight='bold')
        self.axes[1,1].set_ylabel('Probabilidad', fontweight='bold')
        self.axes[1,1].set_xticks(x)
        self.axes[1,1].set_xticklabels(valores)
        self.axes[1,1].legend(loc='upper right')
        self.axes[1,1].grid(True, alpha=0.3, linestyle='--')
