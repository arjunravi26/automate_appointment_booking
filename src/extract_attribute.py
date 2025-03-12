from selenium.webdriver.common.by import By
from utilities.driver import load_driver


def find_element_attributes():
    driver = load_driver()
    element_attributes = []
    form_elements = driver.find_elements(
        By.CSS_SELECTOR, 'form input, form select, form textarea, form button')
    for element in form_elements:
        attributes = {
            'tag': element.tag_name,
            'id': element.get_attribute('id'),
            'class': element.get_attribute('class'),
            'name': element.get_attribute('name'),
            'placeholder': element.get_attribute('placeholder'),
            'required': element.get_attribute('required'),
            "text": element.text.strip()
        }
        element_attributes.append(attributes)
    return element_attributes

if __name__ == "__main__":
    attributes = find_element_attributes()
    print(attributes)
