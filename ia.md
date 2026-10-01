# Registro de Uso de Inteligencia Artificial (Evaluación 3 - API REST)

* **Herramienta utilizada:** Gemini.
* **Pregunta textual realizada:** "Estoy creando una API con Django REST Framework para mi evaluación. ¿Cómo configuro los permisos para poder probar mis rutas GET y POST rápidamente en Thunder Client sin que me dé error 401?"

* **Qué me respondió la IA:** 
  La IA me sugirió modificar mi archivo `settings.py` y configurar la clase de permisos globales con `rest_framework.permissions.AllowAny`. Me indicó que esto apagaría temporalmente la seguridad para permitirme hacer pruebas rápidas sin necesidad de enviar credenciales.

* **Por qué estaba mal y qué hice yo (Corrección crítica):** 
  Descarté esta opción. Configurar `AllowAny` apaga por completo la seguridad y deja la API pública y vulnerable en internet, lo cual es una mala práctica grave sancionada directamente en los requerimientos del proyecto (Criterio 3.1.2). 
  
  En su lugar, implementé el estándar seguro:
  1. Configuré `rest_framework.permissions.IsAuthenticated` por defecto en `settings.py` para bloquear todo el tráfico anónimo.
  2. Implementé `TokenAuthentication` para usar llaves criptográficas truncadas en la cabecera HTTP (`Authorization: Token ...`).
  3. Para los roles, creé la clase de permisos diferenciados `SoloStaffBorra`, garantizando que cualquier usuario autenticado pueda leer y crear, pero que solo los administradores (staff) tengan el privilegio de ejecutar operaciones `DELETE`.