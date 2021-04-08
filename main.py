from flask import Flask
from flask import jsonify
from flask import request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

app = Flask(__name__)

class WebDriver:
    location_data = {}

    def __init__(self):
        self.PATH = "chromedriver.exe"
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(self.PATH, options=self.options)

    def scrape(self, url):  # Passed the URL as a variable
        try:
            self.driver.get(url)  # Get is a method that will tell the driver to open at that particular URL

        except Exception as e:
            self.driver.quit()
            return

        time.sleep(5)  # Waiting for the page to load.

        # in one page
        try:
            names = []
            names_ele = self.driver.find_elements_by_class_name("tYZdQJV9xeh__title-container")
            for name in names_ele:
                names.append(name.text)

            ratings = []
            ratings_ele = self.driver.find_elements_by_class_name("rs9iHBFJiiu__rating")
            for rating in ratings_ele:
                ratings.append(rating.text)

            #print(names)
            #print(ratings)

            b_type = []
            address = []
            elements = self.driver.find_elements_by_xpath("//div[@class='tYZdQJV9xeh__info-line' and @jsinstance='0']")
            for element in elements:
                string = element.text
                if string.find("·") == -1:
                    b_type.append(string)
                    address.append(" ")
                else:
                    parts = string.split("·")
                    b_type.append(parts[0])
                    address.append(parts[1])
            contact_no = []
            elements = self.driver.find_elements_by_xpath("//div[@class='tYZdQJV9xeh__info-line' and @jsinstance='*1']")
            for element in elements:
                string = element.text
                if string.find("·") == -1:
                    contact_no.append(string)
                else:
                    parts = string.split("·")
                    contact_no.append(parts[1])

            #print(b_type)
            #print(address)
            #print(contact_no)

            keys = ["name", "rating", "business type", "address", "contact_no"]
            objects = []

            for entry in zip(names, ratings, b_type, address, contact_no):
                dic = dict(zip(keys, entry))
                objects.append(dic)
            #print(objects)

            agri = objects

            @app.route('/', methods=['GET'])
            def hello_world():
                return jsonify({'message': 'Good, Finder!'})

            @app.route('/agri', methods=['GET'])
            def returnAll():
                return jsonify({'agri': agri})

            @app.route('/agri/<string:name>', methods=['GET'])
            def returnOne(name):
                theOne = agri[0]
                for i, q in enumerate(agri):
                    if q['name'] == name:
                        theOne = agri[i]
                return jsonify({'agri': theOne})

            if __name__ == "__main__":
                app.run(debug=True)
        
        except Exception as e:
            print("Exception occured")
            pass
        
        
        """
        if (self.click_all_reviews_button() == False):  # Clicking the all reviews button and redirecting the driver to the all reviews page.
            return (self.location_data)

        time.sleep(5)  # Waiting for the all reviews page to load.

        self.scroll_the_page()  # Scrolling the page to load all reviews.
        self.expand_all_reviews()  # Expanding the long reviews by clicking see more button in each review.
        self.get_reviews_data()  # Getting all the reviews data.
        """
        self.driver.quit()  # Closing the driver instance.

url = "location_url"
x = WebDriver()
print(x.scrape(url))


