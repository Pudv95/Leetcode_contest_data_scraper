import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fetch import get_user_contest_ranking_info 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

try:

    for index in range(1):
        url = 'https://leetcode.com/contest/weekly-contest-379/ranking/' + str(index+1) + '/'
        driver.get(url)
        print(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table-responsive'))
        )

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table-responsive tbody tr'))
        )

        table = driver.find_element(By.CSS_SELECTOR, '.table-responsive')

        table_text = table.text

        rows = [row.split()[:3] for row in table_text.split('\n')]
        rows[0].append('ratingChange')
        rows[0].append('prevRank')
        rows[0].append('prevRating')
        rows[0].append('attemptedContest')
        for user in rows[1:]:
            newdata = get_user_contest_ranking_info(user[1])
            user.append(newdata['ratingChange'])
            user.append(newdata['prevRank'])
            user.append(newdata['prevRating'])
            user.append(newdata['attemptedContest'])
        if index > 0:
            rows.pop(0)
        with open('table_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(rows)

finally:
    driver.quit()
