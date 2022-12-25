from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

email = "qwerasdf@mail.ru"
password = "12345"

@pytest.fixture(autouse=True)
def testing():
  pytest.driver = webdriver.Chrome()
  pytest.driver.get('http://petfriends.skillfactory.ru/login')
  yield
  pytest.driver.quit()

def test_show_all_pets():
  pytest.driver.implicitly_wait(5)
  pytest.driver.find_element(By.ID, 'email').send_keys(email)
  pytest.driver.find_element(By.ID, 'pass').send_keys(password)
  pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
  images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
  names = pytest.driver.find_elements(By.XPATH, '//h5[@class = "card-title"]')
  descriptions = pytest.driver.find_elements(By.XPATH, '//p[@class = "card-text"]')
  for i in range(len(names)):
    assert images[i].get_attribute('src') != ''
    assert names[i].text != ''
    assert descriptions[i].text != ''
    assert ', ' in descriptions[i].text
    parts = descriptions[i].text.split(', ')
    assert len(parts[0]) > 0
    assert len(parts[1]) > 0

def test_show_my_pets():
  pytest.driver.find_element(By.ID, 'email').send_keys(email)
  pytest.driver.find_element(By.ID, 'pass').send_keys(password)
  pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
  pytest.driver.find_element(By.XPATH, '//a[contains(text(),"Мои питомцы")]').click()
  my_pets = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr')))
  photos = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr/th/img')))
  have_photo = [i for i in photos if i.get_attribute('src') != '' ]
  names = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr/td[1]')))
  has_name = [i for i in names if i.text != '' ]
  unique_names = set([i.text.lower() for i in names ])
  assert len(my_pets) == 4
  assert len(have_photo) >= len(my_pets)//2
  assert len(names) == len(has_name)
  assert len(names) == len(unique_names)
