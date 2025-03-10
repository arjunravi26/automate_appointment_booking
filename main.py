import undetected_chromedriver as uc
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

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
        ec.presence_of_all_elements_located((By.ID, 'name'))
    )
    name_input = driver.find_element(By.ID, 'name')
    name_input.clear()
    name_input.send_keys(name)
    WebDriverWait(driver=driver, timeout=5).until(
        ec.presence_of_all_elements_located((By.ID, 'email'))
    )
    email_input = driver.find_element(By.ID, 'email')
    email_input.clear()
    email_input.send_keys(email)
    WebDriverWait(driver=driver, timeout=5).until(
        ec.presence_of_all_elements_located((By.ID, 'phone'))
    )
    number_input = driver.find_element(By.ID, 'phone')
    number_input.clear()
    number_input.send_keys(phone_number)
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "service"))
    )
    service_input = Select(driver.find_element(By.ID, "service"))
    all_options = service_input.options  # Get a list of all options

    # for option in all_options:
    #     print(option.text)
    service_input.select_by_visible_text(service)
    submit_btn = driver.find_element(By.TAG_NAME, "button")
    submit_btn.click()
    time_slot_page = driver.find_elements(By.CLASS_NAME, 'date-slot')
    print(time_slot_page)
    avaliable_slots = []
    for slot in time_slot_page:
        day = slot.find_element(By.CLASS_NAME, 'date-day').text
        day_times = slot.find_elements(By.CLASS_NAME, 'time-options')
        d_times = []
        for dt in day_times:
            d_times.append(dt.text)

        avaliable_slots.append([day, d_times])

    print(avaliable_slots)


except Exception as e:
    print(f"An error occured: {e}")
finally:
    time.sleep(10)
    driver.quit()
