import time
from decouple import config
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.relative_locator import locate_with
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # used to press enter key
from pyautogui import press, typewrite, hotkey
import datetime

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

projects_assigned = {'R02426_Changchun VOLVO RE-DESIGN 1.2': [datetime.timedelta(hours=float(5.0)),
                                                              datetime.timedelta(hours=float(0.0))],
                     'R02395_AUD_MQB_21_DCU_DIS_CCQ': [datetime.timedelta(hours=float(5.0)),
                                                       datetime.timedelta(hours=float(0.0))],
                     'R02245 AUD_XXXX_16_PNEU': [datetime.timedelta(hours=float(5.0)),
                                                 datetime.timedelta(hours=float(0.0))]}


# projects_assigned = {'Internal: OEMs spec analysis': [5.0, 0.0]}


class Booking:
    def __init__(self, name):

        self.name = name
        self.password = config('PASSWORD')
        page = config('PAGE')
        driver.get(page)
        self.wait = WebDriverWait(driver, 10)
        driver.maximize_window()

    def login(self):
        # Get input field for username and place name
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

    @staticmethod
    def to_datetime(str_or_float_to_datetime):
        result = datetime.timedelta(hours=float(str_or_float_to_datetime))
        return result

    def read_projects_workpackages(self):
        work_packages = driver.find_elements(By.CLASS_NAME, 'x-tree-col')
        all_projects = {}
        print("Wait for the program to read the work packages and hours")
        for index, package in enumerate(work_packages):
            if len(package.text) > 2 and "-2" not in package.text and "In work" not in package.text:
                if package.text not in "Test" and package.text not in "Assigned" and package.text not in "QL Testing":
                    # print(f'Index is:{index} and value is{package.text}')
                    if len(work_packages[index - 6].text) > 10 and work_packages[index - 1].text != '0.00':
                        all_projects[f'{work_packages[index - 6].text}'] = [
                            Booking.to_datetime(work_packages[index - 1].text),
                            Booking.to_datetime(work_packages[index].text)]
        print(f'{self.name} projects are:\n {all_projects}')
        return all_projects

    def go_to_daily_bookings(self):

        driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()  # Button Bookings
        driver.implicitly_wait(3)

        #  ---------------------delete up to here after test-----------------
        def add_hours(element, hours):
            # Helper function
            element.click()
            time.sleep(1)
            element.click()
            time.sleep(2)
            new_value = str(hours).replace(':', '.')[:-3]
            typewrite(f'{new_value}')
            time.sleep(1)
            hotkey('Enter')

        driver.find_element(By.XPATH, '//*[@id="ext-comp-1018__tab0"]').click()  # Button DailyBookings
        time.sleep(15)
        driver.find_element(By.XPATH, '//*[@id="ext-gen37"]').click()  # Button Expand All
        work_packages = driver.find_elements(By.CLASS_NAME, 'x-tree-col')
        for index, package in enumerate(work_packages):
            if len(package.text) > 3:
                if ', ' in package.text:
                    if len(work_packages[index + 3].text) > 3 and float(work_packages[
                                                                            index + 4].text) > 0.01:  # Takes the
                        # value from the time difference column(index+3)
                        # print(float(work_packages[index+3].text)) #-valoare pentru pontaj
                        extra = 0
                        add_one_time = 1  # value added to offset first read by 1 index
                        print(
                            f'Start new day: {work_packages[index].text} with {float(work_packages[index + 3].text)} hours')
                        while ', ' and ' 20' not in work_packages[index + extra + add_one_time].text:
                            # print(f'{index + extra}:{work_packages[index + extra].text}')
                            # Checks the column with Date / Work packages and if it finds a project assigned to the
                            # person and with enough hours left to book in work packages it will fill the entry form and
                            # subtracts the time from the project assigned hours.
                            name_of_project = work_packages[index + extra].text
                            hours_worked = Booking.to_datetime(work_packages[index + 3].text)
                            hours_left_to_book = hours_worked
                            for project in projects_assigned:
                                # print(f"{project} in list")
                                if name_of_project in projects_assigned:
                                    print(name_of_project)
                                    project_assigned_hours_remaining = projects_assigned[f'{name_of_project}'][0]
                                    if project_assigned_hours_remaining > Booking.to_datetime(0.0):
                                        print(
                                            f'Found:{name_of_project} with {project_assigned_hours_remaining} hours remaining')
                                        if hours_worked > project_assigned_hours_remaining:
                                            add_hours(work_packages[index + extra + 2],
                                                      project_assigned_hours_remaining)
                                            projects_assigned[f'{name_of_project}'][
                                                1] += project_assigned_hours_remaining
                                            projects_assigned[f'{name_of_project}'][0] = Booking.to_datetime(0)
                                            hours_left_to_book = hours_worked - project_assigned_hours_remaining
                                        else:
                                            add_hours(work_packages[index + extra + 2],
                                                      hours_left_to_book)
                                            projects_assigned[f'{name_of_project}'][1] = \
                                            projects_assigned[f'{name_of_project}'][1] + hours_left_to_book
                                            projects_assigned[f'{name_of_project}'][0] = \
                                            projects_assigned[f'{name_of_project}'][0] - hours_left_to_book
                                    break
                            add_one_time = 0
                            extra += 6
        print(projects_assigned)
        # print(f'Index is:{index} and value is{package.text}')


name = Booking('iancr')
name.login()
# name.go_to_project_workpackages()
# name.read_projects_workpackages()
name.go_to_daily_bookings()
