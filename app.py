import streamlit as st
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

# 수정된 프리미엄 CSS 스타일 - 카드 오버플로우 문제 해결
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

body {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    background: var(--bg-light);
    color: var(--text-light);
    transition: all 0.3s ease;
}

[data-testid="stAppViewContainer"] {
    background: var(--bg-light);
    transition: all 0.3s ease;
    padding: 1rem;
}

/* 다크모드 적용 */
.dark-mode [data-testid="stAppViewContainer"] {
    background: var(--bg-dark) !important;
    color: var(--text-dark) !important;
}

.dark-mode .premium-card {
    background: var(--card-dark) !important;
    color: var(--text-dark) !important;
}

/* 프리미엄 헤더 */
.premium-header {
    background: var(--gradient-1);
    padding: 2rem;
    border-radius: var(--border-radius);
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow);
}

.premium-header h1 {
    margin: 0;
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
}

.premium-header p {
    margin: 1rem 0 0;
    color: rgba(255,255,255,0.9);
    font-size: 1.1rem;
    font-weight: 500;
    position: relative;
    z-index: 1;
}

/* 🔧 수정된 프리미엄 카드 - 오버플로우 방지 */
.premium-card {
    background: var(--card-light);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid transparent;
    position: relative;
    overflow: hidden; /* 🔧 오버플로우 숨김 */
    min-height: 450px; /* 🔧 높이 증가 */
    display: flex;
    flex-direction: column;
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
    transform: translateY(-4px);
    box-shadow: var(--shadow-hover);
    border-color: var(--primary);
}

.card-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 1rem;
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-shrink: 0; /* 🔧 제목이 줄어들지 않도록 */
}

.card-title::after {
    content: '';
    flex: 1;
    height: 2px;
    background: var(--gradient-2);
    border-radius: 1px;
}

/* 🔧 카드 콘텐츠 영역 */
.card-content {
    flex: 1;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* 통계 카드 */
.stat-card {
    background: var(--gradient-2);
    color: white;
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
    margin: 0.5rem 0;
    box-shadow: var(--shadow);
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: scale(1.02);
}

.stat-number {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

.stat-label {
    font-size: 0.9rem;
    opacity: 0.9;
    font-weight: 500;
}

/* 🔧 수정된 워드클라우드 컨테이너 */
.wordcloud-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 0.8rem;
    padding: 1rem;
    height: 300px; /* 🔧 고정 높이 */
    overflow: hidden; /* 🔧 오버플로우 숨김 */
    align-content: center;
}

.word-item {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: 600;
    transition: all 0.3s ease;
    cursor: pointer;
    text-align: center;
    border: 2px solid transparent;
    white-space: nowrap; /* 🔧 텍스트 줄바꿈 방지 */
}

.word-item:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(139, 69, 19, 0.3);
    border-color: var(--primary);
}

.word-large {
    font-size: 1.6rem; /* 🔧 크기 조정 */
    background: var(--gradient-1);
    color: white;
}

.word-medium {
    font-size: 1.2rem; /* 🔧 크기 조정 */
    background: var(--gradient-2);
    color: white;
}

.word-small {
    font-size: 1rem; /* 🔧 크기 조정 */
    background: linear-gradient(135deg, #DEB887 0%, #F5DEB3 100%);
    color: var(--text-light);
}

/* 인사이트 박스 */
.insight-box {
    background: var(--gradient-2);
    color: white;
    padding: 1rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    border-left: 4px solid var(--warning);
    font-size: 0.9rem; /* 🔧 폰트 크기 조정 */
}

.insight-box h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    font-weight: 600;
}

.insight-box ul {
    margin: 0;
    padding-left: 1rem;
}

.insight-box li {
    margin-bottom: 0.3rem;
    line-height: 1.4;
}

/* 애니메이션 클래스 */
.fade-in {
    animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 반응형 */
@media (max-width: 768px) {
    .premium-header h1 {
        font-size: 1.8rem;
    }
    .premium-header p {
        font-size: 1rem;
    }
    .premium-card {
        padding: 1rem;
        min-height: 400px;
    }
    .wordcloud-container {
        height: 250px;
        gap: 0.5rem;
    }
    .word-large {
        font-size: 1.3rem;
    }
    .word-medium {
        font-size: 1.1rem;
    }
    .word-small {
        font-size: 0.9rem;
    }
}

/* Streamlit 요소 숨기기 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 다크모드 토글
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# 사이드바에 다크모드 토글
with st.sidebar:
    if st.button("🌙 다크모드" if not st.session_state.dark_mode else "☀️ 라이트모드"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# 다크모드 CSS 적용
if st.session_state.dark_mode:
    st.markdown('<div class="dark-mode">', unsafe_allow_html=True)

# 헤더 영역
st.markdown("""
<div class="premium-header fade-in">
    <h1>🍄 표고버섯 소셜 빅데이터 분석</h1>
    <p><strong>2019-2023년 | 총 언급량: 222,000회 | 67% 증가 추세</strong></p>
</div>
""", unsafe_allow_html=True)

# 프리미엄 색상 팔레트
SHIITAKE_COLORS = [
    '#8B4513', '#D2691E', '#CD853F', '#DEB887', 
    '#228B22', '#FF8C00', '#DC143C', '#4682B4'
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
            '재배': {'size': 'small', 'weight': 45}
        },
        'yearly_data': pd.DataFrame({
            '연도': ['2019', '2020', '2021', '2022', '2023'],
            '언급량': [31500, 43800, 45200, 48900, 52600]
        }),
        'seasonal_data': pd.DataFrame({
            '계절': ['봄', '여름', '가을', '겨울'],
            '비율': [26, 17, 29, 28]
        })
    }

data = load_data()

# 1행: 키워드 클라우드, 연도별 추이, 계절별 분포
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔍 주요 키워드</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">', unsafe_allow_html=True)
    
    # 🔧 수정된 워드클라우드 - 크기 제한
    word_html = '<div class="wordcloud-container">'
    for word, props in data['keywords'].items():
        word_html += f'<div class="word-item word-{props["size"]}" title="언급도: {props["weight"]}%">{word}</div>'
    word_html += '</div>'
    
    st.markdown(word_html, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📈 연도별 언급량 추이</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">', unsafe_allow_html=True)
    
    # 🔧 차트 크기 및 마진 조정
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
        hovertemplate='<b>%{x}</b><br>언급량: %{y:,}회<extra></extra>',
        textfont_size=10  # 🔧 텍스트 크기 조정
    )
    fig_yearly.update_layout(
        height=300,  # 🔧 높이 조정
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Pretendard", size=10),
        margin=dict(t=40, b=20, l=20, r=20),  # 🔧 상단 마진 증가
        yaxis=dict(range=[0, max(data['yearly_data']['언급량']) * 1.2])  # 🔧 Y축 범위 조정
    )
    st.plotly_chart(fig_yearly, use_container_width=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🗓️ 계절별 언급 분포</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">', unsafe_allow_html=True)
    
    # 🔧 도넛 차트 크기 및 라벨 위치 조정
    fig_seasonal = px.pie(
        data['seasonal_data'],
        names='계절', values='비율',
        hole=0.5,  # 🔧 구멍 크기 조정
        color_discrete_sequence=SHIITAKE_COLORS[:4]
    )
    fig_seasonal.update_traces(
        textposition='inside',  # 🔧 라벨을 안쪽으로
        textinfo='percent+label',
        textfont_size=11,  # 🔧 폰트 크기 조정
        hovertemplate='<b>%{label}</b><br>비율: %{percent}<extra></extra>',
        pull=[0.05, 0, 0.05, 0]  # 🔧 일부 조각 강조
    )
    fig_seasonal.update_layout(
        height=300,  # 🔧 높이 조정
        font=dict(family="Pretendard", size=10),
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=10)
        )
    )
    st.plotly_chart(fig_seasonal, use_container_width=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# 나머지 섹션들도 동일하게 카드 구조 적용
st.markdown("""
<div class="premium-card fade-in">
    <div class="card-title">💡 핵심 인사이트</div>
    <div class="card-content">
        <div class="insight-box">
            <h4>🚀 성장 동력</h4>
            <ul>
                <li><strong>건강식품 관심 증가</strong> - 면역력 강화 트렌드</li>
                <li><strong>채식/비건 확산</strong> - MZ세대 주도</li>
                <li><strong>스마트팜 연계</strong> - 생산량 증가</li>
            </ul>
        </div>
        
        <div class="insight-box">
            <h4>🎯 타겟별 마케팅</h4>
            <ul>
                <li><strong>40~50대</strong> - 면역·콜레스테롤 중심</li>
                <li><strong>20~30대</strong> - 비건·레시피 콘텐츠</li>
                <li><strong>60대+</strong> - 전통요리·건강식품</li>
            </ul>
        </div>
        
        <div class="insight-box">
            <h4>📱 콘텐츠 전략</h4>
            <ul>
                <li><strong>균형 배치</strong> - 요리 38% vs 건강 32%</li>
                <li><strong>계절 맞춤</strong> - 봄=레시피, 겨울=면역</li>
                <li><strong>긍정 브랜딩</strong> - 76% 긍정 감성 활용</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 푸터
st.markdown("""
---
<div style="text-align: center; color: #999; font-size: 0.9rem; padding: 1rem;">
    <p><strong>📊 데이터 출처</strong>: 네이버·인스타그램·유튜브 | 
    <strong>📅 분석 기간</strong>: 2019–2023년 | 
    <strong>🔬 분석 기법</strong>: 텍스트 마이닝·감성분석·토픽모델링</p>
    <p>🍄 <em>Made with ❤️ by Premium Data Analytics Team</em></p>
</div>
""", unsafe_allow_html=True)

# 다크모드 div 닫기
if st.session_state.dark_mode:
    st.markdown('</div>', unsafe_allow_html=True)

# 사이드바 정보
with st.sidebar:
    st.markdown("### 📋 대시보드 정보")
    st.info("""
    **🍄 표고버섯 빅데이터 분석**
    
    - 📊 총 데이터: 222,000건
    - 📅 기간: 2019-2023년  
    - 📈 성장률: 67% 증가
    - 😊 긍정률: 76%
    """)
