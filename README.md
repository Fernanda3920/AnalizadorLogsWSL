# 🛡️ Analizador de Logs

**Analizador de Logs** es una herramienta forense diseñada para ayudarte a inspeccionar archivos de registro del sistema y detectar posibles amenazas de seguridad. Analiza eventos críticos y muestra comportamientos anómalos o sospechosos en tus logs.

![TImagen de referencia](https://sweet-soapwort-8eb.notion.site/image/attachment%3A9fe100f1-322d-4234-adee-fe41fe1d83a2%3ACaptura_de_pantalla_2025-05-31_213959.png?table=block&id=205ca25a-4af8-80bd-8db5-cc0897578456&spaceId=94349e37-f0b7-4993-ab2d-1cb2c195b95c&width=1420&userId=&cache=v2)
---

## 🎯 Características Principales

El sistema puede detectar y resaltar las siguientes situaciones:

- 🔍 **Rangos de IP sospechosas**  
  Identifica direcciones IP con actividades inusuales o maliciosas.

- 🕒 **Accesos fuera del horario habitual**  
  Encuentra eventos que ocurren fuera del rango horario definido por el usuario.

- ❌ **Errores del servicio**  
  Clasifica errores del sistema, como caídas, respuestas inválidas o errores 5xx.

- 🛑 **Ataques de fuerza bruta**  
  Detección de múltiples intentos de autenticación en un corto período.

- 🔐 **Intentos de login fallidos**  
  Seguimiento de fallos de inicio de sesión repetitivos.

El resultado del análisis de un archivo extensión log de datos simulados teniendo en cuenta los anteriores puntos se ve de la siguiente manera:

![Puntos](https://sweet-soapwort-8eb.notion.site/image/attachment%3A7672320c-8df0-4984-972a-470c162b090b%3ACaptura_de_pantalla_2025-05-31_214114.png?table=block&id=205ca25a-4af8-8092-8571-ebc23d42a5e6&spaceId=94349e37-f0b7-4993-ab2d-1cb2c195b95c&width=1420&userId=&cache=v2)
---

## 🔎 Filtro y Búsqueda Inteligente

Incluye una barra de búsqueda que permite al usuario filtrar resultados específicos según:

- Fechas (e.g. `2025-05-31`, `24/04/2025`)
- Mensajes de error o advertencia
- Usuarios involucrados
- Puertos o servicios específicos

---

## 🧾 Resultados y Exportación

Los resultados del análisis se presentan en una interfaz clara y estructurada, y se pueden:

- 📄 **Exportar como PDF**  
  El informe incluye el usuario que lo generó y la fecha.

- 🖨️ **Imprimir directamente**  
  Ideal para documentar auditorías o compartir hallazgos.

---

## 🛠️ Instalación

Requisitos previos 
1. Entorno Linux
2. Python instalado
3. Entorno virtual activo

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Fernanda3920/AnalizadorLogsWSL.git
   ```
2. Ejecutar el entorno virutal

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   

