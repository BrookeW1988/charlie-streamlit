# Charlie Dashboard - Streamlit Edition 🧠

A real-time dashboard for tracking tasks, growth metrics, and YouTube analytics. Built with Streamlit for easy deployment and maintenance.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red)

## Features

### 📊 Dashboard Tab
- **Real-time task tracking** - Separate columns for Brooke and Charlie
- **Activity log** - Latest actions and updates
- **Work log** - Charlie's completed work
- **Conversation summary** - Last topics discussed
- **Scheduled reminders** - Upcoming automated tasks
- **Active sessions** - Running sub-agents and cron jobs
- **Quick actions** - Links to Slack, GitHub, n8n

### 📈 Growth Tab
- **Workshop countdown** - Days until AI Dream Team (Feb 19+23, 2026)
- **Revenue tracking** - Membership, workshop, consulting
- **Audience growth** - YouTube, Instagram, TikTok, Email
- **Monthly targets** - Path to $20K/month

### ▶️ YouTube Tab
- **Channel stats** - Subscribers, views, video count
- **Top performing videos** - By views and engagement
- **Recent uploads** - Latest content
- **Content ideas** - AI-generated suggestions based on performance
- **Competitor watch** - Track other creators in the space

### 📁 Docs Tab
- **Working folder** - Link to Charlie's Drive
- **Key resources** - WrightMode sites and offers
- **Internal tools** - n8n, GitHub repos, analytics

## Tech Stack

- **Streamlit** - Python web app framework
- **Requests** - API calls to n8n webhooks
- **Pytz** - Timezone handling

## Data Sources

- **Tasks API**: `https://n8n-wrightmode-u50335.vm.elestio.app/webhook/tasks`
- **YouTube API**: `https://n8n-wrightmode-u50335.vm.elestio.app/webhook/charlie-youtube`

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Deploy to Streamlit Cloud

1. **Push to GitHub** (this repo or new one)

2. **Go to** [share.streamlit.io](https://share.streamlit.io)

3. **Click** "New app"

4. **Select:**
   - Repository: `BrookeW1988/charlie-streamlit` (or wherever you push)
   - Branch: `main`
   - Main file path: `app.py`

5. **Click Deploy!**

That's it! Streamlit Cloud will:
- Auto-detect Python version
- Install requirements.txt
- Apply .streamlit/config.toml theme
- Give you a public URL like: `charlie-dashboard.streamlit.app`

## Auto-Deploy

Once connected to GitHub, any push to `main` will automatically redeploy the app.

## Theme

Dark purple/violet theme matching the original dashboard:
- Primary: `#a78bfa` (violet)
- Background: `#1a1a2e` (dark blue)
- Secondary: `#16213e` (navy)
- Text: `#eeeeee` (white)

## Environment Variables

No environment variables required! All APIs are public webhooks.

For future private APIs, add secrets in Streamlit Cloud:
1. Go to app settings
2. Click "Secrets"
3. Add your variables

Access in code:
```python
import streamlit as st
api_key = st.secrets["API_KEY"]
```

## File Structure

```
streamlit-dashboard/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .streamlit/
    └── config.toml       # Theme and server config
```

## Comparison: Vercel vs Streamlit

| Feature | Vercel (current) | Streamlit Cloud |
|---------|------------------|-----------------|
| Language | HTML/JS | Python |
| Deploy | Manual push | Auto on push |
| Data refresh | On page load | On page load + button |
| Caching | Browser localStorage | Server-side (60s) |
| Theme | Custom CSS | config.toml + CSS |
| Hosting | Free tier | Free tier |
| Custom domain | ✅ | ✅ (paid) |

## Why Streamlit?

1. **Python-native** - Easier to extend with data analysis
2. **Auto-deploy** - Push to GitHub, it deploys
3. **Built-in caching** - Reduces API calls
4. **Interactive widgets** - Easy to add filters, forms
5. **No JS debugging** - Python errors are clearer

## Future Enhancements

- [ ] Add task creation form
- [ ] Add task completion buttons
- [ ] Email list signup widget
- [ ] Content calendar view
- [ ] Revenue charts with Plotly
- [ ] Competitor video analysis

---

Built by Charlie 🤖 for Brooke @ WrightMode
