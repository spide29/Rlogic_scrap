import re
import time
import tkinter as tk
import tkinter.ttk as ttk
import os
import requests
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread

chrome_options = Options()
chrome_options.add_argument("--headless")
current_directory = os.getcwd()
webdriver_path = os.path.join(current_directory, "Driver", "chromedriver.exe")
os.environ["PATH"] += os.pathsep + webdriver_path
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://tao.wto.org/welcome.aspx?ReturnUrl=%2fdefault.aspx")
email_field = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$UserName"]')
email_field.send_keys("harishkumar.jayakumar@springbord.com")
password_field = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$Password"]')
password_field.send_keys("Spring@!234")
submit_button = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$LoginButton"]')
submit_button.click()
time.sleep(2)
driver.get("http://tao.wto.org/QueryEdit.aspx")
html_content = driver.page_source
filename = "abc.html"
with open(filename, "w", encoding="utf-8") as file:
    file.write(html_content)
data_list = []
for i in range(2, 158):
    xpath = '//*[@id="ctl00_c_dgCountry"]/tbody/tr[' + str(i) + ']/td[2]'
    a_tag = driver.find_element(By.XPATH, xpath)
    data_list.append(a_tag.text)
print(data_list)
driver.quit()

def on_country_selected(*args):
    selected_country = selected_country_var.get()
    print("Selected Country:", selected_country)
    search_country_in_html()

def on_year_selected(event):
    selected_year = selected_year.get()
    selected_year = dropdown_menu_years.get()
    print("Selected Year:", selected_year)
    search_year_in_html()

def animate_loading_label():
    if loading_label.cget("text")[-3:] == "...":
        loading_label.config(text="Loading")
    else:
        loading_label.config(text=loading_label.cget("text") + ".")
    root.after(500, animate_loading_label)  
def search_country_in_html():
    country = selected_country_var.get()
    loading_label.config(text="Loading...", font=("Arial", 16, "bold"))
    loading_label.pack()
    root.update()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # F:\\Rlogical_scrap_work\\clone\\tarriff_data\\Driver
    current_directory = os.getcwd()
    webdriver_path = os.path.join(current_directory, "Driver", "chromedriver.exe")
    os.environ["PATH"] += os.pathsep + webdriver_path
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://tao.wto.org/welcome.aspx?ReturnUrl=%2fdefault.aspx")
    email_field = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$UserName"]')
    email_field.send_keys("harishkumar.jayakumar@springbord.com")
    password_field = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$Password"]')
    password_field.send_keys("Spring@!234")
    submit_button = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$LoginButton"]')
    submit_button.click()
    time.sleep(2)
    driver.get("http://tao.wto.org/QueryEdit.aspx")
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    country_cells = soup.find_all('td', text=country)
    if country_cells:
        for cell in country_cells:
            input_tag = cell.find_previous('input')
            if input_tag:
                input_id = input_tag.get('id')
                print("Found country:", cell.text)
                print("Input tag ID:", input_id,)
                radio_button = driver.find_element(By.ID, input_id)
                radio_button.click()
                print("Radio button clicked.")
                a_list = []
                for i in range(2, 158):
                    xpath = '//*[@id="ctl00_c_dgCountry"]/tbody/tr[' + str(i) + ']/td[2]'
                    try:
                        a_tag = driver.find_element(By.XPATH, xpath)
                        a_list.append(a_tag.text)
                    except NoSuchElementException:
                        print("Element not found for XPath:", xpath)
                    except StaleElementReferenceException:
                        print("Stale element reference for XPath:", xpath)
                print(a_list)
                year_list = []
                i = 2
                while True:
                    year_xpath = '//*[@id="ctl00_c_dgYear"]/tbody/tr[' + str(i) + ']/td[2]'
                    status_xpath = '//*[@id="ctl00_c_dgYear"]/tbody/tr[' + str(i) + ']/td[3]'
                    try:
                        year_element = driver.find_element(By.XPATH, year_xpath)
                        status_element = driver.find_element(By.XPATH, status_xpath)
                        year = year_element.text
                        status = status_element.text
                        if status.lower() == 'yes':
                            year_list.append(year)
                        i += 1
                    except NoSuchElementException:
                        print("Element not found for XPath:", xpath)
                        break
                    except StaleElementReferenceException:
                        print("Stale element reference for XPath:", xpath)
                print("year",year_list)
                if not year_list:
                    error_label.config(text="No years found for the selected country.")
                else:
                    error_label.config(text="") 
                dropdown_menu_years['menu'].delete(0, 'end')
                for item in year_list:
                    dropdown_menu_years['menu'].add_command(label=item, command=tk._setit(selected_year, item))
                break
            else:
                print("Input tag not found for the country:", cell.text)
    driver.quit()
    loading_label.pack_forget()

def search_year_in_html():
    country = selected_country_var.get()
    year = selected_year.get()
    print("Selected Year:", year)
    loading_label.config(text="Loading...", font=("Arial", 16, "bold"))
    loading_label.pack()
    root.update() 
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    webdriver_path = r"F:\1.2 MIT Django Project\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
    driver.get("https://tao.wto.org/welcome.aspx?ReturnUrl=%2fdefault.aspx")
    email_field = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$UserName"]')
    email_field.send_keys("harishkumar.jayakumar@springbord.com")
    password_field = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$Password"]')
    password_field.send_keys("Spring@!234")
    submit_button = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$LoginButton"]')
    submit_button.click()
    time.sleep(2)
    driver.get("http://tao.wto.org/QueryEdit.aspx")
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # # F:\\Rlogical_scrap_work\\clone\\tarriff_data\\Driver
    # current_directory = os.getcwd()
    # webdriver_path = os.path.join(current_directory, "Driver", "chromedriver.exe")
    # os.environ["PATH"] += os.pathsep + webdriver_path
    # driver = webdriver.Chrome(options=chrome_options)
    # driver.get("https://tao.wto.org/welcome.aspx?ReturnUrl=%2fdefault.aspx")
    # email_field = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$UserName"]')
    # email_field.send_keys("harishkumar.jayakumar@springbord.com")
    # password_field = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$Password"]')
    # password_field.send_keys("Spring@!234")
    # submit_button = driver.find_element(By.XPATH, '//input[@name="ctl00$c$ctrLogin$LoginButton"]')
    # submit_button.click()
    # time.sleep(2)
    # driver.get("http://tao.wto.org/QueryEdit.aspx")
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    country_cells = soup.find_all('td', text=country)
    if country_cells:
        for cell in country_cells:
            input_tag = cell.find_previous('input')
            if input_tag:
                input_id = input_tag.get('id')
                print("Found country:", cell.text)
                print("Input tag ID:", input_id)
                radio_button = driver.find_element(By.ID, input_id)
                radio_button.click()
                print("Radio button clicked.")
    time.sleep(2)
    current_url = driver.current_url
    print("Current URL:", current_url)
    driver.get(current_url)
    html_content = driver.page_source
    filename = "efg.html"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    year_pattern = r"\b{}\b".format(re.escape(year))
    year_cells = soup.find_all('td',  text=re.compile(year_pattern))
    if year_cells:
        for yer_cell in year_cells:
            input_tag = yer_cell.find_previous('input')
            if input_tag:
                time.sleep(3)
                input_id = input_tag.get('id')
                print("Found year:", yer_cell.text)
                print("Input tag ID:", input_id,)
                yeat_radio_button = driver.find_element(By.ID, input_id)
                yeat_radio_button.click()
                print("Radio button clicked.")
    os.remove("efg.html")
    # os.remove("abc.html")
    time.sleep(3)
    pro = driver.find_element(By.ID, 'ctl00_c_lb2')
    pro.click()
    time.sleep(2)
    checkbox = driver.find_element(By.XPATH, '//*[@id="ctl00_c_g_ps_tpn0CheckBox"]')
    checkbox.click()
    time.sleep(3)
    input_field = driver.find_element(By.ID, 'ctl00_c_qryName')
    input_field.send_keys(country+ '_'+ year)
    time.sleep(3)
    save_que = driver.find_element(By.XPATH, '//*[@id="ctl00_c_lbSave"]')
    save_que.click()
    time.sleep(2)
    element = driver.find_element(By.XPATH, '//*[@id="ctl00_LeftNavigationMenu1_mLeftMenun3"]/td/table/tbody/tr/td[1]/a')
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    driver.implicitly_wait(3)
    # driver.get("http://tao.wto.org/ExportReport.aspx")
    time.sleep(3)
    report_export = driver.find_element(By.XPATH, '//*[@id="ctl00_LeftNavigationMenu1_mLeftMenun24"]/td/table/tbody/tr/td/a')
    report_export.click()
    time.sleep(3)
    report_exp = driver.find_element(By.XPATH, '//*[@id="ctl00_c_drpReport"]')
    report_exp.click()
    select = Select(report_exp)
    select.select_by_visible_text("Tariff Line Duties")
    time.sleep(5)
    file_name = driver.find_element(By.CLASS_NAME, 'input_text')
    file_name.click()
    file_name.send_keys(country+ '_'+ year)
    time.sleep(3)
    expo = driver.find_element(By.ID, 'ctl00_c_pickFile_btnExport')
    expo.click()
    time.sleep(40)
    status = driver.find_element(By.ID, 'ctl00_c_viewFile_dgExportFile_ctl02_bReload')
    status.click()
    time.sleep(5)
    down = driver.find_element(By.XPATH, '//*[@id="ctl00_c_viewFile_dgExportFile"]/tbody/tr[2]/td[1]/a')
    down.click()
    loading_label.config(text="Downloading file...", font=("Arial", 16, "bold"))
    root.update()
    
    time.sleep(40)
    
    loading_label.config(text="File downloaded successfully!", font=("Arial", 14, "bold"), fg="green")
    root.update()
    loading_label.pack_forget()
    driver.quit()

root = tk.Tk()
root.title("Tariff data Extraction")
style = ttk.Style()
style.configure('RoundedButton.TButton', borderwidth=0, relief=tk.SOLID, background='blue', font=("Arial", 14))
style.map('RoundedButton.TButton', background=[('active', 'blue')])
window_size = 300
root.geometry(f"{window_size}x{window_size}")
selected_country_var = tk.StringVar(root)
country_label = tk.Label(root, text="Country", font=("Arial", 14))
country_label.pack(anchor='w')
dropdown_menu_countries = tk.OptionMenu(root, selected_country_var, *data_list)
dropdown_menu_countries.config(font=("Arial", 12), width=20)
dropdown_menu_countries.pack(pady=20)
selected_country_var.trace("w", on_country_selected)
selected_year = tk.StringVar(root)
year_label = tk.Label(root, text="Year", font=("Arial", 14))
year_label.pack(anchor='w')
dropdown_menu_years = tk.OptionMenu(root, selected_year, "")
dropdown_menu_years.config(font=("Arial", 12), width=20)
dropdown_menu_years.pack(pady=10)
search_button = ttk.Button(root, text="Search", command=search_year_in_html, style='RoundedButton.TButton')
search_button.pack(pady=10)
loading_label = tk.Label(root, text="")
loading_label.pack()
error_label = tk.Label(root, font=("Arial", 12), fg="red")
error_label.pack()
root.mainloop()