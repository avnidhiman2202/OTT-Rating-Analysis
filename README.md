# OTT Analytics Studio

An interactive OTT movie analytics dashboard built using Python, Streamlit, Pandas, and Plotly.

## About the Project

OTT Analytics Studio explores movie ratings, streaming platform availability, and movie release trends across Netflix, Amazon Prime Video, Hulu, and Disney+.

The project converts raw movie data into meaningful insights through an interactive dashboard.

## Features

- Interactive dark-themed dashboard
- Movie availability comparison across four OTT platforms
- Rotten Tomatoes rating analysis
- Movie rating distribution
- Movie release trends over time
- Searchable movie explorer
- Movie sorting and filtering
- CSV data export

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Matplotlib
- Seaborn

## Dataset

Source: [Movies on Netflix, Prime Video, Hulu and Disney+ – Kaggle](https://www.kaggle.com/datasets/ruchi798/movies-on-netflix-prime-video-hulu-and-disney)

The dataset includes movie titles, release years, age classifications, Rotten Tomatoes ratings, and streaming platform availability.

Dataset coverage ends in 2021.

## Project Structure

```text
OTT-Rating-Analysis/
├── dashboard/
│   └── app.py
├── dataset/
├── src/
│   ├── inspect_data.py
│   ├── clean_data.py
│   └── analyze_data.py
├── visualizations/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd OTT-Rating-Analysis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download the dataset from Kaggle and place the original CSV inside the `dataset/` folder, subject to its license.

Generate the cleaned dataset:

```bash
python src/clean_data.py
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## Learning Outcomes

- Data cleaning and preprocessing
- Exploratory Data Analysis
- Working with Pandas
- Interactive data visualization
- Building dashboards using Streamlit
- Organizing Python projects

## Author

**Avni**

GitHub: [avnidhiman2202](https://github.com/avnidhiman2202)

LinkedIn: [Avni Dhiman](https://www.linkedin.com/in/avni-dhiman-296b71423/)

---

Built as a Python data analytics portfolio project.