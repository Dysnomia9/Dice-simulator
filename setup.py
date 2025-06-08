#!/usr/bin/env python3
"""
Script de configuración para el Simulador de Dados
Instala las dependencias necesarias y verifica el entorno
"""

import sys
import subprocess
import importlib

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 6):
        print(" Error: Se requiere Python 3.6 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - Versión correcta")
    return True

def check_and_install_packages():
    """Verificar e instalar paquetes necesarios"""
    required_packages = {
        'tkinter': 'tkinter',
        'matplotlib': 'matplotlib',
        'numpy': 'numpy'  # matplotlib lo requiere
    }
    
    print("\n🔍 Verificando dependencias...")
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            importlib.import_module(import_name)
            print(f"✅ {package_name} - Instalado")
        except ImportError:
            print(f"❌ {package_name} - No encontrado")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n📦 Instalando paquetes faltantes: {', '.join(missing_packages)}")
        for package in missing_packages:
            if package == 'tkinter':
                print("⚠️  tkinter generalmente viene con Python.")
                print("   En Ubuntu/Debian: sudo apt-get install python3-tk")
                print("   En CentOS/RHEL: sudo yum install tkinter")
                continue
            
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ {package} instalado correctamente")
            except subprocess.CalledProcessError:
                print(f"❌ Error instalando {package}")
                return False
    
    return True

def create_directory_structure():
    """Crear estructura de directorios si no existe"""
    import os
    
    directories = ['gui']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Creado directorio: {directory}")
        else:
            print(f"📁 Directorio existe: {directory}")

def main():
    """Función principal de configuración"""
    print("🎲 CONFIGURANDO SIMULADOR DE DADOS")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear estructura de directorios
    create_directory_structure()
    
    # Verificar e instalar paquetes
    if not check_and_install_packages():
        print("\n❌ Error durante la instalación de dependencias")
        sys.exit(1)
    
    print("\n🎉 CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
    print("\nPara ejecutar el simulador:")
    print("   python3 main.py")
    print("\nArchivos necesarios:")
    print("   ✓ main.py")
    print("   ✓ dice_simulator.py") 
    print("   ✓ graph_manager.py")
    print("   ✓ gui/main_window.py")
    print("   ✓ gui/__init__.py")

if __name__ == "__main__":
    main()