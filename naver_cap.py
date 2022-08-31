import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window()

url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
  if checkbox.is_selected(): # 체크여부 확인
    checkbox.click()

items_to_select = ['시가', '고가', '저가']
for checkbox in checkboxes:
  parent = checkbox.find_element(By.XPATH, '..')
  label = parent.find_element(By.TAG_NAME, 'label')
  # print(label.text)
  if label.text in items_to_select: # items_to_select list 값 찾은 후 check
    checkbox.click()

btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1, 40):
  browser.get(url + str(idx))

  # read_html
  df = pd.read_html(browser.page_source)[1]
  # 불필요한 데이터 삭제
  df.dropna(axis='index' ,how='all', inplace=True)
  df.dropna(axis='columns', how='all', inplace=True)
  if len(df) == 0:
    break

  # 파일 저장
  f_name = 'sise.csv'

  # 2페이지부터는 헤더 제거
  if os.path.exists(f_name):
    df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
  else:
    df.to_csv(f_name, encoding='utf-8-sig', index=False)

  print(f'{idx} 페이지 완료')

browser.quit()