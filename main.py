import streamlit as st
import pandas as pd
import plotly.express as px

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
    "365일간의 일별 박스오피스 데이터를 이용해 "
    "영화의 시간에 따른 변화를 살펴봅니다."
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
    st.error("❌ 필요한 데이터 열을 찾을 수 없습니다.")
    st.write("현재 열 이름:", list(df.columns))
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

# 날짜가 없는 데이터 제거
df = df.dropna(subset=["날짜"])

df = df.sort_values("날짜").reset_index(drop=True)

# --------------------------------------------------
# 그래프 1
# --------------------------------------------------

st.divider()

st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "여러 날짜에 걸쳐 기록된 영화를 선택하면 "
    "시간에 따른 일관객 변화를 확인할 수 있습니다."
)

# 영화별 등장 날짜 수 계산
movie_counts = (
    df.groupby("영화명")["날짜"]
    .nunique()
    .sort_values(ascending=False)
)

# 최소 2일 이상 등장한 영화만 선택
movie_list = sorted(
    movie_counts[movie_counts >= 2].index.tolist()
)

if len(movie_list) == 0:
    st.error("❌ 여러 날짜에 기록된 영화를 찾을 수 없습니다.")
    st.stop()

selected_movie = st.selectbox(
    "🎬 영화를 선택하세요.",
    movie_list
)

# 선택한 영화 데이터
movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")

# --------------------------------------------------
# 그래프 만들기
# --------------------------------------------------

fig = px.line(
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

# 날짜 표시
fig.update_xaxes(
    tickformat="%m-%d"
)

# 마우스를 올렸을 때 표시
fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    height=550,
    hovermode="closest",
    xaxis_title="날짜",
    yaxis_title="일관객 수"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# 그래프 설명
# --------------------------------------------------

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 점을 적어 보세요.",
    placeholder=(
        "예: 이 영화는 개봉 초기에 일관객 수가 가장 높았고 "
        "시간이 지나면서 점차 감소하는 모습을 보인다."
    ),
    height=100,
    key="graph1_note"
)

# --------------------------------------------------
# 그래프 2
# --------------------------------------------------

st.divider()

st.header("📊 그래프 2")

st.info(
    "여기에 두 번째 그래프를 추가할 예정입니다."
)

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "두 번째 그래프에서 알 수 있는 점을 적어 보세요.",
    placeholder="이 그래프를 통해 알 수 있는 내용을 적어 보세요.",
    height=100,
    key="graph2_note"
)

# --------------------------------------------------
# 그래프 3
# --------------------------------------------------

st.divider()

st.header("📊 그래프 3")

st.info(
    "여기에 세 번째 그래프를 추가할 예정입니다."
)

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "세 번째 그래프에서 알 수 있는 점을 적어 보세요.",
    placeholder="이 그래프를 통해 알 수 있는 내용을 적어 보세요.",
    height=100,
    key="graph3_note"
)

# --------------------------------------------------
# 데이터 정보
# --------------------------------------------------

st.divider()

st.subheader("📋 데이터 정보")

st.write(
    f"전체 데이터: **{len(df):,}개 행**"
)

st.write(
    f"그래프에 사용할 영화: **{len(movie_list):,}개**"
)

st.write(
    f"데이터 기간: "
    f"**{df['날짜'].min().strftime('%Y-%m-%d')} ~ "
    f"{df['날짜'].max().strftime('%Y-%m-%d')}**"
)
