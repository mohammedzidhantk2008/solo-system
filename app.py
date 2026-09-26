import streamlit as st
import sqlite3
from datetime import datetime, date
import calendar

# --- PAGE CONFIG ---
st.set_page_config(page_title="Student Dashboard", page_icon="📚", layout="centered")

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
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS mindset_journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            reflection TEXT,
            date_str TEXT
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

def save_mindset_reflection(name, reflection):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    today_str = date.today().strftime("%Y-%m-%d")
    c.execute("INSERT INTO mindset_journal (user_name, reflection, date_str) VALUES (?, ?, ?)", (name, reflection, today_str))
    conn.commit()
    conn.close()

def get_daily_activity_counts(name):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    c.execute("SELECT date_str, COUNT(*) FROM activity_logs WHERE user_name = ? GROUP BY date_str", (name,))
    counts = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return counts

# --- DYNAMIC THEME ENGINE ---
def apply_dynamic_theme(age):
    if age <= 7:
        theme_css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700&display=swap');
            html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #121212; color: #f3f4f6; }
            .stApp { background: linear-gradient(135deg, #0f0f0f 0%, #1c140f 100%); }
            h1, h2, h3 { color: #ff7700 !important; font-weight: 700; }
            .stButton>button { background: linear-gradient(90deg, #ff7700 0%, #e65c00 100%); color: white; border-radius: 8px; font-weight: 700; border: none; }
            div.stCheckbox { background-color: #1a1a1a; padding: 12px 16px; border-radius: 8px; border: 1px solid #332211; margin-bottom: 8px; }
        </style>
        """
    elif 8 <= age <= 13:
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
        theme_css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
            html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #050505; color: #ededed; }
            .stApp { background-color: #050505; background-image: radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 0); background-size: 24px 24px; }
            h1, h2, h3 { font-family: 'JetBrains Mono', monospace !important; color: #38bdf8 !important; }
            .stButton>button { background: #0f172a; color: #38bdf8; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-weight: 600; border: 1px solid #38bdf8; }
            div.stCheckbox { background-color: #0a0a0a; padding: 14px; border-radius: 8px; border: 1px solid #262626; margin-bottom: 8px; }
        </style>
        """
    st.markdown(theme_css, unsafe_allow_html=True)

# --- PORTAL ROUTING ---
st.sidebar.title("🧭 Navigation")
portal_mode = st.sidebar.radio("Select Portal:", ["Student Portal", "Admin Panel"])
users_list = get_all_users()

if portal_mode == "Admin Panel":
    st.markdown("<style>.stApp { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)
    st.title("🔒 Admin Panel")
    st.write("Manage student profiles, configure age levels, and review activity consistency.")
    
    parent_pin = st.text_input("Enter Admin PIN:", type="password")
    
    if parent_pin == "1984":
        st.success("Access Granted.")
        st.markdown("---")
        
        st.subheader("👥 Manage Profiles")
        with st.form("add_profile_form"):
            new_name = st.text_input("Student Name:")
            new_age = st.number_input("Student Age:", min_value=3, max_value=20, value=6)
            submitted_profile = st.form_submit_button("Save Profile")
            if submitted_profile and new_name:
                add_user(new_name, int(new_age))
                st.success(f"Profile saved for {new_name} (Age: {new_age})!")
                st.rerun()
        
        if users_list:
            st.markdown("### Registered Profiles:")
            for name, age in users_list:
                age_val, xp_val = get_user_data(name)
                st.write(f"- **{name}** | Age: {age_val} | Total XP: {xp_val}")
                
            st.markdown("---")
            st.subheader("📊 Activity Heatmap")
            admin_selected_user = st.selectbox("Select Student:", [u[0] for u in users_list])
            
            now = datetime.now()
            year, month = now.year, now.month
            activity_data = get_daily_activity_counts(admin_selected_user)
            cal = calendar.monthcalendar(year, month)
            
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
            st.info("No profiles found.")
            
    elif parent_pin != "":
        st.error("Incorrect PIN.")

elif portal_mode == "Student Portal":
    if not users_list:
        st.warning("⚠️ No profiles registered. Please add one in the Admin Panel.")
    else:
        child_names = [u[0] for u in users_list]
        selected_child = st.selectbox("Select Profile:", child_names)
        
        child_age, child_xp = get_user_data(selected_child)
        apply_dynamic_theme(child_age)
        
        current_level = (child_xp // 100) + 1
        xp_in_level = child_xp % 100
        
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Student:** {selected_child}")
        st.sidebar.markdown(f"**Age:** {child_age}")
        st.sidebar.markdown(f"**Level:** {current_level}")
        st.sidebar.progress(xp_in_level / 100, text=f"XP: {child_xp}")
        
        st.title(f"🚀 Dashboard - {selected_child}")
        st.markdown("---")
        
        already_submitted = has_logged_today(selected_child)
        
        if already_submitted:
            st.success("🎯 Daily tasks already completed for today.")
            st.info("💡 Come back tomorrow to continue your streak.")
        else:
            if child_age <= 7:
                st.header("🌱 Daily Habits")
                st.write("Complete your daily focus tasks.")
                
                with st.form("tier1_form"):
                    c1 = st.checkbox("🧘‍♂️ Meditation: 5-10 Minutes Quiet Focus (+20 XP)")
                    c2 = st.checkbox("⭐ Gratitude: Share One Positive Thought of the Day (+20 XP)")
                    submitted_t1 = st.form_submit_button("💾 Submit Tasks")
                    
                    if submitted_t1:
                        earned = 0
                        tasks = []
                        if c1: earned += 20; tasks.append("Meditation")
                        if c2: earned += 20; tasks.append("Gratitude")
                        
                        if earned > 0:
                            update_user_xp(selected_child, child_xp + earned)
                            for t in tasks: log_activity(selected_child, t)
                            st.success(f"✨ Earned +{earned} XP.")
                            st.rerun()
                        else:
                            st.warning("⚠️ Select at least one task.")
                
            elif 8 <= child_age <= 13:
                st.header("📚 Learning & Logic")
                st.write("Complete your daily reading and logic challenges.")
                
                with st.form("tier2_form"):
                    c1 = st.checkbox("📖 Reading: Read 20 Pages of a Book (+30 XP)")
                    c2 = st.checkbox("🧩 Logic: Solve a Logic Puzzle (+30 XP)")
                    submitted_t2 = st.form_submit_button("💾 Submit Tasks")
                    
                    if submitted_t2:
                        earned = 0
                        tasks = []
                        if c1: earned += 30; tasks.append("Reading Habit")
                        if c2: earned += 30; tasks.append("Logic Puzzle")
                        
                        if earned > 0:
                            update_user_xp(selected_child, child_xp + earned)
                            for t in tasks: log_activity(selected_child, t)
                            st.success(f"⚡ Earned +{earned} XP.")
                            st.rerun()
                        else:
                            st.warning("⚠️ Select at least one task.")
            else:
                st.header("⚡ Advanced Study & Discipline")
                st.write("Log your advanced problem solving and resilience tasks.")
                
                with st.form("tier3_form"):
                    c1 = st.checkbox("📐 Advanced Math: Solve Competitive Problems (+50 XP)")
                    c2 = st.checkbox("🛡️ Resilience: Overcame a Hard Obstacle (+40 XP)")
                    c3 = st.checkbox("⚙️ Discipline: Executed a Task Quietly (+40 XP)")
                    submitted_t3 = st.form_submit_button("💾 Submit Tasks")
                    
                    if submitted_t3:
                        earned = 0
                        tasks = []
                        if c1: earned += 50; tasks.append("Advanced Math")
                        if c2: earned += 40; tasks.append("Resilience")
                        if c3: earned += 40; tasks.append("Quiet Discipline")
                        
                        if earned > 0:
                            update_user_xp(selected_child, child_xp + earned)
                            for t in tasks: log_activity(selected_child, t)
                            st.success(f"🔥 Earned +{earned} XP.")
                            st.rerun()
                        else:
                            st.warning("⚠️ Select at least one task.")

        # --- REFLECTION JOURNAL ---
        st.markdown("---")
        st.subheader("📝 Daily Journal & Reflection")
        st.write("Write down an obstacle you faced today and how you handled it:")
        with st.form("mindset_form"):
            reflection_text = st.text_area("Journal Entry:")
            ref_submitted = st.form_submit_button("💾 Save Entry")
            if ref_submitted and reflection_text:
                save_mindset_reflection(selected_child, reflection_text)
                st.success("✅ Journal entry saved.")
                import sqlite3
import streamlit as st


# Initialize database connection for the 45-Day Checklist module
def init_db():
  conn = sqlite3.connect("study_tracker.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS checklist_45days (
            day_num INTEGER PRIMARY KEY,
            phase TEXT,
            schedule_context TEXT,
            lecture_target TEXT,
            lectures_done TEXT,
            questions_done TEXT
        )
    """)
  conn.commit()
  return conn, cursor


# Pre-populate initial structure if empty (matching the 45-day layout)
def seed_initial_data(cursor, conn):
  cursor.execute("SELECT COUNT(*) FROM checklist_45days")
  if cursor.fetchone()[0] == 0:
    # Phase 1: Days 1 to 21 (Exam Leave)
    for d in range(1, 22):
      phase = "Phase 1: Exam Leave (Days 1 - 21)"
      context = "Exam Leave (Self-Study Hours)"
      target = "Watch 4 Lectures & Practice Qs"
      cursor.execute(
          "INSERT OR IGNORE INTO checklist_45days VALUES (?, ?, ?, ?, ?, ?)",
          (d, phase, context, target, "", "Pending"),
      )
    # Phase 2: Days 22 to 45 (School Reopened)
    for d in range(22, 46):
      phase = "Phase 2: School Reopened (Days 22 - 45)"
      context = (
          "School Evening Routine"
          if d % 7 not in [5, 6]
          else "Weekend Revise/Session"
      )
      target = (
          "Watch 3 Lectures & Practice Qs"
          if d % 7 not in [5, 6]
          else "Watch 4 Lectures & Practice Qs"
      )
      cursor.execute(
          "INSERT OR IGNORE INTO checklist_45days VALUES (?, ?, ?, ?, ?, ?)",
          (d, phase, context, target, "", "Pending"),
      )
    conn.commit()


def render_45day_checklist_module():
  st.subheader("📋 45-Day Study Plan Master Checklist")
  conn, cursor = init_db()
  seed_initial_data(cursor, conn)

  # Filter by Phase
  phase_filter = st.selectbox(
      "Filter Phase",
      [
          "All",
          "Phase 1: Exam Leave (Days 1 - 21)",
          "Phase 2: School Reopened (Days 22 - 45)",
      ],
  )

  if phase_filter == "All":
    cursor.execute("SELECT * FROM checklist_45days ORDER BY day_num")
  else:
    cursor.execute(
        "SELECT * FROM checklist_45days WHERE phase = ? ORDER BY day_num",
        (phase_filter,),
    )

  rows = cursor.fetchall()

  st.markdown("---")
  for row in rows:
    day_num, phase, context, target, lectures_done, questions_done = row

    with st.expander(
        f"Day {day_num} | {context} [{'✅ Done' if questions_done == 'Completed' else '⏳ Pending'}]"
    ):
      cols = st.columns([2, 2, 2])
      with cols[0]:
        st.write(f"**Phase:** {phase}")
        st.write(f"**Context:** {context}")
      with cols[1]:
        st.write(f"**Target:** {target}")
        # Multi-select or checkboxes for lectures 1 to 4/6
        current_done = (
            [int(x) for x in lectures_done.split(",") if x.isdigit()]
            if lectures_done
            else []
        )
        selected_lectures = st.multiselect(
            f"Lectures Done (Day {day_num})",
            options=[1, 2, 3, 4, 5, 6],
            default=current_done,
            key=f"lec_{day_num}",
        )
      with cols[2]:
        q_status = st.selectbox(
            f"Questions Done (Day {day_num})",
            ["Pending", "Completed"],
            index=0 if questions_done != "Completed" else 1,
            key=f"q_{day_num}",
        )

        if st.button(f"Save Day {day_num}", key=f"btn_{day_num}"):
          lectures_str = ",".join(map(str, selected_lectures))
          cursor.execute(
              """UPDATE checklist_45days 
                             SET lectures_done = ?, questions_done = ? 
                             WHERE day_num = ?""",
              (lectures_str, q_status, day_num),
          )
          conn.commit()
          st.success(f"Saved Day {day_num} successfully!")
          st.rerun()


# Make sure this line exists somewhere in your main execution flow in app.py:
render_45day_checklist_module()