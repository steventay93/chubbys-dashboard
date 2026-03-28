import streamlit as st
import random
from datetime import datetime, timedelta
import pandas as pd
from scraper import fetch_competitor_reels, fetch_chubbys_posts, COMPETITOR_ACCOUNTS

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Chubby's — Content Intelligence",
    page_icon="🍗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #080808 !important;
    color: #f0f0f0;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem 2rem !important; max-width: 1400px; }

/* ── Tabs ── */
div[data-testid="stTabs"] {
    background: transparent;
}
div[data-testid="stTabs"] > div:first-child {
    border-bottom: 1px solid #1e1e1e;
    gap: 0;
}
div[data-testid="stTabs"] button {
    color: #555 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.75rem 1.25rem !important;
    border-radius: 0 !important;
    border: none !important;
    background: transparent !important;
    letter-spacing: 0.3px;
    transition: color 0.2s;
}
div[data-testid="stTabs"] button:hover {
    color: #FF4500 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #FF4500 !important;
    border-bottom: 2px solid #FF4500 !important;
}
div[data-testid="stTabPanel"] {
    padding-top: 1.5rem !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #FF4500, #FF6B00) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.25rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
    box-shadow: 0 4px 15px rgba(255,69,0,0.3) !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #111 !important;
    border: 1px dashed #2a2a2a !important;
    border-radius: 12px !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* ── Divider ── */
hr { border-color: #1a1a1a !important; margin: 1.5rem 0 !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #FF4500 !important; }

/* ── Caption ── */
.stCaption { color: #555 !important; font-size: 0.78rem !important; }

/* ── Info/Warning ── */
.stInfo, .stWarning { border-radius: 10px !important; }

/* ── Chart ── */
[data-testid="stArrowVegaLiteChart"] { border-radius: 12px; }

/* ── Expander ── */
details {
    background: #111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 12px !important;
    padding: 0.25rem 0 !important;
    margin-bottom: 0.75rem !important;
}
details summary {
    padding: 0.75rem 1rem !important;
    font-weight: 600 !important;
    color: #f0f0f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Helper: card components ──────────────────────────────────────────────────
def metric_card(label, value, delta=None, delta_positive=True):
    delta_color = "#22c55e" if delta_positive else "#ef4444"
    delta_html = f'<div style="color:{delta_color};font-size:0.8rem;margin-top:4px;font-weight:500;">{delta}</div>' if delta else ""
    return f"""
    <div style="background:#111;border:1px solid #1e1e1e;border-radius:14px;padding:1.25rem 1.5rem;">
        <div style="color:#555;font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;">{label}</div>
        <div style="color:#fff;font-size:1.9rem;font-weight:800;line-height:1;">{value}</div>
        {delta_html}
    </div>"""

def section_header(title, subtitle=None):
    sub = f'<div style="color:#555;font-size:0.85rem;margin-top:4px;">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="margin-bottom:1.5rem;">
        <div style="color:#fff;font-size:1.2rem;font-weight:800;letter-spacing:-0.3px;">{title}</div>
        {sub}
    </div>"""

def concept_card(title, hook, desc, format_label, tags):
    tags_html = "".join([f'<span style="background:#1e1e1e;color:#FF6B00;border:1px solid #2a2a2a;font-size:0.68rem;font-weight:700;padding:3px 10px;border-radius:20px;margin-right:4px;">{t}</span>' for t in tags])
    return f"""
    <div style="background:#111;border:1px solid #1e1e1e;border-left:3px solid #FF4500;border-radius:14px;padding:1.25rem 1.5rem;margin-bottom:1rem;height:100%;">
        <div style="color:#FF4500;font-weight:800;font-size:0.95rem;margin-bottom:6px;">{title}</div>
        <div style="color:#FF6B00;font-style:italic;font-size:0.82rem;margin-bottom:10px;opacity:0.9;">{hook}</div>
        <div style="color:#aaa;font-size:0.85rem;line-height:1.6;margin-bottom:12px;">{desc}</div>
        <div style="color:#555;font-size:0.75rem;margin-bottom:10px;">📱 {format_label}</div>
        <div>{tags_html}</div>
    </div>"""

def audio_card(name, uses, trend):
    trend_color = "#FF4500" if "Explo" in trend else "#FF6B00" if "Hot" in trend else "#f59e0b"
    return f"""
    <div style="background:#111;border:1px solid #1e1e1e;border-radius:12px;padding:1rem 1.25rem;margin-bottom:0.75rem;display:flex;align-items:center;justify-content:space-between;">
        <div>
            <div style="color:#fff;font-size:0.85rem;font-weight:600;">🎵 {name}</div>
            <div style="color:#555;font-size:0.75rem;margin-top:2px;">{uses} uses</div>
        </div>
        <div style="color:{trend_color};font-size:0.75rem;font-weight:700;white-space:nowrap;">{trend}</div>
    </div>"""

def format_card(fmt, desc, tags):
    tags_html = "".join([f'<span style="background:#1a1a1a;color:#888;font-size:0.68rem;padding:2px 8px;border-radius:10px;margin-right:3px;">{t}</span>' for t in tags])
    return f"""
    <div style="background:#111;border:1px solid #1e1e1e;border-radius:12px;padding:1rem 1.25rem;margin-bottom:0.75rem;">
        <div style="color:#fff;font-size:0.9rem;font-weight:700;margin-bottom:6px;">🎬 {fmt}</div>
        <div style="color:#888;font-size:0.82rem;line-height:1.5;margin-bottom:8px;">{desc}</div>
        <div>{tags_html}</div>
    </div>"""

# ─── Header ───────────────────────────────────────────────────────────────────
col_logo, col_info, col_spacer = st.columns([1.2, 3, 2])
with col_logo:
    st.image("logo.png", width=160)
with col_info:
    st.markdown("""
    <div style="padding:0.5rem 0 0 0.5rem;">
        <div style="color:#fff;font-size:1.6rem;font-weight:900;letter-spacing:-0.5px;line-height:1.1;">Content Intelligence</div>
        <div style="color:#FF4500;font-size:0.85rem;font-weight:600;margin-top:4px;letter-spacing:0.5px;">HYPERWAVE STUDIOS · POWERED BY AI</div>
    </div>
    """, unsafe_allow_html=True)
with col_spacer:
    now = datetime.now()
    st.markdown(f"""
    <div style="text-align:right;padding-top:0.75rem;">
        <div style="color:#555;font-size:0.75rem;">Last updated</div>
        <div style="color:#888;font-size:0.85rem;font-weight:600;">{now.strftime('%b %d, %Y · %I:%M %p')}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="border-bottom:1px solid #1a1a1a;margin:1rem 0 0 0;"></div>', unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Analytics",
    "🔥  Trending Intel",
    "👀  Competitor Watch",
    "💡  Content Concepts",
    "📅  Calendar & Shot List",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 · ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(section_header("Chubby's Instagram Analytics", "Upload an Instagram Insights CSV export to populate live data"), unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop Instagram Insights CSV here", type="csv", label_visibility="collapsed")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)
    else:
        st.markdown('<div style="background:#0f0f0f;border:1px dashed #1e1e1e;border-radius:12px;padding:0.75rem 1.25rem;color:#555;font-size:0.82rem;margin-bottom:1.5rem;">📁 No CSV uploaded — showing sample data. Export from Instagram Insights and upload above.</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(metric_card("Followers", "4,821", "↑ +127 this month"), unsafe_allow_html=True)
        with col2:
            st.markdown(metric_card("Avg Engagement", "6.2%", "↑ +0.8% vs last month"), unsafe_allow_html=True)
        with col3:
            st.markdown(metric_card("Reach (30d)", "28.4K", "↑ +12% vs last month"), unsafe_allow_html=True)
        with col4:
            st.markdown(metric_card("Reel Plays", "142K", "↑ +34% vs last month"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="color:#fff;font-size:1rem;font-weight:700;margin-bottom:1rem;">📈 Follower Growth — Last 30 Days</div>', unsafe_allow_html=True)

        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        followers = [4600 + i * 7 + random.randint(-5, 15) for i in range(30)]
        chart_df = pd.DataFrame({"Date": dates, "Followers": followers})
        st.line_chart(chart_df.set_index("Date"), color="#FF4500", height=220)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="color:#fff;font-size:1rem;font-weight:700;margin-bottom:1rem;">🏆 Top Performing Posts</div>', unsafe_allow_html=True)

        top_posts = [
            {"Post": "🔥 Nashville Tenders Drop", "Plays": "38,200", "Likes": "1,840", "Comments": "94", "Saves": "312"},
            {"Post": "🍗 The Chubby Combo Reveal", "Plays": "27,100", "Likes": "1,220", "Comments": "67", "Saves": "198"},
            {"Post": "🌶️ Spice Level Challenge", "Plays": "21,400", "Likes": "980", "Comments": "143", "Saves": "87"},
            {"Post": "🧑‍🍳 Kitchen Behind the Scenes", "Plays": "18,900", "Likes": "890", "Comments": "51", "Saves": "234"},
            {"Post": "🥗 Chubby Fries Closeup", "Plays": "15,600", "Likes": "720", "Comments": "38", "Saves": "156"},
        ]
        st.dataframe(pd.DataFrame(top_posts), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 · TRENDING INTEL
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(section_header("Trending Intel", "Live competitor reels + trending formats in the hot chicken space"), unsafe_allow_html=True)

    col_refresh, col_note = st.columns([1, 4])
    with col_refresh:
        if st.button("🔄  Refresh Live Data"):
            st.cache_data.clear()
    with col_note:
        st.markdown('<div style="color:#555;font-size:0.78rem;padding-top:0.6rem;">Data cached 1 hour · Pulls from Howlin\' Ray\'s, Angry Chickz, Dave\'s, Hattie B\'s, Legend</div>', unsafe_allow_html=True)

    with st.spinner("Fetching competitor reels..."):
        handles = [a["handle"] for a in COMPETITOR_ACCOUNTS]
        reels, scrape_error = fetch_competitor_reels(handles)

    if scrape_error:
        st.markdown(f'<div style="background:#1a0a00;border:1px solid #3a1a00;border-radius:10px;padding:0.75rem 1rem;color:#FF6B00;font-size:0.82rem;margin-bottom:1rem;">⚠️ {scrape_error}</div>', unsafe_allow_html=True)

    if reels:
        cols_per_row = 4
        for i in range(0, min(len(reels), 12), cols_per_row):
            row_reels = reels[i:i+cols_per_row]
            cols = st.columns(cols_per_row)
            for col, reel in zip(cols, row_reels):
                with col:
                    plays = reel.get("plays") or 0
                    likes = reel.get("likes") or 0
                    comments = reel.get("comments") or 0
                    caption = (reel.get("caption") or "")[:80]
                    owner = reel.get("owner", "")
                    url = reel.get("url", "#")
                    thumb = reel.get("thumbnail", "")

                    plays_str = f"{plays:,}" if plays else "—"
                    likes_str = f"{likes:,}" if likes else "—"
                    comments_str = f"{comments:,}" if comments else "—"

                    thumb_html = (
                        f'<img src="{thumb}" style="width:100%;aspect-ratio:3/4;object-fit:cover;display:block;">'
                        if thumb else
                        '<div style="width:100%;aspect-ratio:3/4;background:#1a1a1a;display:flex;align-items:center;justify-content:center;font-size:2.5rem;">🍗</div>'
                    )

                    st.markdown(f"""
                    <a href="{url}" target="_blank" style="text-decoration:none;color:inherit;">
                    <div style="background:#111;border:1px solid #1e1e1e;border-radius:14px;overflow:hidden;margin-bottom:1rem;cursor:pointer;transition:border-color 0.2s,transform 0.2s;display:block;"
                         onmouseover="this.style.borderColor='#FF4500';this.style.transform='translateY(-2px)'"
                         onmouseout="this.style.borderColor='#1e1e1e';this.style.transform='translateY(0)'">
                        <div style="overflow:hidden;position:relative;">
                            {thumb_html}
                            <div style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.7);color:#FF4500;font-size:0.65rem;font-weight:700;padding:2px 8px;border-radius:20px;backdrop-filter:blur(4px);">@{owner}</div>
                        </div>
                        <div style="padding:0.85rem;">
                            <div style="color:#ccc;font-size:0.78rem;line-height:1.4;min-height:2.5rem;margin-bottom:0.6rem;">{caption}{"…" if len(reel.get("caption",""))>80 else ""}</div>
                            <div style="display:flex;gap:0.6rem;color:#555;font-size:0.72rem;border-top:1px solid #1e1e1e;padding-top:0.6rem;">
                                <span title="Views">▶ {plays_str}</span>
                                <span title="Likes">♥ {likes_str}</span>
                                <span title="Comments">💬 {comments_str}</span>
                            </div>
                        </div>
                    </div>
                    </a>
                    """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:#111;border:1px solid #1e1e1e;border-radius:12px;padding:2rem;text-align:center;color:#555;">No reels loaded yet — hit Refresh above to pull live data from competitor accounts.</div>', unsafe_allow_html=True)

    st.markdown('<div style="border-bottom:1px solid #1a1a1a;margin:1.5rem 0;"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div style="color:#fff;font-size:1rem;font-weight:700;margin-bottom:1rem;">🎵 Trending Audios</div>', unsafe_allow_html=True)
        audios = [
            ("original sound - foodie_kings", "124K", "🔥 Exploding"),
            ("Kehlani - Nights Like This (sped up)", "98K", "📈 Rising"),
            ("original sound - grwm.food", "76K", "📈 Rising"),
            ("Lil Durk - The Voice (slowed)", "64K", "⚡ Hot"),
            ("original sound - chickenfever", "51K", "🔥 Exploding"),
            ("Rod Wave - Smooth Sailing", "43K", "📈 Rising"),
        ]
        for a in audios:
            st.markdown(audio_card(*a), unsafe_allow_html=True)

    with col_b:
        st.markdown('<div style="color:#fff;font-size:1rem;font-weight:700;margin-bottom:1rem;">🎬 Trending Formats</div>', unsafe_allow_html=True)
        formats = [
            ("The Crispy Pull-Apart", "Close-up slow-mo of pulling apart a crispy tender. ASMR vibes. Consistently high saves.", ["#ASMR", "#SlowMo", "#FoodPorn"]),
            ("Spice Level Reaction", "Customer tries your hottest level on camera. Authentic = massive shares.", ["#Challenge", "#Reaction"]),
            ("Day In The Kitchen POV", "First-person cook perspective. People love behind-the-scenes.", ["#BehindTheScenes", "#POV"]),
            ("The Stack Shot", "Building the sandwich ingredient by ingredient, slow motion drop.", ["#ASMR", "#Satisfying"]),
            ("Local Love Story", "Interview a regular. 'Why do you keep coming back?' — authenticity wins.", ["#Community", "#Local"]),
        ]
        for f in formats:
            st.markdown(format_card(*f), unsafe_allow_html=True)

    st.markdown('<div style="border-bottom:1px solid #1a1a1a;margin:1.5rem 0;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#fff;font-size:1rem;font-weight:700;margin-bottom:1rem;">🏷️ Hashtag Bank</div>', unsafe_allow_html=True)

    hashtags = ["#nashvillehotchicken","#hotchicken","#friedchicken","#chickensandwich",
                "#foodie","#foodreels","#eatlocal","#inlandempirefood","#fontanaeats",
                "#socaleats","#hotchickensandwich","#crispychicken","#chickentenders",
                "#spicyfood","#foodporn","#reelsfood","#foodtok","#chickenlover"]
    pills = "".join([f'<span style="display:inline-block;background:#111;color:#FF6B00;border:1px solid #2a2a2a;font-size:0.78rem;padding:4px 12px;border-radius:20px;margin:3px;">{h}</span>' for h in hashtags])
    st.markdown(f'<div style="line-height:2.5;">{pills}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 · COMPETITOR WATCH
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(section_header("Competitor Watch", "Key accounts in the Nashville hot chicken + SoCal food space"), unsafe_allow_html=True)

    competitors = [
        {
            "name": "Howlin' Ray's", "handle": "@howlinrays", "location": "Los Angeles, CA",
            "followers": "89K", "posting": "4–5×/week",
            "working": "Behind-the-scenes kitchen clips, spice challenge reactions, slow-mo food shots. Very consistent warm aesthetic.",
            "steal": "Their 'spice reaction' series gets 50K+ views consistently. Authentic, unscripted customer moments."
        },
        {
            "name": "Angry Chickz", "handle": "@theangrychickz", "location": "SoCal — multiple IE locations",
            "followers": "42K", "posting": "3–4×/week",
            "working": "High energy reels with trending audio, showcasing menu variety and heat levels. Heavy UGC reposting.",
            "steal": "They repost customer content constantly — low effort, high trust. Chubby's should be doing this."
        },
        {
            "name": "Legend Hot Chicken", "handle": "@legendhotchicken", "location": "Chino Hills, CA",
            "followers": "18K", "posting": "2–3×/week",
            "working": "Local community feel, consistent branding, heavy food closeups. Tags local food bloggers.",
            "steal": "Actively engages with IE food influencers. Good relationship-building play for Chubby's too."
        },
        {
            "name": "Dave's Hot Chicken", "handle": "@daveshotchicken", "location": "National chain",
            "followers": "312K", "posting": "Daily",
            "working": "Meme-heavy content, celebrity collabs, extreme heat challenges. Very internet-native brand voice.",
            "steal": "Their heat level content formula is repeatable at any scale. Map it to Chubby's menu."
        },
        {
            "name": "Hattie B's", "handle": "@hattiebshot", "location": "National chain",
            "followers": "198K", "posting": "Daily",
            "working": "Brand storytelling, consistent color palette, employee spotlights, event coverage.",
            "steal": "Employee content = highly authentic. People love seeing the humans behind the food."
        },
    ]

    for c in competitors:
        with st.expander(f"**{c['name']}**  ·  {c['handle']}  ·  {c['followers']} followers"):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"""
                <div style="background:#0f0f0f;border-radius:10px;padding:1rem;">
                    <div style="color:#555;font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Account Info</div>
                    <div style="color:#aaa;font-size:0.85rem;margin-bottom:4px;">📍 {c['location']}</div>
                    <div style="color:#aaa;font-size:0.85rem;margin-bottom:12px;">📅 Posts {c['posting']}</div>
                    <div style="color:#555;font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">What's Working</div>
                    <div style="color:#ccc;font-size:0.84rem;line-height:1.5;">{c['working']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="background:#0f0f0f;border:1px solid #FF4500;border-radius:10px;padding:1rem;">
                    <div style="color:#FF4500;font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:8px;">💡 Steal This for Chubby's</div>
                    <div style="color:#ccc;font-size:0.84rem;line-height:1.5;">{c['steal']}</div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 · CONTENT CONCEPTS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(section_header("Content Concepts", "8 ready-to-execute ideas built around Chubby's brand and what's trending"), unsafe_allow_html=True)

    concepts = [
        ("🔥 'Can You Handle It?' Spice Series", "Hook: 'We dare you to try our hottest level...'",
         "Bring in a customer (or the owner) and film a genuine spice reaction. The more real the better. No acting. Gets shared, saved, and commented like crazy.",
         "Reel · 15–30 sec", ["Challenge", "Trending", "High Engagement"]),
        ("🍗 The Chubby Sandwich Build", "Hook: 'This is why people drive 30 minutes for this...'",
         "Slow-mo of each ingredient being layered. Bun, chicken, slaw, pickles, sauce. ASMR audio. No talking needed — let the food speak.",
         "Reel · 10–20 sec", ["ASMR", "Food Porn", "Evergreen"]),
        ("👨‍🍳 Backyard to Brick & Mortar", "Hook: 'They started selling from their backyard in Rialto...'",
         "Tell the Quiroz brothers' origin story. Backyard → food truck → brick and mortar. People root for local businesses they know.",
         "Reel · 30–60 sec", ["Storytelling", "Brand", "Community"]),
        ("🌶️ Heat Level Breakdown", "Hook: 'From mild to stupid hot — here's every level...'",
         "Quick cut showing each heat level with a visual rating. Educational + entertaining. Great for new customers who don't know the menu.",
         "Reel · 20–30 sec", ["Educational", "Menu", "High Saves"]),
        ("🥗 Chubby Fries POV", "Hook: 'You've never had fries like this...'",
         "Overhead shot of Chubby Fries being loaded — chicken, slaw, pickles. The messier the better. Loaded fry content is everywhere right now.",
         "Reel · 10–15 sec", ["Trending", "ASMR", "Easy Shoot"]),
        ("🏘️ Fontana's Best Kept Secret", "Hook: 'The IE doesn't talk about this enough...'",
         "Lean into local pride. Position Chubby's as THE spot in Fontana/IE. Tag local food accounts. Build community before scale.",
         "Reel · 15–30 sec", ["Local", "Community", "Organic Reach"]),
        ("🤳 Customer Takeover", "Hook: 'We let a regular take over our camera for a day...'",
         "Have a loyal customer film their experience. UGC-style performs incredibly well. Feels real because it is.",
         "Reel · 30–45 sec", ["UGC", "Authentic", "Trust Builder"]),
        ("🎵 Trending Audio Drop", "Hook: [No words — just vibes and great food shots]",
         "Pick the top trending audio of the week and build a quick food montage around it. Tight cuts, great footage, trending sound. Fast to make, algorithmic push.",
         "Reel · 10–15 sec", ["Trending", "Algorithm", "Quick Win"]),
    ]

    col1, col2 = st.columns(2)
    for i, (title, hook, desc, fmt, tags) in enumerate(concepts):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(concept_card(title, hook, desc, fmt, tags), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 · CALENDAR & SHOT LIST
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown(section_header("Content Calendar & Shot List", "Weekly post plan + next shoot day checklist"), unsafe_allow_html=True)

    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    st.markdown(f'<div style="color:#555;font-size:0.82rem;margin-bottom:1rem;">Week of {monday.strftime("%B %d, %Y")}</div>', unsafe_allow_html=True)

    calendar_data = {
        0: {"day": "Mon", "posts": ["🍗 Sandwich Build Reel"]},
        1: {"day": "Tue", "posts": []},
        2: {"day": "Wed", "posts": ["🔥 Spice Challenge"]},
        3: {"day": "Thu", "posts": []},
        4: {"day": "Fri", "posts": ["🥗 Chubby Fries Drop", "📸 Weekend Story"]},
        5: {"day": "Sat", "posts": ["🎵 Trending Audio Reel"]},
        6: {"day": "Sun", "posts": []},
    }

    cols = st.columns(7)
    for i, col in enumerate(cols):
        day_info = calendar_data[i]
        date = monday + timedelta(days=i)
        is_today = date.date() == today.date()
        border = "border-color:#FF4500;" if is_today else ""
        today_dot = '<div style="width:6px;height:6px;background:#FF4500;border-radius:50%;margin:0 auto 6px auto;"></div>' if is_today else ""
        posts_html = ""
        for post in day_info["posts"]:
            posts_html += f'<div style="background:#FF4500;color:white;font-size:0.65rem;padding:3px 6px;border-radius:4px;margin-bottom:3px;line-height:1.3;">{post}</div>'
        empty = '<div style="color:#333;font-size:0.72rem;text-align:center;margin-top:0.5rem;">—</div>' if not day_info["posts"] else ""

        with col:
            st.markdown(f"""
            <div style="background:#111;border:1px solid #1e1e1e;{border}border-radius:10px;padding:0.75rem 0.5rem;min-height:120px;">
                {today_dot}
                <div style="color:#555;font-size:0.68rem;text-transform:uppercase;text-align:center;letter-spacing:1px;margin-bottom:4px;">{day_info['day']}</div>
                <div style="color:#888;font-size:0.8rem;text-align:center;margin-bottom:8px;font-weight:600;">{date.day}</div>
                {posts_html}{empty}
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="border-bottom:1px solid #1a1a1a;margin:2rem 0 1.5rem 0;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#fff;font-size:1rem;font-weight:700;margin-bottom:1rem;">🎬 Next Shoot Day — Shot List</div>', unsafe_allow_html=True)

    shots = [
        ("Hero sandwich build — overhead slow-mo", "🔴 Must Get", "Use macro lens, natural light preferred"),
        ("Chubby Fries loaded overhead", "🔴 Must Get", "Steam rising = money shot"),
        ("Kitchen action — chicken going in fryer", "🟡 High Value", "Keep audio on, ASMR gold"),
        ("Customer first bite (candid)", "🟡 High Value", "Ask permission first — keep it real"),
        ("Heat level display — all sauces lined up", "🟡 High Value", "Clean setup, consistent lighting"),
        ("Exterior storefront — golden hour if possible", "🟢 Nice to Have", "Good for ads later"),
        ("B-roll: hands boxing up order", "🟢 Nice to Have", "Always useful for cutaways"),
        ("Staff candid behind counter", "🟢 Nice to Have", "Builds brand personality"),
    ]

    for shot, priority, notes in shots:
        col1, col2, col3 = st.columns([3, 1.2, 2.5])
        with col1:
            st.markdown(f'<div style="color:#f0f0f0;font-size:0.88rem;font-weight:600;padding:0.6rem 0;">{shot}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="font-size:0.82rem;padding:0.6rem 0;">{priority}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="color:#555;font-size:0.8rem;font-style:italic;padding:0.6rem 0;">{notes}</div>', unsafe_allow_html=True)
        st.markdown('<div style="border-bottom:1px solid #141414;"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;color:#2a2a2a;font-size:0.75rem;margin-top:3rem;">
        Chubby's Content Intelligence · Built by Hyperwave Studios
    </div>
    """, unsafe_allow_html=True)
