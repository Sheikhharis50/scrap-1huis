from selenium import webdriver


class Browser:
    def __init__(self, detach=False, maximize=False, headless=False):
        self.options = webdriver.ChromeOptions()
        self.detach = detach

        # setting options
        self.options.add_experimental_option("detach", detach)
        if maximize:
            self.options.add_argument("--start-maximized")
        if headless:
            self.options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=self.options)

    def __enter__(self):
        return self.driver

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if not self.detach:
            self.driver.close()
