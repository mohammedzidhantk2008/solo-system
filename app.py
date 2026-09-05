import streamlit as st
import sqlite3
from datetime import datetime

# --- DATABASE SETUP FOR MULTI-USER & LOGS ---
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
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO activity_logs (user_name, activity, timestamp) VALUES (?, ?, ?)", (name, activity, current_time))
    conn.commit()
    conn.close()

def get_user_logs(name):
    conn = sqlite3.connect("player_system.db")
    c = conn.cursor()
    c.execute("SELECT activity, timestamp FROM activity_logs WHERE user_name = ? ORDER BY id DESC", (name,))
    logs = c.fetchall()
    conn.close()
    return logs

# --- APP INTERFACE ---
st.title("🛡️ The System: Multi-Generational Roadmap")

# User management in sidebar
st.sidebar.header("👥 Player Management")
existing_users = get_all_users()

new_child_name = st.sidebar.text_input("Add New Child Profile:")
if st.sidebar.button("Create Profile"):
    if new_child_name:
        add_user(new_child_name)
        st.sidebar.success(f"Profile created for {new_child_name}!")
        st.rerun()

if existing_users:
    selected_user = st.sidebar.selectbox("Select Active Player:", existing_users)
    
    user_xp = get_user_xp(selected_user)
    current_level = (user_xp // 100) + 1
    xp_in_current_level = user_xp % 100

    st.sidebar.markdown("---")
    st.sidebar.write(f"**Active Player:** {selected_user}")
    st.sidebar.write(f"**Level:** {current_level}")
    st.sidebar.write(f"**Total XP:** {user_xp}")
    st.sidebar.progress(xp_in_current_level / 100, text=f"Progress: {xp_in_current_level}/100 XP")

    # Module / Section Selection
    app_mode = st.selectbox(
        "Select System Module:",
        [
            "📋 Daily Quests & Age Tiers",
            "📖 Mindset & Wisdom Codex (Stoicism & Mastery)"
        ]
    )

    st.markdown("---")

    if app_mode == "📋 Daily Quests & Age Tiers":
        tier = st.selectbox(
            "Select Player Generation / Age Bracket:",
            [
                "Tier 1: Early Childhood Habits (Ages 5-7)", 
                "Tier 2: Foundation & Reading (Grades 4-5)", 
                "Tier 3: The Awakening / IOQM Prep (Grade 8+)"
            ]
        )

        st.markdown("---")
        earned_xp = 0
        completed_tasks = []

        if tier == "Tier 1: Early Childhood Habits (Ages 5-7)":
            st.header(f"🌱 Tier 1: Core Discipline for {selected_user}")
            meditation = st.checkbox("🧘‍♂️ 5-10 Minutes Quiet Meditation (+20 XP)")
            gratitude = st.checkbox("🌟 Share One Positive Thought of the Day (+20 XP)")
            
            if meditation: earned_xp += 20; completed_tasks.append("Meditation")
            if gratitude: earned_xp += 20; completed_tasks.append("Gratitude")

        elif tier == "Tier 2: Foundation & Reading (Grades 4-5)":
            st.header(f"📚 Tier 2: Expanding Horizons for {selected_user}")
            reading_habit = st.checkbox("📖 Read 20 Pages of a Book / Biography (+30 XP)")
            logic_puzzle = st.checkbox("🧩 Solve a Basic Logic or Puzzles Game (+30 XP)")
            
            if reading_habit: earned_xp += 30; completed_tasks.append("Reading Habit")
            if logic_puzzle: earned_xp += 30; completed_tasks.append("Logic Puzzle")

        elif tier == "Tier 3: The Awakening / IOQM Prep (Grade 8+)":
            st.header(f"📐 Tier 3: Mathematical Awakening for {selected_user}")
            ioqm_problem = st.checkbox("🔢 Solve 3 IOQM / Pre-RMO Level Questions (+50 XP)")
            concept_revision = st.checkbox("📝 Review Fundamental Algebra/Geometry Proofs (+50 XP)")
            
            if ioqm_problem: earned_xp += 50; completed_tasks.append("IOQM Problems")
            if concept_revision: earned_xp += 50; completed_tasks.append("Concept Revision")

        if st.button("💾 Claim Tier Progress XP"):
            if earned_xp > 0:
                new_total_xp = user_xp + earned_xp
                update_user_xp(selected_user, new_total_xp)
                for task in completed_tasks:
                    log_activity(selected_user, f"Completed: {task}")
                st.balloons()
                st.success(f"Successfully claimed +{earned_xp} XP for {selected_user}!")
                st.rerun()
            else:
                st.warning("⚠️ Check off at least one activity before claiming XP.")

    elif app_mode == "📖 Mindset & Wisdom Codex (Stoicism & Mastery)":
        st.header("📖 The Mindset & Wisdom Codex")
        st.write("Inspired by legendary mentors like Ryan Holiday and Robert Greene, translated into the path of a true hero.")
        
        st.markdown("### 1. The Obstacle Is the Way (*The Boss Fight Rule*)")
        st.info("💡 **The Lesson:** When something is hard, frustrating, or goes wrong, don't complain. That obstacle is your training ground. It's the exact test you need to level up.")
        obstacle_quest = st.checkbox("🛡️ Defeated a Hard Challenge: Faced a tough puzzle or problem today without giving up (+40 XP)")

        st.markdown("### 2. Ego Is the Enemy (*The Humble Warrior Rule*)")
        st.info("💡 **The Lesson:** True warriors don't brag about how smart or strong they are. They stay quiet, keep their head down, and let their actions do the talking.")
        ego_quest = st.checkbox("🤫 The Secret Helper: Did a kind act or helped someone today without telling anyone or asking for praise (+40 XP)")

        st.markdown("### 3. Mastery (*The Apprentice Rule*)")
        st.info("💡 **The Lesson:** Nobody is born a master. Greatness comes from falling in love with practice and putting in focused repetition every single day.")
        mastery_quest = st.checkbox("⚙️ Deep Focus Training: Spent 15 minutes practicing a core skill (drawing, reading, or math) with zero distractions (+40 XP)")

        codex_earned_xp = 0
        codex_tasks = []

        if obstacle_quest: codex_earned_xp += 40; codex_tasks.append("Mindset: Obstacle Overcome")
        if ego_quest: codex_earned_xp += 40; codex_tasks.append("Mindset: Humble Warrior Act")
        if mastery_quest: codex_earned_xp += 40; codex_tasks.append("Mindset: Mastery Practice")

        if st.button("💾 Claim Wisdom Codex XP"):
            if codex_earned_xp > 0:
                new_total_xp = user_xp + codex_earned_xp
                update_user_xp(selected_user, new_total_xp)
                for task in codex_tasks:
                    log_activity(selected_user, f"Completed: {task}")
                st.balloons()
                st.success(f"Successfully claimed +{codex_earned_xp} Wisdom XP for {selected_user}!")
                st.rerun()
            else:
                st.warning("⚠️ Complete a mindset challenge before claiming XP.")

    # Show History & Everyday Statistics
    st.markdown("---")
    st.subheader(f"📅 Activity History & Timestamps for {selected_user}")
    logs = get_user_logs(selected_user)
    if logs:
        for activity, timestamp in logs:
            st.write(f"* **{timestamp}** — {activity}")
    else:
        st.info("No activity logs recorded yet. Complete quests to build your history!")

else:
    st.warning("⚠️ No profiles found. Please create a child profile using the sidebar input first.")