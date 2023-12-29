import requests
from bs4 import BeautifulSoup
import csv

def crawl_and_save_to_csv(base_url, num_pages, csv_filename):
    data_list = []

    with requests.Session() as session:
    
        for page in range(1, num_pages + 1):
            # 각 페이지의 URL 생성
            url = f'{base_url}&page={page}'
            
            # 페이지별로 데이터 수집
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers)
            # response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all('div', class_='article')
                
                for article in articles:
                    title = article.find('h2').text.strip()
                    link = article.find('a')['href']

                    # 각 제목에 대한 페이지로 이동하여 추가 정보 수집
                    article_response = requests.get(link)
                    if article_response.status_code == 200:
                        article_soup = BeautifulSoup(article_response.text, 'html.parser')
                        additional_info = article_soup.find('div', class_='additional-info').text.strip()
                        data_list.append((title, link, additional_info))
                    else:
                        print(f"Error fetching article: {article_response.status_code}")
            else:
                print(f"Error fetching page {page}: {response.status_code}")

    # 추출한 정보를 CSV 파일로 저장
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Title', 'Link', 'Additional Info'])  # CSV 파일 헤더 작성
        csv_writer.writerows(data_list)

    print(f"크롤링이 완료되었고, 데이터가 '{csv_filename}'에 저장되었습니다.")

# 크롤링할 기본 URL, 페이지 수, 저장할 CSV 파일명 지정
base_url_to_crawl = 'https://m.cmcseoul.or.kr/page/health/bible/detail/{}?p=1&s=10&q=%7B%22deptClsf%22%3A%22A%22%2C%22selectedDept%22%3A%22%22%2C%22hbDtContent%22%3A%22%22%2C%22exposeYn%22%3A%22Y%22%7D'
num_pages_to_crawl = 21
csv_filename_to_save = 'output_data_all_pages.csv'

# 크롤링 및 CSV 저장 함수 호출
crawl_and_save_to_csv(base_url_to_crawl, num_pages_to_crawl, csv_filename_to_save)
