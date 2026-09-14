# Registro de Uso de Inteligencia Artificial (Evaluación 2)

* **Herramienta utilizada:** Gemini.
* **Pregunta textual realizada:** "Necesito implementar un sistema de roles (admin, normal, viewer) para mi aplicación en Django. ¿Cómo configuro los permisos y protejo mis vistas para que solo los usuarios autorizados puedan editar o eliminar registros?"

* **Corrección y justificación adoptada:** 
  La Inteligencia Artificial me entregó una respuesta que contenía dos malas prácticas técnicas, las cuales analicé, rechacé y corregí basándome en los requerimientos formales del proyecto:
  
  1. **Rechazo de modelo personalizado:** La IA sugirió crear un modelo de usuario propio (`Custom User Model`) para manejar los roles e incluso propuso esquemas para manejar contraseñas. Descarté esta opción por razones de seguridad y arquitectura. En su lugar, utilicé el sistema nativo de `Groups` de Django, el cual es el estándar seguro para resolver la autorización sin reinventar la rueda ni exponer credenciales.

  2. **Corrección de vulnerabilidad en vistas:** La IA propuso restringir los permisos de usuario ocultando los botones de "Editar" y "Eliminar" directamente en las plantillas HTML usando etiquetas `{% if %}`. Corregí este error, ya que la validación en el frontend permite que cualquier usuario ejecute una acción escribiendo la ruta URL manualmente. La solución definitiva que implementé fue construir un decorador propio (`@requiere_rol`) que intercepta la petición en el servidor y consulta la base de datos antes de permitir la ejecución de la vista.

