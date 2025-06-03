import re
from datetime import datetime

def extraer_ip(linea):
    """Extrae una dirección IP de una línea de log"""
    ip_match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', linea)
    return ip_match.group(0) if ip_match else None

def extraer_timestamp(linea):
    """Intenta extraer un timestamp de la línea de log"""
    try:
        # Ajusta este patrón según el formato de tus logs
        date_match = re.search(r'([A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', linea)
        if date_match:
            date_str = date_match.group(1)
            return datetime.strptime(date_str, '%b %d %H:%M:%S').replace(year=datetime.now().year)
    except ValueError:
        pass
    return None

def detectar_intentos_login_fallidos(logs, umbral=5):
    """Detecta múltiples intentos de login fallidos desde una misma IP"""
    patron = r'Failed password|authentication failure'
    intentos = {}
    
    for linea in logs:
        if re.search(patron, linea, re.IGNORECASE):
            ip = extraer_ip(linea)
            if ip:
                intentos[ip] = intentos.get(ip, 0) + 1
    
    return [f"Intento de brute force detectado: {ip} ({count} intentos)" 
            for ip, count in intentos.items() if count >= umbral]

def detectar_brute_force(logs, ventana_minutos=5, umbral=10):
    """Detecta muchos intentos en un periodo corto de tiempo"""
    eventos = []
    patron = r'Failed password|authentication failure'
    eventos_fallidos = []
    
    # Primero recolectamos todos los eventos fallidos con sus timestamps
    for linea in logs:
        if re.search(patron, linea, re.IGNORECASE):
            ts = extraer_timestamp(linea)
            ip = extraer_ip(linea)
            if ts and ip:
                eventos_fallidos.append((ts, ip, linea.strip()))
    
    # Analizamos los eventos en ventanas de tiempo
    for i, (ts, ip, linea) in enumerate(eventos_fallidos):
        contador = 1
        for j in range(i+1, len(eventos_fallidos)):
            ts_j, ip_j, linea_j = eventos_fallidos[j]
            if ip_j == ip and (ts_j - ts).total_seconds() <= ventana_minutos*60:
                contador += 1
            else:
                break
        
        if contador >= umbral:
            eventos.append(f"Posible ataque brute force desde {ip}: {contador} intentos en {ventana_minutos} minutos - {linea}")
    
    return eventos

def detectar_accesos_horarios_inesperados(logs, hora_inicio=8, hora_fin=20):
    """Detecta accesos fuera del horario laboral normal"""
    eventos = []
    patron = r'accepted password|session opened'
    
    for linea in logs:
        if re.search(patron, linea, re.IGNORECASE):
            timestamp = extraer_timestamp(linea)
            if timestamp and (timestamp.hour < hora_inicio or timestamp.hour > hora_fin):
                ip = extraer_ip(linea) or "IP desconocida"
                eventos.append(f"Acceso en horario inusual ({timestamp.time()}): {ip} - {linea.strip()}")
    
    return eventos

def detectar_ips_sospechosas(logs):
    """Detecta IPs de rangos conocidos como sospechosos"""
    eventos = []
    rangos_sospechosos = [
        r'10\.',        # IPs internas
        r'192\.168\.',  # IPs internas
        r'172\.(1[6-9]|2[0-9]|3[0-1])\.',  # IPs internas
        r'^(?!66\.249\.).*googlebot\.com$',  # Fake Googlebots
        r'127\.0\.0\.1',                    # Localhost
        r'0\.0\.0\.0'                       # Dirección no enrutable
    ]
    
    for linea in logs:
        ip = extraer_ip(linea)
        if ip:
            for rango in rangos_sospechosos:
                if re.search(rango, ip):
                    eventos.append(f"IP sospechosa detectada: {ip} - {linea.strip()}")
                    break
    
    return eventos

def detectar_errores_servicio(logs):
    """Detecta errores críticos de servicios"""
    patrones = [
        r'error',
        r'failed',
        r'segmentation fault',
        r'core dumped',
        r'permission denied',
        r'stack overflow',
        r'critical',
        r'emergency',
        r'alert'
    ]
    
    eventos = []
    for linea in logs:
        linea = linea.strip()
        if any(re.search(patron, linea, re.IGNORECASE) for patron in patrones):
            eventos.append(linea)
    
    return eventos

def analizar_log(path, filtro=""):
    """Función principal para analizar el archivo de log"""
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lineas = file.readlines()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='latin-1') as file:
            lineas = file.readlines()
    
    eventos_sospechosos = []
    
    # Análisis básico por filtro
    if filtro.strip():
        eventos_sospechosos.extend(
            linea.strip() for linea in lineas 
            if filtro.lower() in linea.lower()
        )
    
    # Añadir más análisis automáticos
    funciones_analisis = [
        detectar_intentos_login_fallidos,
        detectar_brute_force,
        detectar_accesos_horarios_inesperados,
        detectar_ips_sospechosas,
        detectar_errores_servicio
    ]
    
    for funcion in funciones_analisis:
        try:
            eventos_sospechosos.extend(funcion(lineas))
        except Exception as e:
            print(f"Error en {funcion.__name__}: {str(e)}")
    
    # Eliminar duplicados manteniendo el orden
    eventos_unicos = []
    visto = set()
    for evento in eventos_sospechosos:
        if evento not in visto:
            visto.add(evento)
            eventos_unicos.append(evento)
    
    return eventos_unicos