import streamlit as st
import pandas as pd
import segno

# 1. 初始化全域變數
if "responses" not in st.session_state:
    st.session_state.responses = []  
if "current_question" not in st.session_state:
    st.session_state.current_question = {
        "text": "Python 內建用來輸出文字的函式是什麼？",
        "options": {"A": "input()", "B": "print()", "C": "output()", "D": "write()"},
        "correct_answer": "B"
    }

# 2. 自動判別角色
query_params = st.query_params
if query_params.get("role") == "student":
    default_role = "學生端 (手機畫面)"
else:
    default_role = "老師端 (大螢幕/PPT)"

role = st.sidebar.selectbox("請選擇您的角色", ["老師端 (大螢幕/PPT)", "學生端 (手機畫面)"], index=0 if default_role == "老師端 (大螢幕/PPT)" else 1)

# ==================== 老師端 (大螢幕/PPT) ====================
if role == "老師端 (大螢幕/PPT)":
    st.title("👨‍🏫 課堂即時互動系統 - 老師控制台")
    
    q = st.session_state.current_question
    st.subheader(f"目前題目：{q['text']}")
    for k, v in q['options'].items():
        st.write(f"**{k}** : {v}")
        
    st.write(f"💡 正確答案是：**{q['correct_answer']}**")

    # 專屬正式網址
    student_url = "class-interaction-qqspmptpuvrydk4oblxfvw.streamlit.app/?role=student"
    
    # 使用 segno 產生最穩定的 SVG 格式 QR Code
    qr = segno.make(student_url)
    
    # 顯示 QR Code 供學生掃描
    st.image(qr.png_data_uri(scale=5), caption="請學生掃描 QR Code 進入加入答題", width=250)

    st.divider()
    st.subheader("📊 即時答題統計")
    
    if st.session_state.responses:
        df = pd.DataFrame(st.session_state.responses)
        
        # 統計各答案人數
        ans_counts = df['answer'].value_counts().reindex(["A", "B", "C", "D"], fill_value=0)
        st.bar_chart(ans_counts)
        
        # 顯示誰答對的多 (排行榜)
        st.subheader("🏆 答對題數排行榜")
        leaderboard = df[df['correct'] == True]['name'].value_counts().reset_index()
        leaderboard.columns = ['學生姓名', '答對題數']
        st.dataframe(leaderboard, use_container_width=True)
    else:
        st.info("目前還沒有學生送出答案。")
        
    if st.button("清除所有資料重新開始"):
        st.session_state.responses = []
        st.rerun()

# ==================== 學生端 (手機) ====================
else:
    st.title("📱 學生答題系統")
    
    # 學生登入
    student_name = st.text_input("請輸入您的姓名或學號：", key="student_name")
    
    if student_name:
        q = st.session_state.current_question
        st.write(f"### 題目：{q['text']}")
        
        # 顯示選項按鈕
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("A", use_container_width=True):
                is_correct = (q['correct_answer'] == "A")
                st.session_state.responses.append({"name": student_name, "answer": "A", "correct": is_correct})
                st.success("答案 A 已送出！")
        with col2:
            if st.button("B", use_container_width=True):
                is_correct = (q['correct_answer'] == "B")
                st.session_state.responses.append({"name": student_name, "answer": "B", "correct": is_correct})
                st.success("答案 B 已送出！")
        with col3:
            if st.button("C", use_container_width=True):
                is_correct = (q['correct_answer'] == "C")
                st.session_state.responses.append({"name": student_name, "answer": "C", "correct": is_correct})
                st.success("答案 C 已送出！")
        with col4:
            if st.button("D", use_container_width=True):
                is_correct = (q['correct_answer'] == "D")
                st.session_state.responses.append({"name": student_name, "answer": "D", "correct": is_correct})
                st.success("答案 D 已送出！")
    else:
        st.warning("請先輸入姓名才能開始答題。")
