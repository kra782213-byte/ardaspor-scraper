from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Yeni başsız mod
chrome_options.add_argument("--no-sandbox")    # Sandbox'ı devre dışı bırak (root için gerekli)
chrome_options.add_argument("--disable-dev-shm-usage") # Paylaşımlı bellek sorunlarını önle
chrome_options.add_argument("--disable-gpu")   # GPU'yu devre dışı bırak
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
