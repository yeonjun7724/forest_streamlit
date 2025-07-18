# 전체 코드: 모든 텍스트 요소를 HTML 블록 또는 표 형식으로 정리

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="표고버섯 소셜 빅데이터 분석", layout="wide")

# 스타일 CSS 삽입
st.markdown("""
<style>
body {
    background-color: #f9f9f9;
    font-family: 'Malgun Gothic', sans-serif;
}
.main-title {
    font-size: 2.3em;
    font-weight: bold;
    text-align: center;
    padding: 1rem;
    background-color: #2c3e50;
    color: white;
    border-radius: 8px;
    margin-bottom: 1.5rem;
}
.section {
    background-color: white;
    padding: 1.2rem;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    height: 100%;
}
.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 0.7rem;
}
.content-block {
    font-size: 16px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# 제목 출력
st.markdown('<div class="main-title">표고버섯 소셜 빅데이터 분석 (2019-2023)</div>', unsafe_allow_html=True)
st.markdown("#### 총 언급량: 222,000회 | 67% 증가 추세")

# 1행: 워드클라우드 / 연도별 / 계절별
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="section"><div class="section-title">주요 키워드</div>', unsafe_allow_html=True)
    keywords = "표고버섯 표고버섯 면역력 볶음 육수 비타민D 채식 콜레스테롤 재배 베타글루칸 표고전 원목재배 강칠맛 김표고"
    wordcloud = WordCloud(font_path=None, width=400, height=300, background_color='white', colormap='Greens').generate(keywords)
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section"><div class="section-title">연도별 언급량 추이</div>', unsafe_allow_html=True)
    year_data = pd.DataFrame({"연도": ['2019', '2020', '2021', '2022', '2023'], "언급량": [31500, 43800, 45200, 48900, 52600]})
    fig = px.bar(year_data, x='연도', y='언급량', color='언급량', text='언급량', color_continuous_scale='Greens')
    fig.update_traces(textposition='outside')
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="section"><div class="section-title">계절별 언급 분포</div>', unsafe_allow_html=True)
    season_data = pd.DataFrame({"계절": ['봄', '여름', '가을', '겨울'], "비율": [26, 17, 29, 28]})
    fig = px.pie(season_data, names='계절', values='비율', color_discrete_sequence=px.colors.sequential.Greens)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 2행: 감성 / 토픽 / 연령대
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown('<div class="section"><div class="section-title">감성 분석</div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="content-block">
      <tr><td><b>긍정</b></td><td>76% (169,100회)</td></tr>
      <tr><td><b>중립</b></td><td>16% (35,600회)</td></tr>
      <tr><td><b>부정</b></td><td>8% (17,800회)</td></tr>
    </table>
    """, unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5, 2.8))
    ax.barh(['긍정', '중립', '부정'], [76, 16, 8], color=['green', 'gray', 'red'])
    for i, v in enumerate([76, 16, 8]):
        ax.text(v + 1, i, f"{v}%", va='center')
    ax.set_xlim(0, 100)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="section"><div class="section-title">토픽 모델링</div>', unsafe_allow_html=True)
    topic_data = pd.DataFrame({"토픽": ["요리/레시피", "건강/효능", "생산/재배", "유통/가격"], "비율": [38, 32, 18, 12]})
    fig = px.bar(topic_data, x="토픽", y="비율", color="비율", text="비율", color_continuous_scale="Greens")
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="section"><div class="section-title">연령대별 관심도</div>', unsafe_allow_html=True)
    age_data = pd.DataFrame({"연령대": ["20~30대", "40~50대", "60대+"], "비율": [31, 42, 27]})
    fig = px.bar(age_data, x="연령대", y="비율", color="비율", text="비율", color_continuous_scale="Greens")
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <div class="content-block">
    <p><b>20~30대 (69,000회)</b><br>→ 채식/비건 45%, 다이어트 33%</p>
    <p><b>40~50대 (93,450회)</b><br>→ 면역/건강 48%, 전통요리 32%</p>
    <p><b>60대+ (60,050회)</b><br>→ 건강식품 52%, 웰빙 38%</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 3행: 활용도 / 인사이트
col7, col8 = st.columns(2)

with col7:
    st.markdown('<div class="section"><div class="section-title">용도별 활용 분석</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="content-block">
    <p><b>요리 용도 (116,150회)</b><br>
    - 국물/육수 27%<br>- 볶음 25%<br>- 채소섭취대체 15%<br>- 샐러드 8%</p>
    <p><b>건강 효능 (71,170회)</b><br>
    - 면역력 강화 38%<br>- 콜레스테롤 22%<br>- 비타민D 18%<br>- 체중관리 12%</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col8:
    st.markdown('<div class="section"><div class="section-title">핵심 인사이트</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="content-block">
    <ul>
      <li>5년간 67% 증가 (31.5K → 52.6K)</li>
      <li>긍정 감성 76% - 맛과 건강 이중 효능</li>
      <li>요리 용도 38% > 건강 효능 32%</li>
      <li>40~50대 관심도 최고 (42%)</li>
      <li>MZ세대 비건 트렌드 주도</li>
      <li>사계절 고른 언급 분포</li>
      <li>생산/재배 18% - 귀농/스마트팜 연계</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 4행: 트렌드 전망
st.markdown('<div class="section"><div class="section-title">표고버섯 소셜 트렌드 전망</div>', unsafe_allow_html=True)
st.markdown("""
<div class="content-block">
<p><b>[성장 동력]</b><br>
- 건강식품 관심 증가<br>
- 채식/비건 트렌드 확산<br>
- 스마트팜·귀농 연계 생산 증가</p>

<p><b>[마케팅 포인트]</b><br>
- 40~50대: 면역·콜레스테롤 중심 소구<br>
- 20~30대: 비건/레시피 콘텐츠<br>
- 60대+: 전통요리/건강식품 연계</p>

<p><b>[콘텐츠 전략]</b><br>
- 요리 38% vs 건강 32% 균형 콘텐츠<br>
- 계절 맞춤 전략: 겨울=면역, 가을=생산<br>
- 긍정 감성(76%) 활용한 브랜딩 강화</p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 하단 정보
st.markdown("""
---
<div style='font-size:14px;'>
<b>데이터 출처</b>: 소셜미디어 빅데이터 (네이버, 인스타그램, 유튜브 등)<br>
<b>분석 기간</b>: 2019~2023년<br>
<b>분석 기법</b>: 텍스트 마이닝, 감성분석, 토픽모델링
</div>
""", unsafe_allow_html=True)
