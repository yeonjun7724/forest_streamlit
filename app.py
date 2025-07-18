
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from io import BytesIO
import base64

# Set page config
st.set_page_config(
    page_title="표고버섯 소셜 빅데이터 분석",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f8f0, #e8f5e8);
        border-radius: 10px;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2E8B57;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background-color: #f8f9fa;
        border-left: 4px solid #2E8B57;
    }
    .insight-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<div class="main-header">🍄 표고버섯 소셜 빅데이터 분석 대시보드</div>', unsafe_allow_html=True)

# Create three rows of content
# Row 1: Word Cloud, Yearly Mentions, Seasonal Distribution
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown('<div class="section-header">1. 주요 키워드 워드클라우드</div>', unsafe_allow_html=True)

    # Word cloud data based on the image
    wordcloud_text = """
    표고버섯 표고버섯 표고버섯 표고버섯 표고버섯
    건강 건강 건강 건강
    요리 요리 요리
    영양 영양 영양
    맛있는 맛있는
    효능 효능
    면역력 면역력
    비타민 비타민
    단백질
    다이어트
    항암
    콜레스테롤
    혈압
    피부
    """

    # Create word cloud
    wordcloud = WordCloud(
        width=400, 
        height=300,
        background_color='white',
        colormap='Greens',
        font_path=None,
        max_words=50
    ).generate(wordcloud_text)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

with col2:
    st.markdown('<div class="section-header">2. 연도별 표고버섯 언급량</div>', unsafe_allow_html=True)

    # Yearly data from the image
    yearly_data = pd.DataFrame({
        '연도': ['2019', '2020', '2021', '2022', '2023'],
        '언급량': [1200, 1800, 2500, 3200, 2800]
    })

    fig = px.bar(
        yearly_data, 
        x='연도', 
        y='언급량',
        color='언급량',
        color_continuous_scale='Greens',
        title=""
    )
    fig.update_layout(
        height=350,
        showlegend=False,
        xaxis_title="연도",
        yaxis_title="언급량"
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown('<div class="section-header">3. 계절별 언급 분포</div>', unsafe_allow_html=True)

    # Seasonal data from the image
    seasonal_data = pd.DataFrame({
        '계절': ['봄', '여름', '가을', '겨울'],
        '비율': [20, 25, 35, 20]
    })

    fig = px.pie(
        seasonal_data, 
        values='비율', 
        names='계절',
        color_discrete_sequence=['#90EE90', '#32CD32', '#228B22', '#006400']
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# Row 2: Sentiment Analysis, Topic Modeling, Age Group Interest
col4, col5, col6 = st.columns([1, 1, 1])

with col4:
    st.markdown('<div class="section-header">4. 감성 분석</div>', unsafe_allow_html=True)

    # Sentiment analysis metrics
    col4_1, col4_2, col4_3 = st.columns(3)

    with col4_1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("긍정", "65%", "5%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4_2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("중립", "25%", "-2%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4_3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("부정", "10%", "-3%")
        st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="section-header">5. 토픽 모델링</div>', unsafe_allow_html=True)

    # Topic modeling data
    topic_data = pd.DataFrame({
        '토픽': ['건강/영양', '요리/레시피', '재배/농업', '효능/효과', '구매/가격'],
        '비중': [35, 28, 15, 12, 10]
    })

    fig = px.bar(
        topic_data, 
        x='토픽', 
        y='비중',
        color='비중',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        height=350,
        showlegend=False,
        xaxis_title="토픽",
        yaxis_title="비중 (%)"
    )
    fig.update_xaxis(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.markdown('<div class="section-header">6. 연령대별 관심도</div>', unsafe_allow_html=True)

    # Age group data
    age_data = pd.DataFrame({
        '연령대': ['20대', '30대', '40대', '50대', '60대+'],
        '관심도': [15, 25, 30, 20, 10]
    })

    fig = px.bar(
        age_data, 
        x='연령대', 
        y='관심도',
        color='관심도',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        height=350,
        showlegend=False,
        xaxis_title="연령대",
        yaxis_title="관심도 (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

# Row 3: Usage Analysis and Text Insights
col7, col8 = st.columns([1, 1])

with col7:
    st.markdown('<div class="section-header">7. 용도별 활용 분석</div>', unsafe_allow_html=True)

    # Usage analysis data
    usage_data = pd.DataFrame({
        '용도': ['요리 용도', '건강 효능'],
        '비율': [60, 40]
    })

    fig = px.bar(
        usage_data, 
        x='용도', 
        y='비율',
        color='비율',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        height=350,
        showlegend=False,
        xaxis_title="용도",
        yaxis_title="비율 (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

with col8:
    st.markdown('<div class="section-header">8. 핵심 인사이트</div>', unsafe_allow_html=True)

    insights_text = """
    **주요 발견사항:**

    • **계절성 트렌드**: 가을철(35%) 언급량이 가장 높음 - 제철 특성 반영

    • **연령대 특성**: 40대(30%)가 가장 높은 관심도를 보임

    • **감성 분석**: 긍정적 언급이 65%로 압도적으로 높음

    • **토픽 분포**: 건강/영양(35%) > 요리/레시피(28%) 순으로 관심 집중

    • **용도별 활용**: 요리 용도(60%)가 건강 효능(40%)보다 높음
    """

    st.markdown('<div class="insight-box">' + insights_text + '</div>', unsafe_allow_html=True)

# Row 4: Future Trends
st.markdown('<div class="section-header">9. 표고버섯 소셜 트렌드 전망</div>', unsafe_allow_html=True)

forecast_text = """
**2024년 표고버섯 소셜 트렌드 전망:**

🔮 **예상 트렌드**
- **건강 관심 증가**: 면역력 강화에 대한 관심으로 지속적인 언급량 증가 예상
- **요리 콘텐츠 확산**: 소셜미디어 요리 콘텐츠와 함께 표고버섯 활용법 다양화
- **프리미엄화**: 품질 좋은 표고버섯에 대한 소비자 관심 증가

📈 **성장 동력**
- 건강식품으로서의 인식 확산
- 다양한 요리법 개발 및 공유
- 온라인 쇼핑몰을 통한 접근성 향상

⚠️ **주의사항**
- 가격 변동성에 따른 소비자 반응 모니터링 필요
- 품질 관리 및 신뢰성 확보 중요
"""

st.markdown('<div class="insight-box">' + forecast_text + '</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**데이터 분석 기간**: 2019-2023년 | **분석 대상**: 소셜미디어 언급 데이터")
