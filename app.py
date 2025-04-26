from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

openai_api_key = st.secrets["OPENAI_API_KEY"]

# LLM インスタンスの作成
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, api_key=openai_api_key)

# 専門家ごとのシステムプロンプト
expert_prompts = {
    "料理の専門家": "あなたは一流の料理研究家です。家庭料理からプロの技まで詳しく、親切に説明してください。",
    "金融アドバイザー": "あなたは信頼できる金融アドバイザーです。投資、貯金、家計管理などに的確に答えてください。",
    "心理カウンセラー": "あなたは温かく話を聞いてくれる心理カウンセラーです。心に寄り添ってアドバイスをしてください。"
}

# 回答関数
def ask_expert(user_input, role):
    messages = [
        SystemMessage(content=expert_prompts[role]),
        HumanMessage(content=user_input)
    ]
    response = chat(messages)
    return response.content

# --- Streamlit アプリのUI ---

st.title("💬 専門家に聞いてみよう - LLMアプリ")
st.write("以下のフォームに質問を入力し、ラジオボタンで話したい専門家を選んでください。LLMが専門家になりきって回答します。")

# ラジオボタン：専門家の選択
role = st.radio("相談したい専門家を選んでください", list(expert_prompts.keys()))

# テキスト入力
user_input = st.text_area("質問を入力してください")

# 送信ボタン
if st.button("送信"):
    if user_input:
        with st.spinner("専門家が回答中です..."):
            answer = ask_expert(user_input, role)
            st.success("回答：")
            st.write(answer)
    else:
        st.warning("質問内容を入力してください。")

