"""Browser interaction tools for GenericAgent using TMWebDriver."""

from TMWebDriver import Session
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json

# Initialize a shared browser session
_session: Session | None = None


def get_session() -> Session:
    """Get or create the shared browser session."""
    global _session
    if _session is None or not _session.is_active():
        _session = Session()
    return _session


def navigate(url: str) -> dict:
    """Navigate the browser to a given URL.

    Args:
        url: The URL to navigate to.

    Returns:
        A dict with 'success' and 'current_url' keys.
    """
    session = get_session()
    try:
        session.driver.get(url)
        return {"success": True, "current_url": session.driver.current_url}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_page_text() -> dict:
    """Extract all visible text from the current page.

    Returns:
        A dict with 'text' containing the page body text.
    """
    session = get_session()
    try:
        body = session.driver.find_element(By.TAG_NAME, "body")
        return {"success": True, "text": body.text[:8000]}  # Limit to 8k chars
    except Exception as e:
        return {"success": False, "error": str(e)}


def click_element(selector: str, by: str = "css") -> dict:
    """Click an element on the current page.

    Args:
        selector: The selector string for the element.
        by: Selector type — 'css', 'xpath', or 'id'.

    Returns:
        A dict indicating success or failure.
    """
    session = get_session()
    by_map = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID}
    by_strategy = by_map.get(by, By.CSS_SELECTOR)
    try:
        element = WebDriverWait(session.driver, 10).until(
            EC.element_to_be_clickable((by_strategy, selector))
        )
        element.click()
        return {"success": True}
    except TimeoutException:
        return {"success": False, "error": f"Element not clickable within timeout: {selector}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def type_text(selector: str, text: str, by: str = "css") -> dict:
    """Type text into an input element.

    Args:
        selector: The selector string for the input element.
        text: The text to type.
        by: Selector type — 'css', 'xpath', or 'id'.

    Returns:
        A dict indicating success or failure.
    """
    session = get_session()
    by_map = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID}
    by_strategy = by_map.get(by, By.CSS_SELECTOR)
    try:
        element = WebDriverWait(session.driver, 10).until(
            EC.presence_of_element_located((by_strategy, selector))
        )
        element.clear()
        element.send_keys(text)
        return {"success": True}
    except TimeoutException:
        return {"success": False, "error": f"Element not found within timeout: {selector}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Tool registry for agentmain.py to discover
TOOLS = {
    "navigate": navigate,
    "get_page_text": get_page_text,
    "click_element": click_element,
    "type_text": type_text,
}
