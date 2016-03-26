from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Abby goes to checkout her to-do app's homepage
        self.browser.get('http://localhost:8000')

        #She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        #She is invited to enter a to-do item

        #She types "Buy beer" into a text box

        #When she hits enter, the page updates, and now the page lists "1: Buy beer" as an item in a to-do list

        #There is still a text box inviting her to add another item. She enters "Drink beer"

        #The page updates again, and now shows both items on her list

        #Abby sees that the site has generated a unique URL for her - there is text explaining this

        #She visits that URL, and her to-do list is still there

        #She leaves the site

if __name__ == '__main__':
    #launch unittest test runner to find and run test classes and methods 
    unittest.main()
