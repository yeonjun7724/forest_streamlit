import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="🍄 표고버섯 소셜 빅데이터 분석",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS 스타일링 - 카드 효과 강화
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }

    .stApp {
        background: linear-gradient(135deg, #FFF8DC 0%, #F5DEB3 100%);
    }

    /* 카드 스타일 강화 */
    .element-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(139, 69, 19, 0.15);
        border: 1px solid rgba(139, 69, 19, 0.1);
    }

    .stColumn > div {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 8px 32px rgba(139, 69, 19, 0.15);
        border: 1px solid rgba(139, 69, 19, 0.1);
        height: fit-content;
    }

    /* 컨테이너 카드 스타일 */
    .card-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(139, 69, 19, 0.15);
        border: 1px solid rgba(139, 69, 19, 0.1);
    }

    .premium-header {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(139, 69, 19, 0.3);
    }

    .metric-card {
        background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(139, 69, 19, 0.2);
        margin: 0.5rem 0;
    }

    .insight-card {
        background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        border-left: 5px solid #FF8C00;
    }

    .keyword-cloud {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.8rem;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(139, 69, 19, 0.1);
        margin: 1rem 0;
    }

    .keyword-large {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        font-size: 1.8rem;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
    }

    .keyword-medium {
        background: linear-gradient(135deg, #D2691E 0%, #CD853F 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        font-size: 1.4rem;
        font-weight: 600;
        box-shadow: 0 3px 10px rgba(139, 69, 19, 0.25);
    }

    .keyword-small {
        background: linear-gradient(135deg, #DEB887 0%, #F5DEB3 100%);
        color: #2F1B14;
        padding: 8px 16px;
        border-radius: 18px;
        font-size: 1.1rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(139, 69, 19, 0.2);
    }

    /* Streamlit 기본 요소 스타일링 */
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.1);
    }

    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #DEB887;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.1);
    }

    /* 플롯 컨테이너 스타일링 */
    .js-plotly-plot {
        border-radius: 10px;
    }

    /* 서브헤더 스타일링 */
    .stSubheader {
        color: #8B4513;
        font-weight: 700;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="premium-header">
    <h1 style="font-size: 3.5rem; margin-bottom: 1rem; font-weight: 900;">🍄 표고버섯 소셜 빅데이터 분석</h1>
    <p style="font-size: 1.3rem; font-weight: 600;"><strong>2019-2023년 | 총 언급량: 222,000회 | 67% 증가 추세</strong></p>
</div>
""", unsafe_allow_html=True)

# 데이터 준비
yearly_data = pd.DataFrame({
    'Year': ['2019', '2020', '2021', '2022', '2023'],
    'Mentions': [31500, 43800, 45200, 48900, 52600]
})

seasonal_data = pd.DataFrame({
    'Season': ['봄', '여름', '가을', '겨울'],
    'Percentage': [26, 17, 29, 28]
})

sentiment_data = pd.DataFrame({
    'Sentiment': ['긍정', '중립', '부정'],
    'Percentage': [76, 16, 8],
    'Count': [169100, 35600, 17800]
})

topic_data = pd.DataFrame({
    'Topic': ['요리/레시피', '건강/효능', '생산/재배', '유통/가격'],
    'Percentage': [38, 32, 18, 12]
})

age_data = pd.DataFrame({
    'Age_Group': ['20~30대', '40~50대', '60대+'],
    'Percentage': [31, 42, 27],
    'Count': [69000, 93450, 60050]
})

usage_data = pd.DataFrame({
    'Usage': ['국물/육수', '볶음', '채소대체', '샐러드', '면역강화', '콜레스테롤', '비타민D', '체중관리'],
    'Percentage': [27, 25, 18, 8, 38, 22, 18, 12],
    'Category': ['요리', '요리', '요리', '요리', '건강', '건강', '건강', '건강']
})

# 색상 팔레트
SHIITAKE_COLORS = ['#8B4513', '#D2691E', '#CD853F', '#DEB887', '#228B22', '#FF8C00', '#DC143C', '#4682B4']

# Row 1: 키워드 클라우드, 연도별 추이, 계절별 분포
col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("🔍 주요 키워드")
        st.markdown("""
        <div class="keyword-cloud">
            <div class="keyword-large">표고버섯</div>
            <div class="keyword-medium">면역력</div>
            <div class="keyword-medium">볶음</div>
            <div class="keyword-medium">육수</div>
            <div class="keyword-small">비타민D</div>
            <div class="keyword-small">채식</div>
            <div class="keyword-small">콜레스테롤</div>
            <div class="keyword-small">재배</div>
            <div class="keyword-small">베타글루칸</div>
            <div class="keyword-small">표고전</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("📈 연도별 언급량 추이")
        fig_yearly = px.bar(
            yearly_data, 
            x='Year', 
            y='Mentions',
            color='Year',
            color_discrete_sequence=SHIITAKE_COLORS[:5],
            title=""
        )
        fig_yearly.update_layout(
            height=225,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial", size=12),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_yearly.update_traces(
            hovertemplate='<b>%{x}년</b><br>언급량: %{y:,}회<extra></extra>'
        )
        st.plotly_chart(fig_yearly, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("📅 계절별 언급 분포")
        fig_seasonal = px.pie(
            seasonal_data, 
            values='Percentage', 
            names='Season',
            color_discrete_sequence=SHIITAKE_COLORS[:4],
            title=""
        )
        fig_seasonal.update_layout(
            height=225,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial", size=12),
            margin=dict(l=20, r=20, t=20, b=40)
        )
        fig_seasonal.update_traces(
            hovertemplate='<b>%{label}</b><br>비율: %{percent}<extra></extra>'
        )
        st.plotly_chart(fig_seasonal, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Row 2: 감성 분석, 토픽 모델링, 연령대별 관심도
col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("😊 감성 분석")
        fig_sentiment = px.bar(
            sentiment_data, 
            x='Percentage', 
            y='Sentiment',
            orientation='h',
            color='Sentiment',
            color_discrete_map={'긍정': '#228B22', '중립': '#CD853F', '부정': '#DC143C'},
            title=""
        )
        fig_sentiment.update_layout(
            height=225,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial", size=12),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_sentiment.update_traces(
            hovertemplate='<b>%{y}</b><br>비율: %{x}%<br>언급수: %{customdata:,}회<extra></extra>',
            customdata=sentiment_data['Count']
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)

        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; font-size: 1.8rem;">76%</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem;">긍정 (169,100회)</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("📊 토픽 모델링")
        fig_topic = px.bar(
            topic_data, 
            x='Topic', 
            y='Percentage',
            color='Topic',
            color_discrete_sequence=SHIITAKE_COLORS[:4],
            title=""
        )
        fig_topic.update_layout(
            height=225,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial", size=12),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_topic.update_traces(
            hovertemplate='<b>%{x}</b><br>비율: %{y}%<extra></extra>'
        )
        fig_topic.update_xaxes(tickangle=45)
        st.plotly_chart(fig_topic, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("👥 연령대별 관심도")
        fig_age = px.bar(
            age_data, 
            x='Age_Group', 
            y='Percentage',
            color='Age_Group',
            color_discrete_sequence=SHIITAKE_COLORS[:3],
            title=""
        )
        fig_age.update_layout(
            height=225,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial", size=12),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_age.update_traces(
            hovertemplate='<b>%{x}</b><br>비율: %{y}%<br>언급수: %{customdata:,}회<extra></extra>',
            customdata=age_data['Count']
        )
        st.plotly_chart(fig_age, use_container_width=True)

        st.markdown("""
        <div class="insight-card">
            <h4 style="margin-bottom: 1rem; font-size: 1.2rem;">📋 연령대별 특징</h4>
            <p style="margin: 0.5rem 0;"><strong>🔥 20~30대</strong><br>채식/비건 45%, 다이어트 33%</p>
            <p style="margin: 0.5rem 0;"><strong>💪 40~50대</strong><br>면역/건강 48%, 전통요리 32%</p>
            <p style="margin: 0.5rem 0;"><strong>🌿 60대+</strong><br>건강식품 52%, 웰빙 38%</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Row 3: 용도별 활용 분석 & 핵심 인사이트
col1, col2 = st.columns([3, 2])

with col1:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("🍳 용도별 활용 분석")

        # 요리와 건강 용도를 분리하여 그룹화된 막대 차트 생성
        cooking_data = usage_data[usage_data['Category'] == '요리']
        health_data = usage_data[usage_data['Category'] == '건강']

        fig_usage = go.Figure()

        fig_usage.add_trace(go.Bar(
            name='요리',
            x=cooking_data['Usage'],
            y=cooking_data['Percentage'],
            marker_color=SHIITAKE_COLORS[1],
            hovertemplate='<b>%{x}</b><br>요리: %{y}%<extra></extra>'
        ))

        fig_usage.add_trace(go.Bar(
            name='건강',
            x=health_data['Usage'],
            y=health_data['Percentage'],
            marker_color=SHIITAKE_COLORS[0],
            hovertemplate='<b>%{x}</b><br>건강: %{y}%<extra></extra>'
        ))

        fig_usage.update_layout(
            height=300,
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig_usage.update_xaxes(tickangle=45)
        st.plotly_chart(fig_usage, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("💡 핵심 인사이트")

        col2_1, col2_2 = st.columns(2)

        with col2_1:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
                <div style="font-size: 1.3rem; font-weight: bold;">성장률: 67%</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">5년간 언급량 증가</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #228B22 0%, #32CD32 100%);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">😊</div>
                <div style="font-size: 1.3rem; font-weight: bold;">긍정도: 76%</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">맛과 건강의 이중효과</div>
            </div>
            """, unsafe_allow_html=True)

        with col2_2:
            st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🍳</div>
                <div style="font-size: 1.3rem; font-weight: bold;">요리용도: 38%</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">vs 건강효능 32%</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #FF8C00 0%, #FFA500 100%);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👑</div>
                <div style="font-size: 1.3rem; font-weight: bold;">핵심층: 42%</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">40~50대 관심도 최고</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 트렌드 전망 & 마케팅 전략
with st.container():
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.subheader("🔮 표고버섯 소셜 트렌드 전망 & 마케팅 전략")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="insight-card">
            <h4 style="margin-bottom: 1rem; font-size: 1.3rem;">🚀 성장 동력</h4>
            <ul style="margin: 0; padding-left: 1.2rem;">
                <li style="margin: 0.5rem 0;"><strong>건강식품 관심 증가</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">면역력 강화 트렌드</span></li>
                <li style="margin: 0.5rem 0;"><strong>채식/비건 확산</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">MZ세대 주도</span></li>
                <li style="margin: 0.5rem 0;"><strong>스마트팜 연계</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">생산량 증가</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="insight-card">
            <h4 style="margin-bottom: 1rem; font-size: 1.3rem;">🎯 타겟별 마케팅</h4>
            <ul style="margin: 0; padding-left: 1.2rem;">
                <li style="margin: 0.5rem 0;"><strong>40~50대</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">면역·콜레스테롤 중심</span></li>
                <li style="margin: 0.5rem 0;"><strong>20~30대</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">비건·레시피 콘텐츠</span></li>
                <li style="margin: 0.5rem 0;"><strong>60대+</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">전통요리·건강식품</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="insight-card">
            <h4 style="margin-bottom: 1rem; font-size: 1.3rem;">📱 콘텐츠 전략</h4>
            <ul style="margin: 0; padding-left: 1.2rem;">
                <li style="margin: 0.5rem 0;"><strong>균형 배치</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">요리 38% vs 건강 32%</span></li>
                <li style="margin: 0.5rem 0;"><strong>계절 맞춤</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">봄=레시피, 겨울=면역</span></li>
                <li style="margin: 0.5rem 0;"><strong>긍정 브랜딩</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">76% 긍정 감성 활용</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p style="margin-bottom: 0.5rem;"><strong>📊 데이터 출처</strong>: 네이버·인스타그램·유튜브 | 
    <strong>📅 분석 기간</strong>: 2019–2023년 | 
    <strong>🔬 분석 기법</strong>: 텍스트 마이닝·감성분석·토픽모델링</p>
    <p style="font-size: 1.1rem; margin: 0;">🍄 <em>Made with ❤️ by Premium Data Analytics Team</em></p>
</div>
""", unsafe_allow_html=True)
