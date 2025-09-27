from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import time

driver = webdriver.Chrome()

#cara 1
#driver.get("https://demoqa.com/upload-download")

#driver.find_element(By.ID, "uploadFile").send_keys("D:/Kalam/FormTTD.pdf")

#cara 2
driver.get("https://gofile.io/d/90b9cea9-af22-4dc5-b556-1e070666589f")