# Python Test Automation Framework with Playwright

A robust Python test automation framework using Playwright and pytest-bdd for UI tests based on Object Oriented design and Gherkin-style BDD tests.

## Project Structure

```
akronis/
├── config/
│   ├── browser.json
│   ├── reporting.json
│   └── test.json
├── fixtures/
│   ├── __init__.py
│   └── playwright_fixtures.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── controls.py
│   └── ...
├── reports/
│   └── report.html
├── tests/
│   ├── features/
│   │   ├── flight_search.feature
│   │   ├── login.feature
│   │   └── search.feature
│   ├── step_defs/
│   │   ├── __init__.py
│   │   ├── test_flight_search_steps.py
│   │   └── ...
│   ├── test_mytest.py
│   └── ...
├── utils/
│   └── utils.py
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Key Features & Updates

- **Run Standard Pytest and BDD Tests**: The framework supports both classic pytest tests and BDD-style tests (pytest-bdd), allowing teams to choose the best approach for their needs and mix both styles in the same project.
- **BDD Flight Search Scenario**: `flight_search.feature` and `test_flight_search_steps.py` implement a full one-way flight search using Gherkin and pytest-bdd.
- **Object-Oriented BDD Style Test**: `test_sample_oo_bdd_style.py` demonstrates a clear, maintainable, and readable test using page objects and controls, mimicking BDD steps without extra framework complexity. This approach is ideal for technical teams who value maintainability and directness.
- **Persistent Browser Context**: Step definitions use a `scenario_page` fixture to keep the browser open for the entire scenario, ensuring state is maintained across steps.
- **Modular Calendar Controls**: Calendar logic is split into `CalendarField` (activation) and `CalendarPopup` (popup) classes for flexible date selection.
- **Reusable Page Objects**: All controls and page logic are encapsulated in the `pages/` directory for maintainability.

## Setup Instructions

### 1. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```powershell
playwright install chromium
```

Or install all browsers:

```powershell
playwright install
```

## Configuration

Edit files in `config/` to customize settings:

- `browser.json`: browser type, headless mode, slow_mo, viewport
- `test.json`: base_url, timeout
- `reporting.json`: reporting options

## Running Tests

### Run all tests

```powershell
pytest
```

### Run specific feature

```powershell
pytest tests/step_defs/test_flight_search_steps.py
```

## Test Reports

After running tests, an HTML report is generated at `reports/report.html`

## Tips

- Use Page Object Model for maintainability
- Keep selectors DRY in page objects
- Use explicit waits for dynamic content
- Write reusable step definitions
- Run tests in parallel with `pytest-xdist`

## Troubleshooting

- **Timeouts**: Increase timeout in config, check selectors, ensure app is accessible
- **Browser issues**: Ensure Playwright browsers are installed, check headless config
- **Import errors**: Ensure all `__init__.py` files are present, check Python path

## Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
