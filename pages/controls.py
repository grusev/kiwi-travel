import time
from playwright.sync_api import Page, Locator, expect
from typing import Union, List

from data.datadef import Airport, TravelDirection
from utils.utils import wait_until


class RadioButton:
    """Advanced radio button component with label and input child elements"""
    
    def __init__(self, page_or_locator: Union[Page, Locator], data_test_value: str):
        """
        Initialize radio button component
        
        Args:
            page_or_locator: Either a Playwright Page object or a parent Locator to search within
            data_test_value: The data-test attribute value (e.g., "ModePopupOption-return")
        """
        self.page_or_locator = page_or_locator
        self.data_test_value = data_test_value
        
        # Use the provided page or locator as the search context
        self.container = page_or_locator.locator(f'[data-test="{data_test_value}"]')
        self.label = self.container.locator('label')
        self.input = self.container.locator('input[type="radio"]')
    
    def click(self):
        """Click the radio button label to select it"""
        self.label.click()
    
    def is_visible(self) -> bool:
        """Check if the radio button label is visible"""
        return self.label.is_visible()
    
    def is_selected(self) -> bool:
        """Check if the radio button input is selected/checked"""
        return self.input.is_checked()
    
    def wait_until_visible(self, timeout: int = 5000):
        """Wait until the radio button label becomes visible"""
        self.label.wait_for(state="visible", timeout=timeout)
    
    def get_label_text(self) -> str:
        """Get the text content of the label"""
        return self.label.text_content()
    
    def select_if_not_selected(self):
        """Select the radio button only if it's not already selected"""
        if not self.is_selected():
            self.click()


class Checkbox:
    """Advanced checkbox component with label and input child elements"""
    
    def __init__(self, page_or_locator: Union[Page, Locator], data_test_value: str):
        """
        Initialize checkbox component
        
        Args:
            page_or_locator: Either a Playwright Page object or a parent Locator to search within
            data_test_value: The data-test attribute value (e.g., "ModePopupOption-return")
        """
        self.page_or_locator = page_or_locator
        self.data_test_value = data_test_value
        
        # Use the provided page or locator as the search context
        self.container = page_or_locator.locator(f'[data-test="{data_test_value}"]')
        self.label = self.container.locator('label')
        self.input = self.container.locator('input[type="checkbox"]')
    
    def click(self):
        """Click the checkbox label to select it"""
        self.label.click()
    
    def is_visible(self) -> bool:
        """Check if the checkbox label is visible"""
        return self.label.is_visible()
    
    def is_selected(self) -> bool:
        """Check if the checkbox input is selected/checked"""
        return self.input.is_checked()
    
    def wait_until_visible(self, timeout: int = 5000):
        """Wait until the checkbox label becomes visible"""
        self.label.wait_for(state="visible", timeout=timeout)
    
    def get_label_text(self) -> str:
        """Get the text content of the label"""
        return self.label.text_content()
    
    def select(self):
        """Select the checkbox only if it's not already selected"""
        if not self.is_selected():
            self.click()       

    def unselect(self):
        """Unselect the checkbox only if it's currently selected"""
        if self.is_selected():
            self.click()                       


class DirectionsRadioGroup: 
    """Radio button group for selecting trip directions (one-way, return, etc)"""
    
    def __init__(self, page: Page):
        self.page = page
        self.one_way_radio = RadioButton(page, "ModePopupOption-oneWay")
        self.return_trip_radio = RadioButton(page, "ModePopupOption-return")
        self.mutlicity_trip_radio = RadioButton(page, "ModePopupOption-multicity")
        self.nomad_trip_radio = RadioButton(page, "ModePopupOption-nomad")
        self.directions_select = page.locator('[data-test^="SearchFormModesPicker"]')
        self.dialog = page.locator("[role='dialog'][data-test='ModesField']")

    def is_visible(self) -> bool:
        return self.directions_select.is_visible()
    
    def wait_until_visible(self, timeout: int = 5000):
        self.directions_select.wait_for(state="visible", timeout=timeout)

    def is_selected(self, trip_type: TravelDirection) -> bool:
        return trip_type.page_code.lower() in self.directions_select.get_attribute("data-test").lower()
        
    def select_trip_type(self, trip_type: TravelDirection):

        def select_trip_type(trip_type: TravelDirection, radio_button: RadioButton, timeout_: int = 5000):
            radio_button.select_if_not_selected()
            self.dialog.wait_for(state="hidden", timeout=timeout_)
            wait_until(lambda: self.is_selected(trip_type), timeout_seconds=timeout_)

        if self.is_selected(trip_type):
            return  # already selected
        if not self.dialog.is_visible(): 
            # if not opened opened it first
            self.directions_select.click()
            self.dialog.wait_for(state="visible", timeout=5000)
        if trip_type == TravelDirection.ONE_WAY:
            select_trip_type(trip_type, self.one_way_radio)
        elif trip_type == TravelDirection.RETURN:
            select_trip_type(trip_type, self.return_trip_radio)
        elif trip_type == TravelDirection.MULICITY:
            select_trip_type(trip_type, self.mutlicity_trip_radio)
        elif trip_type == TravelDirection.NOMAD:
            select_trip_type(trip_type, self.nomad_trip_radio)
        else:
            raise ValueError(f"Unknown trip type: {trip_type}")


class DestinationInputBox:
    """Special input box for entering multiple values and handling dynamic child elements."""

    def __init__(self, page: Page, data_test_value: str):
        """
        Initialize the special input box.

        Args:
            page: A Playwright Page object.
            data_test_value: The data-test attribute value of the outer element.
        """
        self.page = page
        self.container = self.page.locator(f'[data-test="{data_test_value}"]')
        self.input = self.container.locator('input')

    def add_airport(self, airport: Airport):       
        """
        Type a destination 3 letter code into the input field and press Enter.
        """

        def select_option(page: Page, expected_texts: List[str]) -> str:
            locator = page.locator("[data-test^='PlacePickerRow'][role='button']")

            for i in range(10):
                count = locator.count()
                for i in range(count):
                    text = locator.nth(i).inner_text()
                    if any(expected in text for expected in expected_texts):
                        locator.nth(i).click()
                        return text
                time.sleep(0.5)

            raise ValueError(f"No option found with text {expected_texts}")

        self.eneter_text(airport.code)
        # Wait for the dropdown suggestion to appear (unholly approach but good enough for now)
        select_option(self.page, [airport.code, airport.city])
        #first_option = self.page.locator("[data-test^='PlacePickerRow'][role='button']").first
        #expect(first_option).to_contain_text(airport.city)
        #self.input.press("Enter")

    def eneter_text(self, text: str):
        """
        Type arbitrary text into the input field.
        """
        self.input.click()
        self.input.type(text)

    def get_selected_airports(self) -> list:
        """
        Retrieve the child elements with data-test="PlacePickerInputPlace".
        """
        return self.container.locator('[data-test="PlacePickerInputPlace"]').all()

    def get_selected_airport_values(self) -> list:
        """
        Retrieve the text content of child elements with data-test="PlacePickerInputPlace".
        """
        child_elements = self.get_selected_airports()
        return [element.text_content().replace("\u200e", "").strip() for element in child_elements]
    
    def clear(self):
        """
        Clear all selected airports by clicking the remove buttons.
        """
        for item in self.get_selected_airports():
            remove_button = item.locator("[data-test='PlacePickerInputPlace-close']")
            remove_button.click()
            item.wait_for(state="detached")


class CalendarField:
    """Calendar activation field."""

    def __init__(self, page: Union[Page, Locator], outer_field: str = '[data-test="SearchDateInput"]'):
        """
        Initialize the calendar activation field.
        """
        self.page = page
        self.bounding_element = page.locator(outer_field)
        self.label = self.bounding_element.locator('label')
        self.input_field = self.bounding_element.locator('[data-test="SearchFieldDateInput"]')

    def activate(self):
        """
        Activate the calendar by clicking the activation field.
        """
        self.label.click()

    def get_text(self) -> str:
        """
        Get the text content of the input field.
        """
        return self.input_field.text_content()
    
    def is_visible(self) -> bool:
        """
        Check if the activation field is visible.
        """
        return self.label.is_visible()
    
    def wait_until_visible(self, timeout: int = 5000):
        """
        Wait until the activation field is visible.
        """
        self.label.wait_for(state="visible", timeout=timeout)

    def set_date_plus_days(self, days: int):
        """
        Set the date to current date plus specified number of days.
        """
        self.activate()
        calendar_popup = CalendarPopup(self.page)
        calendar_popup.wait_for_visible()
        calendar_popup.set_date_plus_days(days)


class CalendarPopup:
    """Calendar popup window."""

    def __init__(self, page: Union[Page, Locator]):
        """
        Initialize the calendar popup.
        """
        self.page = page
        self.calendar_popup = page.locator('[data-test="NewDatePickerOpen"]')
        self.month_button = self.calendar_popup.locator('[data-test="DatepickerMonthButton"]')
        self.next_month_button = self.calendar_popup.locator('[data-test="CalendarMoveNextButton"]')
        self.previous_month_button = self.calendar_popup.locator('[data-test="CalendarMovePrevious"]')
        self.selected_day = self.calendar_popup.locator('[data-test="DaySelected-selected"]')
        self.set_date_button = self.calendar_popup.locator('[data-test="SearchFormDoneButton"]')

    def wait_for_visible(self, timeout: int = 5000):
        """
        Wait until the calendar popup is visible.
        """
        self.calendar_popup.wait_for(state="visible", timeout=timeout)

    def is_visible(self) -> bool:
        """
        Check if the calendar popup is visible.
        """
        return self.calendar_popup.is_visible()

    def navigate_to_next_month(self):
        """
        Navigate to the next month using the next month button.
        """
        self.next_month_button.click()

    def navigate_to_previous_month(self):
        """
        Navigate to the previous month using the previous month button.
        """
        self.previous_month_button.click()

    def set_date_plus_days(self, days: int):
        """
        Set the calendar date to the current date plus a specified number of days.
        """
        from datetime import datetime, timedelta

        now = datetime.now()
        target_date = now + timedelta(days=days)
        formatted = target_date.strftime("%Y-%m-%d")

        number_months_displayed = self.month_button.count()
        months_diff = (target_date.year - now.year) * 12 + (target_date.month - now.month)

        if months_diff > (number_months_displayed - 1):
            times_to_click_next = months_diff - (number_months_displayed - 1)
            for _ in range(times_to_click_next):
                self.navigate_to_next_month()
                time.sleep(1)  # small delay to allow UI to update

        # Select the target day
        self.calendar_popup.locator(f'[data-value="{formatted}"]').click()
        self.set_date_button.click()


class SearchFlightsControl:
    """Control for searching flights"""
    
    def __init__(self, page: Page):
        self.page = page
        self.directions_radio_group = DirectionsRadioGroup(page)
        self.origin_input = DestinationInputBox(page, "PlacePickerInput-origin")
        self.destination_input = DestinationInputBox(page, "PlacePickerInput-destination")
        self.calendar_field = CalendarField(page, '[data-test="SearchDateInput"]')
        self.kiwi_hotels_checkbox = Checkbox(page, "accommodationCheckbox")
        self.search_button = page.locator('[data-test="LandingSearchButton"]')
    
    def click_search(self):
        """Click the search button"""
        self.search_button.click()

    def wait_until_visible(self, timeout: int = 5000):
        """Wait until the search button is visible"""
        self.search_button.wait_for(state="visible", timeout=timeout)
