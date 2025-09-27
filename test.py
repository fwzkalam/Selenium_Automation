import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://the-internet.herokuapp.com/windows") #perintah membuka web browser

#driver.find_element(By.ID, "username").send_keys("ica cantik")
#driver.find_element(By.ID, "password").send_keys("123456")
#driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

#driver.find_element(By.LINK_TEXT, "Elemental Selenium").click()

driver.find_element(By.LINK_TEXT, "Click Here").click()

time.sleep(4)

driver.switch_to.window(driver.window_handles[0]) #pindah ke halaman sebelumnya "[0] adalah halaman tab yang terbuka"

time.sleep(4)

driver.switch_to.window(driver.window_handles[1])

time.sleep(8) #kasih jeda (10 detik)
