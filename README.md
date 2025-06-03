# 🛡️ Analizador de Logs

**Analizador de Logs** es una herramienta forense diseñada para ayudarte a inspeccionar archivos de registro del sistema y detectar posibles amenazas de seguridad. Analiza eventos críticos y muestra comportamientos anómalos o sospechosos en tus logs.

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

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/analizador-logs.git
   cd analizador-logs
