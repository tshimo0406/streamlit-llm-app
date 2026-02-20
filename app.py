import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# .envファイルからAPIキーを読み込む
load_dotenv()

# --- ロジック部分：LLMに回答をもらう関数 ---
def get_ai_response(user_input, expert_type):
    # LLMの準備
    llm = ChatOpenAI(model="gpt-4o-mini") 
    
    # 専門家設定の切り替え
    if expert_type == "スポーツ医学専門家":
        system_msg = "あなたは熟練のアスレティックトレーナーです。専門用語を使いつつ、的確に回答してください。"
    elif expert_type == "バレーボール専門家":
        system_msg = "あなたは熟練のバレーボールコーチです。指導者の立場から適切に回答して下さい。"
    else:
        system_msg = "あなたは有能なアシスタントです。ユーザーの質問に親切に答えてください。"

    # プロンプトの組み立て
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human", "{input}")
    ])

    # 実行
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"input": user_input})

# --- UI部分：Streamlitの画面表示 ---
st.title("🤖 専門家切り替えAIチャット")

# アプリの概要
st.markdown("""
## 📋 このアプリについて
このアプリケーションは、異なる専門分野の専門家のアドバイスを受けられるAIチャットツールです。
スポーツに関する質問や相談を、あなたが選んだ専門家の視点から解答します。

## 🎯 使い方
1. **左側のラジオボタン**から、相談したい専門家を選択してください
2. **入力欄**に質問やお悩みを入力してください
3. **「送信」ボタン**をクリックして、AIからの回答を受け取ります

## 💡 利用できる専門家
- **スポーツ医学専門家**: 怪我の予防、身体のケア、パフォーマンス向上について
- **バレーボール専門家**: スキル向上、戦術、チームマネジメントについて

---
""")
st.write("質問を入力して、AIの回答を受け取りましょう。")

# ラジオボタン
expert = st.radio("誰に相談しますか？", ("スポーツ医学専門家", "バレーボール専門家"))

# 入力フォーム
user_msg = st.text_input("質問をどうぞ：")

# ボタン
if st.button("送信"):
    if user_msg:
        with st.spinner("考え中..."):
            answer = get_ai_response(user_msg, expert)
            st.success("回答が届きました！")
            st.write(answer)
    else:
        st.warning("質問を入力してください。")