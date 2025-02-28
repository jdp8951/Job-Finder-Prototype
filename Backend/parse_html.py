from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random

# Configure Chrome Options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Start WebDriver
driver = webdriver.Chrome(options=options)

# Target URL (Modify the job search query)
base_url = "https://www.naukri.com/-jobs-{}"  
job_data = []

try:
    for page in range(1, 31):  # Scraping first 4 pages
        print(f"Getting page {page} ...")
        driver.get(base_url.format(page))
        time.sleep(5)  # Allow page to load

        # Scroll multiple times to load lazy content
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 500);")  # Scroll in small steps
            time.sleep(1)

        try:
            # Wait for job listings to load
            job_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "cust-job-tuple"))
            )
        except Exception:
            print(f"Timeout on page {page}: No jobs found.")
            continue  # Skip to next page

        # Extract job details
        for job in job_elements:
            try:
                title_element = job.find_element(By.CLASS_NAME, "title")
                title = title_element.text
                job_link = title_element.get_attribute("href")

                company = job.find_element(By.CLASS_NAME, "comp-name").text
                location = job.find_element(By.CLASS_NAME, "loc-wrap").text
                experience = job.find_element(By.CLASS_NAME, "exp-wrap").text
                salary_element = job.find_elements(By.CLASS_NAME, "sal-wrap")
                salary = salary_element[0].text if salary_element else "Not mentioned"
                description = job.find_element(By.CLASS_NAME, "job-desc").text
                
                # Extract skills/tags
                skills = [tag.text for tag in job.find_elements(By.CLASS_NAME, "tag-li") if tag.text]

                job_data.append([title, company, location, experience, salary, description, ", ".join(skills), job_link])
            except Exception as e:
                print(f"Error extracting job data: {e}")

        # Random delay to avoid bot detection
        time.sleep(random.randint(4, 7))

except Exception as e:
    print(f"Script error: {e}")

finally:
    driver.quit()  # Close browser

# Save to CSV
df = pd.DataFrame(job_data, columns=["Title", "Company", "Location", "Experience", "Salary", "Description", "Skills", "Job Link"])
df.to_csv("naukri_jobs.csv", index=False)
print(f"✅ Data saved: {len(df)} jobs scraped.")

