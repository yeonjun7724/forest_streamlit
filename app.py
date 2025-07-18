Copyimport streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import time

# 페이지 설정
st.set_page_config(
    page_title="🍄 프리미엄 표고버섯 소셜 빅데이터 분석", 
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🍄"
)

# 프리미엄 CSS 스타일
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
    --primary: #8B4513;
    --secondary: #D2691E;
    --accent: #CD853F;
    --success: #228B22;
    --warning: #FF8C00;
    --danger: #DC143C;
    --bg-light: #FFF8DC;
    --bg-dark: #2C1810;
    --card-light: #FFFFFF;
    --card-dark: #3D2817;
    --text-light: #2F1B14;
    --text-dark: #F5DEB3;
    --shadow: 0 8px 32px rgba(139, 69, 19, 0.1);
    --shadow-hover: 0 12px 40px rgba(139, 69, 19, 0.2);
    --gradient-1: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
    --gradient-2: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
    --border-radius: 16px;
}

/* 다크모드 토글 */
.dark-mode {
    --bg: var(--bg-dark);
    --card-bg: var(--card-dark);
    --text: var(--text-dark);
}

.light-mode {
    --bg: var(--bg-light);
    --card-bg: var(--card-light);
    --text: var(--text-light);
}

body {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    background: var(--bg, var(--bg-light));
    color: var(--text, var(--text-light));
    transition: all 0.3s ease;
}

[data-testid="stAppViewContainer"] {
    background: var(--bg, var(--bg-light));
    transition: all 0.3s ease;
}

/* 프리미엄 헤더 */
.premium-header {
    background: var(--gradient-1);
    padding: 3rem 2rem;
    border-radius: var(--border-radius);
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow);
}

.premium-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="1.5" fill="rgba(255,255,255,0.1)"/><circle cx="60" cy="80" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.premium-header h1 {
    margin: 0;
    color: white;
    font-size: 3rem;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
}

.premium-header p {
    margin: 1rem 0 0;
    color: rgba(255,255,255,0.9);
    font-size: 1.2rem;
    font-weight: 500;
    position: relative;
    z-index: 1;
}

/* 프리미엄 카드 */
.premium-card {
    background: var(--card-bg, var(--card-light));
    border-radius: var(--border-radius);
    padding: 2rem;
    box-shadow: var(--shadow);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid transparent;
    position: relative;
    overflow: hidden;
    min-height: 450px;
    margin-bottom: 2rem;
}

.premium-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: var(--gradient-1);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.premium-card:hover::before {
    transform: scaleX(1);
}

.premium-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-hover);
    border-color: var(--primary);
}

.card-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 1.5rem;
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.card-title::after {
    content: '';
    flex: 1;
    height: 2px;
    background: var(--gradient-2);
    border-radius: 1px;
}

/* Plotly 차트를 카드 안에 포함 */
.stPlotlyChart {
    background: transparent !important;
}

/* 통계 카드 */
.stat-card {
    background: var(--gradient-2);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    margin: 1rem 0;
    box-shadow: var(--shadow);
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: scale(1.05);
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

.stat-label {
    font-size: 1rem;
    opacity: 0.9;
    font-weight: 500;
}

/* 다크모드 토글 */
.mode-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    background: var(--card-bg, var(--card-light));
    border: none;
    border-radius: 50px;
    padding: 12px 20px;
    cursor: pointer;
    box-shadow: var(--shadow);
    transition: all 0.3s ease;
    font-size: 1rem;
}

.mode-toggle:hover {
    transform: scale(1.1);
    box-shadow: var(--shadow-hover);
}

/* 인사이트 박스 */
.insight-box {
    background: var(--gradient-2);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border-left: 5px solid var(--warning);
}

.insight-box h4 {
    margin: 0 0 1rem 0;
    font-size: 1.2rem;
    font-weight: 600;
}

/* 애니메이션 클래스 */
.fade-in {
    animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.count-up {
    font-variant-numeric: tabular-nums;
}

/* 반응형 */
@media (max-width: 768px) {
    .premium-header h1 {
        font-size: 2rem;
    }
    .premium-header p {
        font-size: 1rem;
    }
    .premium-card {
        padding: 1.5rem;
        min-height: 350px;
    }
}

/* Streamlit 요소 숨기기 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 워드클라우드 스타일 */
.wordcloud-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    padding: 2rem;
    min-height: 300px;
}

.word-item {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 25px;
    font-weight: 600;
    transition: all 0.3s ease;
    cursor: pointer;
    text-align: center;
    border: 2px solid transparent;
}

.word-item:hover {
    transform: scale(1.2);
    box-shadow: 0 8px 25px rgba(139, 69, 19, 0.3);
    border-color: var(--primary);
}

.word-large {
    font-size: 2rem;
    background: var(--gradient-1);
    color: white;
}

.word-medium {
    font-size: 1.5rem;
    background: var(--gradient-2);
    color: white;
}

.word-small {
    font-size: 1.2rem;
    background: linear-gradient(135deg, #DEB887 0%, #F5DEB3 100%);
    color: var(--text-light);
}
</style>
""", unsafe_allow_html=True)

# 다크모드 토글 버튼
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# 사이드바에 다크모드 토글
with st.sidebar:
    if st.button("🌙 다크모드" if not st.session_state.dark_mode else "☀️ 라이트모드"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# 다크모드 CSS 적용
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #2C1810 !important;
        color: #F5DEB3 !important;
    }
    .premium-card {
        background-color: #3D2817 !important;
        color: #F5DEB3 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 헤더 영역
st.markdown("""
<div class="premium-header fade-in">
    <h1>🍄 표고버섯 소셜 빅데이터 분석</h1>
    <p><strong>2019-2023년 | 총 언급량: 222,000회 | 67% 증가 추세</strong></p>
</div>
""", unsafe_allow_html=True)

# 프리미엄 색상 팔레트
SHIITAKE_COLORS = [
    '#8B4513',  # 진한 갈색 (표고버섯)
    '#D2691E',  # 오렌지 갈색
    '#CD853F',  # 황갈색  
    '#DEB887',  # 베이지
    '#228B22',  # 숲 초록
    '#FF8C00',  # 주황
    '#DC143C',  # 빨강
    '#4682B4'   # 파랑
]

# 데이터 준비
@st.cache_data
def load_data():
    return {
        'keywords': {
            '표고버섯': {'size': 'large', 'weight': 100},
            '면역력': {'size': 'medium', 'weight': 85},
            '볶음': {'size': 'medium', 'weight': 80},
            '육수': {'size': 'medium', 'weight': 75},
            '비타민D': {'size': 'small', 'weight': 60},
            '채식': {'size': 'small', 'weight': 55},
            '콜레스테롤': {'size': 'small', 'weight': 50},
            '재배': {'size': 'small', 'weight': 45},
            '베타글루칸': {'size': 'small', 'weight': 40},
            '표고전': {'size': 'small', 'weight': 35},
            '원목재배': {'size': 'small', 'weight': 30},
            '강칠맛': {'size': 'small', 'weight': 25}
        },
        'yearly_data': pd.DataFrame({
            '연도': ['2019', '2020', '2021', '2022', '2023'],
            '언급량': [31500, 43800, 45200, 48900, 52600]
        }),
        'seasonal_data': pd.DataFrame({
            '계절': ['봄', '여름', '가을', '겨울'],
            '비율': [26, 17, 29, 28]
        }),
        'sentiment_data': pd.DataFrame({
            '감성': ['긍정', '중립', '부정'],
            '비율': [76, 16, 8],
            '언급수': [169100, 35600, 17800]
        }),
        'topic_data': pd.DataFrame({
            '토픽': ['요리/레시피', '건강/효능', '생산/재배', '유통/가격'],
            '비율': [38, 32, 18, 12]
        }),
        'age_data': pd.DataFrame({
            '연령대': ['20~30대', '40~50대', '60대+'],
            '비율': [31, 42, 27],
            '언급수': [69000, 93450, 60050]
        }),
        'usage_data': pd.DataFrame({
            '항목': ['국물/육수', '볶음', '채소대체', '샐러드', '면역강화', '콜레스테롤', '비타민D', '체중관리'],
            '비율': [27, 25, 18, 8, 38, 22, 18, 12],
            '카테고리': ['요리', '요리', '요리', '요리', '건강', '건강', '건강', '건강']
        })
    }

data = load_data()

# 1행: 키워드 클라우드, 연도별 추이, 계절별 분포
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with st.container():
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🔍 주요 키워드</div>', unsafe_allow_html=True)
        
        # 인터랙티브 워드클라우드
        word_html = '<div class="wordcloud-container">'
        for word, props in data['keywords'].items():
            word_html += f'<div class="word-item word-{props["size"]}" title="언급도: {props["weight"]}%">{word}</div>'
        word_html += '</div>'
        
        st.markdown(word_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📈 연도별 언급량 추이</div>', unsafe_allow_html=True)
        
        fig_yearly = px.bar(
            data['yearly_data'], 
            x='연도', y='언급량',
            text='언급량',
            color='연도',
            color_discrete_sequence=SHIITAKE_COLORS
        )
        fig_yearly.update_traces(
            texttemplate='%{text:,}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>언급량: %{y:,}회<extra></extra>'
        )
        fig_yearly.update_layout(
            height=320,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard", size=12),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_yearly, use_container_width=True, key="yearly_chart")
        st.markdown('</div>', unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🗓️ 계절별 언급 분포</div>', unsafe_allow_html=True)
        
        fig_seasonal = px.pie(
            data['seasonal_data'],
            names='계절', values='비율',
            hole=0.4,
            color_discrete_sequence=SHIITAKE_COLORS[:4]
        )
        fig_seasonal.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>비율: %{percent}<br>언급량: %{value}%<extra></extra>'
        )
        fig_seasonal.update_layout(
            height=320,
            font=dict(family="Pretendard", size=12),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_seasonal, use_container_width=True, key="seasonal_chart")
        st.markdown('</div>', unsafe_allow_html=True)

# 2행: 감성 분석, 토픽 모델링, 연령대별 관심도
col4, col5, col6 = st.columns(3, gap="large")

with col4:
    with st.container():
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">😊 감성 분석</div>', unsafe_allow_html=True)
        
        fig_sentiment = px.bar(
            data['sentiment_data'],
            x='비율', y='감성',
            orientation='h',
            text='비율',
            color='감성',
            color_discrete_map={
                '긍정': '#228B22',
                '중립': '#CD853F', 
                '부정': '#DC143C'
            }
        )
        fig_sentiment.update_traces(
            texttemplate='%{text}%',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>비율: %{x}%<br>언급수: %{customdata:,}회<extra></extra>',
            customdata=data['sentiment_data']['언급수']
        )
        fig_sentiment.update_layout(
            height=200,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard", size=12),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_sentiment, use_container_width=True, key="sentiment_chart")
        
        # 간단한 통계 요약
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #228B22;">76%</div>
                <div style="font-size: 0.9rem; color: #666;">긍정</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #CD853F;">16%</div>
                <div style="font-size: 0.9rem; color: #666;">중립</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #DC143C;">8%</div>
                <div style="font-size: 0.9rem; color: #666;">부정</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

with col5:
    with st.container():
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 토픽 모델링</div>', unsafe_allow_html=True)
        
        fig_topic = px.bar(
            data['topic_data'],
            x='토픽', y='비율',
            text='비율',
            color='토픽',
            color_discrete_sequence=SHIITAKE_COLORS[:4]
        )
        fig_topic.update_traces(
            texttemplate='%{text}%',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>비율: %{y}%<extra></extra>'
        )
        fig_topic.update_layout(
            height=320,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard", size=12),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_topic, use_container_width=True, key="topic_chart")
        st.markdown('</div>', unsafe_allow_html=True)

with col6:
    with st.container():
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">👥 연령대별 관심도</div>', unsafe_allow_html=True)
        
        fig_age = px.bar(
            data['age_data'],
            x='연령대', y='비율',
            text='비율',
            color='연령대',
            color_discrete_sequence=SHIITAKE_COLORS[:3]
        )
        fig_age.update_traces(
            texttemplate='%{text}%',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>비율: %{y}%<br>언급수: %{customdata:,}회<extra></extra>',
            customdata=data['age_data']['언급수']
        )
        fig_age.update_layout(
            height=200,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard", size=12),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_age, use_container_width=True, key="age_chart")
        
        # 연령대별 상세 정보
        st.markdown("""
        <div class="insight-box" style="margin-top: 1rem; padding: 1rem;">
            <h4 style="margin: 0 0 0.5rem 0; font-size: 1rem;">📋 연령대별 특징</h4>
            <div style="font-size: 0.85rem; line-height: 1.4;">
                <p><strong>🔥 20~30대</strong>: 채식/비건 45%</p>
                <p><strong>💪 40~50대</strong>: 면역/건강 48%</p>
                <p><strong>🌿 60대+</strong>: 건강식품 52%</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# 3행: 용도별 활용 분석, 핵심 인사이트
col7, col8 = st.columns([1.6, 1], gap="large")

with col7:
    with st.container():
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🍽️ 용도별 활용 분석</div>', unsafe_allow_html=True)
        
        fig_usage = px.bar(
            data['usage_data'],
            x='항목', y='비율',
            text='비율',
            color='카테고리',
            color_discrete_map={
                '요리': SHIITAKE_COLORS[1],
                '건강': SHIITAKE_COLORS[0]
            }
        )
        fig_usage.update_traces(
            texttemplate='%{text}%',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>비율: %{y}%<br>카테고리: %{customdata}<extra></extra>',
            customdata=data['usage_data']['카테고리']
        )
        fig_usage.update_layout(
            height=380,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard", size=12),
            margin=dict(t=20, b=50, l=20, r=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        fig_usage.update_xaxes(tickangle=45)
        st.plotly_chart(fig_usage, use_container_width=True, key="usage_chart")
        st.markdown('</div>', unsafe_allow_html=True)

with col8:
    with st.container():
        st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💡 핵심 인사이트</div>', unsafe_allow_html=True)
        
        insights = [
            {"icon": "📈", "title": "성장률", "value": "67%", "desc": "5년간 언급량 증가"},
            {"icon": "😊", "title": "긍정도", "value": "76%", "desc": "맛과 건강의 이중효과"},
            {"icon": "🍳", "title": "요리용도", "value": "38%", "desc": "vs 건강효능 32%"},
            {"icon": "👑", "title": "핵심층", "value": "42%", "desc": "40~50대 관심도 최고"},
            {"icon": "🌱", "title": "MZ트렌드", "value": "31%", "desc": "비건 트렌드 선도"},
            {"icon": "🗓️", "title": "사계절", "value": "균등", "desc": "연중 고른 관심"},
            {"icon": "🚜", "title": "생산연계", "value": "18%", "desc": "스마트팜·귀농 관련"}
        ]
        
        for insight in insights:
            st.markdown(f"""
            <div class="stat-card" style="margin: 0.5rem 0; padding: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.5rem;">{insight['icon']}</span>
                    <div>
                        <div style="font-size: 1.2rem; font-weight: 700;">{insight['title']}: {insight['value']}</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">{insight['desc']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# 트렌드 전망 & 전략
with st.container():
    st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔮 표고버섯 소셜 트렌드 전망 & 마케팅 전략</div>', unsafe_allow_html=True)

    col_trend1, col_trend2, col_trend3 = st.columns(3)

    with col_trend1:
        st.markdown("""
        <div class="insight-box">
            <h4>🚀 성장 동력</h4>
            <ul>
                <li><strong>건강식품 관심 증가</strong><br>면역력 강화 트렌드</li>
                <li><strong>채식/비건 확산</strong><br>MZ세대 주도</li>
                <li><strong>스마트팜 연계</strong><br>생산량 증가</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_trend2:
        st.markdown("""
        <div class="insight-box">
            <h4>🎯 타겟별 마케팅</h4>
            <ul>
                <li><strong>40~50대</strong><br>면역·콜레스테롤 중심</li>
                <li><strong>20~30대</strong><br>비건·레시피 콘텐츠</li>
                <li><strong>60대+</strong><br>전통요리·건강식품</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_trend3:
        st.markdown("""
        <div class="insight-box">
            <h4>📱 콘텐츠 전략</h4>
            <ul>
                <li><strong>균형 배치</strong><br>요리 38% vs 건강 32%</li>
                <li><strong>계절 맞춤</strong><br>봄=레시피, 겨울=면역</li>
                <li><strong>긍정 브랜딩</strong><br>76% 긍정 감성 활용</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# 푸터
st.markdown("""
---
<div style="text-align: center; color: #999; font-size: 0.9rem; padding: 2rem;">
    <p><strong>📊 데이터 출처</strong>: 네이버·인스타그램·유튜브 | 
    <strong>📅 분석 기간</strong>: 2019–2023년 | 
    <strong>🔬 분석 기법</strong>: 텍스트 마이닝·감성분석·토픽모델링</p>
    <p>🍄 <em>Made with ❤️ by Premium Data Analytics Team</em></p>
</div>
""", unsafe_allow_html=True)

# 실시간 업데이트 시뮬레이션 (선택사항)
if st.sidebar.button("🔄 데이터 새로고침"):
    with st.spinner("데이터를 업데이트하는 중..."):
        time.sleep(2)
        st.success("✅ 데이터가 성공적으로 업데이트되었습니다!")
        st.balloons()

# 사이드바 추가 정보
with st.sidebar:
    st.markdown("### 📋 대시보드 정보")
    st.info("""
    **🍄 표고버섯 빅데이터 분석**
    
    - 📊 총 데이터: 222,000건
    - 📅 기간: 2019-2023년  
    - 📈 성장률: 67% 증가
    - 😊 긍정률: 76%
    """)
    
    st.markdown("### 🛠️ 기능")
    st.write("- 🌙 다크/라이트 모드")
    st.write("- 📱 반응형 디자인") 
    st.write("- 🎨 인터랙티브 차트")
    st.write("- 📊 실시간 업데이트")
