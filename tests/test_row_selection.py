import unittest

import pandas as pd

from main import select_rows_to_process


class SelectRowsToProcessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = pd.DataFrame(
            [
                {"estado": "Funcional/Terminado", "fecha": "2026-06-18",
                    "detalle": "Primera", "modulo": "Backend"},
                {"estado": "En etapa de pruebas/Debugeo", "fecha": "2026-06-19",
                    "detalle": "Segunda", "modulo": "UI/UX"},
            ]
        )

    def test_defaults_to_first_row_only(self) -> None:
        selected = select_rows_to_process(self.frame, process_all=False)

        self.assertEqual(len(selected), 1)
        self.assertEqual(selected.iloc[0]["detalle"], "Primera")

    def test_process_all_rows_when_requested(self) -> None:
        selected = select_rows_to_process(self.frame, process_all=True)

        self.assertEqual(len(selected), 2)
        self.assertEqual(selected.iloc[1]["detalle"], "Segunda")


if __name__ == "__main__":
    unittest.main()
