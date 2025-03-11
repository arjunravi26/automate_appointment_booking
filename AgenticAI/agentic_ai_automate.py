import json
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
import undetected_chromedriver as uc
from phi.agent.agent import Agent
from phi.model.groq.groq import Groq
from utility import LocatorManager
from dotenv import load_dotenv
load_dotenv()


def agent():
    "Function to load llm model"
    model_name = "llama-3.3-70b-versatile"
    return Agent(model=Groq(id=model_name))


def plan_steps(command: str) -> list:
    """
    Ask the LLM to generate a JSON array where each element is a step.
    Each step should be an object with:
    - action: what to do (e.g., "fill", "click", "select")
    - field: the field name (e.g., "name", "email", "phone", "service", "insurance")
    - locator: the key for the locator from LocatorManager
    - value: (optional) value to fill (if applicable)
    The agent should output valid JSON.
    """
    website_link = "https://arjunravi26.github.io/appointment-booking/"
    prompt = (
        f"Given the command: '{command}', generate a JSON array of step-by-step actions for automating "
        f"the appointment booking process on {website_link}. For each step, include the following keys: "
        f"'action' (one of 'fill', 'click', or 'select'), 'field' (e.g., 'name', 'email', 'phone', etc.), "
        f"'locator' (e.g., 'name_input', 'email_input', etc.), and 'value' (if applicable). "
        f"Include any new fields found in the command automatically. Output JSON format only, not any other things(like heading or any other things.)."
    )
    response = agent().run(prompt)
    print(response.content)
    try:
        steps = json.loads(response.content)
    except Exception as e:
        print(f"Error parsing JSON from LLM response: {e}")
        steps = []
    print("Generated Steps:", steps)
    return steps


def execute_plan(steps: list, driver, context: dict):
    """
    Execute each step based on the generated JSON plan.
    The context dict provides default values for fields.
    """
    for step in steps:
        try:
            action = step.get("action", "").lower()
            field = step.get("field", "").lower()
            locator_key = step.get("locator", "")
            value = step.get("value")
            # If the value is not provided by the agent, check the context.
            if value is None:
                value = context.get(field, "")
            locator = LocatorManager.get_locator(locator_key)
            element = driver.find_element(*locator)
            print(
                f"Executing: {action} on {field} using locator {locator_key}")
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
    time.sleep(5)
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(LocatorManager.get_locator('time_slot')))
    time_slot = driver.find_elements(
        *LocatorManager.get_locator('time_slot'))
    available_slots = []
    for slot in time_slot:
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located(LocatorManager.get_locator('day_text')))
        day = slot.find_element(
            *LocatorManager.get_locator('day_text')).text
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located(LocatorManager.get_locator('time_options')))
        day_times = slot.find_elements(
            *LocatorManager.get_locator('time_options'))
        d_times = []
        for dt in day_times:
            d_times.append(dt.text)
        available_slots .append([day, d_times])
    print(available_slots)


if __name__ == "__main__":
    options = Options()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    website_url = "https://arjunravi26.github.io/appointment-booking/"
    driver.get(url=website_url)

    # Updated user command including a new field "insurance number"
    user_command = (
        "Book an appointment for John Doe with email john@example.com, "
        "phone 1234567890, service Initial Consultation, and insurance number INS12345."
    )
    # Context now includes an entry for insurance (if not provided by the agent)
    context = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "service": "Initial Consultation",
        "insurance": "INS12345"
    }
    steps = plan_steps(user_command)
    execute_plan(steps, driver, context)
    driver.quit()
