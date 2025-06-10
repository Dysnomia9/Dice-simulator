# 🎲 Simulador de Dados - Análisis Probabilístico

Una aplicación de escritorio educativa desarrollada en Python para demostrar conceptos probabilísticos a través de simulaciones interactivas de dados.

## 📋 Características

- **Simulación de 1, 2 o 3 dados** con número configurable de lanzamientos
- **Análisis estadístico avanzado** con comparación teórica vs experimental
- **Visualización gráfica** mediante matplotlib integrado
- **Interfaz gráfica intuitiva** desarrollada con tkinter
- **Análisis de convergencia** según la Ley de los Grandes Números
- **Procesamiento en segundo plano** para mantener la interfaz responsiva
- **Análisis de eventos raros** como obtener múltiples seises

## 🚀 Instalación

### Requisitos del Sistema
- Python 3.7 o superior
- tkinter (generalmente incluido con Python)
- matplotlib
- numpy

### Instalación Automática
```bash
python3 setup.py
```

### Instalación Manual
```bash
pip install matplotlib numpy
```

## 💻 Uso

### Ejecución
```bash
python3 main.py
```

### Funcionalidades Principales
1. **Configurar simulación**: Selecciona número de lanzamientos (1-1,000,000+) y dados (1-3)
2. **Ejecutar análisis**: Haz clic en "SIMULAR" para comenzar
3. **Revisar resultados**: Analiza gráficos y estadísticas detalladas en tiempo real
4. **Comparar datos**: Observa la convergencia experimental hacia valores teóricos

## 🏗️ Arquitectura

### Componentes Principales
- `main.py`: Punto de entrada de la aplicación
- `main_window.py`: Interfaz gráfica y controlador principal
- `dice_simulator.py`: Motor de simulación y análisis estadístico
- `graph_manager.py`: Sistema de visualización con matplotlib

### Patrón de Diseño
Implementa un patrón Modelo-Vista-Controlador adaptado para aplicaciones de escritorio con procesamiento en segundo plano mediante threading.

## 📊 Análisis Disponibles

- **Distribución de resultados** por número de dados
- **Estadísticas descriptivas** (media, mediana, moda, desviación estándar)
- **Análisis específico del 6** con evaluación de convergencia
- **Comparación visual** teórica vs experimental
- **Análisis de frecuencias** detallado para cada configuración
- **Visualización en tiempo real** durante la simulación

## 🛠️ Desarrollo

### Estructura del Proyecto
```
dice-simulator/
├── main.py                 # Entrada principal
├── main_window.py          # Interfaz gráfica
├── dice_simulator.py       # Motor de simulación
├── graph_manager.py        # Visualización
├── setup.py               # Script de configuración
└── README.md              # Documentación
```

### Tecnologías Utilizadas
- **GUI**: tkinter con widgets themed (ttk)
- **Computación científica**: numpy para operaciones vectorizadas
- **Visualización**: matplotlib con FigureCanvasTkAgg
- **Threading**: Python threading para procesamiento no bloqueante
- **Análisis**: collections.Counter para conteo de frecuencias

## 📈 Conceptos Educativos

- **Ley de los Grandes Números**: Convergencia experimental hacia valores teóricos
- **Probabilidad teórica vs experimental**: Comparación directa de resultados
- **Análisis estadístico**: Estadísticas descriptivas y análisis de distribuciones
- **Eventos raros**: Observación de probabilidades bajas (ej: tres seises consecutivos)
- **Distribuciones de probabilidad**: Visualización de patrones estadísticos

## 🎯 Casos de Uso Educativos

### Para Estudiantes
- Comprensión visual de conceptos probabilísticos
- Observación práctica de la convergencia estadística
- Análisis de diferencias entre teoría y práctica

### Para Profesores
- Herramienta de demostración en clases de estadística
- Generación de ejemplos prácticos de probabilidad
- Análisis comparativo de diferentes escenarios

### Para Investigadores
- Validación de modelos probabilísticos básicos
- Generación de datos de prueba para análisis estadísticos
- Demostración de conceptos teóricos

## 🚀 Rendimiento

- **Simulaciones pequeñas** (1,000 lanzamientos): < 1 segundo
- **Simulaciones medianas** (100,000 lanzamientos): 1-5 segundos
- **Simulaciones grandes** (1,000,000+ lanzamientos): Optimizado con numpy

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

### Mejoras Sugeridas
- [ ] Soporte para dados con más caras (d8, d10, d20)
- [ ] Exportación de resultados a CSV/Excel
- [ ] Análisis de secuencias y patrones
- [ ] Comparación entre múltiples simulaciones
- [ ] Interfaz más moderna con themes personalizables

## 📄 Licencia

Este proyecto es de uso libre y está disponible bajo licencia de código abierto. Puedes usarlo, modificarlo y distribuirlo libremente.

## 👨‍💻 Autor

**Ignacio Contreras Norambuena**

Desarrollado como herramienta educativa para la enseñanza de conceptos probabilísticos y estadísticos. en Matematica Aplicada II

---