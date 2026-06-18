from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
from playwright.sync_api import Page, sync_playwright

from config import EXPECTED_COLUMNS, FORM_URL, MODULE_LABELS, PROFILE_DIR, STATE_LABELS


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
        return parsed.strftime("%m/%d/%Y")
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


def normalize_module_label(value: str) -> str:
    key = value.strip().lower()
    return MODULE_LABELS.get(key, value)


def submit_row(page: Page, row: BitacoraRow) -> None:
    page.goto(FORM_URL, wait_until="domcontentloaded")

    page.get_by_text(normalize_state_label(row.estado), exact=True).click()
    page.get_by_label("Fecha del reporte").fill(row.fecha)
    page.get_by_label(
        "Detalle técnico del avance o descripción del error").fill(row.detalle)
    page.get_by_text("Elegir", exact=True).click()
    page.get_by_text(normalize_module_label(row.modulo), exact=True).click()
    page.get_by_text("Enviar", exact=True).click()


def iter_rows(frame: pd.DataFrame) -> Iterable[BitacoraRow]:
    for index, (_, row) in enumerate(frame.iterrows()):
        yield validate_row(row, index)


def run(form_path: Path) -> None:
    frame = read_bitacora(form_path)

    with sync_playwright() as playwright:
        profile_dir = Path(PROFILE_DIR).resolve()
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
        )
        page = context.new_page()

        for row in iter_rows(frame):
            submit_row(page, row)

        context.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automatiza la carga de una bitácora en Google Forms.")
    parser.add_argument("archivo", type=Path,
                        help="Ruta al archivo CSV o Excel con la bitácora")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run(args.archivo)


if __name__ == "__main__":
    main()
