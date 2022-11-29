import time
from decouple import config
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # used to press enter key
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


class Booking:
    def __init__(self, name):

        self.name = name
        self.password = config('PASSWORD')
        page = config('PAGE')
        driver.get(page)
        self.wait = WebDriverWait(driver, 10)
        driver.maximize_window()

    def login(self):
        # Get input field for user name and place name
        driver.find_element(By.XPATH, '//*[@id="txtUserName"]').send_keys(self.name)
        driver.find_element(By.XPATH, '//*[@id="txtPassword"]').send_keys(self.password)
        driver.find_element(By.XPATH, '//*[@id="btnLogin"]').click()

    def go_to_project_workpackages(self):
        # Get project name and number of hours for the project
        driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()  # Button Bookings
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, '//*[@id="ext-comp-1018__tab2"]').click()  # Button Workpackages Overview
        time.sleep(15)
        try:
            driver.find_element(By.ID, 'ext-gen120').click()  # Button expand all
        except NoSuchElementException:
            driver.find_element(By.ID, 'ext-gen116').click()  # Button expand all

    def read_projects_workpackages(self):
        work_packages = driver.find_elements(By.CLASS_NAME, 'x-tree-col')
        all_projects = {}
        print("Wait for the program to read the work packages and hours")
        for index, package in enumerate(work_packages):
            if len(package.text) > 2 and "-2" not in package.text and "In work" not in package.text:
                if package.text not in "Test" and package.text not in "Assigned" and package.text not in "QL Testing":
                    # print(f'Index is:{index} and value is{package.text}')
                    if len(work_packages[index - 6].text) > 10 and work_packages[index - 1].text != '0.00':
                        all_projects[f'{work_packages[index - 6].text}'] = [float(work_packages[index - 1].text),
                                                                            float(work_packages[index].text)]
        print(f'{self.name} projects are:\n {all_projects}')
        return all_projects

    def go_to_daily_bookings(self):
        driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()  # Button Bookings
        driver.implicitly_wait(3)
        #  ---------------------delete up to here after test-----------------
        driver.find_element(By.XPATH, '//*[@id="ext-comp-1018__tab0"]').click()  # Button DailyBookings
        time.sleep(15)
        driver.find_element(By.XPATH, '//*[@id="ext-gen37"]').click()  # Button Expand All
        work_packages = driver.find_elements(By.CLASS_NAME, 'x-tree-col')
        for index, package in enumerate(work_packages):
            if len(package.text) > 3:
                if ', ' in package.text:
                    if len(work_packages[index + 3].text) > 3 and float(work_packages[
                                                                            index + 4].text) > 0.01:  # Takes the value from the time difference column(index+3)
                        # float(work_packages[index+3].text) -valoare pentru pontaj
                        extra = 0
                        add_one_time = 1 # value added to offset first read by 1 index
                        print(f'Start new day: {work_packages[index].text}')
                        while ', ' not in work_packages[index + extra + add_one_time].text:
                            print(f'{index+extra}:{work_packages[index + extra].text}')
                            if work_packages[index + extra].text == 'R02426_Kaunas VOLVO RE-DESIGN 1.2':
                                work_packages[index + extra+ 2].click()
                                time.sleep(1)
                                work_packages[index + extra + 2].click()
                                time.sleep(2)
                                work_packages[index + extra + 2].send_keys('1')
                                time.sleep(1)
                                # work_packages[index + extra + 2].send_keys(Keys.ENTER)
                                print(work_packages[index + extra + 2].text)
                                break

                            add_one_time = 0
                            extra += 6
                # print(f'Index is:{index} and value is{package.text}')


# //*[@id="ext-gen37"] Button DailyBookings
#  and "Test" not in package.text and "Assigned" not in package.text and "QL Testing" not in package.text
# //*[@id="ext-comp-1018__tab0"] -daily bookings
# //*[@id="lbtnUpdateOverview2"] -update overview

nume = Booking('iancr')
nume.login()
# nume.go_to_project_workpackages()
# nume.read_projects_workpackages()
nume.go_to_daily_bookings()
