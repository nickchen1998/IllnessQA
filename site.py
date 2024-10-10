import streamlit as st
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from mongo import get_mongo_database
from pymongo.collection import Collection
from langchain_openai import OpenAIEmbeddings
from llm import get_answer


datasets = {
    "排便問題": {
        "dep": "肝膽腸胃科",
        "url": "https://sp1.hso.mohw.gov.tw/doctor/Often_question/type_detail.php?q_type=%B1%C6%ABK%B0%DD%C3D&UrlClass=%A8x%C1x%B8z%ADG%AC%EC"
    },
    "經痛": {
        "dep": "婦產科",
        "url": "https://sp1.hso.mohw.gov.tw/doctor/Often_question/type_detail.php?UrlClass=%B0%FC%B2%A3%AC%EC&q_like=0&q_type=%B8g%B5h"
    },
    "藥水": {
        "dep": "眼科",
        "url": "https://sp1.hso.mohw.gov.tw/doctor/Often_question/type_detail.php?UrlClass=%B2%B4%AC%EC&q_like=0&q_type=%C3%C4%A4%F4"
    }
}

with st.sidebar:
    st.title("選擇資料集")
    dataset_option = st.selectbox(
        "請選擇在問答時要使用的資料集...",
        [key for key in datasets.keys()]
    )

    st.title("請輸入 OpenAI Key")
    openai_key = st.text_input("請輸入您的 OpenAI Key...", type="password")

    st.title("下載對話紀錄")
    file_format_option = st.selectbox(
        "請選擇要下載的檔案格式...",
        ("CSV", "JSON")
    )
    st.download_button("下載", "dialogue.csv", file_format_option)

st.title("問答機器人")
st.write("本網站並非專業醫療諮詢網站，僅用於學習系統開發，請勿依賴本網站的資訊作為醫療建議。")
st.write(f"目前選擇的資料集為 ”{dataset_option}“，資料來源可以參考 [這個網址]({datasets[dataset_option]['url']})。")

question = st.chat_input("請輸入您的訊息...")

if question and openai_key:
    with st.chat_message("user"):
        st.write(question)

    with get_mongo_database() as database:
        vector_store = MongoDBAtlasVectorSearch(
            collection=Collection(database, name="illness"),
            embedding=OpenAIEmbeddings(model="text-embedding-3-small", api_key=openai_key),
            index_name="illness_refactor_question",
            relevance_score_fn="cosine",
        )
        documents = vector_store.similarity_search(
            query=question,
            k=3,
            pre_filter={"category": {"$eq": dataset_option}}
        )
        answer = get_answer(documents, question)

    with st.chat_message("ai"):
        st.write(answer)

elif question and not openai_key:
    with st.chat_message("ai"):
        st.write("請先輸入您的 OpenAI Key...🔐")

