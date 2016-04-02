from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Abby goes to checkout her to-do app's homepage
        self.browser.get(self.live_server_url)

        #She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #She is invited to enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #She types "Buy beer" into a text box
        inputbox.send_keys('Buy beer')

        #When she hits enter, the page updates, and now the page lists "1: Buy beer" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy beer')

        #There is still a text box inviting her to add another item. She enters "Drink beer"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Drink the beer')
        inputbox.send_keys(Keys.ENTER)

        #The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy beer')
        self.check_for_row_in_list_table('2: Drink the beer')

        #Abby sees that the site has generated a unique URL for her - there is text explaining this
        self.fail('Finish the test!')

        #She visits that URL, and her to-do list is still there

        #She leaves the site
