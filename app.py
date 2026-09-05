import streamlit as st
import sqlite3
from datetime import datetime, date
import calendar

# --- PAGE CONFIG ---
st.set_page_config(page_title="The System: Adaptive Command Center", page_icon="🛡️", layout="centered")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            xp INTEGER
        )
    ''')
    
    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]
    if 'age' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN age INTEGER DEFAULT 6")

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
    c.execute("SELECT name, age FROM users")
    users = c.fetchall()
    conn.close()
    return users

def add_user(name, age):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, age, xp) VALUES (?, ?, 0)", (name, age))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def get_user_data(name):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    c.execute("SELECT age, xp FROM users WHERE name = ?", (name,))
    result = c.fetchone()
    conn.close()
    return result if result else (0, 0)

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

def has_logged_today(name):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    today_str = date.today().strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(*) FROM activity_logs WHERE user_name = ? AND date_str = ?", (name, today_str))
    count = c.fetchone()[0]
    conn.close()
    return count > 0

def get_daily_activity_counts(name):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    c.execute("SELECT date_str, COUNT(*) FROM activity_logs WHERE user_name = ? GROUP BY date_str", (name,))
    counts = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return counts

# --- ADVANCED DYNAMIC DESIGN SYSTEM ---
def apply_dynamic_theme(age):
    if age <= 7:
        # TIER 1: Sleek Orange & Black (Energetic, sharp, not too babyish)
        theme_css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700&display=swap');
            html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #121212; color: #f3f4f6; }
            .stApp { background: linear-gradient(135deg, #0f0f0f 0%, #1c140f 100%); }
            h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif !important; color: #ff7700 !important; font-weight: 700; }
            .stButton>button { background: linear-gradient(90deg, #ff7700 0%, #e65c00 100%); color: white; border-radius: 8px; font-weight: 700; border: none; box-shadow: 0 4px 12px rgba(255, 119, 0, 0.3); }
            div.stCheckbox { background-color: #1a1a1a; padding: 12px 16px; border-radius: 8px; border: 1px solid #332211; margin-bottom: 8px; }
            div.stCheckbox:hover { border-color: #ff7700; }
        </style>
        """
    elif 8 <= age <= 13:
        # TIER 2: Gaming Indigo
        theme_css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@400;600&display=swap');
            html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; }
            .stApp { background: radial-gradient(circle at top, #1e1b4b 0%, #0f172a 100%); }
            h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; color: #c084fc !important; }
            .stButton>button { background: linear-gradient(90deg, #7c3aed 0%, #db2777 100%); color: white; border-radius: 8px; font-weight: 600; }
            div.stCheckbox { background-color: rgba(30, 41, 59, 0.7); padding: 12px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 8px; }
        </style>
        """
    else:
        # TIER 3: Elite Minimalist Cyber / JEE Dark Mode
        theme_css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
            html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #050505; color: #ededed; }
            .stApp { background-color: #050505; background-image: radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 0); background-size: 24px 24px; }
            h1, h2, h3 { font-family: 'JetBrains Mono', monospace !important; color: #38bdf8 !important; }
            .stButton>button { background: #0f172a; color: #38bdf8; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-weight: 600; border: 1px solid #38bdf8; }
            .stButton>button:hover { background: #38bdf8; color: #050505; }
            div.stCheckbox { background-color: #0a0a0a; padding: 14px; border-radius: 8px; border: 1px solid #262626; margin-bottom: 8px; }
        </style>
        """
    st.markdown(theme_css, unsafe_allow_html=True)

# --- NAVIGATION PORTAL ---
st.sidebar.title("🛡️ System Gate")
portal_mode = st.sidebar.radio("Select Portal:", ["🎮 Child Player Portal", "🔒 Parent Admin Portal"])
users_list = get_all_users()

if portal_mode == "🔒 Parent Admin Portal":
    st.markdown("<style>.stApp { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)
    st.title("🔒 Parent Command Center")
    st.write("Secure oversight: Manage profiles, update age parameters, and analyze cross-tier consistency.")
    
    parent_pin = st.text_input("Enter Parent Admin PIN:", type="password")
    
    if parent_pin == "1984":
        st.success("Access Granted, Architect.")
        st.markdown("---")
        
        st.subheader("👥 Manage Child Profiles & Adaptive Ages")
        with st.form("add_profile_form"):
            new_name = st.text_input("Child Name:")
            new_age = st.number_input("Child Age (Controls UI Theme & Unlocks):", min_value=3, max_value=20, value=6)
            submitted_profile = st.form_submit_button("Create / Update Profile")
            if submitted_profile and new_name:
                add_user(new_name, int(new_age))
                st.success(f"Profile saved for {new_name} (Age: {new_age})!")
                st.rerun()
        
        if users_list:
            st.markdown("### Active Profiles:")
            for name, age in users_list:
                age_val, xp_val = get_user_data(name)
                st.write(f"- **{name}** | Age Level: {age_val} | Total XP: {xp_val}")
                
            st.markdown("---")
            st.subheader("📊 Analytics & Heatmap Viewer")
            admin_selected_user = st.selectbox("Select Child to Inspect:", [u[0] for u in users_list])
            
            now = datetime.now()
            year, month = now.year, now.month
            activity_data = get_daily_activity_counts(admin_selected_user)
            cal = calendar.monthcalendar(year, month)
            
            st.markdown(f"#### Consistency Heatmap for {admin_selected_user}")
            cal_html = """
            <style>
            .heat-cal { width: 100%; border-collapse: collapse; font-family: sans-serif; text-align: center; background-color: #121212; color: white; }
            .heat-cal th { padding: 8px; color: #888; font-size: 13px; }
            .heat-cal td { padding: 10px; border: 1px solid #262626; font-size: 13px; border-radius: 4px; }
            .day-box { display: block; width: 25px; height: 25px; line-height: 25px; margin: auto; border-radius: 4px; }
            .level-0 { background-color: #1a1a1a; color: #666; }
            .level-1 { background-color: #ff7700; color: #ffffff; }
            .level-2 { background-color: #cc5500; color: #ffffff; font-weight: bold; }
            </style>
            <table class="heat-cal">
              <tr><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th></tr>
            """
            for week in cal:
                cal_html += "<tr>"
                for day in week:
                    if day == 0:
                        cal_html += "<td></td>"
                    else:
                        date_key = f"{year}-{month:02d}-{day:02d}"
                        count = activity_data.get(date_key, 0)
                        css_class = "level-0" if count == 0 else ("level-1" if count <= 2 else "level-2")
                        cal_html += f'<td><div class="day-box {css_class}">{day}</div></td>'
                cal_html += "</tr>"
            cal_html += "</table>"
            st.markdown(cal_html, unsafe_allow_html=True)
        else:
            st.info("No profiles found. Create one above.")
            
    elif parent_pin != "":
        st.error("❌ Incorrect PIN.")
    else:
        st.info("ℹ️ Enter parent PIN to access administrative management.")

elif portal_mode == "🎮 Child Player Portal":
    if not users_list:
        st.warning("⚠️ No profiles registered. Ask your parent to configure a profile in the Parent Admin Portal.")
    else:
        child_names = [u[0] for u in users_list]
        selected_child = st.selectbox("Select Your Profile:", child_names)
        
        child_age, child_xp = get_user_data(selected_child)
        apply_dynamic_theme(child_age)
        
        current_level = (child_xp // 100) + 1
        xp_in_level = child_xp % 100
        
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Player:** {selected_child}")
        st.sidebar.markdown(f"**Age Index:** {child_age}")
        st.sidebar.markdown(f"**Level:** {current_level}")
        st.sidebar.progress(xp_in_level / 100, text=f"XP: {child_xp}")
        
        st.title(f"⚡ System Portal // Operative: {selected_child}")
        st.markdown("---")
        
        already_submitted = has_logged_today(selected_child)
        
        if already_submitted:
            st.success("🎉 **Daily Quests Already Completed Today!**")
            st.info("You have already locked in your progress for today. Come back tomorrow to keep your streak alive and earn more XP!")
        else:
            if child_age <= 7:
                st.header("🌱 Tier 1: Core Habits & Focus")
                st.write("Build consistency through daily focus and mindset awareness.")
                
                with st.form("tier1_form"):
                    # Clean specific task names without heavy emoji clutter
                    c1 = st.checkbox("Meditation: 5-10 Minutes Quiet Focus (+20 XP)")
                    c2 = st.checkbox("Gratitude: Share One Positive Thought of the Day (+20 XP)")
                    submitted_t1 = st.form_submit_button("💾 Claim Quests")
                    
                    if submitted_t1:
                        earned = 0
                        tasks = []
                        if c1: earned += 20; tasks.append("Meditation")
                        if c2: earned += 20; tasks.append("Gratitude")
                        
                        if earned > 0:
                            update_user_xp(selected_child, child_xp + earned)
                            for t in tasks: log_activity(selected_child, t)
                            st.balloons()
                            st.success(f"Fantastic! Earned +{earned} XP.")
                            st.rerun()
                        else:
                            st.warning("Check off an activity to claim rewards.")
                
                st.markdown("---")
                st.markdown("🔒 **Tier 2 (Ages 8-13):** *Locked until system age requirement is met.*")
                st.markdown("🔒 **Tier 3 (Ages 14+):** *Locked until system age requirement is met.*")

            elif 8 <= child_age <= 13:
                st.header("📚 Tier 2: Expanding Horizons & Logic")
                st.write("Core Protocol: Cultivate continuous learning, literature immersion, and logical reasoning.")
                
                with st.form("tier2_form"):
                    c1 = st.checkbox("Reading: Read 20 Pages of a Book / Biography (+30 XP)")
                    c2 = st.checkbox("Logic: Solve a Logic Puzzle or Strategy Challenge (+30 XP)")
                    submitted_t2 = st.form_submit_button("💾 Claim Quests")
                    
                    if submitted_t2:
                        earned = 0
                        tasks = []
                        if c1: earned += 30; tasks.append("Reading Habit")
                        if c2: earned += 30; tasks.append("Logic Puzzle")
                        
                        if earned > 0:
                            update_user_xp(selected_child, child_xp + earned)
                            for t in tasks: log_activity(selected_child, t)
                            st.balloons()
                            st.success(f"Mission complete! Earned +{earned} XP.")
                            st.rerun()
                        else:
                            st.warning("Check off an activity to claim rewards.")
                
                st.markdown("---")
                st.markdown("✅ **Tier 1:** *Mastered*")
                st.markdown("🔒 **Tier 3 (Ages 14+):** *Locked until system age requirement is met.*")

            else:
                st.header("📐 Tier 3: Advanced Architect Protocol & Mindset Codex")
                st.write("Advanced Directive: High-level problem solving, Stoic resilience, and deep mastery.")
                
                with st.form("tier3_form"):
                    c1 = st.checkbox("Advanced Math: Solve Competitive Problems (+50 XP)")
                    c2 = st.checkbox("Boss Fight: Overcame a hard obstacle without quitting (+40 XP)")
                    c3 = st.checkbox("Humble Warrior: Executed a disciplined act quietly (+40 XP)")
                    submitted_t3 = st.form_submit_button("💾 Commit Progress")
                    
                    if submitted_t3:
                        earned = 0
                        tasks = []
                        if c1: earned += 50; tasks.append("Advanced Math")
                        if c2: earned += 40; tasks.append("Boss Fight")
                        if c3: earned += 40; tasks.append("Humble Warrior")
                        
                        if earned > 0:
                            update_user_xp(selected_child, child_xp + earned)
                            for t in tasks: log_activity(selected_child, t)
                            st.balloons()
                            st.success(f"Sync successful. Earned +{earned} XP.")
                            st.rerun()
                        else:
                            st.warning("Check off an activity to commit progress.")
                
                st.markdown("---")
                st.markdown("✅ **Tier 1 & Tier 2:** *Mastered & Unlocked*")