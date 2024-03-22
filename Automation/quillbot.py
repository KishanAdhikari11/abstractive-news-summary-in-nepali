from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pyautogui
import time
import pyperclip
import pandas as pd



options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()
driver.get("https://quillbot.com/summarize")

time.sleep(5)
pyautogui.click(1000,347,1,0.0,button="left")
screen_width, screen_height = pyautogui.size()

input_area = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "inputBoxSummarizer"))
)
df=pd.read_csv("newdf.csv")
for index,row in df.iterrows():
    pyautogui.click(1000,347,1,0.0,button="left")
    article=row["Article"]        
    time.sleep(5)
    
    input_area.send_keys(article)  

    time.sleep(5)
    input_area.send_keys(Keys.CONTROL + Keys.ENTER)

    copy_clipboard = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/section[1]/div/div/div/section/div[2]/div/div/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[4]/div/span/button"))
    )
    time.sleep(5)
    copy_clipboard.click()
    clipboard_text = pyperclip.paste()
    print(clipboard_text+'\n')
    time.sleep(5)
    with open("summary.txt","a") as f:
        f.write(clipboard_text+'\n')
    input_area.clear()