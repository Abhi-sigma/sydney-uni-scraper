from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BeautifulSoup import BeautifulSoup
import urllib2
import time
import json


driver = webdriver.Chrome(
    "C:/Users/archi/Downloads/chromedriver_win32/chromedriver.exe")
driver.get("https://sydney.edu.au/courses")
driver.implicitly_wait(10)  # seconds
# print driver.page_source
# international_fees = driver.find_element_by_xpath("//*[@id='course-search-simple']/div[2]/div/div/div[1]/ul")
# print international_fees.text
courses_details = {}
next_page = driver.find_element_by_class_name("b-pagination__item--next")
courses_page = "https://sydney.edu.au/courses"
home_page = "https://sydney.edu.au"
counter = 0
# check till the html class "b-pagination__item--next is present on the page"
while next_page:
    # try:
    international_fees = driver.find_element_by_xpath(
        "//*[@id='course-search-simple']/div[2]/div/div/div[1]/ul")
    links = driver.find_elements_by_class_name("b-course-tag")
    for courses in links:
        # get href from the course list
        course_link = courses.get_attribute("href")
        print course_link
        course_text = courses.text
        # opens a course site
        file = urllib2.urlopen(course_link).read()
        # make a soup
        soup = BeautifulSoup(file)
        # find all data-attributes which has a value = data-requirements-url
        # requirements_url = soup.find_all("data-requirements-url")
        # list_fees = soup.find_all("data-fees-url")
        # fees_url = soup.find_all("data-requirements-url")
        requirements_url = [item['data-requirements-url'] for item in soup.findAll('div', attrs = {'data-requirements-url' : True})]
        fees_url = [item['data-fees-url'] for item in soup.findAll('div', attrs = {'data-fees-url' : True})]
        # find all data-attributes which has a value = data-fees-url
        content_json_link_fees = home_page + fees_url[0]
        content_json_requirements_url = home_page + requirements_url[0]
        # open json-fees file from url
        file_json_fees = urllib2.urlopen(content_json_link_fees).read()
        # open json-requiremnets file from url
        file_json_requirements = urllib2.urlopen(content_json_requirements_url).read()
        file_json_requirements_dict = json.loads(file_json_requirements)
        file_json_fees_dict = json.loads(file_json_fees)
        courses_details[course_text] = {}
        courses_details[course_text]["course"] = file_json_fees_dict
        courses_details[course_text]["course"]
    next_page = driver.find_element_by_class_name("b-pagination__item--next")
    print next_page.text
    next_page.click()
    time.sleep(3)
    print "clicking on next page"
    counter = counter+1
    print counter
f = open("demofile.json", "w")
f.write(json.dumps(courses_details))
print courses_details

