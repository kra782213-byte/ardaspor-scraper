import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

def get_channels():
    print("[*] Görünmez tarayıcı başlatılıyor...")
    driver = webdriver.Chrome(options=chrome_options)
    m3u_list = ["#EXTM3U"]
    
    try:
        driver.get("https://ardaspor39.top")
        # Sayfanın tam yüklenmesi için biraz daha uzun bekle
        time.sleep(10)
        
        # 1. Botun ne gördüğünü anlamak için ekran görüntüsü al
        driver.save_screenshot("sayfa_goruntusu.png")
        print("[+] Ekran görüntüsü alındı.")
        
        # 2. Sayfanın HTML kaynağını kaydet (Neyi indirdiğini görmek için)
        with open("sayfa_kaynagi.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("[+] Sayfa kaynağı kaydedildi.")

        # 3. Kanal linklerini aramaya çalış
        elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/channel/']")
        print(f"[*] Bulunan potansiyel kanal linki sayısı: {len(elements)}")
        
        for el in elements:
            try:
                href = el.get_attribute("href")
                kanal_id = href.split('/')[-1]
                name = el.text.strip()
                if not name: name = f"Kanal {kanal_id}"
                    
                m3u_list.append(f'#EXTINF:-1 group-title="Ardaspor", {name}')
                m3u_list.append(f'https://arda-proxy.vercel.app/play/{kanal_id}')
            except:
                pass
                
    except Exception as e:
        print(f"[-] Hata: {e}")
    finally:
        driver.quit()
        
    return "\n".join(m3u_list)

if __name__ == "__main__":
    m3u_content = get_channels()
    with open("ardaspor.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("[+] Liste 'ardaspor.m3u' dosyasına kaydedildi.")
