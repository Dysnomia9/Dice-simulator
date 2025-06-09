import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from collections import Counter

class GraphManager:
    def __init__(self, parent_frame, colores):
        self.parent_frame = parent_frame
        self.colores = colores
        self.tooltip_data = {}
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
        
        # IMPORTANTE: Configurar interactividad para evitar artefactos
        plt.rcParams['figure.autolayout'] = False
        plt.rcParams['toolbar'] = 'None'

    def create_graphs(self):
        """Crear la figura y canvas para los gráficos."""
        # Frame contenedor principal
        self.container_frame = tk.Frame(self.parent_frame, bg=self.colores['bg_frame'])
        self.container_frame.grid(row=0, column=0, sticky='nsew')

        # Configurar el grid del frame contenedor
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)

        # Crear la figura de Matplotlib con configuración específica
        self.fig = Figure(figsize=(10, 7), dpi=80, facecolor='#ECF0F1')
        self.axes = self.fig.subplots(2, 2, gridspec_kw={
            'hspace': 0.4, 'wspace': 0.3, 'left': 0.08,
            'right': 0.95, 'top': 0.88, 'bottom': 0.12
        })
        self.fig.suptitle('Análisis Visual Completo de Resultados',
                         fontsize=14, fontweight='bold', color='#2C3E50')

        # Crear el canvas con configuración específica para evitar artefactos
        self.canvas = FigureCanvasTkAgg(self.fig, self.container_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky='nsew')
        
        # para evitar artefactos visuales
        self.canvas_widget.configure(
            highlightthickness=0, 
            bd=0,
            bg=self.colores['bg_frame'],  # Color de fondo consistente
            relief='flat'
        )
        
        # Deshabilitar la navegación interactiva que puede causar artefactos
        self.canvas.get_tk_widget().bind('<Button-1>', lambda e: None)
        self.canvas.get_tk_widget().bind('<Motion>', lambda e: None)

        # Configurar eventos de redimensionamiento
        self.parent_frame.bind('<Configure>', self.on_parent_configure)
        self.last_size = (0, 0)
        self.resize_job = None
        self.parent_frame.after(100, self.force_initial_resize)
        self.clear_all_graphs()

    def clear_all_graphs(self):
        """Limpiar todos los gráficos."""
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor('#FFFFFF')  # Fondo blanco consistente
            ax.grid(True, alpha=0.3, linestyle='--')
        
        # Forzar redibujado para evitar artefactos
        self.fig.canvas.draw_idle()


    def on_hover(self, event):
        """Handle mouse hover events to display tooltips."""
        if event.inaxes is None:
            return

        # Clear previous annotations
        for ax in self.axes.flat:
            for annotation in ax.texts:
                if hasattr(annotation, '_tooltip_annotation'):
                    annotation.remove()

        subplot_idx = None
        for i, ax in enumerate(self.axes.flat):
            if ax == event.inaxes:
                subplot_idx = i
                break
        
        if subplot_idx is None or subplot_idx not in self.tooltip_data:
            self.canvas.draw_idle()
            return
            
        data = self.tooltip_data[subplot_idx]
        x_data, y_data, labels = data['x_data'], data['y_data'], data['labels']

        if not x_data or not y_data:
            return

        x_mouse = event.xdata
        tolerance = 0.4 if len(x_data) == len(set(x_data)) else 0.2
        
        distances = [abs(x - x_mouse) for x in x_data]
        closest_idx = min(range(len(distances)), key=distances.__getitem__)

        if distances[closest_idx] < tolerance:
            x_pos, y_pos, label = x_data[closest_idx], y_data[closest_idx], labels[closest_idx]
            
            tooltip_text = f"{label}: {y_pos:,}" if isinstance(y_pos, int) else f"{label}: {y_pos:.4f}"
            
            annotation = event.inaxes.annotate(
                tooltip_text,
                xy=(x_pos, y_pos),
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.9, edgecolor='black'),
                fontsize=9, fontweight='bold', ha='left'
            )
            annotation._tooltip_annotation = True
            self.canvas.draw_idle()

    def store_tooltip_data(self, subplot_idx, x_data, y_data, labels):
        """Store data for tooltips."""
        self.tooltip_data[subplot_idx] = {
            'x_data': x_data,
            'y_data': y_data,
            'labels': labels
        }

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
        if self.resize_job:
            self.parent_frame.after_cancel(self.resize_job)
        self.resize_job = self.parent_frame.after(50, lambda: self.resize_figure(width, height))
    
    def resize_figure(self, width, height):
        """Redimensionar la figura según el tamaño del contenedor"""
        try:
            if abs(width - self.last_size[0]) < 10 and abs(height - self.last_size[1]) < 10:
                return
            
            self.last_size = (width, height)
            dpi = self.fig.dpi
            width_inch = max(6, (width - 5) / dpi)
            height_inch = max(4, (height - 5) / dpi)
            width_inch = min(width_inch, 30)
            height_inch = min(height_inch, 25)
            
            aspect_ratio = width_inch / height_inch
            if aspect_ratio > 2.5:
                height_inch = width_inch / 2.0
            elif aspect_ratio < 0.7:
                width_inch = height_inch * 1.0
            
            self.fig.set_size_inches(width_inch, height_inch, forward=False)
            self.adjust_subplot_spacing(width_inch, height_inch)
            self.canvas.draw_idle()
            self.canvas_widget.update_idletasks()
            
        except Exception as e:
            pass
        finally:
            self.resize_job = None
    
    def adjust_subplot_spacing(self, width_inch, height_inch):
        """Ajustar espaciado de subplots según el tamaño"""
        base_hspace, base_wspace, base_left, base_right, base_top, base_bottom = 0.4, 0.3, 0.08, 0.95, 0.88, 0.12
        
        if width_inch > 20: wspace, left, right = 0.15, 0.04, 0.98
        elif width_inch > 15: wspace, left, right = 0.20, 0.06, 0.96
        elif width_inch > 12: wspace, left, right = 0.25, 0.07, 0.95
        else: wspace, left, right = base_wspace, base_left, base_right
        
        if height_inch > 15: hspace, top, bottom = 0.25, 0.92, 0.08
        elif height_inch > 12: hspace, top, bottom = 0.30, 0.90, 0.10
        elif height_inch > 8: hspace, top, bottom = 0.35, 0.88, 0.12
        else: hspace, top, bottom = base_hspace, base_top, base_bottom
        
        self.fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom, wspace=wspace, hspace=hspace)
    
    def clear_all_graphs(self):
        """Limpiar todos los gráficos"""
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor('#FFFFFF')
            ax.grid(True, alpha=0.3, linestyle='--')
        self.tooltip_data.clear()
        self.canvas.draw()
    
    def update_graphs(self, simulator):
        """Actualizar todos los gráficos con los datos del simulador"""
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
        """Gráfico para 1 dado"""
        ax = self.axes[0, 0]
        if not simulator.resultados_1_dado:
            ax.text(0.5, 0.5, 'Sin datos\npara 1 dado', ha='center', va='center', transform=ax.transAxes, fontsize=12, color='gray')
            ax.set_title('1 Dado - Sin datos')
            return
        
        contador = Counter(simulator.resultados_1_dado)
        valores = list(range(1, 7))
        frecuencias = [contador.get(i, 0) for i in valores]
        
        # Store data for tooltip
        labels = [f"Cara {i}" for i in valores]
        self.store_tooltip_data(0, valores, frecuencias, labels)

        bars = ax.bar(valores, frecuencias, alpha=0.8, color='#3498DB', edgecolor='#2C3E50', linewidth=1)
        max_freq = max(frecuencias) if frecuencias else 1
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + max_freq*0.01, f'{height:,}', ha='center', va='bottom', fontweight='bold', fontsize=8)
        
        ax.set_title(f'1 Dado - Distribucion\n({len(simulator.resultados_1_dado):,} lanzamientos)', fontweight='bold')
        ax.set_xlabel('Resultado del dado', fontweight='bold')
        ax.set_ylabel('Frecuencia', fontweight='bold')
        ax.set_xticks(valores)
        ax.grid(True, alpha=0.3, linestyle='--')
    
    def plot_two_dice(self, simulator):
        """Gráfico para 2 dados"""
        ax = self.axes[0, 1]
        if not simulator.resultados_2_dados:
            ax.text(0.5, 0.5, 'Sin datos\npara 2 dados', ha='center', va='center', transform=ax.transAxes, fontsize=12, color='gray')
            ax.set_title('2 Dados - Sin datos')
            return
        
        contador = Counter(simulator.resultados_2_dados)
        valores = list(range(0, 3))
        frecuencias = [contador.get(i, 0) for i in valores]
        etiquetas = ['0 seises', '1 seis', '2 seises']
        
       
        self.store_tooltip_data(1, valores, frecuencias, etiquetas)

        bars = ax.bar(valores, frecuencias, alpha=0.8, color='#27AE60', edgecolor='#2C3E50', linewidth=1)
        max_freq = max(frecuencias) if frecuencias else 1
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + max_freq*0.01, f'{height:,}', ha='center', va='bottom', fontweight='bold', fontsize=8)

        ax.set_title(f'2 Dados - Numero de 6\n({len(simulator.resultados_2_dados):,} lanzamientos)', fontweight='bold')
        ax.set_xlabel('Numero de 6 por lanzamiento', fontweight='bold')
        ax.set_ylabel('Frecuencia', fontweight='bold')
        ax.set_xticks(valores)
        ax.set_xticklabels(etiquetas)
        ax.grid(True, alpha=0.3, linestyle='--')
    
    def plot_three_dice(self, simulator):
        """Gráfico para 3 dados"""
        ax = self.axes[1, 0]
        if not simulator.resultados_3_dados:
            ax.text(0.5, 0.5, 'Sin datos\npara 3 dados', ha='center', va='center', transform=ax.transAxes, fontsize=12, color='gray')
            ax.set_title('3 Dados - Sin datos')
            return
        
        contador = Counter(simulator.resultados_3_dados)
        valores = list(range(0, 4))
        frecuencias = [contador.get(i, 0) for i in valores]
        etiquetas = ['0 seises', '1 seis', '2 seises', '3 seises']


        self.store_tooltip_data(2, valores, frecuencias, etiquetas)

        bars = ax.bar(valores, frecuencias, alpha=0.8, color='#E74C3C', edgecolor='#2C3E50', linewidth=1)
        max_freq = max(frecuencias) if frecuencias else 1
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + max_freq*0.01, f'{height:,}', ha='center', va='bottom', fontweight='bold', fontsize=8)

        ax.set_title(f'3 Dados - Numero de 6\n({len(simulator.resultados_3_dados):,} lanzamientos)', fontweight='bold')
        ax.set_xlabel('Numero de 6 por lanzamiento', fontweight='bold')
        ax.set_ylabel('Frecuencia', fontweight='bold')
        ax.set_xticks(valores)
        ax.set_xticklabels(etiquetas)
        ax.grid(True, alpha=0.3, linestyle='--')
    
    def plot_comparison(self, simulator):
        """Gráfico de comparación teórica vs experimental"""
        if simulator.resultados_3_dados:
            self.plot_three_dice_comparison(simulator)
        elif simulator.resultados_2_dados:
            self.plot_two_dice_comparison(simulator)
        elif simulator.resultados_1_dado:
            self.plot_single_die_comparison(simulator)
        else:
            ax = self.axes[1, 1]
            ax.text(0.5, 0.5, 'Sin datos\npara comparacion', ha='center', va='center', transform=ax.transAxes, fontsize=12, color='gray')
            ax.set_title('Comparacion - Sin datos')
    
    def _plot_comparison_bars(self, ax, x, categorias, prob_exp, prob_teo, width=0.35):
        bars1 = ax.bar([i - width/2 for i in x], prob_exp, width, label='Experimental', alpha=0.8, color='#F39C12', edgecolor='#2C3E50', linewidth=1)
        bars2 = ax.bar([i + width/2 for i in x], prob_teo, width, label='Teorica', alpha=0.8, color='#9B59B6', edgecolor='#2C3E50', linewidth=1)
        
        max_prob = max(max(prob_exp) if prob_exp else [0], max(prob_teo) if prob_teo else [0])
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height + max_prob*0.02, f'{height:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=7)

    def plot_three_dice_comparison(self, simulator):
        ax = self.axes[1,1]
        contador = Counter(simulator.resultados_3_dados)
        total = len(simulator.resultados_3_dados)
        prob_teoricas = simulator.calcular_probabilidades_teoricas(3)
        
        categorias = ['0 seises', '1 seis', '2 seises', '3 seises']
        valores = range(len(categorias))
        prob_exp = [contador.get(i, 0) / total for i in valores]
        prob_teo = [prob_teoricas[f"{i}_seises"] for i in valores]
        
        self._plot_comparison_bars(ax, valores, categorias, prob_exp, prob_teo)


        x_pos = [v - 0.35/2 for v in valores] + [v + 0.35/2 for v in valores]
        y_val = prob_exp + prob_teo
        labels = [f"{cat} (Exp)" for cat in categorias] + [f"{cat} (Teo)" for cat in categorias]
        self.store_tooltip_data(3, x_pos, y_val, labels)
        
        ax.set_title('3 Dados - Teorica vs Experimental', fontweight='bold')
        ax.set_xlabel('Numero de 6 por lanzamiento', fontweight='bold')
        ax.set_ylabel('Probabilidad', fontweight='bold')
        ax.set_xticks(valores)
        ax.set_xticklabels(categorias, rotation=0, ha='center')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, linestyle='--')
    
    def plot_two_dice_comparison(self, simulator):
        ax = self.axes[1,1]
        contador = Counter(simulator.resultados_2_dados)
        total = len(simulator.resultados_2_dados)
        prob_teoricas = simulator.calcular_probabilidades_teoricas(2)
        
        categorias = ['0 seises', '1 seis', '2 seises']
        valores = range(len(categorias))
        prob_exp = [contador.get(i, 0) / total for i in valores]
        prob_teo = [prob_teoricas[f"{i}_seises"] for i in valores]

        self._plot_comparison_bars(ax, valores, categorias, prob_exp, prob_teo)


        x_pos = [v - 0.35/2 for v in valores] + [v + 0.35/2 for v in valores]
        y_val = prob_exp + prob_teo
        labels = [f"{cat} (Exp)" for cat in categorias] + [f"{cat} (Teo)" for cat in categorias]
        self.store_tooltip_data(3, x_pos, y_val, labels)

        ax.set_title('2 Dados - Teorica vs Experimental', fontweight='bold')
        ax.set_xlabel('Numero de 6 por lanzamiento', fontweight='bold')
        ax.set_ylabel('Probabilidad', fontweight='bold')
        ax.set_xticks(valores)
        ax.set_xticklabels(categorias)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, linestyle='--')
    
    def plot_single_die_comparison(self, simulator):
        ax = self.axes[1,1]
        contador = Counter(simulator.resultados_1_dado)
        total = len(simulator.resultados_1_dado)
        prob_teoricas = simulator.calcular_probabilidades_teoricas(1)
        
        categorias = list(range(1, 7))
        valores = range(len(categorias))
        prob_exp = [contador.get(i, 0) / total for i in categorias]
        prob_teo = [prob_teoricas[f"sacar_{i}"] for i in categorias]

        self._plot_comparison_bars(ax, valores, categorias, prob_exp, prob_teo)


        x_pos = [v - 0.35/2 for v in valores] + [v + 0.35/2 for v in valores]
        y_val = prob_exp + prob_teo
        labels = [f"Cara {cat} (Exp)" for cat in categorias] + [f"Cara {cat} (Teo)" for cat in categorias]
        self.store_tooltip_data(3, x_pos, y_val, labels)

        ax.set_title('1 Dado - Teorica vs Experimental', fontweight='bold')
        ax.set_xlabel('Resultado del dado', fontweight='bold')
        ax.set_ylabel('Probabilidad', fontweight='bold')
        ax.set_xticks(valores)
        ax.set_xticklabels(categorias)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, linestyle='--')