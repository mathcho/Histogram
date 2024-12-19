import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
from matplotlib import rc
import os

# 한글 폰트 설정
def setup_font():
    font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    if not os.path.exists(font_path):
        st.error("NanumGothic 폰트를 찾을 수 없습니다. 폰트를 설치하세요.")
        return

    # matplotlib에 폰트 적용
    import matplotlib.font_manager as fm
    fontprop = fm.FontProperties(fname=font_path)
    rc('font', family=fontprop.get_name())
    plt.rcParams['axes.unicode_minus'] = False

# 폰트 설정
setup_font()

# Streamlit 상태 관리
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

# 데이터 불러오기
data = pd.read_csv("subway(20241125).csv", encoding='utf-8-sig')
data = data.dropna(axis=1, how='all')
st.dataframe(data)

# 지도 생성 및 초기 표시
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

# 데이터 전처리
data.columns = data.columns.str.strip()
data.columns = ['★지하철 역명★', '노선명', '★승하차 총 승객수★', '위도', '경도']
data['★승하차 총 승객수★'] = pd.to_numeric(data['★승하차 총 승객수★'], errors='coerce')
data = data.dropna(subset=['★승하차 총 승객수★'])

# 히스토그램 설정
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
    ax.set_xticklabels([int(edge) / 1000 for edge in bin_edges], rotation=45)

    ax.set_title("승하차 총 승객수 히스토그램", fontsize=16)
    ax.set_xlabel("일간 총 승객수(단위 : 천명)", fontsize=14)
    ax.set_ylabel("도수 (지하철역 수)", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)
