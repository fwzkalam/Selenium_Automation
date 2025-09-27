from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://demoqa.com/alerts")

#driver.find_element(By.ID, "alertButton").click()
#driver.find_element(By.ID, "confirmButton").click()
driver.find_element(By.ID, "promtButton").click()
time.sleep(3)
driver.switch_to.alert.send_keys("Hallo!!!") #isi teks box
time.sleep(3)
driver.switch_to.alert.accept()

time.sleep(5)