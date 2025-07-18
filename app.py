import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import matplotlib

# 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(
    page_title="표고버섯 소셜 빅데이터 분석", 
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS: 테마 색상, 카드 레이아웃, 타이포그래피
st.markdown("""
<style>
:root {
  --primary-color: #4a90e2;
  --secondary-color: #50e3c2;
  --accent-color: #f5a623;
  --text-color: #1f2a38;
  --bg-color: #f8fafc;
  --card-bg: #ffffff;
  --font-main: 'Inter', sans-serif;
}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

[data-testid="stAppViewContainer"] {
  background-color: var(--bg-color);
  color: var(--text-color);
  font-family: var(--font-main);
  padding: 1rem 2rem;
}
.card {
  background: var(--card-bg);
  border-radius: 0.75rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}
.main-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--primary-color);
  text-align: center;
  margin-bottom: 0.25rem;
}
.subtitle {
  text-align: center;
  color: #7f8fa4;
  margin-bottom: 2rem;
}
.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--primary-color);
  border-bottom: 2px solid var(--secondary-color);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}
.content-text {
  font-size: 0.9rem;
  line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown('<div class="main-title">표고버섯 소셜 빅데이터 분석 (2019-2023)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">총 언급량: 222,000회 | 67% 증가 추세</div>', unsafe_allow_html=True)

# 색상 맵
COLOR_MAP = ['var(--primary-color)', 'var(--secondary-color)', 'var(--accent-color)', '#bd10e0']

# 1: 키워드 | 연도별 추이 | 계절별 분포
row1 = st.container()
with row1:
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown('<div class="card"><div class="section-title">주요 키워드</div></div>', unsafe_allow_html=True)
        keywords = "표고버섯 면역력 볶음 육수 비타민D 채식 콜레스테롤 재배 베타글루칸 표고전 원목재배 강칠맛"
        wc = WordCloud(font_path='NanumGothic-Regular.ttf', background_color='white', width=400, height=300, colormap='viridis').generate(keywords)
        fig, ax = plt.subplots(figsize=(4,3))
        ax.imshow(wc, interpolation='bilinear'); ax.axis('off')
        st.pyplot(fig)
    with c2:
        st.markdown('<div class="card"><div class="section-title">연도별 언급량 추이</div></div>', unsafe_allow_html=True)
        df_year = pd.DataFrame({"연도":['2019','2020','2021','2022','2023'],"언급량":[31500,43800,45200,48900,52600]})
        fig = px.bar(df_year, x='연도', y='언급량', text='언급량', color='연도', color_discrete_sequence=COLOR_MAP)
        fig.update_traces(textposition='outside')
        fig.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        st.markdown('<div class="card"><div class="section-title">계절별 언급 분포</div></div>', unsafe_allow_html=True)
        df_season = pd.DataFrame({"계절":['봄','여름','가을','겨울'],"비율":[26,17,29,28]})
        fig = px.pie(df_season, names='계절', values='비율', hole=0.4, color_discrete_sequence=COLOR_MAP)
        fig.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=300)
        st.plotly_chart(fig, use_container_width=True)

# 2: 감성 | 토픽 | 연령대
row2 = st.container()
with row2:
    c4, c5, c6 = st.columns(3, gap="large")
    with c4:
        st.markdown('<div class="card"><div class="section-title">감성 분석</div></div>', unsafe_allow_html=True)
        sentiments = [76,16,8]; labels=['긍정','중립','부정']; colors=['var(--primary-color)','var(--secondary-color)','var(--accent-color)']
        fig, ax = plt.subplots(figsize=(4,3))
        ax.barh(labels, sentiments, color=colors)
        for i, v in enumerate(sentiments): ax.text(v+1, i, f"{v}%", va='center', fontweight='600')
        ax.invert_yaxis(); ax.axis('off')
        st.pyplot(fig)
        st.markdown('<p class="content-text"><b>긍정</b>76% (169,100회) | <b>중립</b>16% (35,600회) | <b>부정</b>8% (17,800회)</p>', unsafe_allow_html=True)
    with c5:
        st.markdown('<div class="card"><div class="section-title">토픽 모델링</div></div>', unsafe_allow_html=True)
        df_topic = pd.DataFrame({"토픽":["요리/레시피","건강/효능","생산/재배","유통/가격"],"비율":[38,32,18,12]})
        fig = px.bar(df_topic, x='토픽', y='비율', text='비율', color='토픽', color_discrete_sequence=COLOR_MAP)
        fig.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with c6:
        st.markdown('<div class="card"><div class="section-title">연령대별 관심도</div></div>', unsafe_allow_html=True)
        df_age = pd.DataFrame({"연령대":['20~30대','40~50대','60대+'],"비율":[31,42,27]})
        fig = px.bar(df_age, x='연령대', y='비율', text='비율', color='연령대', color_discrete_sequence=COLOR_MAP)
        fig.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''<div class="content-text">
<p><b>20~30대 (69,000회)</b> 채식/비건 45%, 다이어트 33%</p>
<p><b>40~50대 (93,450회)</b> 면역/건강 48%, 전통요리 32%</p>
<p><b>60대+ (60,050회)</b> 건강식품 52%, 웰빙 38%</p>
</div>''', unsafe_allow_html=True)

# 3: 용도별 | 인사이트
row3 = st.container()
with row3:
    c7, c8 = st.columns([1.5,1], gap="large")
    with c7:
        st.markdown('<div class="card"><div class="section-title">용도별 활용 분석</div></div>', unsafe_allow_html=True)
        df_use = pd.DataFrame({
            '항목':['국물/육수','볶음','채소대체','샐러드','면역강화','콜레스테롤','비타민D','체중관리'],
            '비율':[27,25,18,8,38,22,18,12],
            '카테고리':['요리','요리','요리','요리','건강','건강','건강','건강']
        })
        fig = px.bar(df_use, x='항목', y='비율', text='비율', color='카테고리', color_discrete_sequence=['var(--secondary-color)','var(--primary-color)'])
        fig.update_traces(textposition='outside')
        fig.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=350)
        st.plotly_chart(fig, use_container_width=True)
    with c8:
        st.markdown('<div class="card"><div class="section-title">핵심 인사이트</div></div>', unsafe_allow_html=True)
        st.markdown('''<div class="content-text">
<ul>
  <li>5년간 언급량 67% 증가 (31.5K → 52.6K)</li>
  <li>긍정 감성 76% - 맛과 건강의 이중효과</li>
  <li>요리용도 38% vs 건강효능 32%</li>
  <li>40~50대 관심도 최고 (42%)</li>
  <li>MZ세대 비건 트렌드 선도</li>
  <li>사계절 고른 분포</li>
  <li>생산/재배 18% - 스마트팜·귀농 연계</li>
</ul>
</div>''', unsafe_allow_html=True)

# 4: 트렌드 전망
st.markdown('<div class="card"><div class="section-title">표고버섯 소셜 트렌드 전망</div></div>', unsafe_allow_html=True)
st.markdown('''<div class="content-text">
<p><b>성장 동력</b><br>
• 건강식품 관심 증가<br>
• 채식/비건 트렌드 확산<br>
• 스마트팜·귀농 연계 생산 증가</p>
<p><b>마케팅 포인트</b><br>
• 40~50대: 면역·콜레스테롤 중심 소구<br>
• 20~30대: 비건·레시피 콘텐츠 활용<br>
• 60대+: 전통 요리·건강식품 연계</p>
<p><b>콘텐츠 전략</b><br>
• 요리 레시피 38% vs 건강 정보 32% 균형 배치<br>
• 계절별 맞춤 콘텐츠 (봄=레시피, 겨울=면역)<br>
• 긍정 감성 76% 활용한 브랜딩 강화</p>
</div>''', unsafe_allow_html=True)

# 푸터
st.markdown("""
---
<div class='content-text' style='color:#7f8fa4;'>
<b>데이터 출처</b>: 소셜미디어 빅데이터(네이버, 인스타그램, 유튜브 등)<br>
<b>분석 기간</b>: 2019-2023년<br>
<b>분석 기법</b>: 텍스트 마이닝, 감성분석, 토픽모델링
</div>
""", unsafe_allow_html=True)
