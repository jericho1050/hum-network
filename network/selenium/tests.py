import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

class WebpageTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:8000/') 

        # Wait for the page to load or any specific element I need
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_content'))
        )

    def tearDown(self):
        # Close the browser after the test is complete
        self.driver.quit()

    def test_post(self):
        # Now, you are expected to be logged in manually. To Continue with the test logic
        textarea = self.driver.find_element(By.ID, 'id_content')
        textarea.send_keys("TESTING PURPOSES ONLY")

        post_btn = self.driver.find_element(By.TAG_NAME, 'button')
        post_btn.click()

        newly_post = self.driver.find_element(By.CLASS_NAME, 'content')

        self.assertIn("TESTING PURPOSES ONLY", newly_post.text)

if __name__ == "__main__":
    unittest.main()
