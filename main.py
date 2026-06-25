from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
from playwright.sync_api import Page, sync_playwright

from config import (
    BROWSER_EXECUTABLE_PATH,
    EXPECTED_COLUMNS,
    FORM_URL,
    MODULE_LABELS,
    MODULE_ORDER,
    PROFILE_DIR,
    STATE_LABELS,
)


@dataclass
class BitacoraRow:
    estado: str
    fecha: str
    detalle: str
    modulo: str


def normalize_text(value: object) -> str:
    return str(value).strip()


def normalize_date(value: object) -> str:
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.notna(parsed):
        return parsed.strftime("%Y-%m-%d")
    return normalize_text(value)


def read_bitacora(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        frame = pd.read_excel(path)
    elif suffix == ".csv":
        frame = pd.read_csv(path)
    else:
        raise ValueError("Formato no soportado. Usá CSV o Excel.")

    missing = [
        column for column in EXPECTED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {', '.join(missing)}")

    return frame[EXPECTED_COLUMNS].copy()


def validate_row(row: pd.Series, index: int) -> BitacoraRow:
    estado = normalize_text(row["estado"])
    fecha = normalize_date(row["fecha"])
    detalle = normalize_text(row["detalle"])
    modulo = normalize_text(row["modulo"])

    if not estado:
        raise ValueError(f"Fila {index + 1}: el campo 'estado' está vacío")
    if not fecha:
        raise ValueError(f"Fila {index + 1}: el campo 'fecha' está vacío")
    if not detalle:
        raise ValueError(f"Fila {index + 1}: el campo 'detalle' está vacío")
    if not modulo:
        raise ValueError(f"Fila {index + 1}: el campo 'modulo' está vacío")

    return BitacoraRow(estado=estado, fecha=fecha, detalle=detalle, modulo=modulo)


def normalize_state_label(value: str) -> str:
    key = value.strip().lower()
    return STATE_LABELS.get(key, value)


def emit_alert(message: str) -> None:
    full_message = f"[ALERTA] {message}"
    print(full_message)
    with Path("alerts.log").open("a", encoding="utf-8") as handle:
        handle.write(full_message + "\n")


def normalize_module_label(value: str) -> str:
    key = value.strip().lower()
    return MODULE_LABELS.get(key, value)


def select_module(page: Page, value: str) -> None:
    label = normalize_module_label(value)
    if label not in MODULE_ORDER:
        raise ValueError(
            f"Módulo no soportado: '{label}'. Valores válidos: {', '.join(MODULE_ORDER)}"
        )

    listbox = page.locator('[role="listbox"]').filter(
        has_text="Módulo o componente principal trabajado"
    )
    if listbox.count() == 0:
        listbox = page.get_by_role(
            "listbox",
            name="Módulo o componente principal trabajado",
        )

    opener = listbox.locator('[jsname="LgbsSe"]').first
    if opener.count() == 0:
        listbox.first.click()
    else:
        opener.click(position={"x": 10, "y": 10})

    page.wait_for_timeout(1000)

    target_option = page.locator(
        '[role="option"]').filter(has_text=label).first
    if target_option.count() == 0:
        raise ValueError(f"No se encontró la opción del módulo: {label}")

    target_option.click(position={"x": 5, "y": 5})
    page.wait_for_timeout(500)


def submit_row(page: Page, row: BitacoraRow) -> None:
    page.goto(FORM_URL, wait_until="domcontentloaded")
    page.bring_to_front()
    page.wait_for_timeout(1500)

    try:
        page.get_by_role(
            "radio", name=normalize_state_label(row.estado)).click()
        page.get_by_role("textbox", name="Fecha").fill(row.fecha)
        page.get_by_role(
            "textbox",
            name="Detalle técnico del avance o descripción del error",
        ).fill(row.detalle)
        select_module(page, row.modulo)
        page.get_by_role("button", name="Enviar").click()
    except ValueError as error:
        raise RuntimeError(f"No se pudo completar la fila: {error}") from error


def select_rows_to_process(frame: pd.DataFrame, process_all: bool) -> pd.DataFrame:
    if process_all:
        return frame.copy()
    return frame.head(1).copy()


def iter_rows(frame: pd.DataFrame) -> Iterable[BitacoraRow]:
    for index, (_, row) in enumerate(frame.iterrows()):
        yield validate_row(row, index)


def run(form_path: Path, process_all: bool = False) -> None:
    frame = read_bitacora(form_path)
    selected_frame = select_rows_to_process(frame, process_all=process_all)

    with sync_playwright() as playwright:
        profile_dir = Path(PROFILE_DIR).resolve()
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
            executable_path=BROWSER_EXECUTABLE_PATH,
        )
        page = context.new_page()

        for row in iter_rows(selected_frame):
            try:
                submit_row(page, row)
            except RuntimeError as error:
                emit_alert(str(error))
                emit_alert("El script se detuvo en esa fila. Revisá el valor del módulo y el formulario.")
                break

        context.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automatiza la carga de una bitácora en Google Forms.")
    parser.add_argument("archivo", type=Path,
                        help="Ruta al archivo CSV o Excel con la bitácora")
    parser.add_argument(
        "--process-all",
        action="store_true",
        help="Procesa todas las filas del archivo en lugar de solo la primera.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        run(args.archivo, process_all=args.process_all)
    except Exception as error:
        emit_alert(str(error))
        emit_alert("El script terminó con un error. Revisá el archivo de entrada y los valores del formulario.")


if __name__ == "__main__":
    main()
