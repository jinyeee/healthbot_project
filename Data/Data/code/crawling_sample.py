from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

def crawl_reviews_by_ids(dataframe, base_url_to_crawl, csv_filename_template):
    # 웹 드라이버 초기화
    driver = webdriver.Chrome()

    for index, row in dataframe.iterrows():
        id_value = row['id']
        
        # 페이지별 URL 생성
        url = f"{base_url_to_crawl}/{id_value}/review/visitor?entry=pll"
        
        driver.get(url)
        driver.implicitly_wait(30)

        try:
            # 무한 스크롤
            while True:
                driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/div[2]/div/a').click()
                time.sleep(0.4)
        except Exception as e:
            print(f'Finish scrolling for id {id_value}')

        # 리뷰 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        reviews = soup.select('li.YeINN')
        nickname_list = list()
        content_list = list()
        date_list = list()
        revisit_list = list()

        for review in reviews:
            nickname_element = review.select_one('div.VYGLG')
            if nickname_element:
                nickname = nickname_element.text
            else:
                continue  # 리뷰가 없는 경우 해당 병원은 skip

            content_element = review.select_one('div.ZZ4OK.IwhtZ')
            if content_element:
                content = content_element.text
            else:
                content = ' '

            date = review.select('div._7kR3e>span.tzZTd>time')[0].text
            revisit = review.select('div._7kR3e>span.tzZTd')[1].text

            nickname_list.append(nickname)
            content_list.append(content)
            date_list.append(date)
            revisit_list.append(revisit)

        # 리뷰가 하나도 없는 경우 pass
        if not nickname_list:
            continue

        # 데이터프레임 생성 및 CSV 저장
        csv_filename = f"{csv_filename_template}_{id_value}.csv"
        review_dataframe = pd.DataFrame({'nickname': nickname_list, 'content': content_list, 'date': date_list, 'revisit': revisit_list})
        review_dataframe.to_csv(csv_filename, index=False)

    # 드라이버 종료
    driver.quit()

# 데이터프레임이 있는 경우, 아래와 같이 호출합니다.
base_url_to_crawl = 'https://m.place.naver.com/hospital'
csv_filename_template = 'review_geumcheon'
dataframe_with_ids = pd.read_csv('hospital_geumcheon.csv')  

crawl_reviews_by_ids(df, base_url_to_crawl, csv_filename_template)
