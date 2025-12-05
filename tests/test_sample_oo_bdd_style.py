from playwright.sync_api import Page

from pages.pages import KiwiStartPage, SearchResultsPage
from pages.controls import Airport, TravelDirection
from utils.utils import wait_until


def test_object_oriented_bdd(page: Page):
    """
    A test that mimics BDD steps using page objects and controls.
    This is not a real BDD test but demonstrates similar flow. 
    It is very easy to convert it to a real BDD test using pytest-bdd.
    But the the beuty of those tests is that they are easier to implement and maintain.
    BDD tests are more readable for non-technical people, but they add extra complexity.
    This complexity soon deminishes the benefits of BDD approach. In reality, most BDD tests
    are written and maintained by technical people. 

    Note that this code does not require any technical knowledge to understand its goal.
    It is very clear what the test does. Sometimes more clear than BDD tests.
    """
    kiwi = KiwiStartPage(page)
    kiwi.navigate_to()

    kiwi.SearchFlightsControl.directions_radio_group.select_trip_type(
        trip_type=TravelDirection.ONE_WAY
    )
    assert kiwi.SearchFlightsControl.directions_radio_group.is_selected(
        trip_type=TravelDirection.ONE_WAY
    )

    kiwi.SearchFlightsControl.origin_input.clear()
    kiwi.SearchFlightsControl.origin_input.add_airport(Airport.MAD)
    kiwi.SearchFlightsControl.destination_input.clear() 
    kiwi.SearchFlightsControl.destination_input.add_airport(Airport.RTM)

    kiwi.SearchFlightsControl.calendar_field.set_date_plus_days(7)

    kiwi.SearchFlightsControl.kiwi_hotels_checkbox.unselect()

    kiwi.SearchFlightsControl.click_search()

    SearchResultsPage(page).wait_for_results()
