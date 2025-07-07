# Calculadora VLSM - Profe Pedro

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Esta es una **Calculadora Avanzada de Subredes VLSM** diseñada para estudiantes de redes que necesitan calcular subredes de longitud variable (VLSM) de manera eficiente. El programa toma una IP base, un prefijo CIDR y los requerimientos de hosts para cada subred, y genera una tabla detallada con la asignación de subredes, máscaras, direcciones de red, hosts, broadcast y más. Los resultados se exportan automáticamente a un archivo CSV para facilitar su uso.

Desarrollado por **Profe Pedro** para apoyar el aprendizaje de conceptos de redes.

## Características
- Calcula subredes VLSM optimizando el uso del espacio de direcciones.
- Valida entradas de IP y prefijos CIDR.
- Muestra resultados en una tabla clara usando `tabulate`.
- Exporta resultados a un archivo CSV (`vlsm_resultados.csv`).
- Incluye colores en la consola para mejor legibilidad (usando `colorama`).
- Proporciona sugerencias si el espacio de direcciones es insuficiente.
- Soporta múltiples cálculos consecutivos.

## Requisitos

Para ejecutar la calculadora, necesitas tener instalado:
- **Python 3.6 o superior** (el módulo `ipaddress` está incluido en la biblioteca estándar).
- Las librerías `tabulate` y `colorama` para la tabla y colores en la consola.

### Instalación de Requisitos

1. **Instala Python**:
   - Descarga e instala Python desde [python.org](https://www.python.org/downloads/). Asegúrate de marcar la opción "Add Python to PATH" durante la instalación.
   - Verifica la instalación ejecutando en la terminal:
     ```bash
     python --version
     ```

2. **Instala las dependencias**:
   - Abre una terminal (Command Prompt, PowerShell, o terminal de Linux/Mac).
   - Instala las librerías necesarias con `pip`:
     ```bash
     pip install tabulate colorama
     ```

3. **Clona o descarga el repositorio**:
   - Si tienes Git instalado, clona el repositorio:
     ```bash
     git clone https://github.com/pedrorojas/vlsm-calculator.git
     ```
   - Alternativamente, descarga el código como ZIP desde GitHub y descomprímelo.

4. **Navega al directorio del proyecto**:
   ```bash
   cd vlsm-calculator
