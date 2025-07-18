import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import matplotlib

# 1) 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 2) 페이지 설정
st.set_page_config(page_title="표고버섯 소셜 빅데이터 분석", layout="wide")

# 3) 전역 스타일
st.markdown("""
<style>
/* 전체 배경 및 기본 텍스트 */
[data-testid="stAppViewContainer"] {
  background-color: #f4f7fa;
  color: #2c3e50;
  font-family: 'Malgun Gothic', sans-serif;
}
/* 카드 스타일 */
.card {
  background: #ffffff;
  padding: 1.2rem;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  margin-bottom: 1.5rem;
}
/* 메인 타이틀 */
.main-title {
  font-size: 2.5rem;
  font-weight: 800;
  text-align: center;
  padding: 1rem 0;
  color: #ffffff;
  background: linear-gradient(90deg, #0066cc, #0099ff);
  border-radius: 8px;
  margin-bottom: 1.5rem;
}
/* 섹션 타이틀 */
.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #0066cc;
  margin-bottom: 0.8rem;
}
/* 텍스트 블록 */
.content-text {
  font-size: 0.95rem;
  line-height: 1.6;
}
/* 차트 캔버스 중앙 정렬 */
.chart-container {
  display: flex;
  justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# 4) 헤더
st.markdown('<div class="main-title">표고버섯 소셜 빅데이터 분석 (2019-2023)</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1rem; color:#555;'>총 언급량: 222,000회 | 67% 증가 추세</p>", unsafe_allow_html=True)

# 5) 1행: 워드클라우드 / 연도별 / 계절별
with st.container():
    col1, col2, col3 = st.columns([1.2,1,1])
    # 주요 키워드
    with col1:
        st.markdown('<div class="card"><div class="section-title">주요 키워드</div></div>', unsafe_allow_html=True)
        keywords = "표고버섯 면역력 볶음 육수 비타민D 채식 콜레스테롤 재배 베타글루칸 표고전 원목재배 강칠맛"
        wc = WordCloud(font_path='NanumGothic-Regular.ttf',
                       width=400, height=300,
                       background_color='white',
                       colormap='Greens').generate(keywords)
        fig, ax = plt.subplots(figsize=(4,3))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig, clear_figure=True)

    # 연도별 언급량 추이
    with col2:
        st.markdown('<div class="card"><div class="section-title">연도별 언급량 추이</div></div>', unsafe_allow_html=True)
        year_data = pd.DataFrame({
            "연도": ['2019','2020','2021','2022','2023'],
            "언급량": [31500,43800,45200,48900,52600]
        })
        fig = px.bar(year_data, x='연도', y='언급량', text='언급량',
                     color='언급량', color_continuous_scale='greens')
        fig.update_traces(textposition='outside')
        fig.update_layout(margin=dict(t=10,b=10,l=10,r=10), showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    # 계절별 언급 분포
    with col3:
        st.markdown('<div class="card"><div class="section-title">계절별 언급 분포</div></div>', unsafe_allow_html=True)
        season_data = pd.DataFrame({
            "계절": ['봄','여름','가을','겨울'],
            "비율": [26,17,29,28]
        })
        fig = px.pie(season_data, names='계절', values='비율',
                     color_discrete_sequence=px.colors.sequential.Greens)
        fig.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=300)
        st.plotly_chart(fig, use_container_width=True)

# 6) 2행: 감성분석 / 토픽모델링 / 연령대별
with st.container():
    col4, col5, col6 = st.columns(3)
    # 감성 분석
    with col4:
        st.markdown('<div class="card"><div class="section-title">감성 분석</div></div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4,2.5))
        ax.barh(['긍정','중립','부정'], [76,16,8], color=['#2ecc71','#95a5a6','#e74c3c'])
        for i, v in enumerate([76,16,8]):
            ax.text(v+1, i, f"{v}%", va='center', fontsize=10)
        ax.set_xlim(0,100); ax.invert_yaxis(); ax.axis('off')
        st.pyplot(fig, clear_figure=True)
        st.write('<p class="content-text"><b>긍정</b> 76% (169,100회) | <b>중립</b> 16% (35,600회) | <b>부정</b> 8% (17,800회)</p>', unsafe_allow_html=True)

    # 토픽 모델링
    with col5:
        st.markdown('<div class="card"><div class="section-title">토픽 모델링</div></div>', unsafe_allow_html=True)
        topic_df = pd.DataFrame({
            "토픽": ["요리/레시피","건강/효능","생산/재배","유통/가격"],
            "비율": [38,32,18,12]
        })
        fig = px.bar(topic_df, x='토픽', y='비율', text='비율',
                     color='비율', color_continuous_scale='greens')
        fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10), height=300)
        st.plotly_chart(fig, use_container_width=True)

    # 연령대별 관심도
    with col6:
        st.markdown('<div class="card"><div class="section-title">연령대별 관심도</div></div>', unsafe_allow_html=True)
        age_df = pd.DataFrame({
            "연령대": ["20~30대","40~50대","60대+"],
            "비율": [31,42,27]
        })
        fig = px.bar(age_df, x='연령대', y='비율', text='비율',
                     color='비율', color_continuous_scale='greens')
        fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10), height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.write("""
        <div class="content-text">
        <p><b>20~30대 (69,000회)</b> → 채식/비건 45%, 다이어트 33%</p>
        <p><b>40~50대 (93,450회)</b> → 면역/건강 48%, 전통요리 32%</p>
        <p><b>60대+ (60,050회)</b> → 건강식품 52%, 웰빙 38%</p>
        </div>
        """, unsafe_allow_html=True)

# 7) 3행: 용도별 활용 분석 + 핵심 인사이트
with st.container():
    col7, col8 = st.columns([1.2,1])
    # 용도별 활용 분석
    with col7:
        st.markdown('<div class="card"><div class="section-title">용도별 활용 분석</div></div>', unsafe_allow_html=True)
        usage = pd.DataFrame({
            "항목": ["국물/육수","볶음","채소대체","샐러드","면역력 강화","콜레스테롤","비타민D","체중관리"],
            "비율": [27,25,18,8,38,22,18,12],
            "카테고리": ["요리","요리","요리","요리","건강","건강","건강","건강"]
        })
        fig = px.bar(usage, x='항목', y='비율', color='카테고리', text='비율',
                     color_discrete_sequence=['#27ae60','#2980b9'])
        fig.update_layout(yaxis_title="비율 (%)", margin=dict(t=10,b=10,l=10,r=10), height=350)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    # 핵심 인사이트
    with col8:
        st.markdown('<div class="card"><div class="section-title">핵심 인사이트</div>', unsafe_allow_html=True)
        st.write("""
        <ul class="content-text">
          <li>5년간 67% 성장 (31.5K → 52.6K)</li>
          <li>긍정 감성 76% - 맛과 건강 두 마리 토끼</li>
          <li>요리용도 38% vs 건강효능 32%</li>
          <li>40~50대 관심도 최고 (42%)</li>
          <li>MZ세대 비건·레시피 주도</li>
          <li>사계절 고른 언급 분포</li>
          <li>생산/재배 18% - 스마트팜·귀농 연결</li>
        </ul>
        """, unsafe_allow_html=True)

# 8) 트렌드 전망
st.markdown('<div class="card"><div class="section-title">표고버섯 소셜 트렌드 전망</div></div>', unsafe_allow_html=True)
st.write("""
<div class="content-text">
  <p><b>성장 동력</b><br>
  - 건강식품 관심 증가<br>
  - 채식/비건 트렌드 확산<br>
  - 스마트팜·귀농 연계 생산 확대</p>
  <p><b>마케팅 포인트</b><br>
  - 40~50대: 면역·콜레스테롤 공략<br>
  - 20~30대: 비건·레시피 콘텐츠 강화<br>
  - 60대+: 전통 요리·건강식품 연계</p>
  <p><b>콘텐츠 전략</b><br>
  - 요리38% vs 건강32% 균형 구성<br>
  - 계절별 맞춤(겨울=면역, 가을=생산)<br>
  - 긍정 감성(76%) 강조 브랜딩</p>
</div>
""", unsafe_allow_html=True)

# 9) 하단 정보
st.markdown("""
---
<p style='font-size:0.85rem; color:#555;'>
<b>데이터 출처</b>: 소셜미디어 빅데이터(네이버·인스타·유튜브 등)<br>
<b>분석 기간</b>: 2019–2023년<br>
<b>분석 기법</b>: 텍스트 마이닝, 감성분석, 토픽모델링
</p>
""", unsafe_allow_html=True)
