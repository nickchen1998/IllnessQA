import re
import time
from pprint import pprint
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

browser = Chrome()
browser.get('https://sp1.hso.mohw.gov.tw/doctor/Often_question/type_detail.php?q_type=排便問題&UrlClass=肝膽腸胃科')

category = "排便問題"
doctor_department = "肝膽腸胃科"
for paragraph in browser.find_elements(By.CSS_SELECTOR, "ul.QAunit"):
    time.sleep(10)

    subject = paragraph.find_element(By.CSS_SELECTOR, "li.subject").text

    asker_info = paragraph.find_element(By.CSS_SELECTOR, "li.asker").text
    match = re.search(r'／([男女])／.*?,(\d{4}/\d{2}/\d{2})', asker_info)
    gender = match.group(1)
    question_time = datetime.strptime(match.group(2), '%Y/%m/%d')

    question = paragraph.find_element(By.CSS_SELECTOR, "li.ask").text

    answer = paragraph.find_element(By.CSS_SELECTOR, "li.ans").text

    doctor_info = paragraph.find_element(By.CSS_SELECTOR, "li.doctor").text
    match = re.search(r'／([\u4e00-\u9fa5]+),\s*(\d{4}/\d{2}/\d{2})', doctor_info)
    doctor_name = match.group(1)
    answer_time = datetime.strptime(match.group(2), '%Y/%m/%d')

    view_info = paragraph.find_element(By.CSS_SELECTOR, "li.count").text
    match = re.search(r'(\d+)', view_info)
    view_amount = int(match.group(1)) if match else 0

    data = dict(
        category=category,
        subject=subject,
        question=question,
        gender=gender,
        question_time=question_time,
        answer=answer,
        doctor_name=doctor_name,
        doctor_department=doctor_department,
        answer_time=answer_time,
        view_amount=view_amount
    )
    pprint(data)

    try:
        next_page_element = browser.find_element(By.LINK_TEXT, "下一頁")
        next_page_element.click()
    except NoSuchElementException:
        break

browser.quit()
