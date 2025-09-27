from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# explisitly
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException 

driver = webdriver.Chrome()

#implicitly wait
#driver.implicitly_wait(5) #akan menunggu masing" perintah (5) detik
#driver.get("https://demoqa.com/login")
#driver.get("https://demoqa.com/books")

#driver.find_element(By.ID, "login").click()




#explicitly
driver.get("https://demoqa.com/alerts")

driver.find_element(By.ID, "timerAlertButton").click()

try:
    WebDriverWait(driver, 30).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    print("alert di pencet")
    
except TimeoutException:
    print("alert tidak muncul")
    pass

time.sleep(5)