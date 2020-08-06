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
    
    a = driver.find_elements(By.XPATH, "//ol[@class='list-unstyled g-c-l']")
    start_time_list = []
    tvg_title_list = []
    item1_list = []
    item2_list = []
    episode_number = []
    synopsis_list = []
    for x in a:
        b = x.find_elements(By.XPATH, "//ol[@class='list-unstyled g-c-l']/li")
        for y in b:
            start_time = y.find_elements(By.XPATH, "ol[@class='highlight-box-wrapper']/li//span[@class='timezone--time']")
            for each_start_time in start_time:
                start_time_list.append(each_start_time.text)
            tvg_title = y.find_elements(By.XPATH, "ol[@class='highlight-box-wrapper']//h4[@class='programme__titles']//span[@class='programme__title delta']/span")
            for each_tvg_title in tvg_title:
                tvg_title_list.append(each_tvg_title.text)
            programme_subtitle_centi = y.find_elements(By.XPATH, "ol[@class='highlight-box-wrapper']//h4[@class='programme__titles']//span[@class='programme__subtitle centi']")
            for each_item in programme_subtitle_centi:
                item1 = each_item.find_element(By.XPATH, 'span[1]')
                item1_list.append(item1.text)
                try:
                    item2 = each_item.find_element(By.XPATH, 'span[2]')
                    item2_list.append(item2.text)
                except NoSuchElementException:
                    item2_list.append("")
            synopsis_others = y.find_elements(By.XPATH, "ol[@class='highlight-box-wrapper']//p[@class='programme__synopsis text--subtle centi']")
            for each_item_synopsis_others in synopsis_others:
                try:
                    episode_number_item = each_item_synopsis_others.find_element(By.XPATH, 'abbr/span[1]')
                    episode_number.append(episode_number_item.text)
                except NoSuchElementException:
                    episode_number.append("")
            for each_item_synopsis_others in synopsis_others:
                try:
                    synopsis_text_item = each_item_synopsis_others.find_element(By.XPATH, 'span')
                    synopsis_list.append(synopsis_text_item.text)
                except NoSuchElementException:
                    synopsis_list.append("")

    
    combined_list = list(zip(start_time_list, tvg_title_list, item1_list, item2_list, episode_number, synopsis_list))
    combined_df = pd.DataFrame(combined_list)
    combined_df.columns = ['start_time_list', 'tvg_title_list', 'item1_list', 'item2_list', 'episode_number', 'synopsis_list']
    combined_df.to_excel(r'C:\Users\preml\OneDrive\Desktop\selenium\scripts\cbbc_extract.xlsx', index=False)
    print('Process complete!')
