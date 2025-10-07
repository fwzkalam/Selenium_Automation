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
    """Buat Chrome webdriver sederhana dengan opsi tambahan agar popup password tidak muncul."""
    from selenium.webdriver.chrome.options import Options
    opts = Options()

    # Tambahkan argumen berikut untuk menonaktifkan fitur password manager & credential service
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    opts.add_experimental_option("prefs", prefs)

    # Hilangkan juga info bar "Chrome is being controlled..."
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)

    if headless:
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-gpu")

    # Opsional: nonaktifkan popup notifikasi & credential leak warning
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-save-password-bubble")

    # Jalankan Chrome
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(3)
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
