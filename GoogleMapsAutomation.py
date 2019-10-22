from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import HtmlTestRunner
import requests


class GoogleMapsAutomation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.driver = webdriver.Chrome("C:/Users/damjan/PycharmProjects/Project/Drivers/chromedriver.exe")  # chromedriver imported to PycharmProjects
        cls.driver.implicitly_wait(10)

    def test_status_check(self):  # Test method to check the status of the website

        successful_status_code = {  # Define the list (dictionary) of successful responses. Reference: https://tools.ietf.org/html/rfc7231
            200: 'OK',
            201: 'Created',
            202: 'Accepted',
            203: 'Non-Authoritative Information',
            204: 'No Content',
            205: 'Reset Content'}

        response = requests.get("https://maps.google.com?hl=en")
        self.assertIn(response.status_code, successful_status_code.keys(), 'Site https://maps.google.com?hl=en is not up!')
        print('Web page status: ' + successful_status_code[response.status_code])

    def test_directions(self):

        destination = "Belgrade"
        start = "Budapest"
        destination_search_locator_name = "q"  # Element has unique name identifier
        get_directions_locator_class = "iRxY3GoUYUY__taparea"  # Xpath" //div[contains(text(),'Directions')]
        start_location_locator_xpath = "//input[@placeholder='Choose starting point, or click on the map...']"
        drive_locator_xpath = "//div[@class='directions-travel-mode-icon directions-drive-icon']" # Locating element by class name is not working. Class: "directions-travel-mode-icon directions-drive-icon"
        options_menu_locator_class = "section-directions-options-link"  # Xpath: "//span[contains(text(),'Options')]"
        avoid_highways_locator_xpath = "//label[@for='pane.directions-options-avoid-highways']"  # Not working over id "pane.directions-options-avoid-highways"
        route_distance_locator_xpath = "//div[contains(text(),'km')]"

        self.driver.get("https://maps.google.com?hl=en")
        end_location_search = self.driver.find_element_by_name(destination_search_locator_name)
        end_location_search.send_keys(destination + Keys.ENTER)

        self.driver.find_element_by_class_name(get_directions_locator_class).click()

        start_location_search = self.driver.find_element_by_xpath(start_location_locator_xpath)
        start_location_search.send_keys(start+ Keys.ENTER)

        drive_button = self.driver.find_element_by_xpath(drive_locator_xpath)
        drive_button.click()

        options_menu = self.driver.find_element_by_class_name(options_menu_locator_class)
        options_menu.click()

        avoid_highways_checkbox = self.driver.find_element_by_xpath(avoid_highways_locator_xpath)
        avoid_highways_checkbox.click()

        route_distance = self.driver.find_elements_by_xpath(route_distance_locator_xpath)  # Route selection by distance
        length_of_routes = []
        for element in route_distance:
            length_of_routes.append(float(element.text[:-3]))  # creating a list of distances by removing last 3 characters ' km' from element text
        index = length_of_routes.index(max(length_of_routes))
        route_distance[index].click()

        if len(length_of_routes) > 1:  # Additional click for route selection is needed only if number of routes is greater than 1
            hover = ActionChains(self.driver).move_to_element(route_distance[index])
            hover.perform()
            route_distance[index].click()

    def test_distance(self):

        distance_locator_class = "section-trip-summary-subtitle"

        distance = self.driver.find_element_by_class_name(distance_locator_class)
        self.assertEqual(distance.is_displayed(), True, 'Element not present!')

    def test_duration(self):

        duration_locator_xpath = "//span[@class='delay-light' or @class='delay-medium' or @class='delay-heavy']"  # Depending on traffic conditions, 3 types of duration class are possible

        summary_title = self.driver.find_element_by_xpath(duration_locator_xpath)  # To find better general locator or include 'delay-medium' and 'delay-heavy' class options
        self.assertEqual(summary_title.is_displayed(), True, 'Element not present!')

    @classmethod
    def tearDownClass(cls):

        cls.driver.quit()
        print("Test finished")


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/damjan/PycharmProjects/Project/Reports'))  # Creating html report
