from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def open_homepage(url):
    # Use WebDriverManager for automatic driver setup
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Navigate to the specified URL
    driver.get(url)

    # Do something on the page (optional)
    # Example: Print the page title
    title = driver.title
    print("Page Title:", title)

    # Keep the browser from immediately closing
    while(True):
        pass

    # Close the browser window (optional)
    # driver.close()

# Example usage
if __name__ == "__main__":
    homepage_url = "https://www.imdb.com/"  # Replace with your desired homepage

    open_homepage(homepage_url) 