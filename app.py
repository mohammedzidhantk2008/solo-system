import streamlit as st
import sqlite3
from datetime import datetime, date
import calendar

# --- PAGE CONFIG ---
st.set_page_config(page_title="Parent Command Center", page_icon="🛡️", layout="centered")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            xp INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            activity TEXT,
            date_str TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_all_users():
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    c.execute("SELECT name FROM users")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

def add_user(name):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, xp) VALUES (?, 0)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def get_user_xp(name):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    c.execute("SELECT xp FROM users WHERE name = ?", (name,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def update_user_xp(name, new_xp):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    c.execute("UPDATE users SET xp = ? WHERE name = ?", (new_xp, name))
    conn.commit()
    conn.close()

def log_activity(name, activity):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    today_str = date.today().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO activity_logs (user_name, activity, date_str, timestamp) VALUES (?, ?, ?, ?)", 
              (name, activity, today_str, current_time))
    conn.commit()
    conn.close()

def get_daily_activity_counts(name):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    c.execute("SELECT date_str, COUNT(*) FROM activity_logs WHERE user_name = ? GROUP BY date_str", (name,))
    counts = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return counts

# --- UI: PARENT COMMAND CENTER ---
st.title("🛡️ Parent Command Center")
st.write("Manage daily habits, mindset milestones, and track consistency heatmaps.")

# Sidebar Profile Management
st.sidebar.header("👥 Child Profiles")
existing_users = get_all_users()

new_child_name = st.sidebar.text_input("Add Child Name:")
if st.sidebar.button("Create Profile"):
    if new_child_name:
        add_user(new_child_name)
        st.sidebar.success(f"Added {new_child_name}!")
        st.rerun()

if existing_users:
    selected_user = st.sidebar.selectbox("Select Active Child:", existing_users)
    user_xp = get_user_xp(selected_user)
    current_level = (user_xp // 100) + 1

    st.sidebar.markdown("---")
    st.sidebar.write(f"**Level:** {current_level} | **XP:** {user_xp}")

    # --- MAIN DASHBOARD TABS ---
    tab1, tab2 = st.tabs(["✅ Daily Quick Log", "📅 Consistency Heatmap"])

    with tab1:
        st.subheader(f"Log Activities for: {selected_user}")
        st.write("Check off completed goals for today to lock in XP and paint the calendar.")

        with st.form("daily_form"):
            st.markdown("### 🌱 Core Habits")
            c1 = st.checkbox("🧘‍♂️ Meditation / Focus Exercise (+20 XP)")
            c2 = st.checkbox("📖 Reading & Expanding Horizons (+30 XP)")
            
            st.markdown("### 📐 Math & Logic")
            c3 = st.checkbox("🔢 Problem Solving / IOQM Prep (+50 XP)")

            st.markdown("### 🧠 Mindset Codex (Stoicism)")
            c4 = st.checkbox("🛡️ Boss Fight: Overcame a hard obstacle (+40 XP)")
            c5 = st.checkbox("🤫 Humble Warrior: Did a good deed quietly (+40 XP)")

            submitted = st.form_submit_button("💾 Save Today's Progress")

            if submitted:
                earned_xp = 0
                tasks = []
                if c1: earned_xp += 20; tasks.append("Meditation")
                if c2: earned_xp += 20; tasks.append("Reading")
                if c3: earned_xp += 50; tasks.append("Math/IOQM")
                if c4: earned_xp += 40; tasks.append("Boss Fight")
                if c5: earned_xp += 40; tasks.append("Humble Warrior")

                if earned_xp > 0:
                    update_user_xp(selected_user, user_xp + earned_xp)
                    for t in tasks:
                        log_activity(selected_user, t)
                    st.balloons()
                    st.success(f"Successfully added +{earned_xp} XP for {selected_user}!")
                    st.rerun()
                else:
                    st.warning("⚠️ Please check off at least one activity before saving.")

    with tab2:
        st.subheader(f"📅 Monthly Consistency Heatmap: {selected_user}")
        st.write("Darker shades indicate active progress days. Matches your consistency tracker.")

        # Render custom calendar heatmap grid matching user's photo reference
        now = datetime.now()
        year, month = now.year, now.month
        activity_data = get_daily_activity_counts(selected_user)

        # Calendar month layout
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]

        st.markdown(f"### **{month_name} {year}**")
        
        # HTML/CSS Table styling for dark theme calendar
        cal_html = """
        <style>
        .heat-cal { width: 100%; border-collapse: collapse; font-family: sans-serif; text-align: center; background-color: #0e1117; color: white; }
        .heat-cal th { padding: 10px; color: #888; font-size: 14px; }
        .heat-cal td { padding: 12px; border: 1px solid #262730; font-size: 14px; border-radius: 4px; }
        .day-box { display: block; width: 30px; height: 30px; line-height: 30px; margin: auto; border-radius: 4px; }
        .level-0 { background-color: #161b22; color: #8b949e; }
        .level-1 { background-color: #5c3a21; color: #ffedd5; }
        .level-2 { background-color: #854d0e; color: #fef08a; font-weight: bold; }
        .level-high { background-color: #a16207; color: #ffffff; font-weight: bold; border: 1px solid #fde047; }
        .today-ring { border: 2px solid #ef4444 !important; }
        </style>
        <table class="heat-cal">
          <tr><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th></tr>
        """

        today_str = now.strftime("%Y-%m-%d")

        for week in cal:
            cal_html += "<tr>"
            for day in week:
                if day == 0:
                    cal_html += "<td></td>"
                else:
                    date_key = f"{year}-{month:02d}-{day:02d}"
                    count = activity_data.get(date_key, 0)
                    
                    # Determine color shade based on activity count
                    if count == 0:
                        css_class = "level-0"
                    elif count <= 2:
                        css_class = "level-1"
                    elif count <= 4:
                        css_class = "level-2"
                    else:
                        css_class = "level-high"
                    
                    is_today = " today-ring" if date_key == today_str else ""
                    
                    cal_html += f'<td><div class="day-box {css_class}{is_today}">{day}</div></td>'
            cal_html += "</tr>"
        
        cal_html += "</table>"
        st.markdown(cal_html, unsafe_allow_html=True)
        st.markdown("<br><p style='color: #888; font-size: 12px;'>* Red ring indicates today's date. Brown heat shading reflects activity density.</p>", unsafe_allow_html=True)

else:
    st.info("👋 Welcome! Create your first child profile using the sidebar input to get started.")