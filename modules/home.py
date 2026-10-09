from pathlib import Path

import streamlit as st


def show_home(logo_path=None):

    # ========================================================
    # BRAND LOGO
    # ========================================================

    if logo_path is not None:

        logo_path = Path(logo_path)

        if logo_path.exists():
            st.image(
                str(logo_path),
                width=620
            )


    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
"""<div class="mineops-hero">
<div class="mineops-hero-eyebrow">
MINING OPERATIONS • ENGINEERING • OPTIMIZATION
</div>

<div class="mineops-hero-title">
Mine<span>Ops</span>Lab
</div>

<div class="mineops-hero-tagline">
Mining Operations Optimization &amp; Learning Platform
</div>

<div class="mineops-hero-description">
Explore, analyse and optimize mining operations through
interactive engineering models, equipment analysis and
scenario-based learning.
</div>
</div>""",
        unsafe_allow_html=True,
    )


    # ========================================================
    # PLATFORM PURPOSE
    # ========================================================

    st.subheader("Design. Analyse. Optimize. Learn.")

    st.write(
        """
        MineOpsLab is an interactive engineering environment for
        exploring mining operations. It connects engineering
        calculations with equipment performance, operational
        scenarios and optimization.
        """
    )

    st.write("")


    # ========================================================
    # CORE FUNCTIONS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
"""<div class="mineops-card">
<h3>⚙️ Design</h3>
<p>
Configure mining systems, equipment and operating requirements.
</p>
</div>""",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
"""<div class="mineops-card">
<h3>📊 Analyse</h3>
<p>
Evaluate productivity, cycle times and system performance.
</p>
</div>""",
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
"""<div class="mineops-card">
<h3>🎯 Optimize</h3>
<p>
Investigate alternative equipment and operating configurations.
</p>
</div>""",
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
"""<div class="mineops-card">
<h3>🎓 Learn</h3>
<p>
Connect engineering theory with interactive mining scenarios.
</p>
</div>""",
            unsafe_allow_html=True,
        )


    # ========================================================
    # MATERIAL HANDLING LAB
    # ========================================================

    st.write("")
    st.write("")

    st.subheader("🚛 Material Handling")

    st.write(
        """
        The first MineOpsLab engineering environment focuses on
        surface mine material handling and loader-truck systems.
        """
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
"""<div class="mineops-card">
<h3>🪨 Material &amp; Production</h3>
<p>
Define material properties, production targets and operating requirements.
</p>
</div>""",
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
"""<div class="mineops-card">
<h3>🚜 Loading System</h3>
<p>
Analyse bucket payload, loader passes, loading time and loader productivity.
</p>
</div>""",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
"""<div class="mineops-card">
<h3>🚛 Haulage System</h3>
<p>
Analyse truck cycle time, haulage performance and truck productivity.
</p>
</div>""",
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
"""<div class="mineops-card">
<h3>⚙️ Fleet Matching</h3>
<p>
Integrate loading and haulage performance to determine fleet requirements.
</p>
</div>""",
            unsafe_allow_html=True,
        )

    st.write("")
    st.info(
        "Material Handling is the first operational engineering "
        "environment being developed within MineOpsLab."
    )