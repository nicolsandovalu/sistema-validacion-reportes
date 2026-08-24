# Uso de IA en el Proyecto (Evaluación ES1)

1. **Herramienta usada y propósito:**
   Utilicé Gemini (Google) como asistente de programación para estructurar el proyecto cumpliendo estrictamente con la rúbrica de la ES1. La consulté para redactar el apartado de negocio, diseñar la regla lógica de 4 resultados y resolver errores de configuración en Django.

2. **Consulta concreta y respuesta:**
   Le pregunté: "Al ejecutar runserver me sale el error ModuleNotFoundError: No module named 'miproyecto'. ¿Qué significa?".
   La IA me respondió que el error ocurría porque mi carpeta interna de configuración se llamaba `proyecto` en lugar de `miproyecto`, y que Django seguía buscando el nombre antiguo en el archivo `settings.py`.

3. **Corrección realizada por mí:**
   La IA me sugirió cambiar las rutas en `settings.py`, pero la solución que yo apliqué fue entender que las variables `ROOT_URLCONF` y `WSGI_APPLICATION` deben coincidir exactamente con el nombre de la carpeta que contiene el archivo `urls.py`. Hice el cambio manualmente en el código a `'proyecto.urls'` y guardé el archivo, lo que permitió que el servidor levantara sin problemas.