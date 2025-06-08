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
        # Crear figura con tamaño adaptable
        self.fig = Figure(figsize=(12, 8), dpi=100, facecolor='#ECF0F1')
        
        # Crear subplots con mejor espaciado
        self.axes = self.fig.subplots(2, 2, gridspec_kw={
            'hspace': 0.3,
            'wspace': 0.3,
            'left': 0.08,
            'right': 0.95,
            'top': 0.92,
            'bottom': 0.08
        })
        
        # Título principal
        self.fig.suptitle('📊 Análisis Visual Completo de Resultados', 
                         fontsize=14, fontweight='bold', color='#2C3E50')
        
        # Frame contenedor con scrollbar
        self.container_frame = tk.Frame(self.parent_frame, bg=self.colores['bg_frame'])
        self.container_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas para los gráficos
        self.canvas = FigureCanvasTkAgg(self.fig, self.container_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Configurar redimensionamiento automático
        canvas_widget.bind('<Configure>', self.on_canvas_configure)
        
        # Inicializar gráficos vacíos
        self.clear_all_graphs()
    
    def on_canvas_configure(self, event):
        """Ajustar el tamaño de los gráficos cuando cambia el tamaño de la ventana"""
        try:
            # Calcular nuevo tamaño basado en el evento
            width_inch = max(8, event.width / 100)
            height_inch = max(6, event.height / 100)
            
            # Establecer límites razonables
            width_inch = min(width_inch, 20)
            height_inch = min(height_inch, 15)
            
            # Redimensionar manteniendo proporción
            self.fig.set_size_inches(width_inch, height_inch)
            
            # Ajustar espaciado automáticamente
            self.fig.tight_layout(rect=[0, 0.03, 1, 0.95])
            self.canvas.draw_idle()
        except Exception as e:
            pass  # Ignorar errores durante el redimensionamiento
    
    def clear_all_graphs(self):
        """Limpiar todos los gráficos"""
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor('#FFFFFF')
            ax.grid(True, alpha=0.3, linestyle='--')
        self.canvas.draw()
    
    def update_graphs(self, simulator):
        """Actualizar todos los gráficos con los datos del simulador"""
        self.clear_all_graphs()
        
        # Gráfico 1: Distribución 1 dado
        self.plot_single_die(simulator)
        
        # Gráfico 2: Distribución 2 dados
        self.plot_two_dice(simulator)
        
        # Gráfico 3: Distribución 3 dados
        self.plot_three_dice(simulator)
        
        # Gráfico 4: Comparación teórica vs experimental
        self.plot_comparison(simulator)
        
        # Ajustar layout y redibujar
        self.fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        self.canvas.draw()
    
    def plot_single_die(self, simulator):
        """Gráfico para 1 dado"""
        if not simulator.resultados_1_dado:
            self.axes[0,0].text(0.5, 0.5, 'Sin datos\npara 1 dado', 
                               ha='center', va='center', transform=self.axes[0,0].transAxes,
                               fontsize=12, color='gray')
            self.axes[0,0].set_title(' 1 Dado - Sin datos')
            return
        
        contador = Counter(simulator.resultados_1_dado)
        valores = list(range(1, 7))
        frecuencias = [contador.get(i, 0) for i in valores]
        
        bars = self.axes[0,0].bar(valores, frecuencias, alpha=0.8, 
                                 color='#3498DB', edgecolor='#2C3E50', linewidth=1)
        
        # Añadir números en las barras
        for bar, freq in zip(bars, frecuencias):
            if freq > 0:
                height = bar.get_height()
                self.axes[0,0].text(bar.get_x() + bar.get_width()/2., height + max(frecuencias)*0.01,
                                   f'{freq:,}', ha='center', va='bottom', 
                                   fontweight='bold', fontsize=8)
        
        self.axes[0,0].set_title(f' 1 Dado - Distribución\n({len(simulator.resultados_1_dado):,} lanzamientos)', 
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
            self.axes[0,1].set_title(' 2 Dados - Sin datos')
            return
        
        contador = Counter(simulator.resultados_2_dados)
        valores = list(range(0, 3))
        frecuencias = [contador.get(i, 0) for i in valores]
        etiquetas = ['0 seises', '1 seis', '2 seises']
        
        bars = self.axes[0,1].bar(valores, frecuencias, alpha=0.8, 
                                 color='#27AE60', edgecolor='#2C3E50', linewidth=1)
        
        # Añadir números en las barras
        for bar, freq in zip(bars, frecuencias):
            if freq > 0:
                height = bar.get_height()
                self.axes[0,1].text(bar.get_x() + bar.get_width()/2., height + max(frecuencias)*0.01,
                                   f'{freq:,}', ha='center', va='bottom', 
                                   fontweight='bold', fontsize=8)
        
        self.axes[0,1].set_title(f' 2 Dados - Número de 6\n({len(simulator.resultados_2_dados):,} lanzamientos)', 
                                fontweight='bold')
        self.axes[0,1].set_xlabel('Número de 6 por lanzamiento', fontweight='bold')
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
            self.axes[1,0].set_title(' 3 Dados - Sin datos')
            return
        
        contador = Counter(simulator.resultados_3_dados)
        valores = list(range(0, 4))
        frecuencias = [contador.get(i, 0) for i in valores]
        etiquetas = ['0 seises', '1 seis', '2 seises', '3 seises']
        
        bars = self.axes[1,0].bar(valores, frecuencias, alpha=0.8, 
                                 color='#E74C3C', edgecolor='#2C3E50', linewidth=1)
        
        # Añadir números en las barras
        for bar, freq in zip(bars, frecuencias):
            if freq > 0:
                height = bar.get_height()
                self.axes[1,0].text(bar.get_x() + bar.get_width()/2., height + max(frecuencias)*0.01,
                                   f'{freq:,}', ha='center', va='bottom', 
                                   fontweight='bold', fontsize=8)
        
        self.axes[1,0].set_title(f' 3 Dados - Número de 6\n({len(simulator.resultados_3_dados):,} lanzamientos)', 
                                fontweight='bold')
        self.axes[1,0].set_xlabel('Número de 6 por lanzamiento', fontweight='bold')
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
            self.axes[1,1].text(0.5, 0.5, 'Sin datos\npara comparación', 
                               ha='center', va='center', transform=self.axes[1,1].transAxes,
                               fontsize=12, color='gray')
            self.axes[1,1].set_title(' Comparación - Sin datos')
    
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
                                  label='Teórica', alpha=0.8, color='#9B59B6',
                                  edgecolor='#2C3E50', linewidth=1)
        
        # Añadir valores en las barras
        for bars, probs, label in [(bars1, prob_exp, 'exp'), (bars2, prob_teo, 'teo')]:
            for bar, prob in zip(bars, probs):
                if prob > 0:
                    height = bar.get_height()
                    self.axes[1,1].text(bar.get_x() + bar.get_width()/2., height + 0.005,
                                       f'{prob:.3f}', ha='center', va='bottom', 
                                       fontweight='bold', fontsize=7)
        
        self.axes[1,1].set_title(' 3 Dados - Teórica vs Experimental', fontweight='bold')
        self.axes[1,1].set_xlabel('Número de 6 por lanzamiento', fontweight='bold')
        self.axes[1,1].set_ylabel('Probabilidad', fontweight='bold')
        self.axes[1,1].set_xticks(x)
        self.axes[1,1].set_xticklabels(categorias, rotation=45, ha='right')
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
                                  label='Teórica', alpha=0.8, color='#9B59B6',
                                  edgecolor='#2C3E50', linewidth=1)
        
        # Añadir valores en las barras
        for bars, probs in [(bars1, prob_exp), (bars2, prob_teo)]:
            for bar, prob in zip(bars, probs):
                if prob > 0:
                    height = bar.get_height()
                    self.axes[1,1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                                       f'{prob:.3f}', ha='center', va='bottom', 
                                       fontweight='bold', fontsize=8)
        
        self.axes[1,1].set_title(' 2 Dados - Teórica vs Experimental', fontweight='bold')
        self.axes[1,1].set_xlabel('Número de 6 por lanzamiento', fontweight='bold')
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
                                  label='Teórica', alpha=0.8, color='#9B59B6',
                                  edgecolor='#2C3E50', linewidth=1)
        
        # Añadir valores en las barras
        for bars, probs in [(bars1, prob_exp), (bars2, prob_teo)]:
            for bar, prob in zip(bars, probs):
                if prob > 0:
                    height = bar.get_height()
                    self.axes[1,1].text(bar.get_x() + bar.get_width()/2., height + 0.005,
                                       f'{prob:.3f}', ha='center', va='bottom', 
                                       fontweight='bold', fontsize=7)
        
        self.axes[1,1].set_title(' 1 Dado - Teórica vs Experimental', fontweight='bold')
        self.axes[1,1].set_xlabel('Resultado del dado', fontweight='bold')
        self.axes[1,1].set_ylabel('Probabilidad', fontweight='bold')
        self.axes[1,1].set_xticks(x)
        self.axes[1,1].set_xticklabels(valores)
        self.axes[1,1].legend(loc='upper right')
        self.axes[1,1].grid(True, alpha=0.3, linestyle='--')