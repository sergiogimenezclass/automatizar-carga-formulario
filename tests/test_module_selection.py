import unittest

from playwright.sync_api import sync_playwright

from main import select_module


class ModuleSelectionTests(unittest.TestCase):
    def test_select_module_clicks_the_matching_option(self) -> None:
        html = """
        <html>
          <body>
            <div id="selection"></div>
            <div role="listbox" aria-label="Módulo o componente principal trabajado">
              <div role="option" data-value="Backend">Backend</div>
              <div role="option" data-value="Base de Datos">Base de Datos</div>
              <div role="option" data-value="UI/UX">UI/UX</div>
              <div role="option" data-value="Integración de APIs">Integración de APIs</div>
            </div>
            <script>
              const listbox = document.querySelector('[role="listbox"]');
              listbox.addEventListener('click', (event) => {
                const option = event.target.closest('[role="option"]');
                if (option) {
                  document.getElementById('selection').textContent = option.dataset.value;
                }
              });
            </script>
          </body>
        </html>
        """

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content(html)

            select_module(page, "backend")

            selected = page.locator("#selection").inner_text()
            self.assertEqual(selected, "Backend")
            browser.close()


if __name__ == "__main__":
    unittest.main()
