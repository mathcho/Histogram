# streamlit run app.py
import streamlit as st
import pandas as pd
import time

if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]
with st.sidebar:
    st.caption(f'{ID}님 접속중')
    
st.title('수도권에는 자선냄비를 얼마나 설치하면 좋을까?')
st.write("아래 자료를 바탕으로 수도권에는 자선냄비를 몇 개 설치하면 이유와 함께 답하시오.")
st.image("ingu02.jpg")
st.image("ingu03.jpg")
st.image("ingu01.jpg")
st.write("<2023년 권역별 인구 수(단위 : 천명)>")
data = pd.read_csv("ingudata.csv", encoding='utf-8-sig')
data = data.dropna(axis=1, how='all')
st.dataframe(data)
st.divider()

st.markdown("퀴즈 3 : 위의 자료를 통해 전국에 설치되는 316개 자선냄비 중 수도권에는 몇 개를 설치하면 좋다고 생각하나요~?")

quiz3_input = st.text_area("<내가 생각하는 수도권 자선냄비 설치 개수> :", placeholder="숫자만 입력하세요", height=68)

if "quiz3_input" not in st.session_state:
    st.session_state["quiz3_input"] = "None"
if st.button("퀴즈 3 입력"):
    if not quiz3_input.strip(): 
        st.warning("답을 입력해 주세요!")
    else:
        if quiz3_input.strip().isdigit():
            st.session_state["quiz3_input"] = quiz3_input.strip()
            st.success("다음 내용으로 넘어가세요!")
        else:
            st.error("숫자만 입력하세요!")

with st.sidebar:
    st.caption(f'<내가 생각하는 수도권 자선냄비 설치 개수> : {st.session_state["quiz3_input"]}개')

st.divider()

st.markdown("퀴즈 4 : 퀴즈 3에서 답한 개수의 이유를 상대도수 개념을 포함하여 50글자 이상의 문장으로 서술하시오.")

quiz_input4 = st.text_area("<3에서 답한 개수가 필요한 이유> :", placeholder="50자 이상의 문장을 작성하세요!", height=100)

if st.button("퀴즈 4 확인"):
    text_length4 = len(quiz_input4.strip())
    if text_length4 >= 50:
        if "상대도수" in quiz_input4:
            st.success("다음 내용으로 넘어가세요!")
            progress_text = "로딩중."
            my_bar3 = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar3.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar3.empty()
                st.switch_page("pages/Stage 3.py")    
        else:
            st.error('"상대도수" 개념을 포함하여 50글자 이상으로 답하시오!')
    else:
        st.error(f"작성한 내용은 {text_length4}글자입니다. 50글자 이상 작성하세요.")
    
