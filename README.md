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

## Estructura

- `index.html`: presentación interactiva con 8 diapositivas.

## Objetivo del aula

El desafío final es construir un script que lea una planilla de bitácora y complete una respuesta semanal en el formulario, validando antes de enviar que todos los campos obligatorios estén completos.

## Uso

Abrir `index.html` en un navegador para navegar la presentación con los botones o con las flechas del teclado.