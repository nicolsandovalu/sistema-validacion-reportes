
Problema: Actualmente, la recepción y validación de los reportes mensuales de carga académica de los profesores se revisa de forma manual. Esto retrasa la gestión, cuesta horas de trabajo administrativo y pone en riesgo la confidencialidad al enviar resultados por correo uno a uno. 

Solución: Un programa que evalúa automáticamente la solicitud de un profesor mediante un token y sus horas. El sistema decide si aprueba o rechaza el acceso al reporte, guarda el registro en un archivo JSON y muestra un resumen web de los intentos de acceso.  

Alcance:

Entra: Validación lógica de un intento de acceso a la vez, guardado en formato JSON, y una vista web para mostrar el historial de validaciones.  No entra: Bases de datos, sistemas de login con contraseñas, ni carga masiva de archivos.  

Priorización MoSCoW

Must (Imprescindible): Pedir el token y las horas por consola, usar if/elif para decidir entre 4 resultados (acceso concedido, token inválido, sin horas, dato negativo), guardar en datos.json y mostrar una pantalla web con Django.  

Should (Importante): Limpiar los espacios en blanco extra que el usuario pueda tipear por accidente en el token usando funciones nativas de texto.

Could (Deseable): Mostrar un conteo total de accesos aceptados versus rechazados al final de la tabla en la consola.

Won't (Fuera por ahora): Conexión a bases de datos SQL o consumo de APIs para validación con recursos humanos.