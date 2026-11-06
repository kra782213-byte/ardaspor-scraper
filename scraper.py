import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def get_channels():
    print("[*] Gizli tarayıcı başlatılıyor...")
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    try:
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=156)
    except Exception as e:
        driver = uc.Chrome(options=options)

    m3u_list = ["#EXTM3U"]
    
    try:
        print("[*] Siteye gidiliyor...")
        driver.get("https://ardaspor39.top")
        
        # Sayfanın ve JavaScript'in tam yüklenmesi için 15 saniye bekle
        time.sleep(15)
        
        # BOTUN NE GÖRDÜĞÜNÜ KAYDET
        driver.save_screenshot("bot_ekrani.png")
        with open("sayfa_kaynagi.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("[+] Botun gördüğü ekran ve HTML kaydedildi.")

        # TV sekmesine tıklamayı dene
        try:
            tv_tab = driver.find_element(By.XPATH, "//*[contains(text(), 'TV')]")
            tv_tab.click()
            time.sleep(5)
            driver.save_screenshot("bot_ekrani_tv.png") # TV sekmesi açıldıktan sonra da kaydet
        except:
            print("[-] TV sekmesi bulunamadı.")

        # Kanalları ara
        elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/channel/']")
        print(f"[*] Bulunan kanal linki sayısı: {len(elements)}")
        
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
