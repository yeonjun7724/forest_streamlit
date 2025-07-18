import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="🍄 표고버섯 소셜 빅데이터 분석 대시보드",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

    * {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 40px rgba(139, 69, 19, 0.15);
    }

    .main-header h1 {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .main-header p {
        font-size: 1.2rem;
        font-weight: 500;
        opacity: 0.95;
    }

    .metric-card {
        background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(139, 69, 19, 0.2);
        margin-bottom: 1rem;
    }

    .metric-number {
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 500;
    }

    .insight-card {
        background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #FF8C00;
        box-shadow: 0 8px 32px rgba(139, 69, 19, 0.2);
    }

    .wordcloud-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(139, 69, 19, 0.15);
        margin-bottom: 2rem;
        text-align: center;
    }

    .word-large {
        font-size: 2.5rem;
        font-weight: 900;
        color: #8B4513;
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem;
        display: inline-block;
    }

    .word-medium {
        font-size: 1.8rem;
        font-weight: 700;
        color: #D2691E;
        margin: 0.3rem;
        display: inline-block;
    }

    .word-small {
        font-size: 1.3rem;
        font-weight: 600;
        color: #CD853F;
        margin: 0.2rem;
        display: inline-block;
    }

    .stPlotlyChart {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(139, 69, 19, 0.15);
        padding: 1rem;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #8B4513;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #CD853F;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🍄 표고버섯 소셜 빅데이터 분석</h1>
    <p><strong>2019-2023년 | 총 언급량: 222,000회 | 67% 증가 추세</strong></p>
</div>
""", unsafe_allow_html=True)

# Data preparation
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

# Usage data for cooking and health
usage_cooking = pd.DataFrame({
    'Usage': ['국물/육수', '볶음', '채소대체', '샐러드'],
    'Percentage': [27, 25, 18, 8],
    'Category': ['요리'] * 4
})

usage_health = pd.DataFrame({
    'Usage': ['면역강화', '콜레스테롤', '비타민D', '체중관리'],
    'Percentage': [38, 22, 18, 12],
    'Category': ['건강'] * 4
})

usage_data = pd.concat([usage_cooking, usage_health], ignore_index=True)

# Color palette
SHIITAKE_COLORS = ['#8B4513', '#D2691E', '#CD853F', '#DEB887', '#228B22', '#FF8C00', '#DC143C', '#4682B4']

# Row 1: Keywords, Yearly Trend, Seasonal Distribution
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="section-title">🔍 주요 키워드</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="wordcloud-container">
        <div class="word-large">표고버섯</div><br>
        <div class="word-medium">면역력</div>
        <div class="word-medium">볶음</div>
        <div class="word-medium">육수</div><br>
        <div class="word-small">비타민D</div>
        <div class="word-small">채식</div>
        <div class="word-small">콜레스테롤</div><br>
        <div class="word-small">재배</div>
        <div class="word-small">베타글루칸</div>
        <div class="word-small">표고전</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-title">📈 연도별 언급량 추이</div>', unsafe_allow_html=True)
    fig_yearly = px.bar(yearly_data, x='Year', y='Mentions', 
                       color='Year', color_discrete_sequence=SHIITAKE_COLORS[:5])
    fig_yearly.update_layout(
        showlegend=False,
        height=280,  # 350 -> 280으로 축소
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Noto Sans KR", size=11),  # 폰트 크기 축소
        yaxis_title="언급량 (회)",
        xaxis_title="연도",
        margin=dict(t=20, b=40, l=40, r=20)  # 여백 조정
    )
    fig_yearly.update_traces(
        hovertemplate='<b>%{x}년</b><br>언급량: %{y:,}회<extra></extra>',
        texttemplate='%{y:,.0f}',
        textposition='outside'
    )
    st.plotly_chart(fig_yearly, use_container_width=True)

with col3:
    st.markdown('<div class="section-title">📅 계절별 언급 분포</div>', unsafe_allow_html=True)
    fig_seasonal = px.pie(seasonal_data, values='Percentage', names='Season',
                         color_discrete_sequence=SHIITAKE_COLORS[:4])
    fig_seasonal.update_layout(
        height=280,  # 350 -> 280으로 축소
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Noto Sans KR", size=11),  # 폰트 크기 축소
        margin=dict(t=20, b=20, l=20, r=20)  # 여백 조정
    )
    fig_seasonal.update_traces(
        hovertemplate='<b>%{label}</b><br>비율: %{percent}<extra></extra>',
        textinfo='label+percent',
        textfont_size=11  # 텍스트 크기 축소
    )
    st.plotly_chart(fig_seasonal, use_container_width=True)

# Row 2: Sentiment Analysis, Topic Modeling, Age Groups
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="section-title">😊 감성 분석</div>', unsafe_allow_html=True)
    fig_sentiment = px.bar(sentiment_data, x='Percentage', y='Sentiment', 
                          orientation='h', color='Sentiment',
                          color_discrete_map={'긍정': '#228B22', '중립': '#CD853F', '부정': '#DC143C'})
    fig_sentiment.update_layout(
        showlegend=False,
        height=240,  # 300 -> 240으로 축소
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Noto Sans KR", size=11),  # 폰트 크기 축소
        xaxis_title="비율 (%)",
        yaxis_title="",
        margin=dict(t=20, b=40, l=60, r=20)  # 여백 조정
    )
    fig_sentiment.update_traces(
        hovertemplate='<b>%{y}</b><br>비율: %{x}%<br>언급량: %{customdata:,}회<extra></extra>',
        customdata=sentiment_data['Count'],
        texttemplate='%{x}%',
        textposition='inside'
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)

    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">76%</div>
        <div class="metric-label">긍정 (169,100회)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-title">📊 토픽 모델링</div>', unsafe_allow_html=True)
    fig_topic = px.bar(topic_data, x='Topic', y='Percentage',
                      color='Topic', color_discrete_sequence=SHIITAKE_COLORS[:4])
    fig_topic.update_layout(
        showlegend=False,
        height=280,  # 350 -> 280으로 축소
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Noto Sans KR", size=11),  # 폰트 크기 축소
        yaxis_title="비율 (%)",
        xaxis_title="토픽",
        margin=dict(t=20, b=50, l=40, r=20)  # 여백 조정
    )
    fig_topic.update_traces(
        hovertemplate='<b>%{x}</b><br>비율: %{y}%<extra></extra>',
        texttemplate='%{y}%',
        textposition='outside'
    )
    fig_topic.update_xaxes(tickangle=45)
    st.plotly_chart(fig_topic, use_container_width=True)

with col3:
    st.markdown('<div class="section-title">👥 연령대별 관심도</div>', unsafe_allow_html=True)
    fig_age = px.bar(age_data, x='Age_Group', y='Percentage',
                    color='Age_Group', color_discrete_sequence=SHIITAKE_COLORS[:3])
    fig_age.update_layout(
        showlegend=False,
        height=240,  # 300 -> 240으로 축소
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Noto Sans KR", size=11),  # 폰트 크기 축소
        yaxis_title="비율 (%)",
        xaxis_title="연령대",
        margin=dict(t=20, b=40, l=40, r=20)  # 여백 조정
    )
    fig_age.update_traces(
        hovertemplate='<b>%{x}</b><br>비율: %{y}%<br>언급량: %{customdata:,}회<extra></extra>',
        customdata=age_data['Count'],
        texttemplate='%{y}%',
        textposition='outside'
    )
    st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("""
    <div class="insight-card">
        <h4 style="font-size: 1.1rem; font-weight: bold; margin-bottom: 1rem;">📋 연령대별 특징</h4>
        <p style="margin-bottom: 0.5rem;"><strong>🔥 20~30대</strong><br>채식/비건 45%, 다이어트 33%</p>
        <p style="margin-bottom: 0.5rem;"><strong>💪 40~50대</strong><br>면역/건강 48%, 전통요리 32%</p>
        <p><strong>🌿 60대+</strong><br>건강식품 52%, 웰빙 38%</p>
    </div>
    """, unsafe_allow_html=True)

# Row 3: Usage Analysis & Key Insights
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="section-title">🍳 용도별 활용 분석</div>', unsafe_allow_html=True)

    # Create grouped bar chart
    fig_usage = go.Figure()

    cooking_data = usage_data[usage_data['Category'] == '요리']
    health_data = usage_data[usage_data['Category'] == '건강']

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
        height=320,  # 400 -> 320으로 축소
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Noto Sans KR", size=11),  # 폰트 크기 축소
        yaxis_title="비율 (%)",
        xaxis_title="용도",
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=50, l=40, r=20)  # 여백 조정
    )
    fig_usage.update_xaxes(tickangle=45)
    st.plotly_chart(fig_usage, use_container_width=True)

with col2:
    st.markdown('<div class="section-title">💡 핵심 인사이트</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-card" style="background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">📈</span>
            <div>
                <div class="metric-number" style="font-size: 1.5rem;">성장률: 67%</div>
                <div class="metric-label">5년간 언급량 증가</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-card" style="background: linear-gradient(135deg, #228B22 0%, #32CD32 100%);">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">😊</span>
            <div>
                <div class="metric-number" style="font-size: 1.5rem;">긍정도: 76%</div>
                <div class="metric-label">맛과 건강의 이중효과</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-card" style="background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">🍳</span>
            <div>
                <div class="metric-number" style="font-size: 1.5rem;">요리용도: 38%</div>
                <div class="metric-label">vs 건강효능 32%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-card" style="background: linear-gradient(135deg, #FF8C00 0%, #FFA500 100%);">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">👑</span>
            <div>
                <div class="metric-number" style="font-size: 1.5rem;">핵심층: 42%</div>
                <div class="metric-label">40~50대 관심도 최고</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Trend Forecast & Strategy
st.markdown('<div class="section-title" style="font-size: 2rem; margin-top: 3rem;">🔮 표고버섯 소셜 트렌드 전망 & 마케팅 전략</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="insight-card">
        <h4 style="font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">🚀 성장 동력</h4>
        <ul style="list-style: none; padding: 0;">
            <li style="margin-bottom: 1rem;"><strong>건강식품 관심 증가</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">면역력 강화 트렌드</span></li>
            <li style="margin-bottom: 1rem;"><strong>채식/비건 확산</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">MZ세대 주도</span></li>
            <li><strong>스마트팜 연계</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">생산량 증가</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-card">
        <h4 style="font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">🎯 타겟별 마케팅</h4>
        <ul style="list-style: none; padding: 0;">
            <li style="margin-bottom: 1rem;"><strong>40~50대</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">면역·콜레스테롤 중심</span></li>
            <li style="margin-bottom: 1rem;"><strong>20~30대</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">비건·레시피 콘텐츠</span></li>
            <li><strong>60대+</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">전통요리·건강식품</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="insight-card">
        <h4 style="font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">📱 콘텐츠 전략</h4>
        <ul style="list-style: none; padding: 0;">
            <li style="margin-bottom: 1rem;"><strong>균형 배치</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">요리 38% vs 건강 32%</span></li>
            <li style="margin-bottom: 1rem;"><strong>계절 맞춤</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">봄=레시피, 겨울=면역</span></li>
            <li><strong>긍정 브랜딩</strong><br><span style="font-size: 0.9rem; opacity: 0.9;">76% 긍정 감성 활용</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p style="margin-bottom: 0.5rem;"><strong>📊 데이터 출처</strong>: 네이버·인스타그램·유튜브 | 
    <strong>📅 분석 기간</strong>: 2019–2023년 | 
    <strong>🔬 분석 기법</strong>: 텍스트 마이닝·감성분석·토픽모델링</p>
    <p style="font-size: 1.1rem;">🍄 <em>Made with ❤️ by Premium Data Analytics Team</em></p>
</div>
""", unsafe_allow_html=True)
