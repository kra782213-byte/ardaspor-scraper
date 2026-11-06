import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# GitHub Actions'ta tarayıcıyı görünmez (headless) çalıştırmak için ayarlar
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

def get_channels():
    print("[*] Görünmez tarayıcı başlatılıyor...")
    driver = webdriver.Chrome(options=chrome_options)
    m3u_list = ["#EXTM3U"]
    
    try:
        # 1. Siteye git
        driver.get("https://ardaspor39.top")
        time.sleep(5) # JavaScript'in yüklenmesini bekle
        
        # 2. "TV" sekmesini bul ve tıkla (Sitedeki butonun metnine göre arıyoruz)
        try:
            tv_tab = driver.find_element(By.XPATH, "//*[contains(text(), 'TV')]")
            tv_tab.click()
            time.sleep(5) # Sekme içeriğinin yüklenmesini bekle
        except Exception as e:
            print("[-] TV sekmesi bulunamadı, ana sayfadan devam ediliyor.")

        # 3. Sayfadaki tüm linkleri ve kanal isimlerini bul
        # Sitedeki maç/kanal kutularını (genellikle a etiketi veya div) arıyoruz
        elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/channel/']")
        
        for el in elements:
            try:
                href = el.get_attribute("href")
                kanal_id = href.split('/')[-1]
                name = el.text.strip()
                
                if not name:
                    name = f"Kanal {kanal_id}"
                    
                m3u_list.append(f'#EXTINF:-1 group-title="Ardaspor", {name}')
                m3u_list.append(f'https://b-proxy-delta.vercel.app/play/{kanal_id}') # Kendi Vercel linkini yaz
            except:
                pass
                
    except Exception as e:
        print(f"[-] Hata: {e}")
    finally:
        driver.quit()
        
    return "\n".join(m3u_list)

if __name__ == "__main__":
    m3u_content = get_channels()
    print(m3u_content)
    # Burada istersen bu içeriği Gist'e veya bir dosyaya kaydedebilirsin.
