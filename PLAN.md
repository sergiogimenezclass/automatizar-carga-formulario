# Plan de desarrollo

## Objetivo

Construir una solución en Python para leer una planilla de bitácora y completar automáticamente un Google Form con Playwright, usando una sesión autenticada y validando los datos antes de enviar.

## Fases

### 1. Definir la entrada de datos

- Confirmar el formato de la planilla fuente: CSV o Excel.
- Establecer las columnas mínimas esperadas: estado, fecha, detalle técnico y módulo o componente.
- Normalizar nombres de columnas y tipos de datos para evitar ambigüedades.

### 2. Leer y validar la planilla

- Implementar la carga de archivos con Pandas.
- Validar columnas obligatorias y valores vacíos por fila.
- Mostrar errores claros si falta información o el archivo no cumple el formato esperado.

### 3. Automatizar el formulario

- Abrir Chrome o Chromium con Playwright en modo visible.
- Reutilizar un perfil persistente o una sesión ya autenticada.
- Localizar los campos del Google Form y completar opciones, fecha y texto libre.
- Enviar la respuesta y detectar la confirmación de éxito.

### 4. Agregar trazabilidad

- Registrar qué filas se procesan y cuáles fallan.
- Guardar evidencia mínima ante errores, como logs o capturas.
- Definir si el flujo continúa con la siguiente fila o se detiene ante fallas críticas.

### 5. Preparar el proyecto para uso repetible

- Definir dependencias de Python.
- Agregar configuración para URL del formulario, ruta de datos y perfil autenticado.
- Documentar cómo ejecutar el script y cómo preparar la sesión del navegador.

### 6. Probar con un caso real

- Ejecutar una prueba con una planilla pequeña.
- Verificar que el formulario reciba los valores correctos.
- Ajustar selectores y mapeos según la estructura real del formulario.

## Entregables

- Script principal de automatización.
- Archivo de configuración.
- Documento de instalación y uso.
- Planilla de ejemplo para pruebas.

## Alcance inicial

- Enfocar la primera versión en un formulario concreto.
- Priorizar confiabilidad sobre generalización.
- Mantener el flujo simple y fácil de depurar.