import random
import numpy as np
from collections import Counter
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime

class DiceSimulator:
    def __init__(self):
        self.resultados_1_dado = []
        self.resultados_2_dados = []
        self.resultados_3_dados = []
        self.resultados_detallados = {"1": [], "2": [], "3": []}
        self.total_lanzamientos = {"1": 0, "2": 0, "3": 0}
        self.historial_simulaciones = []
        self.semilla_random = None
        
    def establecer_semilla(self, semilla: Optional[int] = None):
        """Establece una semilla para reproducibilidad"""
        self.semilla_random = semilla
        if semilla is not None:
            random.seed(semilla)
            np.random.seed(semilla)
    
    def calcular_probabilidades_teoricas(self, num_dados: int) -> Dict[str, float]:
        """Calcula las probabilidades teóricas para diferentes escenarios"""
        probabilidades = {}
        
        if num_dados == 1:
            # Para 1 dado: probabilidad de cada cara
            for i in range(1, 7):
                probabilidades[f"sacar_{i}"] = 1/6
                
        elif num_dados == 2:
            # Para 2 dados: probabilidades de 6 en ambos, uno, ninguno
            probabilidades["0_seises"] = (5/6)**2  # 25/36
            probabilidades["1_seises"] = 2 * (1/6) * (5/6)  # 10/36
            probabilidades["2_seises"] = (1/6)**2  # 1/36
            probabilidades["al_menos_1_seis"] = 1 - (5/6)**2  # 11/36
            
        elif num_dados == 3:
            # Para 3 dados: todas las combinaciones posibles
            probabilidades["0_seises"] = (5/6)**3  # 125/216
            probabilidades["1_seises"] = 3 * (1/6) * (5/6)**2  # 75/216
            probabilidades["2_seises"] = 3 * (1/6)**2 * (5/6)  # 15/216
            probabilidades["3_seises"] = (1/6)**3  # 1/216
            probabilidades["al_menos_1_seis"] = 1 - (5/6)**3  # 91/216
            
        return probabilidades
    
    def calcular_estadisticas_avanzadas(self, resultados: List[int]) -> Dict[str, float]:
        """Calcula estadísticas avanzadas de los resultados"""
        if not resultados:
            return {}
            
        resultados_np = np.array(resultados)
        
        return {
            'media': float(np.mean(resultados_np)),
            'mediana': float(np.median(resultados_np)),
            'moda': float(Counter(resultados).most_common(1)[0][0]),
            'desviacion_estandar': float(np.std(resultados_np)),
            'varianza': float(np.var(resultados_np)),
            'rango': float(np.max(resultados_np) - np.min(resultados_np)),
            'cuartil_25': float(np.percentile(resultados_np, 25)),
            'cuartil_75': float(np.percentile(resultados_np, 75))
        }
    
    def simular_dados_vectorizado(self, lanzamientos: int, num_dados: int) -> bool:
        """Versión optimizada de simulación usando numpy para mejor rendimiento"""
        try:
            # Generar todos los lanzamientos de una vez usando numpy
            lanzamientos_dados = np.random.randint(1, 7, size=(lanzamientos, num_dados))
            
            # Contar seises por lanzamiento
            seises_por_lanzamiento = np.sum(lanzamientos_dados == 6, axis=1)
            
            # Preparar resultados detallados
            resultados_detallados = []
            for i in range(lanzamientos):
                resultados_detallados.append({
                    'lanzamiento': i + 1,
                    'dados': lanzamientos_dados[i].tolist(),
                    'seises': int(seises_por_lanzamiento[i])
                })
            
            # Guardar resultados según el número de dados
            if num_dados == 1:
                self.resultados_1_dado.extend(lanzamientos_dados[:, 0].tolist())
                self.resultados_detallados["1"].extend(resultados_detallados)
                self.total_lanzamientos["1"] += lanzamientos
            elif num_dados == 2:
                self.resultados_2_dados.extend(seises_por_lanzamiento.tolist())
                self.resultados_detallados["2"].extend(resultados_detallados)
                self.total_lanzamientos["2"] += lanzamientos
            elif num_dados == 3:
                self.resultados_3_dados.extend(seises_por_lanzamiento.tolist())
                self.resultados_detallados["3"].extend(resultados_detallados)
                self.total_lanzamientos["3"] += lanzamientos
            
            # Guardar en historial
            self.historial_simulaciones.append({
                'timestamp': datetime.now().isoformat(),
                'num_dados': num_dados,
                'lanzamientos': lanzamientos,
                'semilla': self.semilla_random
            })
            
            return True
            
        except Exception as e:
            print(f"Error en simulación vectorizada: {e}")
            return False
    
    def simular_dados(self, lanzamientos: int, num_dados: int) -> bool:
        """Simulación tradicional (fallback si numpy falla)"""
        try:
            resultados = []
            resultados_detallados = []
            
            for i in range(lanzamientos):
                lanzamiento = [random.randint(1, 6) for _ in range(num_dados)]
                seises_count = lanzamiento.count(6)
                
                resultados.append(seises_count)
                resultados_detallados.append({
                    'lanzamiento': i + 1,
                    'dados': lanzamiento.copy(),
                    'seises': seises_count
                })
            
            # Guardar resultados
            if num_dados == 1:
                self.resultados_1_dado.extend([r['dados'][0] for r in resultados_detallados])
                self.resultados_detallados["1"].extend(resultados_detallados)
                self.total_lanzamientos["1"] += lanzamientos
            elif num_dados == 2:
                self.resultados_2_dados.extend(resultados)
                self.resultados_detallados["2"].extend(resultados_detallados)
                self.total_lanzamientos["2"] += lanzamientos
            elif num_dados == 3:
                self.resultados_3_dados.extend(resultados)
                self.resultados_detallados["3"].extend(resultados_detallados)
                self.total_lanzamientos["3"] += lanzamientos
            
            return True
            
        except Exception as e:
            print(f"Error en simulación tradicional: {e}")
            return False
    
   
    def limpiar_resultados(self):
        """Limpia todos los resultados almacenados"""
        self.resultados_1_dado = []
        self.resultados_2_dados = []
        self.resultados_3_dados = []
        self.resultados_detallados = {"1": [], "2": [], "3": []}
        self.total_lanzamientos = {"1": 0, "2": 0, "3": 0}
        self.historial_simulaciones = []
    
    def exportar_resultados(self, archivo: str) -> bool:
        """Exporta resultados a archivo JSON"""
        try:
            datos = {
                'resultados_1_dado': self.resultados_1_dado[-1000:],  # Limitar para tamaño
                'resultados_2_dados': self.resultados_2_dados[-1000:],
                'resultados_3_dados': self.resultados_3_dados[-1000:],
                'total_lanzamientos': self.total_lanzamientos,
                'historial_simulaciones': self.historial_simulaciones,
                'timestamp_exportacion': datetime.now().isoformat()
            }
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exportando resultados: {e}")
            return False
    
    def analizar_un_dado(self) -> str:
        """Análisis mejorado para 1 dado con estadísticas avanzadas"""
        if not self.resultados_1_dado:
            return ""
            
        contador = Counter(self.resultados_1_dado)
        total = len(self.resultados_1_dado)
        prob_teoricas = self.calcular_probabilidades_teoricas(1)
        estadisticas = self.calcular_estadisticas_avanzadas(self.resultados_1_dado)
        
        texto = f" ANÁLISIS AVANZADO DE 1 DADO ({total:,} lanzamientos)\n"
        texto += "═" * 70 + "\n"
        
        # Distribución básica
        texto += " DISTRIBUCIÓN DE RESULTADOS:\n"
        texto += "─" * 50 + "\n"
        
        for i in range(1, 7):
            count = contador.get(i, 0)
            prob_exp = count / total if total > 0 else 0
            prob_teo = prob_teoricas[f"sacar_{i}"]
            texto += f"   Cara {i}: {count:6,} | Exp: {prob_exp:.4f} | Teó: {prob_teo:.4f}\n"
        
        # Estadísticas descriptivas
        texto += f"\n ESTADÍSTICAS DESCRIPTIVAS:\n"
        texto += "─" * 50 + "\n"
        texto += f"   Media:               {estadisticas['media']:.3f}\n"
        texto += f"   Mediana:             {estadisticas['mediana']:.3f}\n"
        texto += f"   Moda:                {estadisticas['moda']:.0f}\n"
        texto += f"   Desviación estándar: {estadisticas['desviacion_estandar']:.3f}\n"
        texto += f"   Varianza:            {estadisticas['varianza']:.3f}\n"
        
        # Probabilidad específica de 6
        seises = contador.get(6, 0)
        prob_6_exp = seises / total if total > 0 else 0
        prob_6_teo = 1/6
        
        texto += f"\n ANÁLISIS ESPECÍFICO DEL 6:\n"
        texto += "─" * 50 + "\n"
        texto += f"   Experimental: {prob_6_exp:.4f} ({prob_6_exp*100:.2f}%) - {seises:,} casos\n"
        texto += f"   Teórica:      {prob_6_teo:.4f} ({prob_6_teo*100:.2f}%)\n"
        texto += f"   Diferencia:   {abs(prob_6_exp - prob_6_teo):.4f}\n"
        
        # Evaluación de la convergencia
        if total >= 1000:
            diferencia_relativa = abs(prob_6_exp - prob_6_teo) / prob_6_teo
            if diferencia_relativa < 0.05:
                texto += f"    Excelente convergencia (diff < 5%)\n"
            elif diferencia_relativa < 0.10:
                texto += f"    Buena convergencia (diff < 10%)\n"
            else:
                texto += f"    Convergencia moderada (diff ≥ 10%)\n"
        
        texto += "\n"
        return texto

    
    def analizar_dos_dados(self) -> str:
        """Análisis mejorado para 2 dados"""
        if not self.resultados_2_dados:
            return ""
            
        contador = Counter(self.resultados_2_dados)
        total = len(self.resultados_2_dados)
        prob_teoricas = self.calcular_probabilidades_teoricas(2)
        estadisticas = self.calcular_estadisticas_avanzadas(self.resultados_2_dados)
        
        texto = f" ANÁLISIS AVANZADO DE 2 DADOS ({total:,} lanzamientos)\n"
        texto += "═" * 70 + "\n"
        
        texto += " DISTRIBUCIÓN DE NÚMERO DE 6:\n"
        texto += "─" * 50 + "\n"
        
        for i in range(3):
            count = contador.get(i, 0)
            prob_exp = count / total if total > 0 else 0
            prob_teo = prob_teoricas[f"{i}_seises"]
            
            texto += f"   {i} seises: {count:6,} | Exp: {prob_exp:.4f} | Teó: {prob_teo:.4f}\n"
        
        # Estadísticas descriptivas
        texto += f"\n ESTADÍSTICAS DESCRIPTIVAS:\n"
        texto += "─" * 50 + "\n"
        texto += f"   Media de 6 por lanzamiento: {estadisticas['media']:.3f}\n"
        texto += f"   Desviación estándar:        {estadisticas['desviacion_estandar']:.3f}\n"
        
        # Análisis de probabilidades compuestas
        al_menos_uno = sum(contador.get(i, 0) for i in range(1, 3))
        prob_al_menos_uno_exp = al_menos_uno / total if total > 0 else 0
        prob_al_menos_uno_teo = prob_teoricas["al_menos_1_seis"]
        
        texto += f"\n EVENTOS COMPUESTOS:\n"
        texto += "─" * 50 + "\n"
        texto += f"   Al menos 1 seis:\n"
        texto += f"     Experimental: {prob_al_menos_uno_exp:.4f} ({prob_al_menos_uno_exp*100:.2f}%)\n"
        texto += f"     Teórica:      {prob_al_menos_uno_teo:.4f} ({prob_al_menos_uno_teo*100:.2f}%)\n"
        texto += f"     Diferencia:   {abs(prob_al_menos_uno_exp - prob_al_menos_uno_teo):.4f}\n"
        
        texto += "\n"
        return texto
    
    def analizar_tres_dados(self) -> str:
        """Análisis mejorado para 3 dados"""
        if not self.resultados_3_dados:
            return ""
            
        contador = Counter(self.resultados_3_dados)
        total = len(self.resultados_3_dados)
        prob_teoricas = self.calcular_probabilidades_teoricas(3)
        estadisticas = self.calcular_estadisticas_avanzadas(self.resultados_3_dados)
        
        texto = f" ANÁLISIS AVANZADO DE 3 DADOS ({total:,} lanzamientos)\n"
        texto += "═" * 70 + "\n"
        
        texto += " DISTRIBUCIÓN DE NÚMERO DE 6:\n"
        texto += "─" * 50 + "\n"
        
        for i in range(4):
            count = contador.get(i, 0)
            prob_exp = count / total if total > 0 else 0
            prob_teo = prob_teoricas[f"{i}_seises"]
            
            texto += f"   {i} seises: {count:6,} | Exp: {prob_exp:.4f} | Teó: {prob_teo:.4f}\n"
        
        # Estadísticas descriptivas
        texto += f"\n ESTADÍSTICAS DESCRIPTIVAS:\n"
        texto += "─" * 50 + "\n"
        texto += f"   Media de 6 por lanzamiento: {estadisticas['media']:.3f}\n"
        texto += f"   Desviación estándar:        {estadisticas['desviacion_estandar']:.3f}\n"
        texto += f"   Mediana:                    {estadisticas['mediana']:.3f}\n"
        
        # Análisis de eventos raros
        exactamente_tres = contador.get(3, 0)
        prob_tres_exp = exactamente_tres / total if total > 0 else 0
        prob_tres_teo = prob_teoricas["3_seises"]
        
        texto += f"\n ANÁLISIS DE EVENTO RARO (3 seises):\n"
        texto += "─" * 50 + "\n"
        texto += f"   Experimental: {prob_tres_exp:.6f} ({prob_tres_exp*100:.4f}%)\n"
        texto += f"   Teórica:      {prob_tres_teo:.6f} ({prob_tres_teo*100:.4f}%)\n"
        texto += f"   Casos observados: {exactamente_tres:,}\n"
        texto += f"   Casos esperados:  {prob_tres_teo * total:.1f}\n"
        
        if total >= 10000:
            if exactamente_tres > 0:
                texto += f"    Evento raro observado (frecuencia esperada: 1 cada {1/prob_tres_teo:.0f} lanzamientos)\n"
            else:
                texto += f"    Evento raro no observado aún (frecuencia esperada: 1 cada {1/prob_tres_teo:.0f} lanzamientos)\n"
        
        texto += "\n"
        return texto