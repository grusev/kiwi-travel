import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page

from pages.pages import KiwiStartPage, SearchResultsPage
from pages.controls import Airport, TravelDirection


# Load all scenarios from the feature file
scenarios('../features/flight_search.feature')


@given(parsers.parse('As an not logged user navigate to homepage {url}'), 
       target_fixture="scenario_page")
def navigate_to_homepage(page: Page, url: str):
    kiwi = KiwiStartPage(page)
    kiwi.navigate_to(url)
    return page


@when(parsers.parse('I select {trip_type} trip type'))
def select_one_way_trip(scenario_page: Page, trip_type: str):
    ttype = TravelDirection.from_string(trip_type)
    kiwi = KiwiStartPage(scenario_page)
    kiwi.SearchFlightsControl.directions_radio_group.select_trip_type(
        trip_type=ttype
    )
    assert kiwi.SearchFlightsControl.directions_radio_group.is_selected(
        trip_type=ttype
    )
    return 


@when(parsers.parse('Set as departure airport {airport_code}'))
def set_departure_airport(scenario_page: Page, airport_code: str):
    airport = Airport.from_string(airport_code)
    kiwi = KiwiStartPage(scenario_page)
    kiwi.SearchFlightsControl.origin_input.clear()
    kiwi.SearchFlightsControl.origin_input.add_airport(airport)


@when(parsers.parse('Set the arrival Airport {airport_code}'))
def set_arrival_airport(scenario_page: Page, airport_code: str):
    airport = Airport.from_string(airport_code)
    kiwi = KiwiStartPage(scenario_page)
    kiwi.SearchFlightsControl.destination_input.clear()
    kiwi.SearchFlightsControl.destination_input.add_airport(airport)


@when(parsers.parse('Set the departure time {weeks:d} week in the future starting current date'))
def set_departure_time(scenario_page: Page, weeks: int):
    """Set the departure time to a number of weeks in the future."""
    kiwi = KiwiStartPage(scenario_page)
    days = weeks * 7
    kiwi.SearchFlightsControl.calendar_field.set_date_plus_days(days)


@when('Uncheck the `Check accommodation with booking.com` option')
def uncheck_accommodation_option(scenario_page: Page):
    """Uncheck the accommodation checkbox."""
    kiwi = KiwiStartPage(scenario_page)
    kiwi.SearchFlightsControl.kiwi_hotels_checkbox.unselect()


@when('Click the search button')
def click_search_button(scenario_page: Page):
    """Click the search button."""
    kiwi = KiwiStartPage(scenario_page)
    kiwi.SearchFlightsControl.click_search()


@then('I am redirected to search results page')
def verify_search_results_page(scenario_page: Page):
    search_results = SearchResultsPage(scenario_page)
    search_results.wait_for_results()
