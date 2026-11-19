
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="OTT Analytics Studio",
    page_icon="🎬",
    layout="wide"
)

# ---------------- THEME ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #080b18, #10152b);
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: #0d1224;
    border-right: 1px solid #252d48;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

.hero {
    padding: 32px;
    border-radius: 18px;
    background: linear-gradient(120deg, #172554, #312e81, #164e63);
    border: 1px solid #334b83;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #cbd5e1;
    font-size: 15px;
}

.metric-card {
    background: linear-gradient(145deg, #151d35, #101629);
    border: 1px solid #293654;
    border-radius: 15px;
    padding: 20px;
    min-height: 115px;
}

.metric-label {
    color: #9caecb;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #22d3ee;
    font-size: 29px;
    font-weight: 800;
    margin-top: 9px;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    margin: 25px 0 12px 0;
}

div[data-testid="stMetric"] {
    background: #151d35;
    border: 1px solid #293654;
    padding: 17px;
    border-radius: 14px;
}

.stSelectbox, .stMultiSelect, .stTextInput {
    background-color: transparent;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #293654;
    border-radius: 12px;
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 25px;
    border-top: 1px solid #293654;
    margin-top: 35px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- DATA LOADING ----------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "dataset" / "processed" / "ott_cleaned.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    return df

if not DATA_FILE.exists():
    st.error("Dataset not found. Please run: python src/clean_data.py")
    st.info(f"Expected file: {DATA_FILE}")
    st.stop()

try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()


# ---------------- COLUMN CHECK ----------------

required_columns = [
    "title", "year", "age", "rotten_tomatoes",
    "rating_category", "netflix", "hulu",
    "prime_video", "disney_plus"
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing columns in dataset: {missing_columns}")
    st.stop()


# ---------------- SIDEBAR ----------------

st.sidebar.title("🎬 OTT Studio")
st.sidebar.caption("Movie Analytics Dashboard")
st.sidebar.divider()

st.sidebar.subheader("Dashboard Filters")

platforms = {
    "Netflix": "netflix",
    "Hulu": "hulu",
    "Prime Video": "prime_video",
    "Disney+": "disney_plus"
}

selected_platform = st.sidebar.selectbox(
    "Select Platform",
    ["All Platforms"] + list(platforms.keys())
)

year_min = int(df["year"].dropna().min())
year_max = int(df["year"].dropna().max())

selected_years = st.sidebar.slider(
    "Release Year",
    year_min,
    year_max,
    (year_min, year_max)
)

categories = ["All"] + sorted(df["rating_category"].dropna().unique().tolist())

selected_category = st.sidebar.selectbox(
    "Rating Category",
    categories
)

ages = ["All"] + sorted(df["age"].dropna().unique().tolist())

selected_age = st.sidebar.selectbox(
    "Age Classification",
    ages
)


# ---------------- FILTER DATA ----------------

filtered_df = df.copy()

if selected_platform != "All Platforms":
    column = platforms[selected_platform]
    filtered_df = filtered_df[filtered_df[column] == 1]

filtered_df = filtered_df[
    filtered_df["year"].between(selected_years[0], selected_years[1])
]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["rating_category"] == selected_category
    ]

if selected_age != "All":
    filtered_df = filtered_df[filtered_df["age"] == selected_age]


# ---------------- HERO ----------------

st.markdown("""
<div class="hero">
    <h1>OTT Analytics Studio</h1>
    <p>Explore movie ratings, streaming platforms and cinema trends through data.</p>
</div>
""", unsafe_allow_html=True)

st.caption("An interactive data analytics project | Dataset coverage: 1914–2021")


# ---------------- KPI METRICS ----------------

total_movies = len(filtered_df)

average_rating = filtered_df["rotten_tomatoes"].mean()

rated_movies = filtered_df["rotten_tomatoes"].notna().sum()

platform_count = sum(
    int(filtered_df[col].sum())
    for col in platforms.values()
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Total Movies", f"{total_movies:,}")

with m2:
    st.metric(
        "Average RT Rating",
        f"{average_rating:.1f}/100" if pd.notna(average_rating) else "N/A"
    )

with m3:
    st.metric("Rated Movies", f"{rated_movies:,}")

with m4:
    st.metric("Platform Listings", f"{platform_count:,}")


# ---------------- PLATFORM ANALYSIS ----------------

st.markdown('<div class="section-title">Platform Performance</div>', unsafe_allow_html=True)

platform_data = []

for name, col in platforms.items():
    platform_df = filtered_df[filtered_df[col] == 1]

    platform_data.append({
        "Platform": name,
        "Movies": len(platform_df),
        "Average Rating": platform_df["rotten_tomatoes"].mean()
    })

platform_df = pd.DataFrame(platform_data)

c1, c2 = st.columns(2)

with c1:
    fig = px.bar(
        platform_df,
        x="Platform",
        y="Movies",
        color="Platform",
        title="Movies Available by Platform",
        color_discrete_sequence=["#22d3ee", "#a78bfa", "#3b82f6", "#ec4899"]
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    rating_platform = platform_df.dropna(subset=["Average Rating"])

    fig = px.bar(
        rating_platform,
        x="Platform",
        y="Average Rating",
        color="Platform",
        title="Average Rotten Tomatoes Rating",
        color_discrete_sequence=["#22d3ee", "#a78bfa", "#3b82f6", "#ec4899"]
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        yaxis_range=[0, 100]
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------- RATING DISTRIBUTION ----------------

st.markdown('<div class="section-title">Rating Insights</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    rating_df = filtered_df.dropna(subset=["rotten_tomatoes"])

    fig = px.histogram(
        rating_df,
        x="rotten_tomatoes",
        nbins=20,
        title="Rotten Tomatoes Rating Distribution",
        color_discrete_sequence=["#22d3ee"]
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

with c4:
    category_data = (
        filtered_df["rating_category"]
        .value_counts()
        .reset_index()
    )
    category_data.columns = ["Category", "Movies"]

    fig = px.pie(
        category_data,
        names="Category",
        values="Movies",
        hole=0.55,
        title="Rating Category Distribution",
        color_discrete_sequence=["#22d3ee", "#a78bfa", "#3b82f6", "#ec4899"]
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------- RELEASE YEAR TREND ----------------

st.markdown('<div class="section-title">Movie Release Trends</div>', unsafe_allow_html=True)

year_data = (
    filtered_df.groupby("year")
    .size()
    .reset_index(name="Movies")
    .sort_values("year")
)

fig = px.line(
    year_data,
    x="year",
    y="Movies",
    markers=True,
    title="Movies Released Over the Years",
    color_discrete_sequence=["#22d3ee"]
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)


# ---------------- MOVIE EXPLORER ----------------

st.markdown('<div class="section-title">Movie Explorer</div>', unsafe_allow_html=True)

search = st.text_input("Search movie by title", placeholder="Enter a movie title...")

explorer_df = filtered_df.copy()

if search:
    explorer_df = explorer_df[
        explorer_df["title"].astype(str).str.contains(
            search, case=False, na=False
        )
    ]

sort_option = st.selectbox(
    "Sort movies by",
    ["Highest Rating", "Lowest Rating", "Newest First", "Oldest First"]
)

if sort_option == "Highest Rating":
    explorer_df = explorer_df.sort_values("rotten_tomatoes", ascending=False, na_position="last")
elif sort_option == "Lowest Rating":
    explorer_df = explorer_df.sort_values("rotten_tomatoes", ascending=True, na_position="last")
elif sort_option == "Newest First":
    explorer_df = explorer_df.sort_values("year", ascending=False)
else:
    explorer_df = explorer_df.sort_values("year", ascending=True)

display_columns = [
    "title", "year", "age", "rotten_tomatoes", "rating_category"
]

st.dataframe(
    explorer_df[display_columns],
    use_container_width=True,
    hide_index=True
)

csv = explorer_df[display_columns].to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Movie Data (CSV)",
    data=csv,
    file_name="ott_movie_analysis.csv",
    mime="text/csv"
)


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    OTT Analytics Studio | Built with Python, Streamlit, Pandas & Plotly
    <br>
    Data source: Movies on Netflix, Prime Video, Hulu and Disney+
</div>
""", unsafe_allow_html=True)
