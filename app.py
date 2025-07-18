import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px

# 기본 설정
st.set_page_config(page_title="표고버섯 소셜 빅데이터 분석", layout="wide")
st.markdown("## 표고버섯 소셜 빅데이터 분석 (2019-2023)")
st.markdown("**총 언급량: 222,000회 | 67% 증가 추세**")

# 레이아웃: 3열 (워드클라우드, 연도별 추이, 계절별 분포)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("주요 키워드")
    keywords = """
    표고버섯 표고버섯 표고버섯 표고버섯 표고버섯 표고버섯 면역력 볶음 볶음 육수 비타민D 채식 콜레스테롤 재배 베타글루칸 표고전 원목재배 강칠맛 김표고
    """
    wordcloud = WordCloud(width=400, height=300, background_color='white', colormap='Greens', font_path=None).generate(keywords)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

with col2:
    st.subheader("연도별 언급량 추이")
    year_data = pd.DataFrame({
        "연도": ['2019', '2020', '2021', '2022', '2023'],
        "언급량": [31500, 43800, 45200, 48900, 52600]
    })
    fig = px.bar(year_data, x='연도', y='언급량', text='언급량', color='언급량', color_continuous_scale='Greens')
    fig.update_traces(texttemplate='%{text:.0s}', textposition='outside')
    fig.update_layout(yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.subheader("계절별 언급 분포")
    season_data = pd.DataFrame({
        "계절": ['봄', '여름', '가을', '겨울'],
        "비율": [26, 17, 29, 28]
    })
    fig = px.pie(season_data, names='계절', values='비율', color_discrete_sequence=px.colors.sequential.Greens)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# 레이아웃: 3열 (감성, 토픽, 연령대)
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("감성 분석")
    st.markdown("- 긍정 76% (169,100회)")
    st.markdown("- 중립 16% (35,600회)")
    st.markdown("- 부정 8% (17,800회)")
    fig, ax = plt.subplots()
    ax.barh(["긍정", "중립", "부정"], [76, 16, 8], color=['green', 'gray', 'red'])
    ax.set_xlim(0, 100)
    for i, v in enumerate([76, 16, 8]):
        ax.text(v + 1, i, f"{v}%", color='black', va='center')
    st.pyplot(fig)

with col5:
    st.subheader("토픽 모델링")
    topic_data = pd.DataFrame({
        "토픽": ["요리/레시피", "건강/효능", "생산/재배", "유통/가격"],
        "비율": [38, 32, 18, 12]
    })
    fig = px.bar(topic_data, x="토픽", y="비율", color='비율', text='비율', color_continuous_scale='Greens')
    fig.update_layout(yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("연령대별 관심도")
    st.markdown("- 20~30대: 31% (69,000회) → 채식/비건(45%), 다이어트(33%)")
    st.markdown("- 40~50대: 42% (93,450회) → 건강/면역(48%), 전통요리(32%)")
    st.markdown("- 60대+: 27% (60,050회) → 약용/건강식품(52%), 웰빙(38%)")
    age_data = pd.DataFrame({
        "연령대": ["20~30대", "40~50대", "60대+"],
        "관심도": [31, 42, 27]
    })
    fig = px.bar(age_data, x="연령대", y="관심도", color='관심도', text='관심도', color_continuous_scale='Greens')
    fig.update_layout(yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

# 레이아웃: 2열 (용도별 분석, 핵심 인사이트)
col7, col8 = st.columns(2)

with col7:
    st.subheader("용도별 활용 분석")
    st.markdown("**요리 용도 (116,150회)**")
    st.markdown("- 국물/육수 27%")
    st.markdown("- 볶음 25%")
    st.markdown("- 채소섭취대체 15%")
    st.markdown("- 샐러드 8%")

    st.markdown("**건강 효능 (71,170회)**")
    st.markdown("- 면역력 강화 38%")
    st.markdown("- 콜레스테롤 22%")
    st.markdown("- 비타민D 18%")
    st.markdown("- 체중관리 12%")

with col8:
    st.subheader("핵심 인사이트")
    st.markdown("""
- **5년간 67% 성장 (31.5K → 52.6K)**  
- **긍정 감성 76%** - 맛과 건강 효능으로 인식  
- **요리용도 38% > 건강효능 32%** 양대 활용축  
- **40~50대 42% 최고 관심층 (건강/면역 중심)**  
- **MZ세대 31% - 채식/비건 트렌드 견인**  
- **계절별 고른 분포 - 사계절 꾸준한 관심**  
- **생산/재배 18% - 귀농·스마트팜 관심 증가**
""")

# 트렌드 전망 박스
st.subheader("표고버섯 소셜 트렌드 전망")
st.markdown("""
**[성장 동력]**  
- 건강식품 관심 증가로 면역·콜레스테롤 효능 주목  
- MZ세대 채식/비건 트렌드로 식물성 단백질 대안 부상  
- 스마트팜·귀농 관심으로 생산/재배 언급 증가  

**[마케팅 포인트]**  
- 40~50대: 건강효능(면역·콜레스테롤) 중심 소구  
- 20~30대: 채식·레시피·다이어트 콘텐츠 활용  
- 60대+: 전통 요리법·농업 정보와 연계  

**[콘텐츠 전략]**  
- 요리 레시피 38% vs 건강정보 32% 균형 배치  
- 계절별 맞춤 콘텐츠 (봄/가을 생산, 겨울 면역)  
- 긍정 감성 76% 활용한 브랜딩 강화
""")

# 하단 정보
st.markdown("---")
st.markdown("**데이터 출처**: 소셜미디어 빅데이터 (네이버, 카카오, 인스타그램, 유튜브, 블로그 등)  \n"
            "**분석 기간**: 2019.01~2023.12  \n"
            "**분석 도구**: 텍스트 마이닝, 감성분석, 토픽모델링")

