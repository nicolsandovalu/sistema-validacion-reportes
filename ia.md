# Uso de Inteligencia Artificial Ev.2

* **Herramienta utilizada:** Gemini.
* **Pregunta textual realizada:** "Cómo implementar un sistema de roles y permisos en Django para dos tipos de usuarios (admin y normal) sin usar un campo personalizado en el modelo, y cómo proteger las vistas."
* **Corrección y justificación adoptada:** La IA propuso inicialmente crear un modelo de usuario personalizado (`Custom User Model`) y manejar la seguridad ocultando los botones de la interfaz con etiquetas `{% if %}`. Corregí esta sugerencia descartando el modelo personalizado para utilizar el sistema nativo de `Groups` de Django, ya que resuelve el problema sin sobre-complejizar la base de datos. Además, justifiqué que ocultar botones HTML no brinda seguridad real, por lo que implementé un decorador (`@requiere_rol`) para validar los grupos directamente en el servidor antes de ejecutar las vistas.

