import sys
import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Configure logging
logging.basicConfig(filename="test_results.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_test(test_name, screenshot_path, test_url):
    options = Options()
    headless_mode = os.getenv("HEADLESS_MODE", "true").lower() == "true"
    if headless_mode:
        options.add_argument("--headless")  # Run in headless mode if enabled
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    driver.get(test_url)  # Use configurable test URL
    
    try:
        if test_name == "Login Test":
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            login_button = driver.find_element(By.NAME, "login")
            
            username_input.send_keys("test")
            password_input.send_keys("test")
            login_button.click()
            
            WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))  # Wait until redirected to dashboard
            
            if "dashboard" in driver.current_url:
                logging.info("Test Passed")
            else:
                logging.info("Test Failed")
        
        # Ensure screenshot directory exists
        screenshot_dir = os.path.dirname(screenshot_path)
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        driver.save_screenshot(screenshot_path)
    except Exception as e:
        logging.error(f"Test encountered an error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_name = sys.argv[1]
    screenshot_path = sys.argv[2]
    test_url = os.getenv("TEST_URL", "https://example.com")  # Configurable test URL
    run_test(test_name, screenshot_path, test_url)
