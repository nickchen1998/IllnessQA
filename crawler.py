import re
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from llm import get_refactor_answer, get_refactor_question, get_content_embedding
from mongo import insert_datas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = Chrome()
browser.get('https://sp1.hso.mohw.gov.tw/doctor/Often_question/type_detail.php?UrlClass=%B2%B4%AC%EC&q_like=0&q_type=%C3%C4%A4%F4')

# 排便問題、肝膽腸胃科 https://sp1.hso.mohw.gov.tw/doctor/Often_question/type_detail.php?q_type=%B1%C6%ABK%B0%DD%C3D&UrlClass=%A8x%C1x%B8z%ADG%AC%EC
# 經痛、婦產科 https://sp1.hso.mohw.gov.tw/doctor/Often_question/type_detail.php?UrlClass=%B0%FC%B2%A3%AC%EC&q_like=0&q_type=%B8g%B5h
# 藥水、眼科 https://sp1.hso.mohw.gov.tw/doctor/Often_question/type_detail.php?UrlClass=%B2%B4%AC%EC&q_like=0&q_type=%C3%C4%A4%F4

category = "藥水"
doctor_department = "眼科"
i = 1
while True:
    print(f"Page {i}")
    datas = []

    for paragraph in browser.find_elements(By.CSS_SELECTOR, "ul.QAunit"):
        try:
            subject = WebDriverWait(paragraph, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.subject"))
            ).text
            print(subject)
        except Exception as e:
            print(e)
            continue

        asker_info = paragraph.find_element(By.CSS_SELECTOR, "li.asker").text
        match = re.search(r'／([男女])／.*?,(\d{4}/\d{2}/\d{2})', asker_info)

        try:
            gender = match.group(1)
        except Exception as e:
            gender = None
        try:
            question_time = datetime.strptime(match.group(2), '%Y/%m/%d')
        except Exception as e:
            question_time = None

        doctor_info = paragraph.find_element(By.CSS_SELECTOR, "li.doctor").text
        match = re.search(r'／([\u4e00-\u9fa5]+),\s*(\d{4}/\d{2}/\d{2})', doctor_info)

        try:
            doctor_name = match.group(1)
        except Exception as e:
            doctor_name = None
        try:
            answer_time = datetime.strptime(match.group(2), '%Y/%m/%d')
        except Exception as e:
            answer_time = None

        view_info = paragraph.find_element(By.CSS_SELECTOR, "li.count").text
        match = re.search(r'(\d+)', view_info)
        view_amount = int(match.group(1)) if match else 0

        try:
            question = paragraph.find_element(By.CSS_SELECTOR, "li.ask").text
            answer = paragraph.find_element(By.CSS_SELECTOR, "li.ans").text
        except Exception as e:
            print(e)
            continue
        refactor_question = get_refactor_question(question)
        refactor_answer = get_refactor_answer(answer)
        refactor_question_embedding = get_content_embedding(refactor_question)

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
            view_amount=view_amount,
            refactor_question=refactor_question,
            refactor_question_embeddings=refactor_question_embedding,
            refactor_answer=refactor_answer
        )
        datas.append(data)

    insert_datas(datas=datas)

    try:
        next_page_element = browser.find_element(By.LINK_TEXT, "下一頁")
        next_page_element.click()
        i += 1
    except Exception as e:
        print(e)
        break



browser.quit()
