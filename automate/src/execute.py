import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from .review import review
from .utilities.driver import load_driver


def execute_plan(steps: list):
    """
    Execute each step based on the generated JSON plan.
    The context dict provides default values for fields.
    """
    driver = load_driver()
    for step in steps:
        print(step)
        try:
            action = step.get("action", "").lower()
            field = step.get("field", "").lower()
            value = step.get("value")
            attribute_by = step.get('locator').get('attribute')
            attribute_name = step.get('locator').get('value')
            # If the value is not provided by the agent, check the context.
            # if value is None:
            #     value = context.get(field, "")
            element = driver.find_element(attribute_by, attribute_name)
            print(
                f"Executing: {action} on {field} using locator {attribute_name}")
            if action == "fill":
                element.clear()
                element.send_keys(value)
                time.sleep(1)
            elif action == "click":
                element.click()
                time.sleep(1)
            elif action == "select":
                # For select, we assume sending keys works or you can integrate with Select class.
                element = Select(element)
                element.select_by_visible_text(value)
                time.sleep(1)
            else:
                print(f"Unknown action: {action}")
        except Exception as e:
            print(
                f"Error executing step for field '{step.get('field')}' with locator '{step.get('locator')}': {e}")
    time.sleep(1)
    # try:
    #     contents = driver.find_element(by=By.TAG_NAME, value='body')
    # except Exception as e:
    #     print(f"Error in scraping body: {e}")

    date_slots = driver.find_elements(By.CLASS_NAME,"date-slot")
    print(date_slots)
    slots = {}
    for date_slot in date_slots:
        day = date_slot.find_element(By.CLASS_NAME,'date-day').text
        avaliable_times = date_slot.find_elements(By.CLASS_NAME,'time-option')
        slots[day] = []
        print(avaliable_times)
        for aval_time in avaliable_times:
            slots[day].append(aval_time.text)
    print(slots)
    driver.quit()
    return slots


if __name__ == "__main__":
    command = "Book an appointment for Nihal with email nihal@gmail.com, phone 1234567890, service Initial Consultation, and insurance number INS12345."
    final_step = review(command)
    execute_plan(final_step)
