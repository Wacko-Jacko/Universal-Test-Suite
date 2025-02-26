from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import sys
import os
import logging

# Configure logging
log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "test_execution.log")
logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize WebDriver (Edge Browser)
def run_test(test_id):
    options = webdriver.EdgeOptions()
    
    try:
        driver = webdriver.Edge(options=options)
    except WebDriverException as e:
        logging.error(f"Error initializing Edge WebDriver: {str(e)}")
        sys.exit(1)
    
    driver.get("https://example.com")
    
    try:
        # Simulate test case execution (example: login test)
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.NAME, "login")
        
        username.send_keys("test")
        password.send_keys("test")
        login_button.click()
        
        # Use explicit wait instead of sleep
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard")))
        
        # Ensure screenshot directory exists
        screenshot_dir = "/app/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        screenshot_path = f"{screenshot_dir}/test_{test_id}.png"
        driver.save_screenshot(screenshot_path)
        
        print(f"Test {test_id} executed successfully. Screenshot saved at {screenshot_path}")
    except Exception as e:
        logging.error(f"Error executing test {test_id}: {str(e)}")
        print(f"Error executing test {test_id}: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_id = sys.argv[1]
    run_test(test_id)
