from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys 
import time
import pyperclip
import pandas as pd
import multiprocessing 

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


driver.get("https://www.bing.com/translator")
driver.maximize_window()


def selectNepali():
    
    button_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div[1]/div[1]/div/table/tbody/tr/td[3]/div/div[1]/select"))
    )
    button_dropdown.click()
    nepali_select = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div/div[1]/div[1]/div/table/tbody/tr/td[3]/div/div[1]/select/optgroup[2]/option[84]")))
    nepali_select.click()

list_of_index=[]



def translate(article):
    input_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/main/div/div[1]/div[1]/div/table/tbody/tr/td[1]/div[1]/div[3]/div/textarea"))
            )
    input_element.send_keys(article)


    time.sleep(3)
    try:

        copy_clipboard = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div[1]/div[1]/div/table/tbody/tr/td[3]/div/div[5]/div/div[5]/div/div"))
        )
        copy_clipboard.click()
        clipboard_text = pyperclip.paste()
        time.sleep(2)
        input_element.clear()

    except:
        clipboard_text=''
        input_element.clear()
    return clipboard_text
print(list_of_index)
    

def translate_summary():
    # time.sleep(2)
    with open(".txt","r") as file:
        for line in file:
            summary=line.strip()
            translate(summary,line,filename="nepalisummaryv2")   

    
def translate_article(file,outputfile):
    time.sleep(2)
    with open(file,"r") as f:
        for line in f:
            items=eval(line)
            time.sleep(2)
            translated=[translate(item) for item in items]
            translated_line=' '.join(translated)
            
            with open(outputfile,"a") as f:
                f.write(translated_line)
                f.write("\n")
        
    
   

selectNepali()
translate_article("republica.txt","republica-npart.txt")
# translate_summary()
   


   
    





