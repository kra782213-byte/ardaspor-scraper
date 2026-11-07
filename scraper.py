import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_channels():
    print("[*] Ağ Dinleyici Bot Başlatılıyor...")
    
    # Selenium Wire için Chrome ayarları
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    # Selenium Wire ayarları (SSL hatalarını yoksay)
    sw_options = {
        'verify_ssl': False,
        'ignore_http_methods': ['OPTIONS', 'HEAD']
    }

    driver = webdriver.Chrome(options=options, seleniumwire_options=sw_options)
    m3u_list = ["#EXTM3U"]
    
    try:
        print("[*] Siteye gidiliyor...")
        driver.get("https://ardaspor39.top")
        time.sleep(10) # Sayfanın yüklenmesini bekle
        
        # TV sekmesine tıkla
        try:
            tv_tab = driver.find_element(By.XPATH, "//*[contains(text(), 'TV')]")
            tv_tab.click()
            time.sleep(5)
        except:
            pass

        print("[*] Ağ trafiği dinleniyor, yayın linkleri aranıyor...")
        
        # Yakalanan m3u8 linklerini topla
        yakalanan_linkler = set()
        
        for request in driver.requests:
            # Eğer istek bir m3u8 veya stream linkiyse
            if request.url and ('m3u8' in request.url or 'stream' in request.url or 'mono' in request.url):
                # CSS CDN'ine ait olanları al
                if 'css.d6e3' in request.url or 'playlist' in request.url:
                    yakalanan_linkler.add(request.url)

        print(f"[*] Yakalanan link sayısı: {len(yakalanan_linkler)}")
        
        # Eğer yakalanan link varsa listeye ekle
        if yakalanan_linkler:
            for index, link in enumerate(yakalanan_linkler):
                m3u_list.append(f'#EXTINF:-1 group-title="Ardaspor Yakalanan", Kanal {index+1}')
                m3u_list.append(link)
        else:
            print("[-] Ağ trafiğinde m3u8 linki yakalanamadı. Sayfayı tarayıp kanal linklerini deniyorum...")
            # Eğer ağdan yakalanamazsa normal HTML'den aramayı dene
            elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/channel/']")
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
