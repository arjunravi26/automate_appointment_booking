from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def extract_page_elements(driver):
    elements_data = []

    # Define a list of tags to extract
    tags = ["input", "textarea", "button", "select", "label"]
    for tag in tags:
        elements = driver.find_elements(By.TAG_NAME, tag)
        for elem in elements:
            try:
                elem_info = {
                    "tag": tag,
                    "id": elem.get_attribute("id"),
                    "name": elem.get_attribute("name"),
                    "class": elem.get_attribute("class"),
                    "placeholder": elem.get_attribute("placeholder"),
                    "text": elem.text.strip()
                }
                elements_data.append(elem_info)
            except Exception as e:
                print(f"Error extracting {tag} element: {e}")
    return elements_data


# Example usage:
driver = uc.Chrome()
url = 'https://arjunravi26.github.io/appointment-booking/'
driver.get(url)
elements = extract_page_elements(driver)
print(elements)
# Now use 'elements' to dynamically update your selectors or re-plan actions.
