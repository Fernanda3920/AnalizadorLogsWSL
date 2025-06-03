import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import getpass
from functions.exportador import exportar_pdf_contenido
from reportlab.lib.pagesizes import A4
import os
from datetime import datetime
from tkinter import filedialog, scrolledtext, ttk
from analizador import (
    analizar_log,
    detectar_intentos_login_fallidos,
    detectar_brute_force,
    detectar_accesos_horarios_inesperados,
    detectar_ips_sospechosas,
    detectar_errores_servicio
)

class AnalizadorLogsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Forense de Logs")
        self.root.geometry("1100x700")
        self.root.configure(bg="#ffffff")

        self.path_archivo = tk.StringVar()
        self.filtro_texto = tk.StringVar(value="authentication failure")
        self.umbral_login = tk.IntVar(value=5)
        self.umbral_brute = tk.IntVar(value=10)
        self.ventana_brute = tk.IntVar(value=5)
        self.hora_inicio = tk.IntVar(value=8)
        self.hora_fin = tk.IntVar(value=20)

        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        # Frame superior - controles
        frame_controles = tk.Frame(self.root, bg="#fdfdfd", padx=10, pady=10)
        frame_controles.pack(fill=tk.X)
        
        # Título
        tk.Label(frame_controles, text="Analizador Forense de Logs", 
                font=("Arial", 14, "bold"), bg="#fdfdfd").grid(row=0, column=0, columnspan=1, pady=5)
        
        # Entrada de filtro
        tk.Label(frame_controles, text="Filtro básico:", bg="#fdfdfd").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(frame_controles, textvariable=self.filtro_texto, width=40).grid(row=1, column=1, sticky=tk.W)
        
        # Botón seleccionar archivo
        tk.Button(frame_controles, text="Seleccionar archivo", 
                 command=self.seleccionar_archivo).grid(row=1, column=2, padx=10)
        
        # Botón analizar
        tk.Button(frame_controles, text="Analizar", 
                 command=self.analizar_archivo, bg="#4CAF50", fg="white").grid(row=1, column=3)
        
        tk.Button(frame_controles, text="Exportar PDF", 
         command=self.exportar_pdf, bg="#2196F3", fg="white").grid(row=1, column=4, padx=10)
        
        # Frame de opciones de análisis
        frame_opciones = tk.LabelFrame(self.root, text="Opciones de Análisis", 
                                     padx=15, pady=15, bg="#f0f0f0")
        frame_opciones.pack(fill=tk.X, padx=20, pady=10)
        
        # Checkboxes para tipos de análisis
        self.cb_login = tk.IntVar(value=1)
        tk.Checkbutton(frame_opciones, text="Intentos login fallidos", variable=self.cb_login, 
                      bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W)
        tk.Label(frame_opciones, text="Umbral:", bg="#f0f0f0").grid(row=0, column=1, sticky=tk.W)
        tk.Spinbox(frame_opciones, from_=1, to=50, width=3, 
                  textvariable=self.umbral_login).grid(row=0, column=2, sticky=tk.W)
                  
        
        self.cb_brute = tk.IntVar(value=1)
        tk.Checkbutton(frame_opciones, text="Detección brute force", variable=self.cb_brute, 
                      bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W)
        tk.Label(frame_opciones, text="Umbral:", bg="#f0f0f0").grid(row=1, column=1, sticky=tk.W)
        tk.Spinbox(frame_opciones, from_=1, to=50, width=3, 
                  textvariable=self.umbral_brute).grid(row=1, column=2, sticky=tk.W)
        tk.Label(frame_opciones, text="Ventana (min):", bg="#f0f0f0").grid(row=1, column=3, sticky=tk.W)
        tk.Spinbox(frame_opciones, from_=1, to=60, width=3, 
                  textvariable=self.ventana_brute).grid(row=1, column=4, sticky=tk.W)
        
        self.cb_horario = tk.IntVar(value=1)
        tk.Checkbutton(frame_opciones, text="Accesos horario inusual", variable=self.cb_horario, 
                      bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W)
        tk.Label(frame_opciones, text="Hora inicio:", bg="#f0f0f0").grid(row=2, column=1, sticky=tk.W)
        tk.Spinbox(frame_opciones, from_=0, to=23, width=3, 
                  textvariable=self.hora_inicio).grid(row=2, column=2, sticky=tk.W)
        tk.Label(frame_opciones, text="Hora fin:", bg="#f0f0f0").grid(row=2, column=3, sticky=tk.W)
        tk.Spinbox(frame_opciones, from_=0, to=23, width=3, 
                  textvariable=self.hora_fin).grid(row=2, column=4, sticky=tk.W)
        
        self.cb_ips = tk.IntVar(value=1)
        tk.Checkbutton(frame_opciones, text="IPs sospechosas", variable=self.cb_ips, 
                      bg="#f0f0f0").grid(row=3, column=0, sticky=tk.W)
        
        self.cb_errores = tk.IntVar(value=1)
        tk.Checkbutton(frame_opciones, text="Errores de servicio", variable=self.cb_errores, 
                      bg="#f0f0f0").grid(row=4, column=0, sticky=tk.W)
        
        # Frame de resultados
        frame_resultados = tk.Frame(self.root, bg="#ffffff")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Notebook (pestañas) para resultados
        self.notebook = ttk.Notebook(frame_resultados)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de resultados generales
        self.tab_general = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.tab_general, text="Resultados Generales")
        
        self.resultado_general = scrolledtext.ScrolledText(
            self.tab_general, wrap=tk.WORD, width=120, height=25)
        self.resultado_general.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.resultado_general.configure(bg="#f8f8f8", font=("Consolas", 10))
    
        self.tab_stats = tk.Frame(self.notebook, bg="#ffffff")
        self.resultado_stats = scrolledtext.ScrolledText(
            self.tab_stats, wrap=tk.WORD, width=120, height=25)
        self.resultado_stats.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.resultado_stats.configure(bg="#f8f8f8", font=("Consolas", 10))
    
    def seleccionar_archivo(self):
        path = filedialog.askopenfilename(
            title="Selecciona un archivo de log",
            filetypes=[("Archivos de log", "*.log"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if path:
            self.path_archivo.set(path)
            self.actualizar_estado()
    
    def actualizar_estado(self):
        pass  
    
    def analizar_archivo(self):
        if not self.path_archivo.get():
            tk.messagebox.showerror("Error", "Por favor selecciona un archivo primero")
            return
        
        # Limpiar resultados anteriores
        self.resultado_general.delete("1.0", tk.END)
        self.resultado_stats.delete("1.0", tk.END)
        
        # Configurar parámetros de análisis según selección del usuario
        filtro = self.filtro_texto.get().strip()
        
        # Leer el archivo
        try:
            with open(self.path_archivo.get(), 'r', encoding='utf-8') as file:
                lineas = file.readlines()
        except UnicodeDecodeError:
            with open(self.path_archivo.get(), 'r', encoding='latin-1') as file:
                lineas = file.readlines()
        
        # Realizar análisis seleccionados
        resultados = {}
        
        # Análisis básico por filtro
        if filtro:
            resultados["Filtro básico"] = [linea.strip() for linea in lineas if filtro.lower() in linea.lower()]
        
        # Intentos de login fallidos
        if self.cb_login.get():
            umbral = self.umbral_login.get()
            resultados["Login fallidos"] = detectar_intentos_login_fallidos(lineas, umbral)
        
        # Brute force
        if self.cb_brute.get():
            umbral = self.umbral_brute.get()
            ventana = self.ventana_brute.get()
            resultados["Brute force"] = detectar_brute_force(lineas, ventana, umbral)
        
        # Horarios inusuales
        if self.cb_horario.get():
            hora_ini = self.hora_inicio.get()
            hora_fin = self.hora_fin.get()
            resultados["Horarios inusuales"] = detectar_accesos_horarios_inesperados(lineas, hora_ini, hora_fin)
        
        # IPs sospechosas
        if self.cb_ips.get():
            resultados["IPs sospechosas"] = detectar_ips_sospechosas(lineas)
        
        # Errores de servicio
        if self.cb_errores.get():
            resultados["Errores servicio"] = detectar_errores_servicio(lineas)
        
        # Mostrar resultados
        self.mostrar_resultados(resultados)
        
    
    def mostrar_resultados(self, resultados):
        self.resultado_general.insert(tk.END, f"Análisis del archivo: {self.path_archivo.get()}\n")
        self.resultado_general.insert(tk.END, "="*80 + "\n\n")
        
        for categoria, eventos in resultados.items():
            if eventos:
                self.resultado_general.insert(tk.END, f"=== {categoria.upper()} ===\n")
                self.resultado_general.insert(tk.END, "\n".join(eventos) + "\n\n")
        
        if not any(resultados.values()):
            self.resultado_general.insert(tk.END, "No se encontraron eventos sospechosos con los filtros aplicados.")
    
    
    def exportar_pdf(self):
        contenido = self.resultado_general.get("1.0", tk.END)
        if not contenido:
            messagebox.showwarning("Aviso", "No hay contenido para exportar.")
            return
        exportar_pdf_contenido(contenido)

   
# Iniciar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorLogsApp(root)
    root.mainloop()