# streamlit run app.py
import streamlit as st
import pandas as pd
import time

if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]
with st.sidebar:
    st.caption(f'{ID}님 접속중')

st.title('구세군 자선냄비란?')
st.image("jason pot02.jpg")
st.write("구세군이 11월26일 서울 광화문광장에서 2024 구세군 자선냄비 시종식을 개최하며 연말 자선냄비 거리모금의 시작을 알렸다. 이날 타종 세레머니와 구조물 점등식으로 시작된 구세군 자선냄비는 11월 27일부터 12월 31일까지 전국 316개의 포스트에서 진행된다.")
st.write("올해는 특별히 처음 시도하는 키오스크 모금을 비롯해 QR모금, 간편결제 가능한 온라인 모금 캠페인 등을 도입하여 시민들이 편하고 쉽게 기부에 참여할 수 있도록 시대에 맞춘 자선냄비로 진행될 예정이다. 구세군은 유동 인구가 많은 퇴근 시간대에 맞추어 시종식을 가짐으로 자선냄비가 시민들과 함께하고 있음을 강조했고, Light of Love 주제를 담아 빛으로 만들어진 조형물로 볼거리도 제공했다.")
st.write("한국의 자선냄비 거리모금은 연말을 대표하는 나눔 문화 확산 운동이다. 1928년 명동에서 시작되어 한국전쟁, 외환위기 그리고 코로나 시기 등 어려운 상황속에서도 96년동안 거리에서 사랑의 종소리를 울려오고 있으며, 연말 자선냄비를 시작으로 연중에도 정기후원과 다양한 나눔사업을 통해 이웃들의 필요를 채우고 있다.")

st.markdown("퀴즈 1 : 위의 기사를 통해 알 수 있는 2024년 전국 구세군 자선냄비의 설치 개수에 대해 답하시오.")

quiz1_input = st.text_area("<전국 자선냄비 설치 개수> :", placeholder="숫자만 입력하세요", height=68)

if st.button("퀴즈 1 확인"):
    if quiz1_input == "316":
        st.success("정답입니다!")

    else:
        st.error(f"기사를 다시 읽고, 답은 숫자만 입력하세요.")

st.divider()

st.markdown("퀴즈 2 : 기사를 읽고 자선냄비를 설치하는 장소를 선정하는 기준은 무엇일지 20글자 이상의 문장으로 서술하시오.")

quiz_input2 = st.text_area("<의견 서술> :", placeholder="20자 이상의 문장을 작성하세요!", height=100)

if st.button("퀴즈 2 확인"):
    text_length = len(quiz_input2)
    if text_length >= 20:
        st.success("다음 페이지로 이동합니다")
        progress_text = "로딩중."
        my_bar2 = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar2.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar2.empty()
            st.switch_page("pages/Stage 2.py")        
    else:
        st.error(f"작성한 내용은 {text_length}글자입니다. 20글자 이상 작성하세요.")