from selenium import webdriver
import pytest

@pytest.fixture(scope='function')
def setup(request):
    print("initiating chrome driver")

    # chromedriver should be added to Windows PATH directory
    driver = webdriver.Chrome()
    request.instance.driver = driver
    driver.get('https://www.aptekagemini.pl/')
    assert test_data.main_page_title in driver.title
    driver.maximize_window()

    yield driver
    driver.close()

class test_data:

    registration_page_url = 'https://www.aptekagemini.pl/user/createAccount'
    login_page_url = 'https://www.aptekagemini.pl/user/loginUser'

    # user data
    username = 'malinowska2020@o2.pl'
    user_password = '123456'

    # expected results
    main_page_title = 'Apteka Gemini'
    registration_page_title = 'Koszyk'
    login_page_title = 'AptekaGemini.pl'



class components:
    # gets the desired url
    def open_site(self, url, title):
        self.driver.get(url)
        assert title in self.driver.title, 'błąd otwierania strony'

    # enters desired value into desired input
    def fill_input(self, input, value):
        input.send_keys(value)

    # clicks on desired element
    def click_on_element(self, element):
        element.click()

    def assert_if_element_is_displayed(self, element):
        assert element.is_displayed()



    def fill_login(self, value):
        input = self.driver.find_element_by_id('st_form-user-email')
        components.fill_input(self, input, value)

    def fill_registration_password(self, value):
        input = self.driver.find_element_by_id('st_form-user-password1')
        components.fill_input(self, input, value)

    def fill_registration_password_confirmation(self, value):
        input = self.driver.find_element_by_id('st_form-user-password2')
        components.fill_input(self, input, value)

    def fill_login_password(self, value):
        input = self.driver.find_element_by_xpath("//input[@type='password']")
        components.fill_input(self, input, value)

    def check_user_privacy(self):
        element = self.driver.find_element_by_id('st_form-user-privacy')
        components.click_on_element(self, element)

    def submit_account(self):
        element = self.driver.find_element_by_id('st_button-user-account')
        components.click_on_element(self, element)

    def submit_login(self):
        element = self.driver.find_element_by_xpath("//button[@class='act_button login']")
        components.click_on_element(self, element)

    def check_for_terms_not_matched(self):
        element = self.driver.find_element_by_xpath('//span[contains(text(),"regulamin")]')
        components.assert_if_element_is_displayed(self, element)

    def check_if_user_logged_in(self):
        element = self.driver.find_element_by_xpath("//a[@class='nav-user-link']")
        components.click_on_element(self, element)
        self.driver.implicitly_wait(5)
        element = self.driver.find_element_by_xpath("//a[@class='user_mail']")
        components.assert_if_element_is_displayed(self, element)

    # closes browser window
    def close(self):
        self.driver.quit()


@pytest.mark.usefixtures("setup")
class TestRunRegistration:
    def test_registration_no_user_privacy(self):
        components.open_site(self, test_data.registration_page_url, test_data.registration_page_title)
        components.fill_login(self, test_data.username)
        components.fill_registration_password(self, test_data.user_password)
        components.fill_registration_password_confirmation(self, test_data.user_password)
    # clicks the submit button without checking 'user policy' checkbox
        components.submit_account(self)
        components.check_for_terms_not_matched(self)

@pytest.mark.usefixtures("setup")
class TestRunLogin:
    def test_login_positive (self):
        components.open_site(self, test_data.login_page_url, test_data.login_page_title)
        components.fill_login(self, test_data.username)
        components.fill_login_password(self, test_data.user_password)
        components.submit_login(self)
        components.check_if_user_logged_in(self)



