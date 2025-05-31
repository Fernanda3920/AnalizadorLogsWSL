import re

# Clasifica la peligrosidad de un evento y devuelve un emoji
def clasificar_evento(linea):
    if "authentication failure" in linea:
        return "[ALTA] "  # Alta
    elif "sudo" in linea and "session opened" not in linea and "session closed" not in linea:
        return "[MEDIA] "  # Media
    elif "session opened" in linea or "session closed" in linea:
        return "[BAJA] "  # Baja
    else:
        return "[NEUTRA] "  # Neutra o sin clasificar