# 📊 Sales Intelligence Dashboard

A beautiful, interactive sales data dashboard built with **Streamlit** and **Plotly**.

## Features
- 📈 Multi-category revenue trends (area / bar / line)
- 🍩 Category mix donut chart
- 📊 Daily transaction volume
- 🌍 Regional bubble chart (revenue × customers × satisfaction)
- 🏆 Top products bar chart + data table
- 🎛️ Sidebar filters: category, metric, date range, chart style

## Project Structure
```
streamlit-dashboard/
├── app.py                  # Main application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit theme config
└── .gitignore
```

## Local Setup

```bash
# 1. Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
# → Opens at http://localhost:8501
```

## 🚀 Deploy to Streamlit Community Cloud (FREE)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial dashboard commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Community Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your **GitHub** account
3. Click **"New app"**
4. Fill in:
   - **Repository**: `YOUR_USERNAME/YOUR_REPO`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy!"** 🎉

Your app will be live at:
`https://YOUR_USERNAME-YOUR_REPO-app-XXXXX.streamlit.app`

> ✅ **Free tier** includes: unlimited public apps, 1 GB RAM, community support.

## Customisation Tips
- **Swap sample data** → replace `generate_data()` with a CSV read or DB query
- **Add pages** → create `pages/` folder with extra `.py` files (Streamlit multi-page)
- **Secrets** → use `st.secrets` and the Streamlit Cloud Secrets manager for API keys
