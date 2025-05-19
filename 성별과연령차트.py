import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import plotly.graph_objects as go

# 데이터 불러오기
file_path = r"C:\Users\dohyu\OneDrive\DOCUME~1-DESKTOP-7UOBLKN-51910\명지대학교\2025-1학기\캡스톤 디자인\자치구별_연령별_성별_인구수_UTF8BOM_sorted.csv"
df = pd.read_csv(file_path)

# 자치구 선택
gu_list = df['자치구'].unique()
selected_gu = st.selectbox("자치구 선택", gu_list, index=0)
gu_df = df[df['자치구'] == selected_gu]

# 연령 순서 보존 (파일에 정렬되어 있다고 가정)
age_order = gu_df['연령'].unique().tolist()
age_df = gu_df.groupby('연령')['인구수'].sum().reindex(age_order)
bar_x = age_df.index.tolist()
bar_y = age_df.values.tolist()

# 65세 이상부터 색상 다르게 (고령자 강조)
color1 = "#1959a8"
color2 = "#fa6e30"
bar_colors = []
found_old = False
for label in bar_x:
    # "65" 또는 "70" 이상 포함된 라벨에서 색상 변경
    if any(x in label for x in ["65", "70", "75", "80", "85", "90", "95"]):
        found_old = True
    bar_colors.append(color2 if found_old else color1)

# 성별 집계 및 퍼센트
male_sum = gu_df[gu_df['성별'] == '남자']['인구수'].sum()
female_sum = gu_df[gu_df['성별'] == '여자']['인구수'].sum()
total_sum = male_sum + female_sum
percent_man = male_sum / total_sum if total_sum else 0
percent_woman = female_sum / total_sum if total_sum else 0

# 원형 liquidFill(남)
option_man = {
    "series": [{
        "type": "liquidFill",
        "shape": "circle",
        "data": [percent_man],
        "backgroundStyle": {"color": "#fff"},
        "outline": {
            "show": True,
            "borderDistance": 0,
            "itemStyle": {
                "borderWidth": 2,
                "borderColor": "#5AC1F2",
                "shadowBlur": 0
            }
        },
        "color": ["#5AC1F2"],
        "label": {
            "normal": {
                "formatter": "남성\n{:.1f}%".format(percent_man * 100),
                "fontSize": 16,
                "fontWeight": "bold",
                "color": "#5AC1F2"
            }
        }
    }]
}
# 원형 liquidFill(여)
option_woman = {
    "series": [{
        "type": "liquidFill",
        "shape": "circle",
        "data": [percent_woman],
        "backgroundStyle": {"color": "#fff"},
        "outline": {
            "show": True,
            "borderDistance": 0,
            "itemStyle": {
                "borderWidth": 2,
                "borderColor": "#F576AB",
                "shadowBlur": 0
            }
        },
        "color": ["#F576AB"],
        "label": {
            "normal": {
                "formatter": "여성\n{:.1f}%".format(percent_woman * 100),
                "fontSize": 16,
                "fontWeight": "bold",
                "color": "#F576AB"
            }
        }
    }]
}

# ---- 레이아웃: 왼쪽(남/여 원형) + 오른쪽(바차트) ----
col1, col2 = st.columns([1, 4])
with col1:
    st.write("")  # 상단 여백
    st_echarts(option_man, height="120px")
    st_echarts(option_woman, height="120px")

with col2:
    fig = go.Figure(
        data=[go.Bar(
            x=bar_x,
            y=bar_y,
            marker_color=bar_colors
        )]
    )
    fig.update_layout(
        title="연령별 인구수 (남+여 합계)",
        xaxis_title="연령대",
        yaxis_title="인구수",
        yaxis=dict(
            tickformat=",",        # 17,000 처럼 전체 숫자 표기
            separatethousands=True
        ),
        margin=dict(l=30, r=20, t=40, b=40),
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)
