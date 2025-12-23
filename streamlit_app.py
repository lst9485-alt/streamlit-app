import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# 1. 페이지 설정
st.set_page_config(
    page_title="재테크 통합 솔루션",
    page_icon="💎",
    layout="wide"
)

# 2. CSS 디자인 (이 부분이 따옴표 안에 정확히 들어가야 에러가 안 납니다)
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# 3. 헤더
st.markdown("### 💎 당신의 미래를 설계하는 **Premium 재테크 시뮬레이터**")
st.divider()

# 4. 사이드바 설정
with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    current_age = st.number_input("현재 나이", 20, 80, 35)
    retire_age = st.number_input("은퇴 나이", current_age+1, 90, 60)
    current_cash = st.number_input("현재 순자산 (만원)", value=5000)
    monthly_save = st.number_input("월 저축액 (만원)", value=200)
    invest_rate = st.slider("연평균 수익률 (%)", 1.0, 15.0, 5.0)

# 5. 계산 로직
ages = np.arange(current_age, 91)
assets = []
money = current_cash

for age in ages:
    if age < retire_age:
        money += monthly_save * 12
    else:
        money -= 300 * 12  # 은퇴 후 지출
    money *= (1 + invest_rate / 100)
    assets.append(max(0, money))

df_result = pd.DataFrame({'나이': ages, '자산': assets})

# 6. 결과 출력
col1, col2 = st.columns(2)
col1.metric("은퇴 시점 자산", f"{assets[retire_age-current_age]:,.0f} 만원")
col2.metric("90세 최종 자산", f"{assets[-1]:,.0f} 만원")

chart = alt.Chart(df_result).mark_area(line={'color':'#1f77b4'}).encode(
    x='나이',
    y='자산',
    tooltip=['나이', '자산']
).properties(height=400)

st.altair_chart(chart, use_container_width=True)
