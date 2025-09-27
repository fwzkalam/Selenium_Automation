from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

driver.get("https://demoqa.com/menu")
driver.implicitly_wait(20)

#cara1
#menu = driver.find_element(By.LINK_TEXT, "Main Item 2")
#hover = ActionChains(driver).move_to_element(menu)
#hover.perform()

#cara2
ActionChains(driver).move_to_element(
    (driver.find_element(By.XPATH, '//*[@id="nav"]/li[2]/a'))
).perform()
ActionChains(driver).move_to_element(
    (driver.find_element(By.XPATH, "//*[@id='nav']/li[2]/ul/li[3]/a"))
).perform()


time.sleep(5)
