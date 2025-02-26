from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from pyhtmlreport import Report  # ExtentReports alternative for Python

report = Report()
report.setup(report_folder=f"/app/reports/report_{int(time.time())}", module_name="Test Reports", release_name="v1.0")

def run_test():
    browser = os.getenv("BROWSER", "edge").lower()
    test_url = os.getenv("TEST_URL", "https://example.com")
    
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Edge()
    
    driver.get(test_url)
    report.write_step(f"Navigated to {test_url}", status=report.status.Started)
    
    try:
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.NAME, "login")
        
        username.send_keys("test")
        password.send_keys("test")
        login_button.click()
        
        time.sleep(2)
        screenshot_path = "/app/screenshots/test_report.png"
        driver.save_screenshot(screenshot_path)
        
        report.write_step("Login successful", status=report.status.Pass, screenshot=screenshot_path)
    except Exception as e:
        report.write_step(f"Error: {str(e)}", status=report.status.Fail)
    finally:
        driver.quit()
        report.generate_report()
        print("Test report generated successfully.")

if __name__ == "__main__":
    run_test()
