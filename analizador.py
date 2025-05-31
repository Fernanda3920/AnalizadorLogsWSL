
from clasificador_logs import clasificar_evento

def analizar_log(path, filtro_texto):
    eventos = []
    filtros = [f.strip().lower() for f in filtro_texto.split(",")]
    with open(path, "r", encoding="utf-8", errors="ignore") as archivo:
        for linea in archivo:
            if any(f in linea.lower() for f in filtros) and ("sudo" in linea or "authentication failure" in linea):
                icono = clasificar_evento(linea)
                eventos.append(f"{icono} {linea.strip()}")
    return eventos
