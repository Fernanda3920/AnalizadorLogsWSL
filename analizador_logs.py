import tkinter as tk
from tkinter import filedialog, scrolledtext

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

# Analiza líneas del log que contengan eventos sospechosos y el filtro de texto
def analizar_log(path, filtro_texto):
    eventos = []
    with open(path, "r", encoding="utf-8", errors="ignore") as archivo:
        for linea in archivo:
            if ("sudo" in linea or "authentication failure" in linea) and filtro_texto.lower() in linea.lower():
                icono = clasificar_evento(linea)
                eventos.append(f"{icono} {linea.strip()}")
    return eventos

# Selecciona archivo y analiza según el filtro
def seleccionar_archivo():
    path = filedialog.askopenfilename(title="Selecciona un archivo de log")
    if path:
        filtro = variable_texto.get().strip()
        eventos = analizar_log(path, filtro)
        resultado.delete("1.0", tk.END)  
        if eventos:
            resultado.insert(tk.END, "\n".join(eventos))
        else:
            resultado.insert(tk.END, "No se encontraron eventos sospechosos con ese filtro.")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Analizador Forense de Logs")
ventana.geometry("1000x600")
ventana.configure(bg="#ffffff")

mi_label = tk.Label(ventana, text="Analizador forense de Logs")
mi_label.pack()  
variable_texto = tk.StringVar()


textbox = tk.Entry(ventana, textvariable=variable_texto, width=50)
textbox.place(x=18, y=60)
textbox.insert(0, "authentication failure")

# Botón para seleccionar archivo y analizar
boton = tk.Button(ventana, text="Seleccionar archivo de log", command=seleccionar_archivo)
boton.place(x=790, y=50)
boton.configure(bg="#f7f7f7")

# Área de resultados
resultado = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=120, height=28)
resultado.place(x=10, y=90)
resultado.configure(bg="#bbc1d6")

ventana.mainloop()
