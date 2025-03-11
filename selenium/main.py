import undetected_chromedriver as uc
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from utility import LocatorManager

driver = uc.Chrome()
name = "Arjun Ravi"
email = "arjunravi726@gmail.com"
phone_number = "9847637962"
service = "Initial Consultation"
services = [
    "Initial Consultation",
    "Follow-up Appointment",
    "Regular Check-up",
    "Emergency Service"
]
try:
    url = 'https://arjunravi26.github.io/appointment-booking/'
    driver.get(url=url)
    time.sleep(1)
    driver.maximize_window()
    WebDriverWait(driver=driver, timeout=5).until(
        ec.presence_of_all_elements_located(
            LocatorManager.get_locator('name_input'))
    )
    name_input = driver.find_element(*LocatorManager.get_locator('name_input'))
    name_input.clear()
    name_input.send_keys(name)
    WebDriverWait(driver=driver, timeout=5).until(
        ec.presence_of_all_elements_located(
            LocatorManager.get_locator('email_input'))
    )
    email_input = driver.find_element(
        *LocatorManager.get_locator('email_input'))
    email_input.clear()
    email_input.send_keys(email)
    WebDriverWait(driver=driver, timeout=5).until(
        ec.presence_of_all_elements_located(
            LocatorManager.get_locator('phone_input'))
    )
    number_input = driver.find_element(
        *LocatorManager.get_locator('phone_input'))
    number_input.clear()
    number_input.send_keys(phone_number)
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(
            LocatorManager.get_locator('service_dropdown'))
    )
    service_input = Select(driver.find_element(
        *LocatorManager.get_locator('service_dropdown')))
    all_options = service_input.options
    service_input.select_by_visible_text(service)
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(LocatorManager.get_locator('submit_button')))
    submit_btn = driver.find_element(
        *LocatorManager.get_locator('submit_button'))
    submit_btn.click()
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(LocatorManager.get_locator('time_slot')))
    time_slot = driver.find_elements(*LocatorManager.get_locator('time_slot'))
    available_slots = []
    for slot in time_slot:
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located(LocatorManager.get_locator('day_text')))
        day = slot.find_element(*LocatorManager.get_locator('day_text')).text
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located(LocatorManager.get_locator('time_options')))
        day_times = slot.find_elements(*LocatorManager.get_locator('time_options'))
        d_times = []
        for dt in day_times:
            d_times.append(dt.text)
        available_slots .append([day, d_times])
    print(available_slots)

except Exception as e:
    print(f"An error occured: {e}")
finally:
    time.sleep(10)
    driver.quit()
