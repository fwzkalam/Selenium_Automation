"""
login_tests_simple.py
Sederhana, mudah dibaca, dan langsung menjalankan beberapa skenario login:
- Positive: standard_user / secret_sauce -> sukses
- Negative: empty username, empty password, wrong credentials, locked_out_user

Cara pakai:
  python -m pip install selenium webdriver-manager
  python login_tests_simple.py
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"

# ----------------------
# Helper / Utility
# ----------------------
def create_driver(headless=False):
    """Buat Chrome webdriver sederhana. Headless opsional."""
    from selenium.webdriver.chrome.options import Options
    opts = Options()
    if headless:
        # Non-headless default so developer can see browser (easier debugging)
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=1200,800")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(2)  # timeout singkat agar test responsif
    return driver

def open_login_page(driver):
    driver.get(BASE_URL)

def fill_and_submit(driver, username, password):
    """Isi form login dan submit."""
    # temukan elemen
    user_input = driver.find_element(By.ID, "user-name")
    pass_input = driver.find_element(By.ID, "password")
    login_btn = driver.find_element(By.ID, "login-button")

    # bersihkan dan ketik
    user_input.clear()
    user_input.send_keys(username)
    pass_input.clear()
    pass_input.send_keys(password)
    login_btn.click()

def get_error_message(driver, wait_seconds=3):
    """Ambil pesan error yang muncul (jika ada)."""
    try:
        wait = WebDriverWait(driver, wait_seconds)
        el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message-container h3")))
        return el.text.strip()
    except Exception:
        return ""

def is_on_inventory_page(driver):
    """Cek apakah berhasil masuk (url mengandung /inventory.html)."""
    return "/inventory.html" in driver.current_url

# ----------------------
# Test cases (simple)
# ----------------------
def test_positive_login(driver):
    print("TEST: Positive login (standard_user)")
    open_login_page(driver)
    fill_and_submit(driver, "standard_user", "secret_sauce")
    # beri waktu sedikit untuk redirect
    time.sleep(1)
    if is_on_inventory_page(driver):
        print("  -> PASS: berhasil login dan menuju inventory.")
    else:
        print("  -> FAIL: tidak menuju inventory. error:", get_error_message(driver))

def test_empty_username(driver):
    print("TEST: Empty username")
    open_login_page(driver)
    fill_and_submit(driver, "", "secret_sauce")
    err = get_error_message(driver)
    print("  -> pesan error:", err if err else "(tidak ada pesan error)")

def test_empty_password(driver):
    print("TEST: Empty password")
    open_login_page(driver)
    fill_and_submit(driver, "standard_user", "")
    err = get_error_message(driver)
    print("  -> pesan error:", err if err else "(tidak ada pesan error)")

def test_wrong_credentials(driver):
    print("TEST: Wrong credentials")
    open_login_page(driver)
    fill_and_submit(driver, "user_wrong", "pass_wrong")
    err = get_error_message(driver)
    print("  -> pesan error:", err if err else "(tidak ada pesan error)")

def test_locked_out_user(driver):
    print("TEST: locked_out_user (should be locked)")
    open_login_page(driver)
    fill_and_submit(driver, "locked_out_user", "secret_sauce")
    err = get_error_message(driver)
    print("  -> pesan error:", err if err else "(tidak ada pesan error)")

# ----------------------
# Runner (main)
# ----------------------
if __name__ == "__main__":
    drv = create_driver(headless=False)   # set headless=True bila tidak ingin tampilan browser
    try:
        # jalankan semua test sekuensial, mudah dibaca
        test_positive_login(drv)
        # kembali ke halaman login agar test independen
        drv.get(BASE_URL)
        test_empty_username(drv)
        drv.get(BASE_URL)
        test_empty_password(drv)
        drv.get(BASE_URL)
        test_wrong_credentials(drv)
        drv.get(BASE_URL)
        test_locked_out_user(drv)
    finally:
        print("Selesai. menutup browser dalam 2 detik...")
        time.sleep(2)
        drv.quit()
