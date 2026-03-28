import streamlit as st
import json
import random
from datetime import datetime, timedelta
import pandas as pd

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Chubby's Chicken — Content Intelligence",
    page_icon="🍗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Brand Styling ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main { background-color: #0f0f0f; }
    
    .stApp {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    
    .brand-header {
        background: linear-gradient(135deg, #FF4500, #FF6B00);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .brand-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .brand-header p {
        color: rgba(255,255,255,0.85);
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }
    
    .metric-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        color: #FF4500;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0 0 0.5rem 0;
    }
    
    .metric-card .value {
        color: white;
        font-size: 2rem;
        font-weight: 900;
        line-height: 1;
    }
    
    .metric-card .delta {
        color: #00C851;
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }
    
    .concept-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-left: 4px solid #FF4500;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .concept-card h4 {
        color: #FF4500;
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        font-weight: 700;
    }
    
    .concept-card p {
        color: #cccccc;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .concept-card .tag {
        display: inline-block;
        background: #FF4500;
        color: white;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 20px;
        margin-top: 0.75rem;
        margin-right: 0.25rem;
        text-transform: uppercase;
    }
    
    .competitor-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .competitor-card h4 {
        color: white;
        margin: 0 0 0.25rem 0;
    }
    
    .competitor-card .handle {
        color: #FF4500;
        font-size: 0.85rem;
        margin: 0 0 0.75rem 0;
    }
    
    .trend-pill {
        display: inline-block;
        background: #2a2a2a;
        color: #FF6B00;
        border: 1px solid #FF4500;
        font-size: 0.8rem;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 0.25rem;
    }
    
    .calendar-day {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 0.75rem;
        min-height: 80px;
    }
    
    .calendar-day.has-post {
        border-color: #FF4500;
    }
    
    .calendar-day h5 {
        color: #888;
        font-size: 0.7rem;
        text-transform: uppercase;
        margin: 0 0 0.5rem 0;
    }
    
    .calendar-day .post-item {
        background: #FF4500;
        color: white;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 4px;
        margin-bottom: 3px;
    }
    
    .shot-item {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
    }

    div[data-testid="stTabs"] button {
        color: #888 !important;
        font-weight: 600;
    }
    
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #FF4500 !important;
        border-bottom-color: #FF4500 !important;
    }
    
    .stButton > button {
        background: #FF4500;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 700;
    }
    
    .stButton > button:hover {
        background: #FF6B00;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-header">
    <h1>🍗 Chubby's Chicken</h1>
    <p>Content Intelligence Dashboard · Powered by Hyperwave Studios</p>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Analytics",
    "🔥 Trending Intel",
    "👀 Competitor Watch",
    "💡 Content Concepts",
    "📅 Content Calendar"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## 📊 Chubby's Instagram Analytics")
    st.markdown("*Upload your Instagram Insights export (CSV) or view sample data below.*")
    
    uploaded_file = st.file_uploader("Upload Instagram Insights CSV", type="csv", key="analytics_upload")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("📁 No CSV uploaded — showing sample data. Export your Instagram Insights and upload above.")
        
        # Sample metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Followers</h3>
                <div class="value">4,821</div>
                <div class="delta">↑ +127 this month</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>Avg Engagement</h3>
                <div class="value">6.2%</div>
                <div class="delta">↑ +0.8% vs last month</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>Reach (30d)</h3>
                <div class="value">28.4K</div>
                <div class="delta">↑ +12% vs last month</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>Reels Plays</h3>
                <div class="value">142K</div>
                <div class="delta">↑ +34% vs last month</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 📈 Follower Growth (Last 30 Days)")
        
        # Sample chart data
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        followers = [4600 + i * 7 + random.randint(-5, 15) for i in range(30)]
        chart_df = pd.DataFrame({"Date": dates, "Followers": followers})
        st.line_chart(chart_df.set_index("Date"), color="#FF4500")
        
        st.markdown("### 🏆 Top Performing Posts")
        
        top_posts = [
            {"Post": "🔥 Nashville Tenders Drop", "Plays": "38,200", "Likes": "1,840", "Comments": "94", "Saved": "312"},
            {"Post": "🍗 The Chubby Combo Reveal", "Plays": "27,100", "Likes": "1,220", "Comments": "67", "Saved": "198"},
            {"Post": "🌶️ Spice Level Challenge", "Plays": "21,400", "Likes": "980", "Comments": "143", "Saved": "87"},
            {"Post": "🧑‍🍳 Kitchen Behind the Scenes", "Plays": "18,900", "Likes": "890", "Comments": "51", "Saved": "234"},
            {"Post": "🥗 Chubby Fries Closeup", "Plays": "15,600", "Likes": "720", "Comments": "38", "Saved": "156"},
        ]
        
        st.dataframe(pd.DataFrame(top_posts), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: TRENDING INTEL
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## 🔥 Trending in Nashville Hot Chicken")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎵 Trending Audios Right Now")
        
        audios = [
            {"Audio": "original sound - foodie_kings", "Uses": "124K", "Trend": "🔥 Exploding"},
            {"Audio": "Kehlani - Nights Like This (sped up)", "Uses": "98K", "Trend": "📈 Rising"},
            {"Audio": "original sound - grwm.food", "Uses": "76K", "Trend": "📈 Rising"},
            {"Audio": "Lil Durk - The Voice (slowed)", "Uses": "64K", "Trend": "⚡ Hot"},
            {"Audio": "original sound - chickenfever", "Uses": "51K", "Trend": "🔥 Exploding"},
            {"Audio": "Rod Wave - Smooth Sailing", "Uses": "43K", "Trend": "📈 Rising"},
        ]
        
        for audio in audios:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎵 {audio['Audio']}</h3>
                <div style="color:white; font-size:1.1rem; font-weight:700;">{audio['Uses']} uses</div>
                <div style="color:#FF6B00; font-size:0.85rem;">{audio['Trend']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎬 Trending Content Formats")
        
        formats = [
            {
                "format": "The Crispy Pull-Apart",
                "desc": "Close-up slow-mo of pulling apart a crispy tender. ASMR vibes. Insane engagement on food accounts right now.",
                "tags": ["#ASMR", "#SlowMo", "#FoodPorn"]
            },
            {
                "format": "Spice Level Reaction",
                "desc": "Customer tries your hottest level on camera. Authentic reactions = massive shares and comments.",
                "tags": ["#SpiceChallenge", "#Challenge"]
            },
            {
                "format": "Day In The Kitchen POV",
                "desc": "First-person cook's perspective. People love seeing behind the scenes of how food is made.",
                "tags": ["#BehindTheScenes", "#POV", "#Chef"]
            },
            {
                "format": "The Stack Shot",
                "desc": "Building the sandwich from bottom to top, each ingredient dropping in slow motion.",
                "tags": ["#FoodBuild", "#ASMR", "#Satisfying"]
            },
            {
                "format": "Local Love Story",
                "desc": "Interview a regular customer. 'Why do you keep coming back?' — authenticity wins every time.",
                "tags": ["#LocalBusiness", "#Community"]
            },
        ]
        
        for f in formats:
            tags_html = " ".join([f'<span class="tag">{t}</span>' for t in f["tags"]])
            st.markdown(f"""
            <div class="concept-card">
                <h4>🎬 {f['format']}</h4>
                <p>{f['desc']}</p>
                {tags_html}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### 🏷️ Top Hashtags in the Space")
    
    hashtags = ["#nashvillehotchicken", "#hotchicken", "#friedchicken", "#chickensandwich", 
                "#foodie", "#foodreels", "#eatlocal", "#inlandempirefood", "#fontanaeats",
                "#socaleats", "#hotchickensandwich", "#crispychicken", "#chickentenders",
                "#spicyfood", "#foodporn", "#reelsfood", "#foodtok", "#chickenlover"]
    
    pills_html = " ".join([f'<span class="trend-pill">{h}</span>' for h in hashtags])
    st.markdown(f'<div style="line-height:2.5">{pills_html}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: COMPETITOR WATCH
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## 👀 Competitor Watch")
    st.markdown("*Accounts we're monitoring in the Nashville hot chicken + SoCal food space.*")
    
    competitors = [
        {
            "name": "Howlin' Ray's",
            "handle": "@howlinrays",
            "location": "Los Angeles, CA",
            "followers": "89K",
            "posting": "4-5x/week",
            "whats_working": "Behind-the-scenes kitchen clips, spice challenge reactions, slow-mo food shots. Very consistent aesthetic — warm tones, tight crops.",
            "steal_this": "Their 'spice reaction' series gets 50K+ views consistently. Authentic, unscripted customer moments."
        },
        {
            "name": "Angry Chickz",
            "handle": "@theangrychickz",
            "location": "SoCal (multiple IE locations)",
            "followers": "42K",
            "posting": "3-4x/week",
            "whats_working": "High energy reels with trending audio, showcasing menu variety and heat levels. Heavy use of user-generated content.",
            "steal_this": "They repost customer content constantly — low effort, high trust. Chubby's should be doing this."
        },
        {
            "name": "Legend Hot Chicken",
            "handle": "@legendhotchicken",
            "location": "Chino Hills, CA",
            "followers": "18K",
            "posting": "2-3x/week",
            "whats_working": "Local community feel, consistent branding, heavy food closeups. Tags local food bloggers.",
            "steal_this": "Actively engages with IE food influencers. Good relationship-building play for Chubby's too."
        },
        {
            "name": "Dave's Hot Chicken",
            "handle": "@daveshotchicken",
            "location": "National chain",
            "followers": "312K",
            "posting": "Daily",
            "whats_working": "Meme-heavy content, celebrity collabs, extreme heat challenges. Very internet-native brand voice.",
            "steal_this": "Their 'heat level' content formula is repeatable at any scale. Map it to Chubby's menu."
        },
        {
            "name": "Hattie B's",
            "handle": "@hattiebshot",
            "location": "National chain",
            "followers": "198K",
            "posting": "Daily",
            "whats_working": "Brand storytelling, consistent color palette (red/yellow), employee spotlights, event coverage.",
            "steal_this": "Employee content = highly authentic. People love seeing the humans behind the food."
        },
    ]
    
    for c in competitors:
        with st.expander(f"**{c['name']}** · {c['handle']} · {c['followers']} followers"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**📍 Location:** {c['location']}")
                st.markdown(f"**📅 Posting Freq:** {c['posting']}")
                st.markdown(f"**✅ What's Working:**")
                st.markdown(c['whats_working'])
            with col2:
                st.markdown(f"**💡 Steal This for Chubby's:**")
                st.markdown(f"> {c['steal_this']}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: CONTENT CONCEPTS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## 💡 Content Concepts for Chubby's")
    st.markdown("*Ideas built around what's trending + what works in the hot chicken space.*")
    
    col1, col2 = st.columns(2)
    
    concepts = [
        {
            "title": "🔥 'Can You Handle It?' Spice Series",
            "hook": "Hook: 'We dare you to try our hottest level...'",
            "desc": "Bring in a customer (or the owner) and film a genuine spice reaction. The more real, the better. No acting. This format is proven — gets shared, saves, and comments.",
            "format": "Reel · 15-30 sec",
            "tags": ["Challenge", "Trending", "High Engagement"]
        },
        {
            "title": "🍗 The Chubby Sandwich Build",
            "hook": "Hook: 'This is why people drive 30 minutes for this sandwich...'",
            "desc": "Slow-mo shot of each ingredient being layered. The bun, the chicken, the slaw, the pickles, the sauce. ASMR audio. No talking needed — let the food speak.",
            "format": "Reel · 10-20 sec",
            "tags": ["ASMR", "Food Porn", "Evergreen"]
        },
        {
            "title": "👨‍🍳 Backyard to Brick & Mortar",
            "hook": "Hook: 'They started selling hot chicken from their backyard in Rialto...'",
            "desc": "Tell the Quiroz brothers' story. Started in a backyard, went food truck, now brick and mortar. This is a compelling origin story — people root for local businesses they know.",
            "format": "Reel · 30-60 sec",
            "tags": ["Storytelling", "Brand Building", "Community"]
        },
        {
            "title": "🌶️ Heat Level Breakdown",
            "hook": "Hook: 'From mild to stupid hot — here's every level...'",
            "desc": "Quick cut showing each heat level with a visual rating. Maybe a reaction clip for each. Educational + entertaining. Great for new customers who don't know the menu.",
            "format": "Reel · 20-30 sec",
            "tags": ["Educational", "Menu", "High Saves"]
        },
        {
            "title": "🥗 Chubby Fries POV",
            "hook": "Hook: 'You've never had fries like this...'",
            "desc": "Close-up overhead shot of the Chubby Fries being loaded — chicken, slaw, pickles. The messier the better. People LOVE loaded fry content right now.",
            "format": "Reel · 10-15 sec",
            "tags": ["Trending", "ASMR", "Easy Shoot"]
        },
        {
            "title": "🏘️ 'Fontana's Best Kept Secret'",
            "hook": "Hook: 'The IE doesn't talk about this enough...'",
            "desc": "Lean into local pride. Position Chubby's as THE spot in Fontana/IE. Tag local food accounts. Use local hashtags. Build community before scale.",
            "format": "Reel · 15-30 sec",
            "tags": ["Local", "Community", "Organic Reach"]
        },
        {
            "title": "🤳 Customer Takeover",
            "hook": "Hook: 'We let a regular customer take over our camera for a day...'",
            "desc": "Have a loyal customer film their experience — arrival, ordering, first bite reaction. UGC-style content performs incredibly well. Feels real because it is.",
            "format": "Reel · 30-45 sec",
            "tags": ["UGC", "Authentic", "Trust Builder"]
        },
        {
            "title": "🎵 Trending Audio Drop",
            "hook": "Hook: [No words needed — just vibes]",
            "desc": "Pick the top trending audio of the week and build a quick food montage around it. Tight cuts, great food shots, trending sound. Fast to make, high algorithmic push.",
            "format": "Reel · 10-15 sec",
            "tags": ["Trending", "Algorithm", "Quick Win"]
        },
    ]
    
    for i, concept in enumerate(concepts):
        col = col1 if i % 2 == 0 else col2
        with col:
            tags_html = " ".join([f'<span class="tag">{t}</span>' for t in concept["tags"]])
            st.markdown(f"""
            <div class="concept-card">
                <h4>{concept['title']}</h4>
                <p style="color:#FF6B00; font-style:italic; margin-bottom:0.5rem;">{concept['hook']}</p>
                <p>{concept['desc']}</p>
                <div style="margin-top:0.5rem; color:#888; font-size:0.8rem;">📱 {concept['format']}</div>
                {tags_html}
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: CONTENT CALENDAR
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("## 📅 Content Calendar")
    
    # Get current week's Monday
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    
    st.markdown(f"### Week of {monday.strftime('%B %d, %Y')}")
    
    # Sample calendar data
    calendar_data = {
        0: {"day": "Monday", "posts": ["🍗 Sandwich Build Reel"]},
        1: {"day": "Tuesday", "posts": []},
        2: {"day": "Wednesday", "posts": ["🔥 Spice Challenge Clip"]},
        3: {"day": "Thursday", "posts": []},
        4: {"day": "Friday", "posts": ["🥗 Chubby Fries Drop", "📸 Story: Weekend Special"]},
        5: {"day": "Saturday", "posts": ["🎵 Trending Audio Montage"]},
        6: {"day": "Sunday", "posts": []},
    }
    
    cols = st.columns(7)
    for i, col in enumerate(cols):
        day_info = calendar_data[i]
        date = monday + timedelta(days=i)
        is_today = date.date() == today.date()
        
        with col:
            border = "border: 2px solid #FF4500;" if is_today else ""
            posts_html = ""
            for post in day_info["posts"]:
                posts_html += f'<div class="post-item">{post}</div>'
            
            has_post_class = "has-post" if day_info["posts"] else ""
            today_label = " 📍" if is_today else ""
            
            st.markdown(f"""
            <div class="calendar-day {has_post_class}" style="{border}">
                <h5>{day_info['day'][:3].upper()} {date.strftime('%-d') if hasattr(date, 'strftime') else date.day}{today_label}</h5>
                {posts_html if posts_html else '<div style="color:#444; font-size:0.75rem;">No post</div>'}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Shot list section
    st.markdown("### 🎬 Next Shoot Day — Shot List")
    
    shot_list = [
        {"shot": "Hero sandwich build — overhead slow-mo", "priority": "🔴 Must Get", "notes": "Use macro lens, natural light if possible"},
        {"shot": "Chubby Fries loaded overhead", "priority": "🔴 Must Get", "notes": "Steam rising = money shot"},
        {"shot": "Kitchen action — chicken going in fryer", "priority": "🟡 High Value", "notes": "Get audio on, ASMR gold"},
        {"shot": "Customer first bite reaction (candid)", "priority": "🟡 High Value", "notes": "Ask permission first, keep it authentic"},
        {"shot": "Heat level display — all sauces lined up", "priority": "🟡 High Value", "notes": "Clean setup, consistent lighting"},
        {"shot": "Exterior storefront — golden hour if possible", "priority": "🟢 Nice to Have", "notes": "Good for ads later"},
        {"shot": "B-roll: hands boxing up order", "priority": "🟢 Nice to Have", "notes": "Always useful for cutaways"},
        {"shot": "Staff portrait / candid behind counter", "priority": "🟢 Nice to Have", "notes": "Builds brand personality"},
    ]
    
    for shot in shot_list:
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            st.markdown(f"**{shot['shot']}**")
        with col2:
            st.markdown(shot['priority'])
        with col3:
            st.markdown(f"*{shot['notes']}*")
        st.divider()
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#444; font-size:0.8rem;'>Built by Hyperwave Studios · Chubby's Chicken Content Intelligence v1.0</div>",
        unsafe_allow_html=True
    )
