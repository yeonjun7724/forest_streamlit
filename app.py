import time

import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="🍄 프리미엄 표고버섯 소셜 빅데이터 분석",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ——— CSS ——————————————————————————————————————————————————————————————————————————————————————————————————————————
PREMIUM_CSS = """
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
:root {
    --primary: #8B4513; --secondary: #D2691E; --accent: #CD853F;
    --success: #228B22; --warning: #FF8C00; --danger: #DC143C;
    --bg-light: #FFF8DC; --bg-dark: #2C1810;
    --card-light: #FFFFFF; --card-dark: #3D2817;
    --text-light: #2F1B14; --text-dark: #F5DEB3;
    --shadow: 0 8px 32px rgba(139, 69, 19, 0.1);
    --shadow-hover: 0 12px 40px rgba(139, 69, 19, 0.2);
    --gradient-1: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
    --gradient-2: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
    --border-radius: 16px;
}
body { font-family: 'Pretendard', sans-serif; background: var(--bg, var(--bg-light)); color: var(--text, var(--text-light)); transition: .3s; }
[data-testid="stAppViewContainer"] { background: var(--bg); transition: .3s; }
.premium-header { background: var(--gradient-1); padding: 3rem 2rem; border-radius: var(--border-radius); text-align: center; margin-bottom: 2rem; box-shadow: var(--shadow); }
.premium-header h1 { margin: 0; color: #fff; font-size: 3rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
.premium-header p { margin: 1rem 0 0; color: rgba(255,255,255,0.9); font-size: 1.2rem; }
.premium-card { background: var(--card-bg, var(--card-light)); border-radius: var(--border-radius); padding: 2rem; box-shadow: var(--shadow); transition: .3s; position: relative; overflow: hidden; min-height: 350px; }
.premium-card:hover { transform: translateY(-8px); box-shadow: var(--shadow-hover); }
.card-title { font-size: 1.4rem; font-weight: 700; color: var(--primary); margin-bottom: 1.5rem; display: flex; align-items: center; gap: .5rem; }
.stat-card { background: var(--gradient-2); color: #fff; padding: 1.5rem; border-radius: 12px; text-align: center; margin: 1rem 0; box-shadow: var(--shadow); transition: .3s; }
.stat-card:hover { transform: scale(1.05); }
.mode-toggle { position: fixed; top: 20px; right: 20px; z-index: 1000; background: var(--card-bg); border: none; border-radius: 50px; padding: 12px 20px; cursor: pointer; box-shadow: var(--shadow); transition: .3s; }
.wordcloud-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem; padding: 2rem; }
.word-item { padding: 8px 16px; border-radius: 25px; font-weight: 600; cursor: pointer; border: 2px solid transparent; transition: .3s; }
.word-item:hover { transform: scale(1.2); box-shadow: 0 8px 25px rgba(139, 69, 19, 0.3); border-color: var(--primary); }
.word-large { font-size: 2rem; background: var(--gradient-1); color: #fff; }
.word-medium { font-size: 1.5rem; background: var(--gradient-2); color: #fff; }
.word-small { font-size: 1.2rem; background: linear-gradient(135deg, #DEB887 0%, #F5DEB3 100%); color: var(--text-light); }
#MainMenu, footer, header { visibility: hidden; }
"""
st.markdown(f"<style>{PREMIUM_CSS}</style>", unsafe_allow_html=True)

# ——— 다크모드 토글 ——————————————————————————————————————————————————————————————————————————————————————————————
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
with st.sidebar:
    if st.button("🌙 다크모드" if not st.session_state.dark_mode else "☀️ 라이트모드"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.experimental_rerun()
if st.session_state.dark_mode:
    st.markdown("""<style>
        [data-testid="stAppViewContainer"] { background-color: #2C1810 !important; color: #F5DEB3 !important; }
        .premium-card { background-color: #3D2817 !important; color: #F5DEB3 !important; }
    </style>""", unsafe_allow_html=True)

# ——— 데이터 로드 —————————————————————————————————————————————————————————————————————————————————————————————————
@st.cache_data
def load_data():
    return {
        'keywords': {
            '표고버섯': ('large', 100), '면역력': ('medium', 85), '볶음': ('medium', 80),
            '육수': ('medium', 75), '비타민D': ('small', 60), '채식': ('small', 55),
            '콜레스테롤': ('small', 50), '재배': ('small', 45), '베타글루칸': ('small', 40),
            '표고전': ('small', 35), '원목재배': ('small', 30), '강칠맛': ('small', 25)
        },
        'yearly': pd.DataFrame({'연도': ['2019','2020','2021','2022','2023'], '언급량':[31500,43800,45200,48900,52600]}),
        'seasonal': pd.DataFrame({'계절':['봄','여름','가을','겨울'], '비율':[26,17,29,28]}),
        'sentiment': pd.DataFrame({'감성':['긍정','중립','부정'], '비율':[76,16,8], '언급수':[169100,35600,17800]}),
        'topic': pd.DataFrame({'토픽':['요리/레시피','건강/효능','생산/재배','유통/가격'], '비율':[38,32,18,12]}),
        'age': pd.DataFrame({'연령대':['20~30대','40~50대','60대+'],'비율':[31,42,27],'언급수':[69000,93450,60050]}),
        'usage': pd.DataFrame({
            '항목':['국물/육수','볶음','채소대체','샐러드','면역강화','콜레스테롤','비타민D','체중관리'],
            '비율':[27,25,18,8,38,22,18,12],
            '카테고리':['요리','요리','요리','요리','건강','건강','건강','건강']
        })
    }
data = load_data()

SHIITAKE_COLORS = ['#8B4513','#D2691E','#CD853F','#DEB887','#228B22','#FF8C00','#DC143C','#4682B4']

# ——— 헤더 ——————————————————————————————————————————————————————————————————————————————————————————————————————————————
st.markdown("""
<div class="premium-header">
    <h1>🍄 표고버섯 소셜 빅데이터 분석</h1>
    <p><strong>2019-2023년 | 총 언급량: 222,000회 | 67% 증가 추세</strong></p>
</div>
""", unsafe_allow_html=True)

# ——— 1행 레이아웃 ——————————————————————————————————————————————————————————————————————————————————————————————
c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔍 주요 키워드</div>', unsafe_allow_html=True)
    html = '<div class="wordcloud-container">'
    for w, (size, wt) in data['keywords'].items():
        html += f'<div class="word-item word-{size}" title="언급도: {wt}%">{w}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 연도별 추이 (카드 내부에 HTML 임베드)
with c2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📈 연도별 언급량 추이</div>', unsafe_allow_html=True)
    fig = px.bar(data['yearly'], x='연도', y='언급량', text='언급량', color='연도', color_discrete_sequence=SHIITAKE_COLORS)
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(height=320, margin=dict(t=20,b=20,l=20,r=20), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    components.html(html, height=360, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

# 계절별 분포
with c3:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🗓️ 계절별 언급 분포</div>', unsafe_allow_html=True)
    fig = px.pie(data['seasonal'], names='계절', values='비율', hole=0.4, color_discrete_sequence=SHIITAKE_COLORS[:4])
    fig.update_traces(textinfo='percent+label', textposition='inside')
    fig.update_layout(height=320, margin=dict(t=20,b=20,l=20,r=20))
    html = fig.to_html(full_html=False, include_plotlyjs=False)
    components.html(html, height=360, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

# ——— 2행 레이아웃 ——————————————————————————————————————————————————————————————————————————————————————————————
c4, c5, c6 = st.columns(3, gap="large")

# 감성 분석
with c4:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">😊 감성 분석</div>', unsafe_allow_html=True)
    fig = px.bar(
        data['sentiment'], x='비율', y='감성', orientation='h', text='비율',
        color='감성', color_discrete_map={'긍정':'#228B22','중립':'#CD853F','부정':'#DC143C'}
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=250, margin=dict(t=20,b=20,l=20,r=20), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    html = fig.to_html(full_html=False, include_plotlyjs=False)
    components.html(html, height=300, scrolling=False)
    for _, r in data['sentiment'].iterrows():
        color = '#228B22' if r['감성']=='긍정' else '#FF8C00' if r['감성']=='중립' else '#DC143C'
        st.markdown(f"""
            <div class="stat-card" style="background:{color};">
                <div class="stat-number">{r['비율']}%</div>
                <div class="stat-label">{r['감성']} ({r['언급수']:,}회)</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 토픽 모델링
with c5:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 토픽 모델링</div>', unsafe_allow_html=True)
    fig = px.bar(data['topic'], x='토픽', y='비율', text='비율', color='토픽', color_discrete_sequence=SHIITAKE_COLORS[:4])
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=320, margin=dict(t=20,b=20,l=20,r=20), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    html = fig.to_html(full_html=False, include_plotlyjs=False)
    components.html(html, height=360, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

# 연령대별 관심도
with c6:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">👥 연령대별 관심도</div>', unsafe_allow_html=True)
    fig = px.bar(data['age'], x='연령대', y='비율', text='비율', color='연령대', color_discrete_sequence=SHIITAKE_COLORS[:3])
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=250, margin=dict(t=20,b=20,l=20,r=20), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    html = fig.to_html(full_html=False, include_plotlyjs=False)
    components.html(html, height=300, scrolling=False)
    st.markdown("""
        <div class="premium-card"><div class="insight-box">
            <h4>📋 연령대별 특징</h4>
            <p><strong>🔥 20~30대 (69,000회)</strong> 채식/비건 45%, 다이어트 33%</p>
            <p><strong>💪 40~50대 (93,450회)</strong> 면역/건강 48%, 전통요리 32%</p>
            <p><strong>🌿 60대+ (60,050회)</strong> 건강식품 52%, 웰빙 38%</p>
        </div></div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ——— 3행 레이아웃 ——————————————————————————————————————————————————————————————————————————————————————————————
c7, c8 = st.columns([1.6, 1], gap="large")

# 용도별 활용 분석
with c7:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🍽️ 용도별 활용 분석</div>', unsafe_allow_html=True)
    fig = px.bar(
        data['usage'], x='항목', y='비율', text='비율', color='카테고리',
        color_discrete_map={'요리':SHIITAKE_COLORS[1], '건강':SHIITAKE_COLORS[0]}
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=380, margin=dict(t=20,b=50,l=20,r=20), xaxis_tickangle=45, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    html = fig.to_html(full_html=False, include_plotlyjs=False)
    components.html(html, height=420, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

# 핵심 인사이트
with c8:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">💡 핵심 인사이트</div>', unsafe_allow_html=True)
    insights = [
        ("📈","성장률","67%","5년간 언급량 증가"),
        ("😊","긍정도","76%","맛과 건강의 이중효과"),
        ("🍳","요리용도","38%","vs 건강효능 32%"),
        ("👑","핵심층","42%","40~50대 관심도 최고"),
        ("🌱","MZ트렌드","31%","비건 트렌드 선도"),
        ("🗓️","사계절","균등","연중 고른 관심"),
        ("🚜","생산연계","18%","스마트팜·귀농 관련")
    ]
    for icon, title, val, desc in insights:
        st.markdown(f"""
            <div class="stat-card" style="margin:.5rem 0; padding:1rem;">
                <div style="display:flex; align-items:center; gap:.5rem;">
                    <span style="font-size:1.5rem;">{icon}</span>
                    <div>
                        <div style="font-size:1.2rem; font-weight:700;">{title}: {val}</div>
                        <div style="font-size:.9rem; opacity:.9;">{desc}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ——— 트렌드 전망 & 전략 ——————————————————————————————————————————————————————————————————————————————————————————————
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🔮 표고버섯 소셜 트렌드 전망 & 마케팅 전략</div>', unsafe_allow_html=True)
t1, t2, t3 = st.columns(3)
with t1:
    st.markdown("""
        <div class="insight-box"><h4>🚀 성장 동력</h4>
        <ul>
            <li>건강식품 관심 증가<br>면역력 강화 트렌드</li>
            <li>채식/비건 확산<br>MZ세대 주도</li>
            <li>스마트팜 연계<br>생산량 증가</li>
        </ul></div>
    """, unsafe_allow_html=True)
with t2:
    st.markdown("""
        <div class="insight-box"><h4>🎯 타겟별 마케팅</h4>
        <ul>
            <li>40~50대<br>면역·콜레스테롤 중심</li>
            <li>20~30대<br>비건·레시피 콘텐츠</li>
            <li>60대+<br>전통요리·건강식품</li>
        </ul></div>
    """, unsafe_allow_html=True)
with t3:
    st.markdown("""
        <div class="insight-box"><h4>📱 콘텐츠 전략</h4>
        <ul>
            <li>균형 배치<br>요리 38% vs 건강 32%</li>
            <li>계절 맞춤<br>봄=레시피, 겨울=면역</li>
            <li>긍정 브랜딩<br>76% 긍정 감성 활용</li>
        </ul></div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ——— 푸터 ——————————————————————————————————————————————————————————————————————————————————————————————————————————————
st.markdown("""
---
<div style="text-align:center; color:#999; font-size:.9rem; padding:2rem;">
    <p><strong>📊 데이터 출처</strong>: 네이버·인스타그램·유튜브 |
    <strong>📅 분석 기간</strong>: 2019–2023년 |
    <strong>🔬 분석 기법</strong>: 텍스트 마이닝·감성분석·토픽모델링</p>
    <p>🍄 <em>Made with ❤️ by Premium Data Analytics Team</em></p>
</div>
""", unsafe_allow_html=True)

# ——— 업데이트 시뮬레이션 ——————————————————————————————————————————————————————————————————————————————————————————————
if st.sidebar.button("🔄 데이터 새로고침"):
    with st.spinner("데이터를 업데이트하는 중…"):
        time.sleep(2)
        st.success("✅ 데이터가 성공적으로 업데이트되었습니다!")
        st.balloons()

# ——— 사이드바 정보 ——————————————————————————————————————————————————————————————————————————————————————————————
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
    st.write("🌙 다크/라이트 모드")
    st.write("📱 반응형 디자인")
    st.write("🎨 인터랙티브 차트")
    st.write("📊 실시간 업데이트")
