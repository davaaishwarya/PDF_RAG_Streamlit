import streamlit as st
import json

st.set_page_config(
    page_title="CareerAI",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# LOAD CAREER DATA
# =========================================================

with open("careers.json", encoding="utf-8") as f:
    careers = json.load(f)


# Convert strings into lists
for c in careers:
    c["skills"] = [s.strip() for s in c["skills"].split(",")]
    c["interests"] = [i.strip() for i in c["interests"].split(",")]
    c["roadmap"] = [r.strip() for r in c["roadmap"].split("→")]


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#eef2ff,#fff,#f5f3ff);
}

[data-testid="stSidebar"] {
    background: linear-gradient(#172554,#4c1d95);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    color: white;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
}

.hero h1 {
    color: white;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin: 12px 0;
    box-shadow: 0 4px 15px #0001;
}

.metric {
    text-align: center;
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 15px #0001;
}

.num {
    font-size: 30px;
    font-weight: bold;
    color: #2563eb;
}

.skill {
    display: inline-block;
    background: #eff6ff;
    color: #2563eb;
    padding: 6px 10px;
    margin: 3px;
    border-radius: 15px;
}

.missing {
    display: inline-block;
    background: #fef2f2;
    color: #dc2626;
    padding: 6px 10px;
    margin: 3px;
    border-radius: 15px;
}

.step {
    background: #f5f3ff;
    padding: 10px;
    margin: 5px;
    border-radius: 8px;
    color: #4c1d95;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "<h1 style='text-align:center'>🎓 CareerAI</h1>"
        "<p style='text-align:center'>Smart Student Career Assistant</p>"
        "<p style='text-align:center'>🟢 Online</p>",
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🎯 Analyzer",
            "📊 Explorer",
            "ℹ️ About"
        ]
    )


# =========================================================
# HEADER FUNCTION
# =========================================================

def header(title, text):

    st.markdown(
        f"""
        <div class='hero'>
            <h1>{title}</h1>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    header(
        "🎓 CareerAI",
        "Smart Student Career Assistant"
    )

    st.markdown("""
    <div class="card">

    <h2>👋 Welcome to CareerAI</h2>

    <p>
    Find suitable technology careers using your skills and interests.
    </p>

    <h3>How it works</h3>

    <p>
    👨‍🎓 Profile →
    💻 Skills →
    ❤️ Interest →
    🎯 Matching →
    📚 Skill Gap →
    🛣️ Roadmap
    </p>

    </div>
    """, unsafe_allow_html=True)


    a, b, c = st.columns(3)

    for col, num, text in [
        (a, "12+", "Career Paths"),
        (b, "50+", "Skills"),
        (c, "100%", "Interactive")
    ]:

        col.markdown(
            f"""
            <div class='metric'>
                <div class='num'>{num}</div>
                {text}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# ANALYZER
# =========================================================

elif page == "🎯 Analyzer":

    header(
        "🎯 Career Analyzer",
        "Find the career matching your profile"
    )


    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        name = st.text_input("👤 Name")

        degree = st.selectbox(
            "🎓 Degree",
            [
                "B.Tech",
                "B.Sc",
                "BCA",
                "MCA",
                "M.Tech",
                "MBA",
                "Other"
            ]
        )

        percentage = st.slider(
            "📊 Percentage",
            0,
            100,
            75
        )


    # -----------------------------------------------------
    # ALL SKILLS
    # -----------------------------------------------------

    skills_all = sorted({
        skill
        for career in careers
        for skill in career["skills"]
    })


    # -----------------------------------------------------
    # ALL INTERESTS
    # -----------------------------------------------------

    interests_all = sorted({
        interest
        for career in careers
        for interest in career["interests"]
    })


    with c2:

        skills = st.multiselect(
            "💻 Your Skills",
            skills_all
        )

        interest = st.selectbox(
            "❤️ Interest",
            interests_all
        )


    # -----------------------------------------------------
    # ANALYZE BUTTON
    # -----------------------------------------------------

    if st.button(
        "🚀 ANALYZE CAREER",
        type="primary",
        use_container_width=True
    ):

        if not name or not skills:

            st.warning(
                "Enter your name and select your skills."
            )

        else:

            results = []


            # -------------------------------------------------
            # MATCH CAREERS
            # -------------------------------------------------

            for career in careers:

                matches = len(
                    set(skills) &
                    set(career["skills"])
                )


                # Skill score
                score = (
                    matches /
                    len(career["skills"])
                ) * 75


                # Interest score
                if interest in career["interests"]:
                    score += 25


                missing = [
                    skill
                    for skill in career["skills"]
                    if skill not in skills
                ]


                results.append(
                    (
                        min(round(score), 100),
                        career,
                        matches,
                        missing
                    )
                )


            # -------------------------------------------------
            # BEST MATCH
            # -------------------------------------------------

            score, career, matches, missing = max(
                results,
                key=lambda x: x[0]
            )


            # -------------------------------------------------
            # RESULT HEADER
            # -------------------------------------------------

            st.markdown(
                f"""
                <div class="hero">

                    <h1>
                        {career["icon"]}
                        {career["career"]}
                    </h1>

                    <h1>
                        {score}%
                    </h1>

                    <p>
                        Career Match for {name}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


            # -------------------------------------------------
            # METRICS
            # -------------------------------------------------

            a, b, d = st.columns(3)

            a.metric(
                "🎯 Match",
                f"{score}%"
            )

            b.metric(
                "💻 Matching Skills",
                matches
            )

            d.metric(
                "📚 Skills to Learn",
                len(missing)
            )


            # =================================================
            # YOUR SKILLS
            # =================================================

            st.markdown(
                """
                <div class='card'>
                <h2>💻 Your Skills</h2>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                "".join(
                    f"""
                    <span class='skill'>
                    ✅ {skill}
                    </span>
                    """
                    for skill in skills
                ),
                unsafe_allow_html=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # =================================================
            # SKILLS TO LEARN
            # =================================================

            st.markdown(
                """
                <div class='card'>
                <h2>📚 Skills to Learn</h2>
                """,
                unsafe_allow_html=True
            )


            if missing:

                st.markdown(
                    "".join(
                        f"""
                        <span class='missing'>
                        ❌ {skill}
                        </span>
                        """
                        for skill in missing
                    ),
                    unsafe_allow_html=True
                )

            else:

                st.success(
                    "🎉 You already have all required skills!"
                )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # =================================================
            # YOUR INTEREST
            # =================================================

            st.markdown(
                """
                <div class='card'>
                <h2>❤️ Your Interest</h2>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <span class='skill'>
                ❤️ {interest}
                </span>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # =================================================
            # CAREER INTERESTS
            # =================================================

            st.markdown(
                """
                <div class='card'>
                <h2>💡 Career Interests</h2>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                "".join(
                    f"""
                    <span class='skill'>
                    ⭐ {item}
                    </span>
                    """
                    for item in career["interests"]
                ),
                unsafe_allow_html=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # =================================================
            # REQUIRED SKILLS
            # =================================================

            st.markdown(
                """
                <div class='card'>
                <h2>🛠️ Required Skills</h2>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                "".join(
                    f"""
                    <span class='skill'>
                    🔹 {skill}
                    </span>
                    """
                    for skill in career["skills"]
                ),
                unsafe_allow_html=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # =================================================
            # LEARNING ROADMAP
            # =================================================

            st.markdown(
                """
                <div class='card'>
                <h2>🛣️ Learning Roadmap</h2>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                "".join(
                    f"""
                    <div class='step'>
                    {i}️⃣ {step}
                    </div>
                    """
                    for i, step in enumerate(
                        career["roadmap"],
                        1
                    )
                ),
                unsafe_allow_html=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# =========================================================
# EXPLORER
# =========================================================

elif page == "📊 Explorer":

    header(
        "📊 Career Explorer",
        "Explore available technology careers"
    )


    for career in careers:

        with st.expander(
            f'{career["icon"]} {career["career"]}'
        ):

            st.write(
                "**Skills:**",
                ", ".join(career["skills"])
            )

            st.write(
                "**Interests:**",
                ", ".join(career["interests"])
            )

            st.write(
                "**Roadmap:**",
                " → ".join(career["roadmap"])
            )


# =========================================================
# ABOUT
# =========================================================

else:

    header(
        "ℹ️ About CareerAI",
        "Smart Student Career Assistant"
    )


    st.markdown("""
    <div class="card">

    <h2>🎓 CareerAI</h2>

    <p>
    Career recommendation system for students.
    </p>

    <h3>🛠 Technologies</h3>

    <p>
    Python • Streamlit • JSON
    </p>

    <h3>🧠 Architecture</h3>

    <p>
    Profile → Skills → Matching → Career →
    Skill Gap → Roadmap
    </p>

    </div>
    """, unsafe_allow_html=True)