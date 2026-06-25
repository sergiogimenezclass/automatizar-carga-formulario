from pathlib import Path

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdQX7tSwuHjo520MKvavNuTO3Uzf1kpt4gb_d22p4tagDMqrg/viewform"
PROFILE_DIR = Path(".perfil_google_chrome")
BROWSER_EXECUTABLE_PATH = "/usr/bin/google-chrome"

EXPECTED_COLUMNS = [
    "estado",
    "fecha",
    "detalle",
    "modulo",
]

STATE_LABELS = {
    "funcional/terminado": "Funcional/Terminado",
    "en etapa de pruebas/debugeo": "En etapa de pruebas/Debugeo",
    "bloqueado por dependencias": "Bloqueado por dependencias",
}

MODULE_LABELS = {
    "backend": "Backend",
    "base de datos": "Base de Datos",
    "ui/ux": "UI/UX",
    "integración de apis": "Integración de APIs",
}

MODULE_ORDER = [
    "Backend",
    "Base de Datos",
    "Opción 3",
    "UI/UX",
    "Integración de APIs",
]
