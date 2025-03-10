from selenium.webdriver.common.by import By
class LocatorManager:
    LOCATORS = {
        "name_input": (By.ID, "name"),
        "email_input": (By.ID, "email"),
        "phone_input": (By.ID, "phone"),
        "service_dropdown": (By.ID, "service"),
        "submit_button": (By.TAG_NAME, "button"),
        "time_slot": (By.CLASS_NAME, "date-slot"),
        "day_text": (By.CLASS_NAME, "date-day"),
        "time_options": (By.CLASS_NAME, "time-options")
    }

    @classmethod
    def get_locator(cls, element_name):
        """
        Retrieve the locator tuple for a given element name.
        """
        locator = cls.LOCATORS.get(element_name)
        if locator is None:
            raise Exception(f"Locator for '{element_name}' is not defined.")
        return locator