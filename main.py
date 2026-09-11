import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# 기본 설정
# ==================================================

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

# ==================================================
# 데이터 불러오기
# ==================================================

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

# 필요한 열
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
    st.write("현재 열:", list(df.columns))
    st.write("없는 열:", missing_columns)
    st.stop()

# ==================================================
# 데이터 정리
# ==================================================

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

# ==================================================
# 그래프 1
# 영화별 일관객 변화
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
# 일관객 합계 TOP 5 영화
# ==================================================

st.divider()

st.header("📊 그래프 2. 일관객 합계 TOP 5 영화의 날짜별 변화")

st.write(
    "전체 기간 동안 일관객 합계가 가장 큰 5편을 골라 "
    "날짜별 일관객 변화를 비교합니다."
)

# 영화별 기간 전체 일관객 합계
movie_total = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values(
        "일관객",
        ascending=False
    )
)

# TOP 5
top5_movies = movie_total.head(5)["영화명"].tolist()

top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계가 가장 큰 TOP 5 영화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_xaxes(
    tickformat="%m-%d"
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=600,
    hovermode="closest",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.caption(
    "💡 오른쪽 범례에서 영화 이름을 클릭하면 "
    "해당 영화의 선을 숨기거나 다시 표시할 수 있습니다."
)

# TOP 5 표
st.write("**🏆 기간 전체 일관객 합계 TOP 5**")

top5_display = movie_total.head(5).copy()

top5_display["일관객"] = top5_display[
    "일관객"
].map(
    lambda x: f"{int(x):,}명"
)

top5_display.columns = [
    "영화명",
    "기간 전체 일관객 합계"
]

st.dataframe(
    top5_display,
    hide_index=True,
    use_container_width=True
)

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 2에서 알 수 있는 점을 적어 보세요.",
    placeholder=(
        "예: 기간 전체 일관객 합계가 높은 영화들의 "
        "날짜별 관객 수 변화를 비교할 수 있다."
    ),
    height=100,
    key="graph2_note"
)

# ==================================================
# 그래프 3
# 날짜별 TOP 10 일관객 합계
# ==================================================

st.divider()

st.header("📉 그래프 3. 날짜별 TOP 10 일관객 합계")

st.write(
    "각 날짜의 박스오피스 10위권 영화들의 일관객을 모두 더해 "
    "전체 관객 규모를 영역 그래프로 보여줍니다."
)

# 날짜별 TOP 10 일관객 합계
top10_daily = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# --------------------------------------------------
# 일관객 합계가 가장 큰 날짜 TOP 3
# --------------------------------------------------

top3_days = (
    top10_daily
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

# --------------------------------------------------
# 영역 그래프
# --------------------------------------------------

fig3 = px.area(
    top10_daily,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 TOP 10 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "TOP 10 일관객 합계"
    }
)

fig3.update_xaxes(
    tickformat="%m-%d"
)

fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>TOP 10 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)

# --------------------------------------------------
# TOP 3 날짜 표시
# --------------------------------------------------

for _, row in top3_days.iterrows():

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"{row['날짜'].strftime('%Y-%m-%d')}"
            f"<br><b>{int(row['일관객']):,}명</b>"
        ),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-60
    )

# TOP 3 지점
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers",
    marker=dict(size=10),
    name="TOP 3"
)

fig3.update_layout(
    height=600,
    hovermode="closest",
    xaxis_title="날짜",
    yaxis_title="TOP 10 일관객 합계"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# TOP 3 표
st.write("**🏆 일관객 합계가 가장 컸던 날짜 TOP 3**")

top3_display = (
    top10_daily
    .nlargest(3, "일관객")
    .sort_values(
        "일관객",
        ascending=False
    )
    .copy()
)

top3_display["날짜"] = top3_display[
    "날짜"
].dt.strftime("%Y-%m-%d")

top3_display["일관객"] = top3_display[
    "일관객"
].map(
    lambda x: f"{int(x):,}명"
)

top3_display.columns = [
    "날짜",
    "TOP 10 일관객 합계"
]

st.dataframe(
    top3_display,
    hide_index=True,
    use_container_width=True
)

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 3에서 알 수 있는 점을 적어 보세요.",
    placeholder=(
        "예: 특정 날짜에는 TOP 10 영화의 일관객 합계가 크게 증가했으며, "
        "관객이 가장 많이 몰린 날짜를 확인할 수 있다."
    ),
    height=100,
    key="graph3_note"
)

# ==================================================
# 그래프 4
# 기간 전체 일관객 TOP 10
# ==================================================

st.divider()

st.header("🏆 그래프 4. 기간 전체 일관객 TOP 10")

st.write(
    "이 기간 동안 10위권에 등장한 영화들의 일관객을 모두 더해 "
    "관객 수가 가장 많은 TOP 10 영화를 보여줍니다."
)

# 영화별 일관객 합계 + 10위권 등장 일수
movie_summary = (
    df.groupby("영화명")
    .agg(
        기간_일관객=("일관객", "sum"),
        등장_일수=("날짜", "nunique")
    )
    .reset_index()
)

# TOP 10
top10_movies = (
    movie_summary
    .sort_values(
        "기간_일관객",
        ascending=False
    )
    .head(10)
    .sort_values(
        "기간_일관객",
        ascending=True
    )
)

fig4 = px.bar(
    top10_movies,
    x="기간_일관객",
    y="영화명",
    orientation="h",
    text="기간_일관객",
    title="기간 전체 일관객 TOP 10",
    labels={
        "기간_일관객": "기간 전체 일관객",
        "영화명": "영화"
    }
)

fig4.update_traces(
    texttemplate="%{text:,}명",
    textposition="outside",
    hovertemplate=(
        "영화: %{y}"
        "<br>기간 전체 일관객: %{x:,}명"
        "<br>10위권 등장 일수: %{customdata}일"
        "<extra></extra>"
    ),
    customdata=top10_movies["등장_일수"]
)

fig4.update_layout(
    height=600,
    yaxis={
        "categoryorder": "total ascending"
    },
    xaxis_title="기간 전체 일관객",
    yaxis_title="영화",
    showlegend=False
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.caption(
    "💡 막대에 마우스를 올리면 해당 영화의 "
    "기간 전체 일관객과 10위권 등장 일수를 확인할 수 있습니다."
)

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 4에서 알 수 있는 점을 적어 보세요.",
    placeholder=(
        "예: 기간 동안 많은 관객을 모은 영화가 어떤 영화인지 "
        "비교할 수 있다."
    ),
    height=100,
    key="graph4_note"
)

# ==================================================
# 그래프 5
# 월 × 요일별 일관객 합계 히트맵
# ==================================================

st.divider()

st.header("🔥 그래프 5. 월 × 요일별 일관객 히트맵")

st.write(
    "날짜에서 월과 요일을 추출해 "
    "월별·요일별 일관객 합계를 비교합니다."
)

# --------------------------------------------------
# 월과 요일 추출
# --------------------------------------------------

df["월"] = df["날짜"].dt.month

weekday_map = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일"
}

df["요일"] = df["날짜"].dt.dayofweek.map(
    weekday_map
)

weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

# --------------------------------------------------
# 월 × 요일별 합계
# --------------------------------------------------

heatmap_data = (
    df.groupby(
        ["월", "요일"],
        observed=False
    )["일관객"]
    .sum()
    .reset_index()
)

heatmap_data["요일"] = pd.Categorical(
    heatmap_data["요일"],
    categories=weekday_order,
    ordered=True
)

heatmap_data = heatmap_data.sort_values(
    ["월", "요일"]
)

# --------------------------------------------------
# 피벗
# --------------------------------------------------

heatmap_pivot = heatmap_data.pivot(
    index="월",
    columns="요일",
    values="일관객"
)

heatmap_pivot = heatmap_pivot.reindex(
    columns=weekday_order
)

# --------------------------------------------------
# 히트맵
# --------------------------------------------------

fig5 = px.imshow(
    heatmap_pivot,
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    },
    x=weekday_order,
    y=heatmap_pivot.index,
    text_auto=".3s",
    aspect="auto",
    title="월 × 요일별 일관객 합계"
)

fig5.update_xaxes(
    categoryorder="array",
    categoryarray=weekday_order
)

fig5.update_yaxes(
    title="월",
    tickmode="linear",
    dtick=1
)

fig5.update_layout(
    height=600,
    xaxis_title="요일",
    yaxis_title="월",
    coloraxis_colorbar_title="일관객"
)

fig5.update_traces(
    hovertemplate=(
        "%{y}월 %{x}"
        "<br>일관객 합계: %{z:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.caption(
    "💡 색이 진할수록 해당 월·요일에 기록된 "
    "10위권 영화들의 일관객 합계가 많다는 의미입니다."
)

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 5에서 알 수 있는 점을 적어 보세요.",
    placeholder=(
        "예: 주말에 평일보다 일관객 합계가 높고, "
        "특정 달의 관객 수가 특히 많은 것을 알 수 있다."
    ),
    height=100,
    key="graph5_note"
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
