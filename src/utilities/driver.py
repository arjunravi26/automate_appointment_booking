import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from typeguard import typechecked


@typechecked
def load_driver(url: str = "https://arjunravi26.github.io/appointment-booking/") -> Chrome:
    options = Options()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    try:
        driver.get(url=url)
    except Exception as e:
        print(f"Exception occured! {e}")
    return driver
