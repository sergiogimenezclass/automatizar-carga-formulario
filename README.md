# Automatizar carga de formulario con Python

Presentación práctica sobre cómo automatizar la carga de un Google Form de terceros cuando la información ya existe en una planilla Excel o CSV.

El proyecto propone usar Python para leer los datos con Pandas y controlar un navegador con Playwright, de modo que el formulario se complete y envíe de forma automática, como si lo hiciera una persona.

## Problema

La carga manual de formularios es repetitiva, lenta y propensa a errores. En este caso, el formulario se completa con una bitácora de desarrollo que puede ser diaria, semanal o mensual, y cuyos datos suelen repetirse desde una planilla ya preparada.

## Solución propuesta

La idea es transformar la planilla en instrucciones para automatizar el navegador:

Excel o CSV -> Python -> Pandas -> Playwright -> Google Form

Playwright abre Chrome o Chromium, entra al formulario, completa los campos y envía la respuesta desde una sesión ya autenticada.

## Caso de uso

La presentación toma como ejemplo una bitácora de estado de desarrollo de software con campos como:

- Estado
- Fecha del reporte
- Detalle técnico
- Módulo o componente trabajado

También contempla distintos tipos de entrada en el formulario, como opciones, fecha, texto libre y desplegables.

## Tecnologías

- Python
- Pandas
- Playwright
- Google Forms

## Instalación

### 1. Requisitos previos

- Python 3.13 o superior.
- Acceso a una cuenta de Google ya autenticada en el perfil del navegador que vas a usar.

### 2. Crear y activar un entorno virtual

1. Crear el entorno virtual en la carpeta del proyecto:

```bash
python -m venv .venv
```

2. Activarlo desde la terminal:

```bash
source .venv/bin/activate
```

3. Verificar que quedó activo. Normalmente vas a ver `(.venv)` al principio de la línea de la terminal:

```bash
which python
python --version
```

4. Si más adelante cerrás la terminal, repetí solo el paso de activación:

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Verificar la planilla de entrada

La herramienta espera un archivo CSV o Excel con estas columnas:

- `estado`
- `fecha`
- `detalle`
- `modulo`

Un ejemplo válido está en [bitacora_ejemplo.csv](bitacora_ejemplo.csv).

## Estructura

- `index.html`: presentación interactiva con 8 diapositivas.
- `main.py`: script principal que lee la planilla y completa el formulario.
- `config.py`: configuración del formulario y normalización de valores.
- `bitacora_ejemplo.csv`: archivo de ejemplo para probar la automatización.
- `PLAN.md`: plan de desarrollo del proyecto.

## Uso

1. Activar el entorno virtual siguiendo los pasos de la sección anterior.
2. Preparar el archivo CSV o Excel con las columnas requeridas.
3. Instalar dependencias si todavía no lo hiciste:

```bash
pip install -r requirements.txt
playwright install chromium
```

4. Ejecutar el script indicando la ruta del archivo:

```bash
python main.py bitacora_ejemplo.csv
```

5. Se abrirá un navegador con Playwright usando el perfil persistente definido en `.perfil_google_chrome`.
6. El script leerá cada fila de la planilla, completará el formulario y enviará la respuesta.

### Formato esperado del formulario

El formulario actual solicita estos campos:

- Estado: `Funcional/Terminado`, `En etapa de pruebas/Debugeo` o `Bloqueado por dependencias`.
- Fecha del reporte: se normaliza automáticamente al formato `yyyy-mm-dd`, que es el que usa el campo de fecha del formulario.
- Detalle técnico del avance o descripción del error.
- Módulo o componente principal trabajado: `Backend`, `Base de Datos`, `UI/UX` o `Integración de APIs`.

## Objetivo del aula

El desafío final es construir un script que lea una planilla de bitácora y complete una respuesta semanal en el formulario, validando antes de enviar que todos los campos obligatorios estén completos.

## Presentación

Abrir `index.html` en un navegador para navegar la presentación con los botones o con las flechas del teclado.