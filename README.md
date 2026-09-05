# 🛡️ Parent Command Center & Mentorship System

## 🌟 Overview
A secure, multi-generational habit tracking and mentorship web application designed for parental oversight and long-term personal development. It features a password-protected administrative portal and age-adaptive child portals that evolve dynamically as the child matures.

## 🚀 Key Features
1. **Dual-Portal Architecture:**
   - **Parent Admin Portal:** Protected by a secure PIN (`1984`), allowing parents to manage child profiles, configure age parameters, and review cross-tier consistency heatmaps.
   - **Child Player Portal:** A gamified experience where children log daily quests and track their XP and levels.
2. **Age-Adaptive Dynamic Styling Engine:** 
   - **Ages 5–7:** High-energy, sharp orange and black palette optimized for young kids.
   - **Ages 8–13:** Gaming-inspired indigo and cosmic interface.
   - **Ages 14+:** Minimalist dark-mode cyberpunk/terminal aesthetic tailored for advanced study and focus.
3. **Age-Gating & Security:** Advanced tiers remain strictly locked until the child reaches the required age tier or parental authorization is updated.
4. **Anti-Cheat Mechanics:** Enforces a once-per-day submission lock to prevent infinite XP farming and preserve authentic habit discipline.
5. **Consistency Heatmap:** Built-in monthly calendar view displaying daily activity density at a glance.

## 💻 Tech Stack
- **Language:** Python
- **Framework:** Streamlit
- **Database:** SQLite (`player_system.db`)
- **Styling:** Dynamic CSS-in-Python injection based on age brackets
