import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


class Booking:
    def __init__(self, name):
        self.name = name
        password = 'qlpttadmin'
        driver.get('http://suas062-vm/ptt/Login.aspx?change_user=true')
        self.wait = WebDriverWait(driver, 10)

    def login(self):
        # Get input field for user name and place name
        driver.find_element(By.XPATH, '//*[@id="txtUserName"]').send_keys("iancr")
        driver.find_element(By.XPATH, '//*[@id="txtPassword"]').send_keys("qlpttadmin")
        driver.find_element(By.XPATH, '//*[@id="btnLogin"]').click()

    def get_project_hours(self):
        # Get project name and number of hours for the project
        driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()  # Button Bookings
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, '//*[@id="ext-comp-1018__tab2"]').click()  # Button Workpackages Overview
        time.sleep(10)
        try:
            driver.find_element(By.ID, 'ext-gen120').click()  # Button expand all
        except NoSuchElementException:
            driver.find_element(By.ID, 'ext-gen116').click()  # Button expand all
        work_packages = driver.find_elements(By.CLASS_NAME, 'x-tree-col')
        all_projects = {}
        project = ''
        for index, package in enumerate(work_packages):
            if len(package.text) > 2 and "-2" not in package.text and "In work" not in package.text:
                if package.text not in "Test" and package.text not in "Assigned" and package.text not in "QL Testing":
                    if len(package.text) > 5:
                        project = package.text
                        all_projects[f'{package.text}'] = []
                    else:
                        if len(work_packages[index - 1].text) > 5:
                            all_projects[f'{work_packages[index-1].text}'] = work_packages[index].text
                        # else:
                        #     all_projects[f'{work_packages[index - 2].text}'] = work_packages[index].text
                        # print(work_packages[index].text)
                    # print(work_packages[690].text)
                    # print(package.text)
                    # print(index)
        print(all_projects)


#  and "Test" not in package.text and "Assigned" not in package.text and "QL Testing" not in package.text
# //*[@id="ext-comp-1018__tab0"] -daily bookings
# //*[@id="lbtnUpdateOverview2"] -update overview
nume = Booking('iancr')
nume.login()
nume.get_project_hours()
