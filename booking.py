import time
import math
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from pyautogui import press, typewrite, hotkey


def convert_to_minutes(string):
    string_in = string.split('.')
    minutes = int(string_in[0]) * 60 + int(string_in[1])
    return minutes


def convert_to_hours(value):
    hours = int(value) / 60
    minutes = int(value) % 60
    # print(f'from add_hours:{math.floor(hours)}.{str(minutes).zfill(2)}')
    return f'{math.floor(hours)}.{str(minutes).zfill(2)}'


projects_assigned = {'R02426_Changchun VOLVO RE-DESIGN 1.2': [convert_to_minutes('11.3'),
                                                              convert_to_minutes('0.0')],
                     'R02428_RVS21xGM13': [convert_to_minutes('1.2'),
                                           convert_to_minutes('0.0')],
                     'R02209 MiniMab TVS N289_dPV': [convert_to_minutes('1.01'),
                                                     convert_to_minutes('0.0')]}


# projects_assigned = {'Internal: OEMs spec analysis': [5.0, 0.0]}


class Booking:
    def __init__(self, username):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.username = username
        self.password = config('PASSWORD')
        page = config('PAGE')
        self.driver.get(page)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.maximize_window()

    def login(self):
        # Get input field for username and place name
        self.driver.find_element(By.XPATH, '//*[@id="txtUserName"]').send_keys(self.username)
        self.driver.find_element(By.XPATH, '//*[@id="txtPassword"]').send_keys(self.password)
        self.driver.find_element(By.XPATH, '//*[@id="btnLogin"]').click()

    def go_to_project_workpackages(self):
        # Get project name and number of hours for the project
        self.driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()  # Button Bookings
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.XPATH, '//*[@id="ext-comp-1018__tab2"]').click()  # Button Workpackages Overview
        time.sleep(15)
        try:
            self.driver.find_element(By.ID, 'ext-gen120').click()  # Button expand all
        except NoSuchElementException:
            self.driver.find_element(By.ID, 'ext-gen116').click()  # Button expand all

    @staticmethod
    def convert_to_minutes(string):
        string_new = string.split('.')
        minutes = int(string_new[0]) * 60 + int(string_new[1])
        return minutes

    @staticmethod
    def add_hours(element, minutes_in):
        # Helper function for add_project_hours
        element.click()
        time.sleep(1)
        element.click()
        time.sleep(2)
        # new_value = str(hours).replace(':', '.')[:-3]
        # print(f'Data in:{hours} vs data out:{new_value}')
        # typewrite(f'{new_value}')
        typewrite(convert_to_hours(minutes_in))
        time.sleep(1)
        hotkey('Enter')

    def read_projects_workpackages(self):
        work_packages = self.driver.find_elements(By.CLASS_NAME, 'x-tree-col')
        all_projects = {}
        print("Wait for the program to read the work packages and hours")
        for index, package in enumerate(work_packages):
            if len(package.text) > 2 and "-2" not in package.text and "In work" not in package.text:
                if package.text not in "Test" and package.text not in "Assigned" and package.text not in "QL Testing":
                    # print(f'Index is:{index} and value is{package.text}')
                    if len(work_packages[index - 6].text) > 10 and work_packages[index - 1].text != '0.00':
                        all_projects[f'{work_packages[index - 6].text}'] = [
                            convert_to_minutes(work_packages[index - 1].text),
                            convert_to_minutes(work_packages[index].text)]
        print(f'{self.username} projects are:\n {all_projects}')
        return all_projects

    def go_to_daily_bookings(self):

        self.driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.XPATH, '//*[@id="lbtnBooking"]').click()  # Button Bookings
        self.driver.implicitly_wait(3)

        #  ---------------------delete up to here after test-----------------
        self.driver.find_element(By.XPATH, '//*[@id="ext-comp-1018__tab0"]').click()  # Button DailyBookings
        time.sleep(15)
        self.driver.find_element(By.XPATH, '//*[@id="ext-gen37"]').click()  # Button Expand All

    def add_project_hours(self):
        global minutes_left_to_book
        work_packages = self.driver.find_elements(By.CLASS_NAME, 'x-tree-col')
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
                        try:
                            while ', ' and ' 20' not in work_packages[index + extra + add_one_time].text:
                                # print(index + extra + add_one_time)
                                # print(f'{index + extra}:{work_packages[index + extra].text}')
                                # Checks the column with Date / Work packages and if it finds a project assigned to the
                                # person and with enough hours left to book in work packages it will fill the entry form and
                                # subtracts the time from the project assigned hours.
                                name_of_project = work_packages[index + extra].text
                                minutes_worked = convert_to_minutes(work_packages[index + 3].text)
                                minutes_left_to_book = minutes_worked
                                for project in projects_assigned:
                                    # print(f"{project} in list")
                                    if name_of_project in projects_assigned:
                                        # print(name_of_project)
                                        project_assigned_minutes_remaining = projects_assigned[f'{name_of_project}'][0]
                                        if project_assigned_minutes_remaining > 0:
                                            # print(
                                            #     f'IF:{minutes_left_to_book} = {minutes_worked} - {project_assigned_minutes_remaining}')
                                            # print( f'Found:{name_of_project} with {project_assigned_minutes_remaining}
                                            # hours remaining')
                                            if minutes_worked > project_assigned_minutes_remaining:
                                                self.add_hours(work_packages[index + extra + 2],
                                                               project_assigned_minutes_remaining)
                                                projects_assigned[f'{name_of_project}'][
                                                    1] += project_assigned_minutes_remaining
                                                projects_assigned[f'{name_of_project}'][0] = 0
                                                minutes_left_to_book = minutes_worked - project_assigned_minutes_remaining
                                                print(
                                                    f'IF:{minutes_left_to_book} = {minutes_worked} - {project_assigned_minutes_remaining}')
                                            else:
                                                self.add_hours(work_packages[index + extra + 2],
                                                               minutes_left_to_book)
                                                projects_assigned[f'{name_of_project}'][1] = \
                                                    projects_assigned[f'{name_of_project}'][1] + minutes_left_to_book
                                                projects_assigned[f'{name_of_project}'][0] = \
                                                    projects_assigned[f'{name_of_project}'][0] - minutes_left_to_book
                                        break
                                add_one_time = 0
                                extra += 6
                        except IndexError:
                            pass
        projects_assigned['Hours not booked'] = [0, minutes_left_to_book]
        # print(f'Index is:{index} and value is{package.text}')
        return [projects_assigned]
