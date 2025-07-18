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

# CSS: 세련된 카드, 그라디언트 헤더, 균일 타이포그래피
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
:root {
  --primary: #3b82f6;
  --secondary: #06b6d4;
  --accent: #f97316;
  --bg: #f1f5f9;
  --card-bg: #ffffff;
  --text: #374151;
}
[data-testid="stAppViewContainer"] {
  font-family: 'Inter', sans-serif;
  background-color: var(--bg);
  color: var(--text);
  padding: 2rem;
}
/* 헤더 그라디언트 배경 */
.header {
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  padding: 1.5rem;
  border-radius: 0.75rem;
  text-align: center;
  margin-bottom: 2rem;
}
.header h1 {
  margin: 0;
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
}
.header p {
  margin: 0.5rem 0 0;
  color: rgba(255,255,255,0.85);
  font-size: 1rem;
}
/* 카드 스타일 */
.card {
  background: var(--card-bg);
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  min-height: 350px;
  display: flex;
  flex-direction: column;
}
.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 1rem;
  position: relative;
}
.section-title::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 3rem;
  height: 3px;
  background: var(--secondary);
}
.content-text {
  line-height: 1.6;
  flex-grow: 1;
}
/* 카드 hover 효과 */
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transition: all 0.2s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown("""
<div class="header">
  <h1>표고버섯 소셜 빅데이터 분석 (2019-2023)</h1>
  <p>총 언급량: 222,000회 | 67% 증가 추세</p>
</div>
""", unsafe_allow_html=True)

# 공통 색상
COLOR_SEQ = ['#3b82f6', '#06b6d4', '#f97316', '#8b5cf6']

# 1열: 키워드, 연도별, 계절별
with st.container():
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown('<div class="card"><div class="section-title">주요 키워드</div></div>', unsafe_allow_html=True)
        words = "표고버섯 면역력 볶음 육수 비타민D 채식 콜레스테롤 재배 베타글루칸 표고전 원목재배 강칠맛"
        wc = WordCloud(font_path='NanumGothic-Regular.ttf', background_color='white', width=400, height=300, colormap='viridis').generate(words)
        fig, ax = plt.subplots(figsize=(4,3))
        ax.imshow(wc, interpolation='bilinear'); ax.axis('off')
        st.pyplot(fig)
    with c2:
        st.markdown('<div class="card"><div class="section-title">연도별 언급량 추이</div></div>', unsafe_allow_html=True)
        df_y = pd.DataFrame({"연도":['2019','2020','2021','2022','2023'],"언급량":[31500,43800,45200,48900,52600]})
        fig = px.bar(df_y, x='연도', y='언급량', text='언급량', color='연도', color_discrete_sequence=COLOR_SEQ)
        fig.update_traces(textposition='outside')
        fig.update_layout(margin=dict(t=20,b=20,l=20,r=20), height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        st.markdown('<div class="card"><div class="section-title">계절별 언급 분포</div></div>', unsafe_allow_html=True)
        df_s = pd.DataFrame({"계절":['봄','여름','가을','겨울'],"비율":[26,17,29,28]})
        fig = px.pie(df_s, names='계절', values='비율', hole=0.35, color_discrete_sequence=COLOR_SEQ)
        fig.update_layout(margin=dict(t=20,b=20,l=20,r=20), height=320)
        st.plotly_chart(fig, use_container_width=True)

# 2열: 감성, 토픽, 연령대
with st.container():
    c4, c5, c6 = st.columns(3, gap="large")
    with c4:
        st.markdown('<div class="card"><div class="section-title">감성 분석</div></div>', unsafe_allow_html=True)
        vals = [76,16,8]; labs=['긍정','중립','부정']
        fig, ax = plt.subplots(figsize=(4,3))
        ax.barh(labs, vals, color=COLOR_SEQ[:3])
        for i,v in enumerate(vals): ax.text(v+1, i, f"{v}%", va='center', fontweight='600')
        ax.invert_yaxis(); ax.axis('off');
        st.pyplot(fig)
        st.markdown('<div class="content-text"><b>긍정</b>76% (169,100회) | <b>중립</b>16% (35,600회) | <b>부정</b>8% (17,800회)</div>', unsafe_allow_html=True)
    with c5:
        st.markdown('<div class="card"><div class="section-title">토픽 모델링</div></div>', unsafe_allow_html=True)
        df_t = pd.DataFrame({"토픽":["요리/레시피","건강/효능","생산/재배","유통/가격"],"비율":[38,32,18,12]})
        fig = px.bar(df_t, x='토픽', y='비율', text='비율', color='토픽', color_discrete_sequence=COLOR_SEQ)
        fig.update_layout(margin=dict(t=20,b=20,l=20,r=20), height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with c6:
        st.markdown('<div class="card"><div class="section-title">연령대별 관심도</div></div>', unsafe_allow_html=True)
        df_a = pd.DataFrame({"연령대":['20~30대','40~50대','60대+'],"비율":[31,42,27]})
        fig = px.bar(df_a, x='연령대', y='비율', text='비율', color='연령대', color_discrete_sequence=COLOR_SEQ)
        fig.update_layout(margin=dict(t=20,b=20,l=20,r=20), height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        <div class="content-text">
          <p><b>20~30대 (69,000회)</b> 채식/비건 45%, 다이어트 33%</p>
          <p><b>40~50대 (93,450회)</b> 면역/건강 48%, 전통요리 32%</p>
          <p><b>60대+ (60,050회)</b> 건강식품 52%, 웰빙 38%</p>
        </div>
        ''', unsafe_allow_html=True)

# 3열: 용도별, 인사이트
with st.container():
    c7, c8 = st.columns([1.6,1], gap="large")
    with c7:
        st.markdown('<div class="card"><div class="section-title">용도별 활용 분석</div></div>', unsafe_allow_html=True)
        df_u = pd.DataFrame({
            '항목':['국물/육수','볶음','채소대체','샐러드','면역강화','콜레스테롤','비타민D','체중관리'],
            '비율':[27,25,18,8,38,22,18,12],
            '카테고리':['요리','요리','요리','요리','건강','건강','건강','건강']
        })
        fig = px.bar(df_u, x='항목', y='비율', text='비율', color='카테고리', color_discrete_sequence=[COLOR_SEQ[1], COLOR_SEQ[0]])
        fig.update_traces(textposition='outside')
        fig.update_layout(margin=dict(t=20,b=20,l=20,r=20), height=360)
        st.plotly_chart(fig, use_container_width=True)
    with c8:
        st.markdown('<div class="card"><div class="section-title">핵심 인사이트</div></div>', unsafe_allow_html=True)
        st.markdown('''
        <div class="content-text">
        <ul>
          <li>5년간 언급량 67% 증가 (31.5K → 52.6K)</li>
          <li>긍정 감성 76% - 맛과 건강의 이중효과</li>
          <li>요리용도 38% vs 건강효능 32%</li>
          <li>40~50대 관심도 최고 (42%)</li>
          <li>MZ세대 비건 트렌드 선도</li>
          <li>사계절 고른 분포</li>
          <li>생산/재배 18% - 스마트팜·귀농 연계</li>
        </ul>
        </div>
        ''', unsafe_allow_html=True)

# 트렌드 전망 & 푸터
st.markdown('<div class="card"><div class="section-title">표고버섯 소셜 트렌드 전망</div></div>', unsafe_allow_html=True)
st.markdown('''
<div class="content-text">
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
</div>
''', unsafe_allow_html=True)
st.markdown('''
---
<p style='color:#9ca3af; font-size:0.8rem;'>
<b>데이터 출처</b>: 네이버·인스타그램·유튜브<br>
<b>분석 기간</b>: 2019–2023년<br>
<b>분석 기법</b>: 텍스트 마이닝·감성분석·토픽모델링
</p>
''', unsafe_allow_html=True)
