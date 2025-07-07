import ipaddress
import math
import re
import csv
from tabulate import tabulate
from colorama import init, Fore, Style

# Inicializar colorama para colores en la consola
init()

def mostrar_mensaje(tipo, mensaje):
    """Muestra mensajes con formato y colores según el tipo."""
    colores = {
        "error": Fore.RED,
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW
    }
    print(f"{colores.get(tipo, Fore.WHITE)}{mensaje}{Style.RESET_ALL}")

def es_ip_valida(ip):
    """Valida que la IP ingresada tenga el formato correcto."""
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(pattern, ip) is not None

def validar_entrada():
    """Valida la entrada de IP base y prefijo CIDR."""
    while True:
        try:
            ip_base = input("📥 IP base (ej. 192.168.0.0): ")
            if not es_ip_valida(ip_base):
                raise ValueError("Formato de IP inválido")
            mascara_base = int(input("🧮 Prefijo CIDR base (ej. 24): "))
            if mascara_base < 8 or mascara_base > 30:
                raise ValueError("El prefijo CIDR debe estar entre 8 y 30")
            red_original = ipaddress.IPv4Network(f"{ip_base}/{mascara_base}", strict=False)
            return red_original, mascara_base
        except ValueError as e:
            mostrar_mensaje("error", f"Error: {e}. Por favor ingrese valores válidos.")

def obtener_requerimientos():
    """Solicita el número de subredes y hosts necesarios."""
    while True:
        try:
            n_subredes = int(input("🔢 ¿Cuántas subredes necesitas?: "))
            if n_subredes <= 0:
                mostrar_mensaje("error", "Debe ser al menos 1 subred")
                continue
            break
        except ValueError:
            mostrar_mensaje("error", "Ingrese un número entero válido")
    
    requerimientos = []
    for i in range(n_subredes):
        while True:
            try:
                h = int(input(f"👥 Hosts necesarios para subred #{i+1}: "))
                if h <= 0:
                    mostrar_mensaje("warning", "Debe ser al menos 1 host. Usando valor mínimo 1")
                    h = 1
                requerimientos.append(h)
                break
            except ValueError:
                mostrar_mensaje("error", "Ingrese un número entero válido")
    return sorted(requerimientos, reverse=True), n_subredes

def verificar_espacio(red_original, requerimientos):
    """Verifica si hay suficiente espacio para las subredes."""
    total_hosts = sum(req + 2 for req in requerimientos)  # +2 por red y broadcast
    espacio_disponible = red_original.num_addresses
    if total_hosts > espacio_disponible:
        mostrar_mensaje("error", f"Espacio insuficiente: {total_hosts} hosts requeridos vs {espacio_disponible} disponibles")
        bits_needed = math.ceil(math.log2(total_hosts))
        nuevo_prefijo = 32 - bits_needed
        mostrar_mensaje("info", f"📝 Sugerencia: Use un prefijo /{nuevo_prefijo} para soportar {total_hosts} hosts")
        return False
    return True

def exportar_a_csv(subredes, nombre_archivo="vlsm_resultados.csv"):
    """Exporta los resultados de las subredes a un archivo CSV."""
    columnas = ["Subred", "Dirección Red", "Máscara", "Wildcard", "Prefijo", 
                "Primer Host", "Último Host", "Broadcast", "Hosts Útiles"]
    with open(nombre_archivo, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(subredes)
    mostrar_mensaje("success", f"📁 Resultados exportados a {nombre_archivo}")

def calcular_vlsm():
    """Calcula las subredes VLSM y muestra los resultados."""
    print("\n" + "═"*55)
    print("🧮 CALCULADORA AVANZADA DE SUBREDES VLSM - PROFE PEDRO")
    print("═"*55 + "\n")
    
    # Obtener entrada
    red_original, mascara_base = validar_entrada()
    requerimientos, n_subredes = obtener_requerimientos()
    
    # Verificar espacio disponible
    if not verificar_espacio(red_original, requerimientos):
        return
    
    # Calcular subredes
    siguiente_ip = red_original.network_address
    subredes = []
    espacio_total_utilizado = 0
    error_asignacion = False

    for i, h in enumerate(requerimientos):
        # Calcular prefijo necesario
        bits_host = math.ceil(math.log2(h + 2))  # +2 por red y broadcast
        nuevo_prefijo = 32 - bits_host
        
        # Validar prefijo
        if nuevo_prefijo <= mascara_base:
            mostrar_mensaje("error", f"Subred {i+1}: Prefijo /{nuevo_prefijo} inválido (debe ser mayor que /{mascara_base})")
            error_asignacion = True
            break
        if nuevo_prefijo > 30:
            mostrar_mensaje("warning", f"Subred {i+1}: Prefijo /{nuevo_prefijo} no permitido. Usando máximo /30")
            nuevo_prefijo = 30
        
        try:
            # Crear subred
            subred = ipaddress.IPv4Network((siguiente_ip, nuevo_prefijo), strict=False)
            
            # Verificar que esté dentro de la red base
            if not red_original.supernet_of(subred):
                mostrar_mensaje("error", f"Subred {i+1} excede rango base: {subred}")
                error_asignacion = True
                break
            
            # Calcular hosts y wildcard
            primer_host = subred.network_address + 1
            ultimo_host = subred.broadcast_address - 1
            wildcard = ipaddress.IPv4Address(int(ipaddress.IPv4Address('255.255.255.255')) - int(subred.netmask))
            hosts_utiles = subred.num_addresses - 2
            espacio_total_utilizado += subred.num_addresses
            
            subredes.append({
                "Subred": f"Sub-{i+1}",
                "Dirección Red": str(subred.network_address),
                "Máscara": str(subred.netmask),
                "Wildcard": str(wildcard),
                "Prefijo": f"/{nuevo_prefijo}",
                "Primer Host": str(primer_host),
                "Último Host": str(ultimo_host),
                "Broadcast": str(subred.broadcast_address),
                "Hosts Útiles": hosts_utiles
            })
            
            # Actualizar siguiente IP
            siguiente_ip = subred.broadcast_address + 1
            
            # Verificar fin de espacio
            if siguiente_ip > red_original.broadcast_address:
                mostrar_mensaje("warning", f"Espacio agotado en subred #{i+1}")
                break
                
        except Exception as e:
            mostrar_mensaje("error", f"Error crítico en subred #{i+1}: {str(e)}")
            error_asignacion = True
            break

    # Mostrar resultados
    if subredes and not error_asignacion:
        print("\n" + "═"*50)
        print("📊 REPORTE DETALLADO DE ASIGNACIÓN VLSM")
        print("═"*50)
        
        # Estadísticas generales
        espacio_total = red_original.num_addresses
        porcentaje_utilizado = (espacio_total_utilizado / espacio_total) * 100
        hosts_asignados = sum(s['Hosts Útiles'] for s in subredes)
        hosts_solicitados = sum(requerimientos)
        
        mostrar_mensaje("success", f"\n🔹 Red base: {red_original}")
        mostrar_mensaje("info", f"🔹 Subredes asignadas: {len(subredes)}/{n_subredes}")
        mostrar_mensaje("info", f"🔹 Hosts solicitados: {hosts_solicitados}")
        mostrar_mensaje("info", f"🔹 Hosts asignados: {hosts_asignados}")
        mostrar_mensaje("info", f"🔹 Espacio utilizado: {espacio_total_utilizado}/{espacio_total} ({porcentaje_utilizado:.2f}%)")
        
        # Mostrar tabla
        print("\n📋 TABLA DE SUBREDES:")
        columnas = ["Subred", "Dirección Red", "Máscara", "Wildcard", 
                    "Prefijo", "Primer Host", "Último Host", 
                    "Broadcast", "Hosts Útiles"]
        
        tabla_datos = [[sub[col] for col in columnas] for sub in subredes]
        print(tabulate(tabla_datos, headers=columnas, tablefmt="grid", stralign="center", numalign="center"))
        
        # Exportar a CSV
        exportar_a_csv(subredes)
        
        # Mostrar subredes no asignadas
        if len(subredes) < n_subredes:
            print("\n⚠️ SUBREDES NO ASIGNADAS:")
            for i in range(len(subredes), n_subredes):
                mostrar_mensaje("warning", f"  • Subred #{i+1}: {requerimientos[i]} hosts")
    else:
        mostrar_mensaje("error", "No se pudo asignar ninguna subred. Revise los parámetros.")

def desea_continuar():
    """Pregunta si el usuario desea continuar calculando otra red."""
    while True:
        respuesta = input("\n¿Desea calcular otra red? (s/n): ").lower()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        elif respuesta in ['n', 'no']:
            return False
        mostrar_mensaje("error", "Por favor, ingrese 's' o 'n'")

if __name__ == "__main__":
    while True:
        calcular_vlsm()
        if not desea_continuar():
            mostrar_mensaje("success", "\n¡Gracias por usar la calculadora VLSM! 👋")
            mostrar_mensaje("success", "Atte. Profe Pedro")
            break