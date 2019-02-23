import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.urls import reverse_lazy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from utils.django.tests import get_chromedriver

User = get_user_model()


class Command(BaseCommand):
    HOST = 'localhost:8000'
    URL = f'{HOST}{reverse_lazy("members:signup")}'
    EMAIL = settings.TEST_COMPANY_EMAIL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = get_chromedriver()

    def handle(self, *args, **options):
        User.objects.filter(email=self.EMAIL).delete()

        # 회원가입 페이지
        self.driver.get(self.URL)

        # 채용연계기업 회원가입 클릭
        self.driver.find_element_by_css_selector('a[href="/signup/company/"]').click()

        # 폼이 나올때까지 기다리기
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#signup-company-form')
            )
        )

        # 폼 채우기
        self.driver.find_element_by_id('id_email').send_keys(self.EMAIL)
        self.driver.find_element_by_id('id_last_name').send_keys('이')
        self.driver.find_element_by_id('id_first_name').send_keys('한영')
        self.driver.find_element_by_id('id_password1').send_keys('dlgksdud')
        self.driver.find_element_by_id('id_password2').send_keys('dlgksdud')
        self.driver.find_element_by_id('id_phone_number').send_keys('010-1234-1234')
        self.driver.find_element_by_id('id__position').send_keys('사원')
        Select(self.driver.find_element_by_id('id__company')).select_by_index(0)
        self.driver.find_element_by_id('id_hire_job_groups').find_element_by_css_selector('input[type="checkbox"]').click()
        self.driver.find_element_by_css_selector('label[for="check-signup1"]').click()
        self.driver.find_element_by_css_selector('label[for="check-signup2"]').click()

        # 회원가입 버튼 클릭
        self.driver.find_element_by_css_selector('button#btn-submit').click()

        # Index나올때까지 기다리기
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.index-container')
            )
        )
        self.driver.find_element_by_css_selector('.alert.alert-success')
        time.sleep(5)
