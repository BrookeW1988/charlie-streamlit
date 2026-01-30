"""
Charlie Dashboard - Streamlit Edition
A real-time dashboard for tracking tasks, growth metrics, and YouTube analytics.
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz

# =============================================================================
# CONFIG & CONSTANTS
# =============================================================================

st.set_page_config(
    page_title="Charlie Dashboard 🧠",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# API Endpoints
TASKS_API = "https://n8n-wrightmode-u50335.vm.elestio.app/webhook/tasks"
YOUTUBE_API = "https://n8n-wrightmode-u50335.vm.elestio.app/webhook/charlie-youtube"

# Workshop details
WORKSHOP_DATE_1 = datetime(2026, 2, 19, 10, 0, 0, tzinfo=pytz.timezone('Australia/Perth'))
WORKSHOP_DATE_2 = datetime(2026, 2, 23, 10, 0, 0, tzinfo=pytz.timezone('Australia/Perth'))
WORKSHOP_PRICE = 1997
WORKSHOP_GOAL = 10
WORKSHOP_SOLD = 1

# Competitor data (fallback)
COMPETITORS = [
    {"name": "Grace Leung", "handle": "@graceleungyl", "subs": "112K", "style": "Grounded, marketing"},
    {"name": "Sabrina Ramonov", "handle": "@sabrina_ramonov", "subs": "119K", "style": "High output, systems"},
    {"name": "Natalie Choprasert", "handle": "@brandnat", "subs": "Growing", "style": "Solopreneur focused"},
    {"name": "Jack Roberts", "handle": "@Itssssss_Jack", "subs": "108K", "style": "Technical, agencies"},
    {"name": "Nate Herk", "handle": "@nateherk", "subs": "510K", "style": "n8n, technical"},
    {"name": "Nick Saraev", "handle": "@nicksaraev", "subs": "252K", "style": "Make.com, automation agencies"},
]

# =============================================================================
# CUSTOM CSS - Dark Purple/Violet Theme
# =============================================================================

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header */
    .dashboard-header {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    
    .dashboard-title {
        font-size: 2rem;
        font-weight: 700;
        color: #eee;
        margin: 0;
    }
    
    .status-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-awake {
        background: #22c55e;
        color: #000;
    }
    
    .status-sleeping {
        background: #64748b;
        color: #fff;
    }
    
    /* Card styling */
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #a78bfa;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #888;
        margin-top: 5px;
    }
    
    /* Task cards */
    .task-card {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 3px solid #a78bfa;
    }
    
    .task-card.high {
        border-left-color: #ef4444;
    }
    
    .task-card.done {
        border-left-color: #22c55e;
        opacity: 0.6;
    }
    
    .task-card.in-progress {
        border-left-color: #f59e0b;
    }
    
    .task-title {
        font-weight: 500;
        color: #eee;
        margin-bottom: 5px;
    }
    
    .task-meta {
        font-size: 0.8rem;
        color: #888;
    }
    
    /* Activity items */
    .activity-item {
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        font-size: 0.9rem;
    }
    
    .activity-time {
        color: #a78bfa;
        font-size: 0.75rem;
    }
    
    /* Workshop countdown */
    .countdown-box {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .countdown-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 10px;
    }
    
    .countdown-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #fff;
    }
    
    .countdown-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
    }
    
    /* Revenue cards */
    .revenue-card {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .revenue-name {
        font-weight: 600;
        color: #eee;
    }
    
    .revenue-desc {
        font-size: 0.85rem;
        color: #888;
    }
    
    .revenue-amount {
        font-size: 1.2rem;
        font-weight: 700;
        color: #22c55e;
    }
    
    /* Video items */
    .video-item {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 3px solid #ff0000;
    }
    
    .video-title {
        font-weight: 500;
        color: #eee;
        margin-bottom: 5px;
    }
    
    .video-stats {
        font-size: 0.8rem;
        color: #888;
    }
    
    /* Competitor items */
    .competitor-item {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .competitor-name {
        font-weight: 500;
        color: #eee;
    }
    
    .competitor-handle {
        font-size: 0.8rem;
        color: #888;
    }
    
    .competitor-subs {
        font-weight: 600;
        color: #ff0000;
    }
    
    /* Progress bars */
    .progress-container {
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
        height: 8px;
        overflow: hidden;
        margin: 8px 0;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 4px;
    }
    
    .progress-bar.yt { background: #ff0000; }
    .progress-bar.ig { background: #E1306C; }
    .progress-bar.tt { background: #00f2ea; }
    .progress-bar.email { background: #a78bfa; }
    
    /* Quick links */
    .quick-link {
        display: block;
        color: #a78bfa;
        text-decoration: none;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .quick-link:hover {
        color: #8b5cf6;
    }
    
    /* Tab styling fix */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.05);
        padding: 5px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #888;
        border-radius: 8px;
        padding: 10px 20px;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #a78bfa;
        color: #000;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1rem;
        font-weight: 600;
        color: #eee;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .section-header.brooke { color: #f472b6; }
    .section-header.charlie { color: #a78bfa; }
    .section-header.youtube { color: #ff0000; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA FETCHING
# =============================================================================

@st.cache_data(ttl=60)  # Cache for 60 seconds
def fetch_tasks():
    """Fetch tasks data from n8n API."""
    try:
        response = requests.get(TASKS_API, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch tasks: {e}")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_youtube():
    """Fetch YouTube data from n8n API."""
    try:
        response = requests.get(YOUTUBE_API, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None  # YouTube data is optional

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_time_ago(iso_string):
    """Format ISO timestamp to relative time."""
    if not iso_string:
        return ""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        now = datetime.now(pytz.UTC)
        diff = now - dt
        
        minutes = int(diff.total_seconds() / 60)
        hours = int(diff.total_seconds() / 3600)
        days = int(diff.total_seconds() / 86400)
        
        if minutes < 1:
            return "Just now"
        elif minutes < 60:
            return f"{minutes}m ago"
        elif hours < 24:
            return f"{hours}h ago"
        elif days < 7:
            return f"{days}d ago"
        else:
            return dt.strftime("%b %d")
    except:
        return ""

def format_number(num):
    """Format large numbers with K/M suffixes."""
    if not num:
        return "--"
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    if num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)

def get_charlie_status(data):
    """Determine if Charlie is awake or sleeping."""
    if not data or 'charlieLastActive' not in data:
        return False
    try:
        last_active = datetime.fromisoformat(data['charlieLastActive'].replace('Z', '+00:00'))
        now = datetime.now(pytz.UTC)
        return (now - last_active).total_seconds() < 300  # 5 minutes
    except:
        return False

def get_workshop_countdown():
    """Calculate countdown to workshop."""
    now = datetime.now(pytz.timezone('Australia/Perth'))
    time_to_workshop = WORKSHOP_DATE_1 - now
    
    if time_to_workshop.total_seconds() < 0:
        time_to_workshop = WORKSHOP_DATE_2 - now
    
    days = time_to_workshop.days
    hours = time_to_workshop.seconds // 3600
    
    return days, hours

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_header(data):
    """Render the dashboard header with Charlie status."""
    is_awake = get_charlie_status(data)
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        status_icon = "⚡" if is_awake else "😴"
        status_text = "Awake" if is_awake else "Sleeping"
        status_class = "status-awake" if is_awake else "status-sleeping"
        
        st.markdown(f"""
            <div class="dashboard-header">
                <span style="font-size: 1.5rem;">{status_icon}</span>
                <h1 class="dashboard-title">Charlie</h1>
                <span class="status-badge {status_class}">{status_text}</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if data and 'lastUpdated' in data:
            st.caption(f"Last sync: {format_time_ago(data['lastUpdated'])}")
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

def render_stats_bar(data):
    """Render the stats bar at the top."""
    if not data:
        return
    
    brooke_active = len([t for t in data.get('forBrooke', []) if t.get('status') != 'done'])
    charlie_active = len([t for t in data.get('forCharlie', []) if t.get('status') != 'done'])
    all_done = len([t for t in data.get('forBrooke', []) + data.get('forCharlie', []) if t.get('status') == 'done'])
    
    # Count overdue
    now = datetime.now()
    overdue = 0
    for task in data.get('forBrooke', []) + data.get('forCharlie', []):
        if task.get('status') != 'done' and task.get('due'):
            try:
                due_date = datetime.fromisoformat(task['due'].replace('Z', '+00:00'))
                if due_date.replace(tzinfo=None) < now:
                    overdue += 1
            except:
                pass
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{brooke_active}</div>
                <div class="metric-label">Brooke's Tasks</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{charlie_active}</div>
                <div class="metric-label">Charlie's Tasks</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #22c55e;">{all_done}</div>
                <div class="metric-label">Done This Week</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        color = "#ef4444" if overdue > 0 else "#22c55e"
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {color};">{overdue}</div>
                <div class="metric-label">Overdue</div>
            </div>
        """, unsafe_allow_html=True)

def render_task(task, is_high_priority=False):
    """Render a single task card."""
    status = task.get('status', 'pending')
    priority = task.get('priority', 'normal')
    
    card_class = "task-card"
    if status == 'done':
        card_class += " done"
    elif status == 'in-progress':
        card_class += " in-progress"
    elif priority == 'high':
        card_class += " high"
    
    status_emoji = {
        'done': '✅',
        'in-progress': '🔄',
        'pending': '⏳'
    }.get(status, '⏳')
    
    priority_badge = "🔥 " if priority == 'high' else ""
    
    st.markdown(f"""
        <div class="{card_class}">
            <div class="task-title">{priority_badge}{task.get('title', 'Untitled')}</div>
            <div class="task-meta">
                {status_emoji} {status.replace('-', ' ').title()}
                {' • Due: ' + task.get('due', '')[:10] if task.get('due') else ''}
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_tasks_column(tasks, title, emoji, color_class):
    """Render a column of tasks."""
    active_tasks = [t for t in tasks if t.get('status') != 'done']
    
    st.markdown(f"""
        <div class="section-header {color_class}">
            {emoji} {title} <span style="background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; margin-left: 5px;">{len(active_tasks)}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if not active_tasks:
        st.info("✨ All clear!")
    else:
        for task in active_tasks[:10]:
            render_task(task)

def render_activity_log(activity):
    """Render the activity log."""
    st.markdown('<div class="section-header">📊 Activity</div>', unsafe_allow_html=True)
    
    if not activity:
        st.info("No activity")
        return
    
    for item in activity[:8]:
        st.markdown(f"""
            <div class="activity-item">
                <div>{item.get('action', '')}</div>
                <div class="activity-time">{format_time_ago(item.get('time'))}</div>
            </div>
        """, unsafe_allow_html=True)

def render_work_log(work_log):
    """Render Charlie's work log."""
    st.markdown('<div class="section-header">📋 Charlie\'s Work Log</div>', unsafe_allow_html=True)
    
    if not work_log:
        st.info("Work log will appear here")
        return
    
    for item in work_log[:10]:
        st.markdown(f"""
            <div class="activity-item">
                <div class="activity-time">{format_time_ago(item.get('time'))}</div>
                <div>{item.get('action', '')}</div>
            </div>
        """, unsafe_allow_html=True)

def render_reminders(reminders):
    """Render scheduled reminders."""
    st.markdown('<div class="section-header">⏰ Scheduled Reminders</div>', unsafe_allow_html=True)
    
    if not reminders:
        st.info("No reminders set")
        return
    
    for r in reminders[:5]:
        st.markdown(f"""
            <div class="activity-item">
                <div style="color: #f59e0b; font-weight: 600;">⏰ {r.get('schedule', '')}</div>
                <div>{r.get('text', '')}</div>
            </div>
        """, unsafe_allow_html=True)

def render_conversation(conversation):
    """Render last conversation summary."""
    st.markdown('<div class="section-header">💬 Last Conversation</div>', unsafe_allow_html=True)
    
    if not conversation or not conversation.get('topics'):
        st.info("No recent conversation")
        return
    
    topics_html = " ".join([f'<span style="background: #a78bfa; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin-right: 5px;">{t}</span>' for t in conversation.get('topics', [])])
    
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;">
            <div style="margin-bottom: 10px;">{topics_html}</div>
            <p style="color: #888; margin: 0;">{conversation.get('summary', '')}</p>
            <div class="activity-time" style="margin-top: 8px;">{format_time_ago(conversation.get('time'))}</div>
        </div>
    """, unsafe_allow_html=True)

def render_sessions(sessions):
    """Render active sessions."""
    st.markdown('<div class="section-header">🧵 Sessions & Sub-agents</div>', unsafe_allow_html=True)
    
    if not sessions:
        st.info("No active sessions")
        return
    
    for s in sessions:
        type_emoji = {'cron': '🔄', 'thread': '💬'}.get(s.get('type'), '🧵')
        st.markdown(f"""
            <div class="activity-item">
                <div style="color: #f59e0b; font-weight: 600;">{type_emoji} {s.get('type', '')} {' • ' + s.get('tokens', '') if s.get('tokens') else ''}</div>
                <div>{s.get('name', '')}</div>
            </div>
        """, unsafe_allow_html=True)

def render_quick_links():
    """Render quick action links."""
    st.markdown('<div class="section-header">🔗 Quick Actions</div>', unsafe_allow_html=True)
    
    links = [
        ("💬 Message Charlie", "https://app.slack.com/client/T08H8MQ9LTR/D0AAQAGHTGT"),
        ("📁 Docs Repo", "https://github.com/BrookeW1988/wrightmode-docs"),
        ("⚡ n8n", "https://n8n-wrightmode-u50335.vm.elestio.app"),
        ("🛠️ Dashboard Repo", "https://github.com/BrookeW1988/charlie-dashboard"),
    ]
    
    for label, url in links:
        st.markdown(f'<a href="{url}" target="_blank" class="quick-link">{label}</a>', unsafe_allow_html=True)

# =============================================================================
# GROWTH TAB COMPONENTS
# =============================================================================

def render_workshop_countdown():
    """Render the workshop countdown widget."""
    days, hours = get_workshop_countdown()
    revenue = WORKSHOP_SOLD * WORKSHOP_PRICE
    progress = (WORKSHOP_SOLD / WORKSHOP_GOAL) * 100
    
    st.markdown(f"""
        <div class="countdown-box">
            <div class="countdown-title">🎯 AI Dream Team Workshop</div>
            <div class="countdown-value">{days}d {hours}h</div>
            <div class="countdown-label">until Feb 19 + 23, 2026</div>
            <div style="margin-top: 15px; display: flex; justify-content: center; gap: 30px;">
                <div>
                    <div style="font-size: 1.5rem; font-weight: 700;">{WORKSHOP_SOLD}/{WORKSHOP_GOAL}</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">seats sold</div>
                </div>
                <div>
                    <div style="font-size: 1.5rem; font-weight: 700;">${revenue:,}</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">revenue</div>
                </div>
                <div>
                    <div style="font-size: 1.5rem; font-weight: 700;">{progress:.0f}%</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">to goal</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_revenue_streams():
    """Render revenue streams section."""
    st.markdown('<div class="section-header">💰 Revenue Streams</div>', unsafe_allow_html=True)
    
    streams = [
        ("Membership", "10 members × $147", "$1,470", "recurring"),
        ("AI Dream Team Workshop", f"${WORKSHOP_PRICE:,} per seat", f"${WORKSHOP_SOLD * WORKSHOP_PRICE:,}", "Feb launch"),
        ("Stack to Scale", "$12,000+ AUD", "Pipeline", "see leads"),
        ("Consulting", "Wright Stack Consult $1,200", "--", "ad hoc"),
    ]
    
    for name, desc, amount, note in streams:
        color = "#22c55e" if "$" in amount and amount != "--" else "#f59e0b"
        st.markdown(f"""
            <div class="revenue-card">
                <div>
                    <div class="revenue-name">{name}</div>
                    <div class="revenue-desc">{desc}</div>
                </div>
                <div style="text-align: right;">
                    <div class="revenue-amount" style="color: {color};">{amount}</div>
                    <div style="font-size: 0.75rem; color: #666;">{note}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_audience_growth():
    """Render audience growth metrics."""
    st.markdown('<div class="section-header">📈 Audience Growth</div>', unsafe_allow_html=True)
    
    platforms = [
        ("YouTube", "336 → 12K", 3, "yt"),
        ("Instagram", "2,600 → 10K", 26, "ig"),
        ("TikTok", "2,600 → 10K", 26, "tt"),
        ("Email List", "~700", 70, "email"),
    ]
    
    for name, goal, progress, css_class in platforms:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-weight: 500; color: #eee;">{name}</span>
                    <span style="color: #888;">{goal}</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar {css_class}" style="width: {progress}%;"></div>
                </div>
                <div style="font-size: 0.75rem; color: #666;">{progress}% to goal</div>
            </div>
        """, unsafe_allow_html=True)

def render_monthly_targets():
    """Render monthly targets."""
    st.markdown('<div class="section-header">🎯 To Hit $20K/month</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; color: #888; line-height: 1.8;">
            <p><strong style="color: #eee;">Option A:</strong> 8 workshop seats ($19,976)</p>
            <p><strong style="color: #eee;">Option B:</strong> 2 Stack to Scale ($24,000+)</p>
            <p><strong style="color: #eee;">Option C:</strong> Mix — 4 workshop + 1 S2S + membership</p>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
            <p><strong style="color: #22c55e;">Current MRR:</strong> $1,470 (7% of goal)</p>
        </div>
    """, unsafe_allow_html=True)

# =============================================================================
# YOUTUBE TAB COMPONENTS
# =============================================================================

def render_youtube_stats(yt_data):
    """Render YouTube stats bar."""
    channel = yt_data.get('channel', {}) if yt_data else {}
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        (col1, format_number(channel.get('subscribers', 336)), "Subscribers"),
        (col2, format_number(channel.get('totalViews', 159443)), "Total Views"),
        (col3, str(channel.get('videoCount', '10')), "Videos"),
        (col4, format_number(channel.get('views30d', 0)), "Views (30d)"),
    ]
    
    for col, value, label in stats:
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color: #ff0000;">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)

def render_top_videos(yt_data):
    """Render top performing videos."""
    st.markdown('<div class="section-header youtube">🔥 Top Performing Videos</div>', unsafe_allow_html=True)
    
    # Fallback data
    videos = [
        {"title": "Clawdbot (Moltbot) is ALL HYPE! (Why I'm Already Cancelling)", "views": 2661, "likes": 45, "comments": 52, "publishedAt": "2026-01-28"},
        {"title": "The AI assistant nobody talks about (but it runs on your computer)", "views": 714, "likes": 9, "comments": 0, "publishedAt": "2026-01-28"},
        {"title": "Best AI tools for creators on a $20/month budget", "views": 642, "likes": 8, "comments": 0, "publishedAt": "2026-01-27"},
        {"title": "Why I'm learning Claude Code with zero dev background", "views": 611, "likes": 18, "comments": 2, "publishedAt": "2026-01-23"},
        {"title": "How to use Claude AI without code or a terminal", "views": 603, "likes": 3, "comments": 0, "publishedAt": "2026-01-22"},
    ]
    
    if yt_data and yt_data.get('topVideos'):
        videos = yt_data['topVideos'][:5]
    
    for v in videos:
        st.markdown(f"""
            <div class="video-item">
                <div class="video-title">{v.get('title', '')}</div>
                <div class="video-stats">
                    👁️ {format_number(v.get('views', 0))} • 
                    👍 {format_number(v.get('likes', 0))} • 
                    💬 {format_number(v.get('comments', 0))} • 
                    📅 {format_time_ago(v.get('publishedAt'))}
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_recent_videos(yt_data):
    """Render recent videos."""
    st.markdown('<div class="section-header youtube">📹 Recent Videos</div>', unsafe_allow_html=True)
    
    videos = [
        {"title": "Why Clawdbot could expose your credentials", "views": 120, "publishedAt": "2026-01-30"},
        {"title": "Turn Your Google Docs into an AI Employee (NotebookLM Tutorial)", "views": 6, "publishedAt": "2026-01-30"},
        {"title": "How to build a TikTok dashboard when you don't know where to start", "views": 324, "publishedAt": "2026-01-29"},
    ]
    
    if yt_data and yt_data.get('recentVideos'):
        videos = yt_data['recentVideos'][:5]
    
    for v in videos:
        st.markdown(f"""
            <div class="video-item">
                <div class="video-title">{v.get('title', '')}</div>
                <div class="video-stats">
                    👁️ {format_number(v.get('views', 0))} • 
                    📅 {format_time_ago(v.get('publishedAt'))}
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_content_ideas(yt_data):
    """Render content ideas."""
    st.markdown('<div class="section-header">💡 Content Ideas</div>', unsafe_allow_html=True)
    
    ideas = [
        {"title": "Hot takes on trending AI tools = viral", "reason": "Clawdbot video got 2.6K views (4x average). Opinion pieces with strong stance perform best.", "source": "Your top performer"},
        {"title": "Budget-friendly AI lists", "reason": "$20/month tools video (642 views) resonates. Your audience wants accessible, not enterprise.", "source": "Your #3 video"},
        {"title": "Personal journey content", "reason": "Claude Code learning video (611 views, 18 likes) = high engagement. Authenticity sells.", "source": "Your #4 video"},
    ]
    
    if yt_data and yt_data.get('ideas'):
        ideas = yt_data['ideas']
    
    for idea in ideas:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 3px solid #22c55e;">
                <div style="font-weight: 500; color: #eee; margin-bottom: 5px;">{idea.get('title', '')}</div>
                <div style="font-size: 0.85rem; color: #888;">{idea.get('reason', '')}</div>
                <div style="font-size: 0.75rem; color: #a78bfa; margin-top: 5px;">Inspired by: {idea.get('source', '')}</div>
            </div>
        """, unsafe_allow_html=True)

def render_competitors():
    """Render competitor watch."""
    st.markdown('<div class="section-header youtube">👀 Competitor Watch</div>', unsafe_allow_html=True)
    
    for c in COMPETITORS:
        st.markdown(f"""
            <div class="competitor-item">
                <div>
                    <div class="competitor-name">{c['name']}</div>
                    <div class="competitor-handle">{c['handle']}</div>
                </div>
                <div style="text-align: right;">
                    <div class="competitor-subs">{c['subs']}</div>
                    <div style="font-size: 0.75rem; color: #888;">{c['style']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_youtube_links():
    """Render YouTube quick links."""
    st.markdown('<div class="section-header">🔗 YouTube Links</div>', unsafe_allow_html=True)
    
    links = [
        ("📺 Your Channel", "https://www.youtube.com/channel/UCa8MNaxyYOo7Z--L6STLWLw"),
        ("🎬 YouTube Studio", "https://studio.youtube.com"),
        ("👀 Grace Leung", "https://www.youtube.com/@graceleungyl"),
        ("👀 Sabrina Ramonov", "https://www.youtube.com/@sabrina_ramonov"),
    ]
    
    for label, url in links:
        st.markdown(f'<a href="{url}" target="_blank" class="quick-link">{label}</a>', unsafe_allow_html=True)

# =============================================================================
# DOCS TAB
# =============================================================================

def render_docs_tab():
    """Render the docs tab."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">📁 Working Folder</div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 8px;">
                <a href="https://drive.google.com/drive/folders/1rcxPDxH44qR1qqSHhLTijHUxEHnuEWDw" target="_blank" style="color: #a78bfa; font-size: 1.1rem; text-decoration: none;">📂 Open Charlie's Drive Folder</a>
                <p style="color: #888; font-size: 0.85rem; margin-top: 10px;">This is where Charlie saves docs, reports, and deliverables.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-header" style="margin-top: 20px;">🔗 Key Resources</div>', unsafe_allow_html=True)
        resources = [
            ("🌐 wrightmode.com", "https://wrightmode.com"),
            ("🎯 AI Dream Team", "https://wrightmode.com/aidreamteam"),
            ("👥 Membership", "https://wrightmode.com/membership"),
            ("💼 Consulting", "https://wrightmode.com/consulting"),
            ("📧 Newsletter Signup", "https://wrightmode.myflodesk.com/signup"),
        ]
        for label, url in resources:
            st.markdown(f'<a href="{url}" target="_blank" class="quick-link">{label}</a>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-header">📄 Recent Deliverables</div>', unsafe_allow_html=True)
        st.info("Deliverables will appear here")
        
        st.markdown('<div class="section-header" style="margin-top: 20px;">🛠️ Internal Tools</div>', unsafe_allow_html=True)
        tools = [
            ("⚡ n8n Automations", "https://n8n-wrightmode-u50335.vm.elestio.app"),
            ("📊 Dashboard Repo", "https://github.com/BrookeW1988/charlie-dashboard"),
            ("📁 Docs Repo", "https://github.com/BrookeW1988/wrightmode-docs"),
            ("📱 TikTok Analytics", "https://content-system-theta.vercel.app/"),
        ]
        for label, url in tools:
            st.markdown(f'<a href="{url}" target="_blank" class="quick-link">{label}</a>', unsafe_allow_html=True)

# =============================================================================
# MAIN APP
# =============================================================================

def main():
    # Fetch data
    data = fetch_tasks()
    yt_data = fetch_youtube()
    
    # Render header
    render_header(data)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Growth", "▶️ YouTube", "📁 Docs"])
    
    # =========================================================================
    # DASHBOARD TAB
    # =========================================================================
    with tab1:
        if data:
            render_stats_bar(data)
        
        # Main grid
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Brooke's tasks
            if data:
                render_tasks_column(data.get('forBrooke', []), "For Brooke", "👩", "brooke")
            
            # Conversation summary
            if data:
                st.markdown("<br>", unsafe_allow_html=True)
                render_conversation(data.get('conversation', {}))
        
        with col2:
            # Charlie's tasks
            if data:
                render_tasks_column(data.get('forCharlie', []), "For Charlie", "🤖", "charlie")
            
            # Reminders
            if data:
                st.markdown("<br>", unsafe_allow_html=True)
                render_reminders(data.get('reminders', []))
        
        with col3:
            # Activity log
            if data:
                render_activity_log(data.get('activity', []))
            
            # Quick links
            st.markdown("<br>", unsafe_allow_html=True)
            render_quick_links()
        
        # Work log - full width
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            if data:
                render_work_log(data.get('workLog', []))
        
        with col2:
            if data:
                render_sessions(data.get('sessions', []))
    
    # =========================================================================
    # GROWTH TAB
    # =========================================================================
    with tab2:
        # Workshop countdown at top
        render_workshop_countdown()
        
        # Stats bar
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value" style="color: #22c55e;">$1,470</div>
                    <div class="metric-label">MRR (Membership)</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value" style="color: #f59e0b;">$20K</div>
                    <div class="metric-label">Monthly Goal</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value" style="color: #ef4444;">7%</div>
                    <div class="metric-label">Progress</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Main content
        col1, col2 = st.columns([2, 1])
        
        with col1:
            render_revenue_streams()
        
        with col2:
            render_audience_growth()
            st.markdown("<br>", unsafe_allow_html=True)
            render_monthly_targets()
    
    # =========================================================================
    # YOUTUBE TAB
    # =========================================================================
    with tab3:
        render_youtube_stats(yt_data)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            render_top_videos(yt_data)
            st.markdown("<br>", unsafe_allow_html=True)
            render_content_ideas(yt_data)
        
        with col2:
            render_recent_videos(yt_data)
            st.markdown("<br>", unsafe_allow_html=True)
            render_competitors()
            st.markdown("<br>", unsafe_allow_html=True)
            render_youtube_links()
    
    # =========================================================================
    # DOCS TAB
    # =========================================================================
    with tab4:
        render_docs_tab()

if __name__ == "__main__":
    main()
