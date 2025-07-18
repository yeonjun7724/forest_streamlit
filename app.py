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
st.set_page_config(page_title="표고버섯 소셜 빅데이터 분석", layout="wide")

# 전체 스타일
st.markdown("""
<style>
/* 앱 배경 및 기본 폰트 */
[data-testid="stAppViewContainer"] {
  background-color: #f8fafc;
  color: #1f2a38;
  font-family: 'Malgun Gothic', sans-serif;
}
/* 카드 공통 */
.card {
  background: #ffffff;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  margin-bottom: 1rem;
}
/* 메인 타이틀 */
.main-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffffff;
  background: linear-gradient(90deg, #4a90e2, #50e3c2);
  padding: 1rem;
  text-align: center;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}
/* 섹션 타이틀 */
.section-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #4a90e2;
  margin-bottom: 0.8rem;
}
/* 텍스트 스타일 */
.content-text {
  font-size: 0.9rem;
  line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown('<div class="main-title">표고버섯 소셜 빅데이터 분석 (2019-2023)</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#7f8fa4;'>총 언급량: 222,000회 | 67% 증가 추세</p>", unsafe_allow_html=True)

# 공통 컬러 맵
COLOR_MAP = ['#4a90e2', '#50e3c2', '#f5a623', '#bd10e0']

# 1행: 주요 키워드, 연도별 언급량 추이, 계절별 분포
with st.container():
    c1, c2, c3 = st.columns(3)
    # 주요 키워드
    with c1:
        st.markdown('<div class="card"><div class="section-title">주요 키워드</div></div>', unsafe_allow_html=True)
        keywords = "표고버섯 면역력 볶음 육수 비타민D 채식 콜레스테롤 재배 베타글루칸 표고전 원목재배 강칠맛"
        wc = WordCloud(font_path='NanumGothic-Regular.ttf', width=400, height=300,
                       background_color='white', colormap='viridis').generate(keywords)
        fig, ax = plt.subplots(figsize=(4,3))
        ax.imshow(wc, interpolation='bilinear'); ax.axis('off')
        st.pyplot(fig, clear_figure=True)
    # 연도별 언급량 추이
    with c2:
        st.markdown('<div class="card"><div class="section-title">연도별 언급량 추이</div></div>', unsafe_allow_html=True)
        year_df = pd.DataFrame({"연도":['2019','2020','2021','2022','2023'],
                                "언급량":[31500,43800,45200,48900,52600]})
        fig = px.bar(year_df, x='연도', y='언급량', text='언급량',
                     color='연도', color_discrete_sequence=COLOR_MAP)
        fig.update_traces(textposition='outside')
        fig.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    # 계절별 언급 분포
    with c3:
        st.markdown('<div class="card"><div class="section-title">계절별 언급 분포</div></div>', unsafe_allow_html=True)
        season_df = pd.DataFrame({"계절":['봄','여름','가을','겨울'],
                                  "비율":[26,17,29,28]})
        fig = px.pie(season_df, names='계절', values='비율',
                     color_discrete_sequence=COLOR_MAP)
        fig.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=300)
        st.plotly_chart(fig, use_container_width=True)

# 2행: 감성 분석, 토픽 모델링, 연령대별 관심도
with st.container():
    c4, c5, c6 = st.columns(3)
    # 감성 분석
    with c4:
        st.markdown('<div class="card"><div class="section-title">감성 분석</div></div>', unsafe_allow_html=True)
        sentiments = [76,16,8]
        labels = ['긍정','중립','부정']
        colors = ['#4a90e2','#50e3c2','#f5a623']
        fig, ax = plt.subplots(figsize=(4,2.5))
        ax.barh(labels, sentiments, color=colors)
        for i,v in enumerate(sentiments): ax.text(v+1, i, f"{v}%", va='center', fontsize=10)
        ax.invert_yaxis(); ax.axis('off');
        st.pyplot(fig, clear_figure=True)
        st.write('<p class="content-text"><b>긍정</b>76% (169,100회) | <b>중립</b>16% (35,600회) | <b>부정</b>8% (17,800회)</p>', unsafe_allow_html=True)
    # 토픽 모델링
    with c5:
        st.markdown('<div class="card"><div class="section-title">토픽 모델링</div></div>', unsafe_allow_html=True)
        topic_df = pd.DataFrame({"토픽":["요리/레시피","건강/효능","생산/재배","유통/가격"],
                                 "비율":[38,32,18,12]})
        fig = px.bar(topic_df, x='토픽', y='비율', text='비율',
                     color='토픽', color_discrete_sequence=COLOR_MAP)
        fig.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    # 연령대별 관심도
    with c6:
        st.markdown('<div class="card"><div class="section-title">연령대별 관심도</div></div>', unsafe_allow_html=True)
        age_df = pd.DataFrame({"연령대":['20~30대','40~50대','60대+'],
                               "비율":[31,42,27]})
        fig = px.bar(age_df, x='연령대', y='비율', text='비율',
                     color='연령대', color_discrete_sequence=COLOR_MAP)
        fig.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.write("""
        <div class="content-text">
          <p><b>20~30대 (69,000회)</b> 채식/비건 45%, 다이어트 33%</p>
          <p><b>40~50대 (93,450회)</b> 면역/건강 48%, 전통요리 32%</p>
          <p><b>60대+ (60,050회)</b> 건강식품 52%, 웰빙 38%</p>
        </div>
        """, unsafe_allow_html=True)

# 3행: 용도별 활용 분석, 핵심 인사이트
with st.container():
    c7, c8 = st.columns([1.3,1])
    # 용도별 활용 분석
    with c7:
        st.markdown('<div class="card"><div class="section-title">용도별 활용 분석</div></div>', unsafe_allow_html=True)
        use_df = pd.DataFrame({
            '항목':['국물/육수','볶음','채소대체','샐러드','면역강화','콜레스테롤','비타민D','체중관리'],
            '비율':[27,25,18,8,38,22,18,12],
            '카테고리':['요리','요리','요리','요리','건강','건강','건강','건강']
        })
        fig = px.bar(use_df, x='항목', y='비율', text='비율',
                     color='카테고리', color_discrete_sequence=['#50e3c2','#4a90e2'])
        fig.update_traces(textposition='outside')
        fig.update_layout(margin=dict(t=5,b=5,l=5,r=5), height=350)
        st.plotly_chart(fig, use_container_width=True)
    # 핵심 인사이트
    with c8:
        st.markdown('<div class="card"><div class="section-title">핵심 인사이트</div></div>', unsafe_allow_html=True)
        st.write("""
        <ul class="content-text">
          <li>5년간 언급량 67% 증가 (31.5K → 52.6K)</li>
          <li>긍정 감성 76% - 맛과 건강의 이중효과</li>
          <li>요리용도 38% vs 건강효능 32%</li>
          <li>40~50대 관심도 최고 (42%)</li>
          <li>MZ세대 비건 트렌드 선도</li>
          <li>사계절 고른 분포</li>
          <li>생산/재배 18% - 스마트팜·귀농 연계</li>
        </ul>
        """, unsafe_allow_html=True)

# 4행: 트렌드 전망
st.markdown('<div class="card"><div class="section-title">표고버섯 소셜 트렌드 전망</div></div>', unsafe_allow_html=True)
st.write("""
<div class="content-text">
  <p><b>성장 동력</b><br>
  - 건강식품 관심 증가<br>
  - 채식/비건 트렌드 확산<br>
  - 스마트팜·귀농 연계 생산 증가</p>
  <p><b>마케팅 포인트</b><br>
  - 40~50대: 면역·콜레스테롤 중심 소구<br>
  - 20~30대: 비건·레시피 콘텐츠 활용<br>
  - 60대+: 전통 요리·건강식품 연계</p>
  <p><b>콘텐츠 전략</b><br>
  - 요리 레시피 38% vs 건강 정보 32% 균형 배치<br>
  - 계절별 맞춤 콘텐츠 (봄=레시피, 겨울=면역)<br>
  - 긍정 감성 76% 활용한 브랜딩 강화</p>
</div>
""", unsafe_allow_html=True)

# 하단 정보
st.markdown("""
---
<p class='content-text' style='color:#7f8fa4;'>
<b>데이터 출처</b>: 소셜미디어 빅데이터(네이버, 인스타그램, 유튜브 등)<br>
<b>분석 기간</b>: 2019-2023년<br>
<b>분석 기법</b>: 텍스트 마이닝, 감성분석, 토픽모델링
</p>
""", unsafe_allow_html=True)
