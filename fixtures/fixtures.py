from typing import Any, Generator
import os
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from pathlib import Path
from utils.utils import load_config
from pytest_html import extras


@pytest.fixture(scope="session")
def browser_config():
    """Load browser configuration and override settings for CI environment"""
    config = load_config("browser.json")
    
    # Detect if running in GitHub actions and adjust settings
    if os.getenv("GITHUB_ACTIONS") == "true":
        config["headless"] = True
        config["browser"] = "chromium"
    
    return config


@pytest.fixture(scope="session")
def test_config():
    """Load test configuration"""
    return load_config("test.json")


@pytest.fixture(scope="session")
def reporting_config():
    """Load reporting configuration"""
    return load_config("reporting.json")


@pytest.fixture(scope="session")
def base_url(test_config) -> str:
    """Get base URL from test config"""
    return test_config.get("base_url", "")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_config):
    """Configure browser launch arguments"""
    return {
        "headless": browser_config.get("headless", True),
        "slow_mo": browser_config.get("slow_mo", 0)
    }


@pytest.fixture(scope="session")
def browser_type(playwright, browser_config):
    """Select browser type from config"""
    browser_name = browser_config.get("browser", "chromium")
    if browser_name == "firefox":
        return playwright.firefox
    elif browser_name == "webkit":
        return playwright.webkit
    else:
        return playwright.chromium


@pytest.fixture(scope="session")
def browser(browser_type: Browser, browser_type_launch_args) -> Generator[Browser, Any, Any]:
    """Launch browser with config settings"""
    browser = browser_type.launch(**browser_type_launch_args)
    yield browser
    browser.close()


@pytest.fixture
def pwcontext(browser: Browser, browser_config, base_url) -> Generator[BrowserContext, Any, Any]:
    """Create browser context with configuration"""
    context = browser.new_context(
        viewport=browser_config.get("viewport", {"width": 1920, "height": 1080}),
        base_url=base_url
    )
    yield context
    context.close()

@pytest.fixture
def page(pwcontext: BrowserContext, test_config, request) -> Generator[Page, Any, Any]:
    """Create a new page for each test with failure capture"""
    
    page = pwcontext.new_page()
    page.set_default_timeout(test_config.get("timeout", 30000))
    
    yield page
    
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.failed :
            try:
                reports_dir = Path("reports")
                reports_dir.mkdir(exist_ok=True)
                
                test_name = request.node.name
                html_filename = f"{test_name}_failure.html"
                html_path = reports_dir / html_filename
                
                html_content = page.content()
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"HTML saved to: {html_path}")
            except Exception as e:
                print(f"Failed to capture HTML: {e}")
    
    page.close()



