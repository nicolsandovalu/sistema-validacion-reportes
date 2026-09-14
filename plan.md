# Plan de Desarrollo y Arquitectura del Sistema

## 1. El Problema
El problema principal es la pérdida excesiva de tiempo generando reportes operativos para los profesores y enviando individualmente a cada uno sus métricas. Además, la gestión manual mediante archivos locales o correos uno a uno aumenta el riesgo de errores humanos, filtraciones de datos sensibles y accesos no autorizados a información que no corresponde.

## 2. La Solución (Alcance Actualizado - Evaluación 2)
La solución es automatizar la ingesta y distribución de métricas mediante un sistema back-end seguro. El sistema permite a los administradores subir la información en masa mediante archivos CSV, y generar de forma automática tokens de acceso que se envían por correo a cada profesor. Con este token, los docentes ingresan a una vista pública aislada donde consultan exclusivamente sus propios reportes individuales. 

Para soportar esta operativa cumpliendo con los estándares de seguridad de la Evaluación 2, la solución integra:
* **Persistencia Relacional:** Todo el almacenamiento en JSON ha sido reemplazado por una base de datos **SQLite** gestionada mediante el ORM de Django[cite: 4].
* **Gestión de Datos:** Implementación de un sistema **CRUD completo** con validación de entradas para administrar los reportes de manera centralizada[cite: 4].
* **Seguridad y Privacidad:** Control de acceso basado en roles para el panel administrativo, asegurando que no existan filtraciones ni visualización cruzada de datos.
* **Preservación Histórica:** Implementación de **borrado lógico (soft delete)** para ocultar evaluaciones obsoletas o erróneas sin destruir los registros históricos de la base de datos[cite: 4].

## 3. Priorización MoSCoW

### MUST (Debe tener)
* Autenticación nativa de administradores (**Login** y Logout)[cite: 4].
* Base de datos relacional **SQLite** configurada de forma segura[cite: 4].
* Vistas **CRUD** completas con manejo de errores (`try/except`) para evitar caídas del servidor[cite: 4].
* Control de acceso estricto mediante **roles** (Grupos de Django) validado a nivel de backend[cite: 4].
* Mecanismo de **borrado lógico** (`soft delete`) para los registros[cite: 4].
* Generación de tokens únicos y portal de validación seguro para los docentes.

### SHOULD (Debería tener)
* Carga masiva de datos estructurados mediante el procesamiento y validación de archivos CSV.
* Envío automático de correos electrónicos informando el token al profesor registrado.

### COULD (Podría tener)
* Filtros dinámicos en el dashboard administrativo (por nombre, estado y programa) para facilitar la auditoría.
* Alertas visuales (`messages`) en la interfaz para informar sobre el éxito o fracaso de la ingesta de datos.

### WON'T (No tendrá por ahora)
* Sistema de autenticación con modelo de usuario personalizado (Custom User Model), delegando esta responsabilidad al sistema nativo de Django por seguridad[cite: 4].
* Borrado físico (Hard delete) de los registros en la base de datos.