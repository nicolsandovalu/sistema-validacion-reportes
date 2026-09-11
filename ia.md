# Uso de Inteligencia Artificial Ev.2

1. **Herramienta utilizada:** Gemini.
2. **Consulta textual:** "Genera la estructura de base de datos para mi modelo de profesores en models.py con borrado lógico, e implementa el decorador para restringir el acceso a la subida de archivos CSV por roles."
3. **Corrección aplicada:** La IA inicialmente sugirió guardar las credenciales en un modelo propio y usar `EMAIL_BACKEND` que generaba conflictos con `MAILERS`. Corregí la implementación para usar exclusivamente el sistema de autenticación nativo de Django y modifiqué el diccionario de configuración en `settings.py` para imprimir los correos en consola sin romper el servidor.



# Uso de IA en el Proyecto (Evaluación ES1)

**1. **Herramienta usada y propósito:**
   Utilicé Gemini (Google) como asistente de programación para estructurar el proyecto cumpliendo estrictamente con la rúbrica de la ES1. La consulté para redactar el apartado de negocio, diseñar la regla lógica de 4 resultados y resolver errores de configuración en Django.

**2. Qué se consultó a la herramienta de IA:**
- Consulté cómo solucionar el error `ModuleNotFoundError: No module named 'core'` que bloqueaba la consola al intentar ejecutar `python manage.py startapp core`.
- Consulté el motivo del error `ModuleNotFoundError: No module named 'miproyecto'` que apareció al intentar levantar el servidor con `runserver`.
- Pedí sugerencias para estructurar el formulario HTML interactivo y simular la validación con un diccionario en lugar de quemar un solo token en el código.

**3. Qué corregí a partir de las respuestas:**
- **Corrección de carga de App:** Comprendí que el error de 'core' se daba por el orden de ejecución de Django. Fui a `settings.py`, borré temporalmente `'core'` de `INSTALLED_APPS`, ejecuté el comando `startapp` con éxito y luego volví a registrar la aplicación.
- **Corrección de rutas de configuración:** Para el error de `runserver`, identifiqué que mi carpeta interna se llamaba `proyecto` pero Django buscaba `miproyecto`. Modifiqué manualmente las variables `ROOT_URLCONF = 'proyecto.urls'` y `WSGI_APPLICATION = 'proyecto.wsgi.application'` en el archivo `settings.py` para sincronizar los nombres, logrando que el servidor levantara.
- **Corrección de Lógica:** Reemplacé la validación estática en `solucion.py` por un diccionario (`TOKENS_AUTORIZADOS`), actualizando los condicionales `if/elif` para validar el token contra esta nueva estructura.