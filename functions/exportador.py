from textwrap import wrap

def exportar_pdf_contenido(contenido):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from tkinter import messagebox
    from tkinter.filedialog import asksaveasfilename
    import getpass
    import os
    from datetime import datetime

    if not contenido.strip():
        messagebox.showwarning("Aviso", "No hay contenido para exportar.")
        return

    path_pdf = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not path_pdf:
        return

    c = canvas.Canvas(path_pdf, pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin

    user = getpass.getuser()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, f"Exportado por: {user} - Fecha: {fecha}")
    y -= 20

    c.setFont("Helvetica", 10)
    line_height = 14
    max_chars_per_line = 120  # Ajusta este valor según el tamaño de fuente

    for linea in contenido.splitlines():
        lineas_envueltas = wrap(linea, width=max_chars_per_line)
        for sublinea in lineas_envueltas:
            if y <= margin:
                c.showPage()
                y = height - margin
                c.setFont("Helvetica", 10)
            c.drawString(margin, y, sublinea)
            y -= line_height

    c.save()
    messagebox.showinfo("Éxito", f"Informe exportado exitosamente a:\n{os.path.abspath(path_pdf)}")
