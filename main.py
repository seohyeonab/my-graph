import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/"
    "modudata/main/data/kobis_daily.csv"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "일별 박스오피스 데이터를 이용해 "
    "영화 관객 수가 시간에 따라 어떻게 변하는지 살펴봅니다."
)

# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------

try:
    df = pd.read_csv(
        DATA_URL,
        encoding="utf-8-sig"
    )
except Exception as e:
    st.error("❌ 데이터를 불러오지 못했습니다.")
    st.write(e)
    st.stop()

# 열 이름 정리
df.columns = df.columns.astype(str).str.strip()

# 필요한 열 확인
required_columns = [
    "날짜",
    "순위",
    "영화코드",
    "영화명",
    "일관객",
    "누적관객",
    "스크린수",
    "상영횟수"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error("❌ 데이터의 열을 제대로 읽지 못했습니다.")
    st.write("현재 열:", list(df.columns))
    st.write("없는 열:", missing_columns)
    st.stop()

# --------------------------------------------------
# 데이터 정리
# --------------------------------------------------

df["날짜"] = pd.to_datetime(
    df["날짜"].astype(str),
    format="%Y%m%d",
    errors="coerce"
)

numeric_columns = [
    "순위",
    "영화코드",
    "일관객",
    "누적관객",
    "스크린수",
    "상영횟수"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df["영화명"] = (
    df["영화명"]
    .astype(str)
    .str.strip()
)

# 날짜가 없는 행 제거
df = df.dropna(subset=["날짜"])

df = df.sort_values("날짜").reset_index(drop=True)

# ==================================================
# 그래프 1
# ==================================================

st.divider()

st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다."
)

# 영화별 등장 날짜 수
movie_counts = (
    df.groupby("영화명")["날짜"]
    .nunique()
    .sort_values(ascending=False)
)

# 최소 2일 이상 기록된 영화만 사용
movie_list = movie_counts[
    movie_counts >= 2
].index.tolist()

if not movie_list:
    st.error("❌ 여러 날짜에 기록된 영화가 없습니다.")
    st.stop()

# 가장 많은 날짜에 등장한 영화가 기본 선택
selected_movie = st.selectbox(
    "🎬 영화를 선택하세요.",
    movie_list,
    index=0
)

movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig1.update_xaxes(
    tickformat="%m-%d"
)

fig1.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig1.update_layout(
    height=500,
    hovermode="closest"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 1에서 알 수 있는 점을 적어 보세요.",
    placeholder=(
        "예: 영화의 일관객 수가 개봉 후 어떻게 변화하는지 알 수 있다."
    ),
    height=100,
    key="graph1_note"
)

# ==================================================
# 그래프 2
# ==================================================

st.divider()

st.header("📊 그래프 2. 날짜별 박스오피스 1위 관객 수")

st.write(
    "매일 박스오피스 1위를 차지한 영화의 일관객 수가 "
    "시간에 따라 어떻게 변했는지 보여줍니다."
)

# 순위 1위만 추출
rank1_df = df[
    df["순위"] == 1
].copy()

# 같은 날짜에 1위 데이터가 여러 개라면 합치지 않고
# 날짜별 최대값을 사용
rank1_daily = (
    rank1_df
    .groupby("날짜", as_index=False)["일관객"]
    .max()
    .sort_values("날짜")
)

fig2 = px.line(
    rank1_daily,
    x="날짜",
    y="일관객",
    markers=True,
    title="날짜별 박스오피스 1위 영화의 일관객 수",
    labels={
        "날짜": "날짜",
        "일관객": "1위 영화 일관객 수"
    }
)

fig2.update_xaxes(
    tickformat="%m-%d"
)

fig2.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=500,
    hovermode="closest"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 2에서 알 수 있는 점을 적어 보세요.",
    placeholder=(
        "예: 날짜에 따라 박스오피스 1위 영화의 관객 규모가 어떻게 달라지는지 알 수 있다."
    ),
    height=100,
    key="graph2_note"
)

# ==================================================
# 그래프 3
# ==================================================

st.divider()

st.header("📉 그래프 3. 날짜별 TOP 10 전체 관객 수")

st.write(
    "매일 박스오피스 10위 안에 든 영화들의 일관객 수를 모두 더해 "
    "전체적인 영화 관객 규모의 변화를 살펴봅니다."
)

# 날짜별 TOP 10 일관객 합계
top10_daily = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

fig3 = px.line(
    top10_daily,
    x="날짜",
    y="일관객",
    markers=True,
    title="날짜별 박스오피스 TOP 10 전체 관객 수",
    labels={
        "날짜": "날짜",
        "일관객": "TOP 10 전체 관객 수"
    }
)

fig3.update_xaxes(
    tickformat="%m-%d"
)

fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>TOP 10 전체 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig3.update_layout(
    height=500,
    hovermode="closest"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 3에서 알 수 있는 점을 적어 보세요.",
    placeholder=(
        "예: 날짜에 따라 전체적인 영화 관객 규모가 증가하거나 감소하는 모습을 알 수 있다."
    ),
    height=100,
    key="graph3_note"
)

# ==================================================
# 데이터 정보
# ==================================================

st.divider()

st.subheader("📋 데이터 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "전체 데이터",
        f"{len(df):,}개"
    )

with col2:
    st.metric(
        "영화 종류",
        f"{df['영화명'].nunique():,}개"
    )

with col3:
    st.metric(
        "데이터 날짜",
        f"{df['날짜'].nunique():,}일"
    )

st.caption(
    f"데이터 기간: "
    f"{df['날짜'].min().strftime('%Y-%m-%d')} ~ "
    f"{df['날짜'].max().strftime('%Y-%m-%d')}"
)
