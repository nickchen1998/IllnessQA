from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from env_settings import EnvSettings
from langchain_openai.embeddings import OpenAIEmbeddings


def get_llm():
    env_settings = EnvSettings()
    return ChatOpenAI(
        api_key=env_settings.OPENAI_API_KEY,
        model_name="gpt-4o"
    )


def get_refactor_answer(paragraph: str):
    prompt = ChatPromptTemplate.from_template(
        """
你是一個專業的醫生，下面是一篇醫生針對某個患者描述的情況的回應，請幫我使用繁體中文做重點整理，讓患者可以更清楚狀況。
請針對我給予的文章做回覆整理，不要使用文章以外的內容做回覆。
----
文章: {paragraph}
"""
    )
    chain = prompt | get_llm()
    return chain.invoke({"paragraph": paragraph}).content


def get_refactor_question(paragraph: str):
    prompt = ChatPromptTemplate.from_template(
        """
你是一個要去診所進行看診的換診，下面是你的問題，請幫我是用繁體中文做重點整理，讓醫生可以更清楚你的症狀。
過程中請不要針對我的病況給予我任何建議，請幫我整理問題就好，並且不要使用文章以外的內容。
我希望可以把內容縮減在 100 字以內，並且使用簡答的方式整理成一句話，並且不要列點。
請直接給我回覆，不需要給予開頭或結尾。
----
文章: {paragraph}
"""
    )
    chain = prompt | get_llm()
    return chain.invoke({"paragraph": paragraph}).content


def get_content_embedding(content: str) -> list:
    env_settings = EnvSettings()
    embedding = OpenAIEmbeddings(
        openai_api_key=env_settings.OPENAI_API_KEY,
        model="text-embedding-3-small"
    )
    return embedding.embed_query(content)
