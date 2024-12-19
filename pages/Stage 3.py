import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static, st_folium
import time
import matplotlib.pyplot as plt
from matplotlib import rc


if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]
with st.sidebar:
    st.caption(f'{ID}님 접속중')
    
if "quiz3_input" not in st.session_state:
    st.session_state["quiz3_input"] = "None"
with st.sidebar:
    st.caption(f'<내가 생각하는 수도권 자선냄비 설치 개수> : {st.session_state["quiz3_input"]}개')
    
st.title('수도권 중 어디에 자선냄비를 설치해야 할까?')
st.write("유동인구가 많은 서울 지하철 역에 자선냄비를 설치하고자 할 때, 아래 자료를 바탕으로 수도권에는 자선냄비를 어디에 설치해야 하는지 이유와 함께 설명하시오.")

data = pd.read_csv("subway(20241125).csv", encoding='utf-8-sig')
data = data.dropna(axis=1, how='all')
st.dataframe(data)

m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

for _, row in data.iterrows():
    if not pd.isnull(row['위도']) and not pd.isnull(row['경도']):
        popup = folium.Popup(f"<div style='white-space: nowrap;'>{row['★지하철 역명★']}</div>", max_width=200)
        
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=5,  # 점의 크기 설정
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.7,
            popup=popup
        ).add_to(m)

folium_static(m)

st.divider()

st.write("위의 자료를 히스토그램으로 표현하고 자료를 분석해보자.")

rc('font', family='NanumGothic')  # 또는 family='NanumGothic', family='AppleGothic'
plt.rcParams['axes.unicode_minus'] = False  
data.columns = data.columns.str.strip()
data.columns = ['★지하철 역명★','노선명','★승하차 총 승객수★','위도','경도']

data['★승하차 총 승객수★'] = pd.to_numeric(data['★승하차 총 승객수★'], errors='coerce')

data = data.dropna(subset=['★승하차 총 승객수★'])

st.sidebar.header("히스토그램 설정")
start = st.sidebar.number_input("첫 번째 계급 시작값", value=0, step=500)
bin_size = st.sidebar.number_input("계급의 크기", value=5000, step=500)

if bin_size <= 0:
    st.sidebar.error("계급의 크기는 0보다 커야 합니다.")
else:
    bins = range(start, int(data['★승하차 총 승객수★'].max()) + bin_size, bin_size)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    counts, bin_edges, patches = ax.hist(data['★승하차 총 승객수★'], bins=bins, edgecolor='k', alpha=0.7)
    
    for count, x_pos in zip(counts, bin_edges[:-1]):
        ax.text(x_pos + bin_size / 2, count + 1, int(count), ha='center', fontsize=10)

    ax.set_xticks(bin_edges)
    ax.set_xticklabels([int(edge)/1000 for edge in bin_edges], rotation=45)

    ax.set_title("승하차 총 승객수 히스토그램", fontsize=16)
    ax.set_xlabel("일간 총 승객수(단위 : 천명)", fontsize=14)
    ax.set_ylabel("도수 (지하철역 수)", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)
    
selected_bins = st.sidebar.multiselect(
        "지도에 표시할 계급 범위 선택",
        options=[f"{int(bin_edges[i])} ~ {int(bin_edges[i + 1])}" for i in range(len(bin_edges) - 1)],
        default=[]
    )

filtered_data = pd.DataFrame()
for bin_range in selected_bins:
    bin_start, bin_end = map(int, bin_range.split(" ~ "))
    filtered_data = pd.concat([
        filtered_data,
        data[(data['★승하차 총 승객수★'] >= bin_start) & (data['★승하차 총 승객수★'] < bin_end)]
    ])

m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

for _, row in filtered_data.iterrows():
    if not pd.isnull(row['위도']) and not pd.isnull(row['경도']):
        popup = folium.Popup(f"<div style='white-space: nowrap;'>{row['★지하철 역명★']}</div>", max_width=200)
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=7,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.7,
            popup=popup
        ).add_to(m)

st.subheader("선택한 계급 범위에 해당하는 지하철 역")
folium_static(m)


st.markdown(f'퀴즈 5 : 앞서 퀴즈 3에서 답을 했듯이 수도권에 {st.session_state["quiz3_input"]}개의 자선냄비를 설치한다면, 그 위치와 설치 기준은 무엇인지 히스토그램과 지도를 바탕으로 설명하시오. [계급의 시작값], [계급의 크기], [계급의 개수], [계급(데이터 값)], [도수], [히스토그램]의 용어가 포함되도록 50글자 이상의 문장으로 서술하시오.')

quiz_input5 = st.text_area("<3에서 답한 개수가 필요한 이유> :", placeholder="50자 이상의 문장을 작성하세요!", height=100)

if st.button("퀴즈 5 확인"):
    text_length5 = len(quiz_input5.strip())
    if text_length5 >= 50:
        if "상대도수" in quiz_input5:
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
        st.error(f"작성한 내용은 {text_length5}글자입니다. 50글자 이상 작성하세요.")