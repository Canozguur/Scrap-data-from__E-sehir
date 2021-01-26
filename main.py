from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
list_of_tel_no = []
list_of_ilçeler = []
list_of_tam_adres = []
list_of_firmalar = []
index = []
data = {"Firma Adı":list_of_firmalar,
        "TEL_NO":list_of_tel_no,
        "ilçe":list_of_ilçeler,
        "Tam Adres":list_of_tam_adres,
        }

class start:
    def __init__(self):
        self.index_num = 0
        self.basic()



    def basic(self):
        # Burası çalışıyormu emin değilim daha
        self.driver = webdriver.Chrome(r"C:\Users\Canoz\OneDrive\Masaüstü\chromedriver")

        self.driver.get("https://www.e-sehir.com/turkiye-haritasi/edirne-egitim-kurumlari.html")
        x = self.driver.find_element_by_class_name("panel-body")
        z = x.find_elements_by_tag_name("p")
        katsayı = 1
        for i in range(32):
            if katsayı != 1:
                self.driver.get("https://www.e-sehir.com/turkiye-haritasi/edirne-egitim-kurumlari.html")
            data = self.driver.find_element_by_xpath(f'//*[@id="main_panel"]/div/div[2]/p[{i+1}]')
            if i == 0 or i ==2 or i==4 or i == 6 or i == 7 or i==8 or i==9 or i==10 or i==13 or i==14  or i==16 or i==20 or i==23 or i==24 or i==25:
                continue
            self.name_of_list = data.text
            if str(data.text).split(" ")[-1] == "Listesi":
                print("okey")
                print(data.text)
                self.link = data.find_element_by_tag_name("a").get_attribute("href")
                print(self.link)
                self.search_list()
            katsayı+=1
    def search_list(self):
        self.driver.get(self.link)
        x = self.driver.find_element_by_class_name("panel-body")
        z = x.find_elements_by_tag_name("p")
        katsayı = 1
        for i in range (len(z)):
            if katsayı != 1:
                self.driver.get(self.link)

            data = self.driver.find_element_by_xpath(f'//*[@id="main_panel"]/div/div[2]/p[{i+1}]')
            print(data.text)
            self.kurum_adı = data.text
            try:
                self.kurum_link = data.find_element_by_tag_name("a").get_attribute("href")
                print(self.kurum_link)
                self.kurum_git()
                katsayı += 1
            except Exception:
                break

    def kurum_git(self):

        self.driver.get(self.kurum_link)
        all_info =self.driver.find_element_by_tag_name("address")

        tel_no = str(self.driver.find_element_by_xpath('//*[@id="main_panel"]/div/div[2]/address/div').text)
        telefon_No = str(all_info.find_elements_by_tag_name('abbr')[0].text)
        ilçe = str(all_info.find_element_by_tag_name("b").text)
        print("ilçe :" ,ilçe)
        print(tel_no)
        print("Tam Adres :",all_info.text)
        print("kurum adı :",self.kurum_adı)
        tam_adres = all_info.text
        list_of_tel_no.append(tel_no)
        list_of_ilçeler.append(ilçe)
        list_of_tam_adres.append(tam_adres)
        list_of_firmalar.append(self.kurum_adı)

        self.index_num += 1
        index.append(self.index_num)

start()


df = pd.DataFrame(data, columns=['Firma Adı',"TEL_NO","ilçe","Tam Adres",],index=index)

writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Edirne')
writer.save()
