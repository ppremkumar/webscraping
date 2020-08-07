import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

with webdriver.Chrome() as driver:
    driver.maximize_window()
    driver.get("https://www.bbc.co.uk/schedules/p00fzl9r")
    time.sleep(5)
    
    schedule_data = driver.find_elements(By.XPATH, "//ol[@class='list-unstyled g-c-l']")
    start_time_list = []
    tvg_title_list = []
    item1_list = []
    item2_list = []
    episode_number = []
    synopsis_list = []
    for x in schedule_data:
        b = x.find_elements(By.XPATH, "//ol[@class='list-unstyled g-c-l']/li")
        for y in b:
            start_time = y.find_elements(By.XPATH, "ol[@class='highlight-box-wrapper']/li//span[@class='timezone--time']")
            for each_start_time in start_time:
                start_time_list.append(each_start_time.text)
            program_body = y.find_elements(By.XPATH, "ol[@class='highlight-box-wrapper']//div[@class='programme__body']")
            for each_program_body_item in program_body:
                try:
                    tvg_title = each_program_body_item.find_element(By.XPATH, "h4[@class='programme__titles']//span[@class='programme__title delta']/span[1]")
                    tvg_title_list.append(tvg_title.text)
                except NoSuchElementException:
                    tvg_title_list.append("")
                try:
                    item1 = each_program_body_item.find_element(By.XPATH, "h4[@class='programme__titles']//span[@class='programme__subtitle centi']/span[1]")
                    item1_list.append(item1.text)
                except  NoSuchElementException:
                    item1_list.append("")
                try:
                    item2 = each_program_body_item.find_element(By.XPATH, "h4[@class='programme__titles']//span[@class='programme__subtitle centi']/span[2]")
                    item2_list.append(item2.text)
                except  NoSuchElementException:
                    item2_list.append("")

    
    combined_list = list(zip(start_time_list, tvg_title_list, item1_list, item2_list))
    combined_df = pd.DataFrame(combined_list)
    combined_df.columns = ['start_time_list', 'tvg_title_list', 'item1_list', 'item2_list']
    combined_df.to_excel(r'C:\Users\preml\OneDrive\Desktop\selenium\scripts\cbbc_extract.xlsx', index=False)
    print('Process complete!')
