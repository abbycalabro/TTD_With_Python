from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(StaticLiveServerTestCase):
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
        abby_list_url = self.browser.current_url
        self.assertRegex(abby_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy beer')

        #There is still a text box inviting her to add another item. She enters "Drink beer"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Drink the beer')
        inputbox.send_keys(Keys.ENTER)

        #The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy beer')
        self.check_for_row_in_list_table('2: Drink the beer')

        #Now a new user, Francis, comes along to the site.

        ##We use a new browser session to make sure that no info of Abby's is coming through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Francis visits the home page. There is no sign of Abby's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy beer', page_text)
        self.assertNotIn('Drink the beer', page_text)

        #Francis starts a new list by entering a new item. He is less interesting than Abby...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        #Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, abby_list_url)

        #Again, there is no trace of Abby's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy beer', page_text)
        self.assertIn('Buy milk', page_text)

        #Satisfied, they both go back to sleep
        #Abby sees that the site has generated a unique URL for her - there is text explaining this
        #She visits that URL, and her to-do list is still there
        #She leaves the site

    def test_layout_and_styling(self):
        #Abby goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        #She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual( 
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5 #plus or minus 5 pixels
        )

        #She starts a new list and sees the input is nicely centered there, too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

