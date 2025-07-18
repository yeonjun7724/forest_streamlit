import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# Page configuration
st.set_page_config(
    page_title="🍄 표고버섯 종합 분석 대시보드",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

    * {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .main {
        background-color: #f8f5f0;
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
        max-height: 280px;
        overflow: hidden;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #8B4513;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #CD853F;
    }

    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
    }

    .stSelectbox>div>div>div {
        background: white;
        border-radius: 10px;
        border: 2px solid #CD853F;
    }

    .stDateInput>div>div>input {
        background: white;
        border-radius: 10px;
        border: 2px solid #CD853F;
    }

    .stButton>button {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        height: 3em;
        width: 100%;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.3);
    }

    .stButton>button:hover {
        box-shadow: 0 6px 20px rgba(139, 69, 19, 0.4);
        transform: translateY(-2px);
    }

    .stRadio>div>label {
        background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        margin: 0.2rem;
        font-weight: 600;
    }

    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(139, 69, 19, 0.15);
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# CSV 파일 경로
CSV_MACRO = "final.csv"
CSV_PRED = "12개월후_예측_vs_실제_비교.csv"

# CSV 로드 함수
def load_csv(path):
    df = None
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            df = pd.read_csv(path, encoding=enc)
            break
        except:
            df = None
    if df is None:
        st.error(f"❌ 파일 로드 실패: {path}")
        return pd.DataFrame()
    # 날짜 컬럼 자동 탐색
    date_col = next(
        (c for c in df.columns if c.lower() in ("date","조사일","일자","날짜")),
        df.columns[0]
    )
    df = df.rename(columns={date_col: "date"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

# ================================
# 페이지 1: 소셜 빅데이터 분석
# ================================
def social_bigdata_page():
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
            height=220,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Noto Sans KR", size=11),
            yaxis_title="언급량 (회)",
            xaxis_title="연도",
            margin=dict(t=20, b=40, l=40, r=20)
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
            height=220,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Noto Sans KR", size=11),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        fig_seasonal.update_traces(
            hovertemplate='<b>%{label}</b><br>비율: %{percent}<extra></extra>',
            textinfo='label+percent',
            textfont_size=11
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
            height=180,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Noto Sans KR", size=11),
            xaxis_title="비율 (%)",
            yaxis_title="",
            margin=dict(t=20, b=40, l=60, r=20)
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
            height=220,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Noto Sans KR", size=11),
            yaxis_title="비율 (%)",
            xaxis_title="토픽",
            margin=dict(t=20, b=50, l=40, r=20)
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
            height=180,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Noto Sans KR", size=11),
            yaxis_title="비율 (%)",
            xaxis_title="연령대",
            margin=dict(t=20, b=40, l=40, r=20)
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
            height=260,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Noto Sans KR", size=11),
            yaxis_title="비율 (%)",
            xaxis_title="용도",
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=50, l=40, r=20)
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

# ================================
# 페이지 2: 유통 정보 대시보드
# ================================
def main_dashboard_page():
    st.markdown("""
    <div class="main-header">
        <h1>🍄 표고버섯 유통 정보 대시보드</h1>
        <p><strong>실시간 가격 정보 | 예측 분석 | 생산자 전용 서비스</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size:18px; text-align: center; margin-bottom: 2rem;'>접속 유형을 선택하세요:</p>", unsafe_allow_html=True)

    choice = st.radio("",
        ["👩‍🌾 생산자", "🛍 구매자", "👀 비회원"],
        horizontal=True,
    )

    if st.button("🚪 접속하기"):
        st.session_state.user_type = choice.replace("👩‍🌾 ", "").replace("🛍 ", "").replace("👀 ", "")

def socioecon_page():
    st.markdown("""
    <div class="main-header">
        <h1>📈 사회경제 지표 (2022–2025)</h1>
        <p><strong>표고버섯 생산에 영향을 미치는 주요 경제 지표</strong></p>
    </div>
    """, unsafe_allow_html=True)

    df = load_csv(CSV_MACRO)
    if df.empty:
        return
    df = df.sort_values("date")

    indicators = [
        "소비자물가지수",
        "시간당 최저임금(원)",
        "평균유가",
        "산업용 전기 (₩/kWh)",
        "LPG (₩/L)",
        "LNG (₩/MMBtu)",
    ]

    # 3×2 그리드
    for row_idx, row in enumerate([indicators[:3], indicators[3:]]):
        cols = st.columns(3, gap="small")
        for col_idx, (ind, col) in enumerate(zip(row, cols)):
            with col:
                if ind not in df.columns:
                    st.warning(f"⚠️ '{ind}' 컬럼이 없습니다.")
                    continue

                st.markdown(f'<div class="section-title">{ind}</div>', unsafe_allow_html=True)
                dmin = df["date"].min().date()
                dmax = df["date"].max().date()

                # 시작일 / 종료일 입력
                c1, c2 = st.columns(2)
                with c1:
                    start = st.date_input(
                        "시작일",
                        value=dmin,
                        min_value=dmin,
                        max_value=dmax,
                        key=f"{ind}_start_{row_idx}_{col_idx}"
                    )
                with c2:
                    end = st.date_input(
                        "종료일",
                        value=dmax,
                        min_value=dmin,
                        max_value=dmax,
                        key=f"{ind}_end_{row_idx}_{col_idx}"
                    )

                # 필터링 & 차트
                mask = (df["date"] >= pd.to_datetime(start)) & (df["date"] <= pd.to_datetime(end))
                series = df.loc[mask, ind]
                
                with st.container():
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(6,4))
                    ax.plot(series.index, series.values, color='#8B4513', linewidth=2)
                    ax.set_facecolor('#fafafa')
                    ax.tick_params(axis="x", rotation=45, labelsize=10)
                    ax.tick_params(axis="y", labelsize=10)
                    ax.grid(True, alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

def price_trend_page():
    st.markdown("""
    <div class="main-header">
        <h1>💰 단가 트렌드</h1>
        <p><strong>지역별 · 등급별 · 유통채널별 가격 분석</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # (1) 데이터 로드 및 전처리
    try:
        df = pd.read_csv(CSV_MACRO, encoding="utf-8")
    except:
        st.error("CSV 파일을 불러올 수 없습니다.")
        return

    df["조사일"] = pd.to_datetime(df["조사일"], errors="coerce")
    df["등급"] = df["등급"].astype(int)
    df["유통구분"] = df["유통구분"].astype(int)
    df["당일"] = pd.to_numeric(df["당일"].astype(str).str.replace(",", ""), errors="coerce")
    df = df.dropna(subset=["조사일","도","등급","유통구분","당일"])

    # (2) 필터: 도 / 등급 / 유통구분
    st.markdown('<div class="section-title">🎯 조건 선택</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    도_list = sorted(df["도"].unique())
    등급_list = sorted(df["등급"].unique())
    유통_list = sorted(df["유통구분"].unique())
    with c1:
        sel_do = st.selectbox("🏷️ 도 선택", 도_list)
    with c2:
        sel_grade = st.selectbox("🎖️ 등급 선택", 등급_list)
    with c3:
        sel_dist = st.selectbox("🚚 유통구분 선택", 유통_list)

    # 날짜 범위
    dmin = df["조사일"].min().date()
    dmax = df["조사일"].max().date()

    # (3) 월별 단가
    st.markdown('<div class="section-title">📊 월별 단가 트렌드</div>', unsafe_allow_html=True)
    sm, em = st.columns(2)
    with sm:
        start_m = st.date_input("시작일 (월별)", dmin, min_value=dmin, max_value=dmax, key="start_month")
    with em:
        end_m = st.date_input("종료일 (월별)", dmax, min_value=dmin, max_value=dmax, key="end_month")

    dfm = df[
        (df["도"] == sel_do) &
        (df["등급"] == sel_grade) &
        (df["유통구분"] == sel_dist) &
        (df["조사일"] >= pd.to_datetime(start_m)) &
        (df["조사일"] <= pd.to_datetime(end_m))
    ].copy()
    
    if dfm.empty:
        st.warning("해당 조건의 월별 데이터가 없습니다.")
    else:
        dfm["년월"] = dfm["조사일"].dt.to_period("M")
        monthly = dfm.groupby("년월")["당일"].mean().reset_index()
        monthly["년월_str"] = monthly["년월"].astype(str)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(12,6))
        ax1.plot(monthly["년월_str"], monthly["당일"], marker="o", color='#8B4513', linewidth=3, markersize=8)
        ax1.set_xlabel("년월", fontsize=12)
        ax1.set_ylabel("실제평균단가 (원)", fontsize=12)
        ax1.tick_params(axis="x", rotation=45)
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#fafafa')
        plt.tight_layout()
        st.pyplot(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # (4) 일별 단가 조회
    st.markdown('<div class="section-title">📅 일별 단가 조회</div>', unsafe_allow_html=True)
    sd, ed = st.columns(2)
    with sd:
        start_d = st.date_input("시작일 (일별)", dmin, min_value=dmin, max_value=dmax, key="start_day")
    with ed:
        end_d = st.date_input("종료일 (일별)", dmax, min_value=dmin, max_value=dmax, key="end_day")

    dfd = df[
        (df["도"] == sel_do) &
        (df["등급"] == sel_grade) &
        (df["유통구분"] == sel_dist) &
        (df["조사일"] >= pd.to_datetime(start_d)) &
        (df["조사일"] <= pd.to_datetime(end_d))
    ].copy()
    
    if dfd.empty:
        st.warning("해당 조건의 일별 데이터가 없습니다.")
    else:
        daily = (
            dfd.groupby(dfd["조사일"].dt.date)["당일"]
               .mean()
               .reset_index()
               .rename(columns={"조사일":"date","당일":"avg_price"})
        )
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(12,6))
        ax2.plot(daily["date"], daily["avg_price"], marker="o", color='#D2691E', linewidth=3, markersize=6)
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("단가 (평균, 원)", fontsize=12)
        ax2.tick_params(axis="x", rotation=45)
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('#fafafa')
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def future_page():
    st.markdown("""
    <div class="main-header">
        <h1>🔮 미래 단가 예측</h1>
        <p><strong>AI 기반 가격 예측 및 실제 데이터 비교</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # CSV 불러오기
    try:
        dfp = pd.read_csv(CSV_PRED, encoding="utf-8")
    except:
        try:
            dfp = pd.read_csv(CSV_PRED, encoding="cp949") 
        except:
            st.error("예측 데이터 파일을 불러올 수 없습니다.")
            return

    # 전처리
    dfp["등급_num"] = pd.to_numeric(dfp["등급_num"], errors="coerce")
    dfp["유통_num"] = pd.to_numeric(dfp["유통_num"], errors="coerce")
    dfp = dfp.dropna(subset=["도","등급_num","유통_num","예상단가(원)"])

    # UI: 등급 & 유통구분 선택
    st.markdown('<div class="section-title">🎯 조건 선택</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        sel_g = st.selectbox("🎖️ 등급 선택", sorted(dfp["등급_num"].unique()))
    with c2:
        sel_u = st.selectbox("🚚 유통구분 선택", sorted(dfp["유통_num"].unique()))

    # 필터링
    df_sel = dfp[(dfp["등급_num"]==sel_g) & (dfp["유통_num"]==sel_u)]
    if df_sel.empty:
        st.warning("해당 조합의 예측 결과가 없습니다.")
        return

    df_out = df_sel[["도","예상단가(원)"]].set_index("도")

    # 좌: 테이블, 우: 차트
    col_table, col_chart = st.columns([1,2], gap="small")

    with col_table:
        st.markdown('<div class="section-title">🏷️ 도별 예상단가</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        styled = df_out.style.set_table_styles([
            {
                "selector": "th",
                "props": [("font-size", "16px"), ("text-align","center"), ("background-color", "#8B4513"), ("color", "white")]
            },
            {
                "selector": "td", 
                "props": [("font-size", "14px"), ("text-align","center")]
            },
        ]).format({"예상단가(원)": "{:,}원"})
        st.dataframe(styled, width=400, height=400)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chart:
        st.markdown('<div class="section-title">📊 도별 예상단가 Bar Chart</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10,6))
        colors = ['#8B4513', '#D2691E', '#CD853F', '#DEB887', '#228B22', '#FF8C00', '#DC143C', '#4682B4']
        bars = ax.bar(df_out.index, df_out["예상단가(원)"], color=colors[:len(df_out)])
        ax.set_ylabel("예상단가(원)", fontsize=12)
        ax.set_xlabel("도", fontsize=12)
        ax.tick_params(axis="x", rotation=45, labelsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_facecolor('#fafafa')
        
        # 바 위에 값 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{height:,.0f}원', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 갭 계산 & 강조 테이블
    df_sel["갭_평균"] = df_sel["예상단가(원)"] - df_sel["실제평균단가"]
    df_sel["갭_마지막"] = df_sel["예상단가(원)"] - df_sel["마지막판매단가"]

    df_gap = df_sel[[
        "도",
        "실제평균단가",
        "예상단가(원)",
        "갭_평균",
        "마지막판매단가",
        "갭_마지막"
    ]].rename(columns={
        "실제평균단가":"실제평균(원)",
        "예상단가(원)":"예측단가(원)",
        "갭_평균":"갭(평균)",
        "마지막판매단가":"마지막실제(원)",
        "갭_마지막":"갭(마지막)"
    }).set_index("도")

    styled = (
        df_gap
        .style
        .format({
            "실제평균(원)": "{:,.0f}원",
            "예측단가(원)": "{:,.0f}원",
            "갭(평균)": "{:+,.0f}원",
            "마지막실제(원)": "{:,.0f}원",
            "갭(마지막)": "{:+,.0f}원",
        })
        .background_gradient(
            subset=["갭(평균)","갭(마지막)"],
            cmap="RdYlBu_r"
        )
        .set_table_styles([
            {"selector": "th", "props":[("font-size","14px"), ("background-color", "#8B4513"), ("color", "white")]},
            {"selector": "td", "props":[("font-size","12px")]}
        ])
    )

    st.markdown("---")
    st.markdown('<div class="section-title">📊 도별 예측 vs 실제 & 갭 분석</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.dataframe(styled, use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

def producer_page():
    st.markdown("""
    <div class="main-header">
        <h1>👩‍🌾 생산자 전용 페이지</h1>
        <p><strong>표고버섯 생산 관련 종합 정보</strong></p>
    </div>
    """, unsafe_allow_html=True)

    tab = st.sidebar.radio(
        "📋 메뉴 선택",
        ["📈 사회경제 지표", "💰 단가 트렌드", "🔮 미래 단가 예측"]
    )
    
    if tab == "📈 사회경제 지표":
        socioecon_page()
    elif tab == "💰 단가 트렌드":
        price_trend_page()
    else:
        future_page()

# ================================
# 메인 앱 로직
# ================================
def main():
    # 사이드바에서 페이지 선택
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%); 
                padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h2 style="color: white; margin: 0;">🍄 표고버섯</h2>
        <p style="color: white; margin: 0; opacity: 0.9;">종합 분석 시스템</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "📋 페이지 선택",
        ["📊 소셜 빅데이터 분석", "💼 유통 정보 대시보드"]
    )

    if page == "📊 소셜 빅데이터 분석":
        social_bigdata_page()
    elif page == "💼 유통 정보 대시보드":
        # 유통 정보 대시보드 내에서의 상태 관리
        if "user_type" not in st.session_state:
            st.session_state.user_type = ""
        
        if st.session_state.user_type == "":
            main_dashboard_page()
        else:
            st.sidebar.markdown(f"""
            <div style="background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%); 
                        padding: 1rem; border-radius: 10px; margin: 1rem 0; text-align: center;">
                <p style="color: white; margin: 0; font-weight: bold;">접속 유형: {st.session_state.user_type}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.sidebar.button("🚪 로그아웃"):
                st.session_state.user_type = ""
                st.rerun()
            elif st.session_state.user_type == "생산자":
                producer_page()
            else:
                st.markdown("""
                <div class="insight-card" style="text-align: center; margin: 3rem auto; max-width: 600px;">
                    <h3>❌ 접근 권한이 없습니다</h3>
                    <p>해당 페이지는 생산자 전용입니다.</p>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
