# Calculadora VLSM - Profe Pedro

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Bienvenidos a la **Calculadora Avanzada de Subredes VLSM**, una herramienta en Python diseñada para estudiantes de redes que necesitan calcular subredes de longitud variable (VLSM) de manera eficiente. Este programa optimiza la asignación de direcciones IP, generando una tabla detallada con direcciones de red, máscaras, hosts, broadcast y más. Los resultados se exportan a un archivo CSV para facilitar su uso.

Desarrollado por **Profe Pedro** para apoyar el aprendizaje de conceptos de redes en el aula.

## Características
- Calcula subredes VLSM optimizando el espacio de direcciones según los requerimientos de hosts.
- Valida entradas de IP y prefijos CIDR para evitar errores.
- Genera una tabla clara con `tabulate`, mostrando:
  - Dirección de red
  - Máscara de subred
  - Máscara wildcard
  - Prefijo CIDR
  - Primer y último host
  - Dirección de broadcast
  - Hosts útiles
- Exporta resultados a `vlsm_resultados.csv`.
- Usa colores en la consola con `colorama` para una mejor experiencia.
- Sugiere prefijos alternativos si el espacio es insuficiente.
- Permite realizar múltiples cálculos consecutivos.

## Requisitos

Para ejecutar la calculadora, necesitas:
- **Python 3.6 o superior** (incluye el módulo `ipaddress` por defecto).
- Librerías Python: `tabulate` y `colorama`.

### Instalación de Requisitos

1. **Instala Python**:
   - Descarga Python desde [python.org](https://www.python.org/downloads/).
   - Marca "Add Python to PATH" durante la instalación.
   - Verifica la instalación en una terminal:
     ```bash
     python --version
     ```

2. **Instala las dependencias**:
   - En una terminal, ejecuta:
     ```bash
     pip install tabulate colorama
     ```

3. **Clona o descarga el repositorio**:
   - **Opción 1: Clonar con Git**:
     - Clona el repositorio:
       ```bash
       git clone https://github.com/profepedrorojas/Calculadora_VLSM.git
       ```
     - Esto creará una carpeta llamada `Calculadora_VLSM`.
   - **Opción 2: Descargar como ZIP**:
     - Descarga el ZIP desde la página de GitHub.
     - Descomprime el archivo. La carpeta se llamará `Calculadora_VLSM-main`.
     - (Opcional) Renombra la carpeta a `Calculadora_VLSM` para consistencia:
       ```bash
       mv Calculadora_VLSM-main Calculadora_VLSM
       ```

4. **Navega al directorio del proyecto**:
   ```bash
   cd Calculadora_VLSM
   
5. **Ejecuta la aplicación**:
   ```bash
   python vlsm.py
   
