
from pathlib import Path

import streamlit as st


# ============================================================
# MODULE IMPORTS
# ============================================================

from modules.home import show_home

from modules.material_production import (
    show_material_production,
)

from modules.loading_system import (
    show_loading_system,
)

from modules.haulage_system import (
    show_haulage_system,
)

from modules.fleet_matching import (
    show_fleet_matching,
)

from modules.analysis_lab import (
    show_analysis_lab,
)

from modules.scenario_comparison import (
    show_scenario_comparison,
)

from modules.optimization import (
    show_optimization,
)

from modules.coming_soon import (
    show_coming_soon,
)


# ============================================================
# MINEOPSLAB APPLICATION SHELL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"

LOGO_PATH = ASSETS_DIR / "mineopslab_logo.png"

APP_ICON_PATH = ASSETS_DIR / "mineopslab_icon.png"

SIDEBAR_ICON_PATH = ASSETS_DIR / "sidebar_icon.png"

FAVICON_PATH = ASSETS_DIR / "favicon.png"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

page_icon = (
    str(FAVICON_PATH)
    if FAVICON_PATH.exists()
    else "🚛"
)

st.set_page_config(
    page_title="MineOpsLab",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL DESIGN SYSTEM
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   APPLICATION
========================================================== */

.stApp {
    background: #F3F6FA;
    color: #172033;
}

.block-container {
    max-width: 1280px;
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}

[data-testid="stMain"] {
    background: #F3F6FA;
}

[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3 {
    color: #14213D;
}

[data-testid="stMain"] p {
    color: #475467;
}


/* ==========================================================
   SIDEBAR
========================================================== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #081426 0%,
        #0D2038 55%,
        #142B49 100%
    );

    border-right:
        1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

[data-testid="stSidebar"] img {
    border-radius: 14px;
}


/* ==========================================================
   SIDEBAR BRAND
========================================================== */

.sidebar-brand-name {
    color: #FFFFFF;
    font-size: 26px;
    font-weight: 850;
    letter-spacing: -0.5px;
    margin-top: 7px;
    margin-bottom: 3px;
}

.sidebar-brand-name span {
    color: #F4A261;
}

.sidebar-brand-tagline {
    color: #AFC0D2;
    font-size: 11px;
    line-height: 1.5;
    margin-bottom: 12px;
}


/* ==========================================================
   SIDEBAR NAVIGATION SECTIONS
========================================================== */

.nav-section {
    color: #8298B1 !important;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin-top: 20px;
    margin-bottom: 8px;
}


/* ==========================================================
   SIDEBAR BUTTONS
========================================================== */

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    border-radius: 8px;
    text-align: left;
    justify-content: flex-start;
    font-size: 14px;
    font-weight: 600;
    min-height: 40px;

    border:
        1px solid rgba(255,255,255,0.08);

    transition: all 0.15s ease;
}

[data-testid="stSidebar"]
.stButton > button[kind="secondary"] {
    background: transparent;
    color: #DCE6F0;
}

[data-testid="stSidebar"]
.stButton > button[kind="secondary"]:hover {
    background:
        rgba(255,255,255,0.07);

    border-color:
        rgba(255,255,255,0.15);
}

[data-testid="stSidebar"]
.stButton > button[kind="primary"] {
    background: #F4A261;
    color: #14213D;
    border-color: #F4A261;
    font-weight: 750;
}


/* ==========================================================
   SIDEBAR FOOTER
========================================================== */

.sidebar-footer {
    margin-top: 30px;
    padding-top: 16px;

    border-top:
        1px solid rgba(255,255,255,0.10);
}

.sidebar-footer-title {
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 750;
}

.sidebar-footer-text {
    color: #8298B1;
    font-size: 10px;
    line-height: 1.5;
    margin-top: 4px;
}


/* ==========================================================
   PAGE HEADER
========================================================== */

.mineops-page-header {
    margin-bottom: 28px;
}

.mineops-eyebrow {
    color: #D9792B;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.mineops-page-title {
    color: #14213D;
    font-size: 38px;
    font-weight: 850;
    letter-spacing: -1px;
    line-height: 1.15;
}

.mineops-page-subtitle {
    color: #667085;
    font-size: 15px;
    line-height: 1.65;
    max-width: 850px;
    margin-top: 8px;
}


/* ==========================================================
   CARDS
========================================================== */

.mineops-card {
    background: #FFFFFF;

    border:
        1px solid #E4E7EC;

    border-radius: 14px;
    padding: 22px;

    box-shadow:
        0 1px 2px rgba(16,24,40,0.04);

    height: 100%;
}

.mineops-card h3 {
    color: #14213D;
    margin-top: 0;
    margin-bottom: 12px;
}

.mineops-card p {
    color: #475467;
    line-height: 1.65;
}


/* ==========================================================
   METRICS
========================================================== */

[data-testid="stMetric"] {
    background: #FFFFFF;

    border:
        1px solid #E4E7EC;

    border-radius: 12px;
    padding: 14px 16px;

    box-shadow:
        0 1px 2px rgba(16,24,40,0.03);
}

[data-testid="stMetricLabel"] {
    color: #667085;
}

[data-testid="stMetricValue"] {
    color: #14213D;
}


/* ==========================================================
   DATAFRAMES
========================================================== */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}


/* ==========================================================
   EXPANDERS
========================================================== */

[data-testid="stExpander"] {
    background: #FFFFFF;

    border:
        1px solid #E4E7EC;

    border-radius: 12px;
}


/* ==========================================================
   RESPONSIVE DESIGN
========================================================== */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    .mineops-page-title {
        font-size: 32px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"


# ============================================================
# NAVIGATION CALLBACK
# ============================================================

def navigate(page_name):
    st.session_state.current_page = page_name


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND ICON
    # --------------------------------------------------------

    if SIDEBAR_ICON_PATH.exists():

        st.image(
            str(SIDEBAR_ICON_PATH),
            width=88,
        )

    elif APP_ICON_PATH.exists():

        st.image(
            str(APP_ICON_PATH),
            width=88,
        )

    else:

        st.markdown("### 🚛")

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.markdown(
        """
<div class="sidebar-brand-name">
Mine<span>Ops</span>Lab
</div>

<div class="sidebar-brand-tagline">
Mining Operations Optimization &amp; Learning Platform
</div>
""",
        unsafe_allow_html=True,
    )

    # ========================================================
    # PLATFORM
    # ========================================================

    st.markdown(
        '<div class="nav-section">Platform</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "Home",
        key="nav_Home",
        width="stretch",
        type=(
            "primary"
            if st.session_state.current_page == "Home"
            else "secondary"
        ),
    ):

        navigate("Home")
        st.rerun()

    # ========================================================
    # MATERIAL HANDLING
    # ========================================================

    st.markdown(
        '<div class="nav-section">Material Handling</div>',
        unsafe_allow_html=True,
    )

    material_pages = [
        "Material & Production",
        "Loading System",
        "Haulage System",
        "Fleet Matching",
    ]

    for page_name in material_pages:

        if st.button(
            page_name,
            key=f"nav_{page_name}",
            width="stretch",
            type=(
                "primary"
                if st.session_state.current_page == page_name
                else "secondary"
            ),
        ):

            navigate(page_name)
            st.rerun()

    # ========================================================
    # ANALYSIS
    # ========================================================

    st.markdown(
        '<div class="nav-section">Analysis</div>',
        unsafe_allow_html=True,
    )

    analysis_pages = [
        "Sensitivity Analysis",
        "Scenario Comparison",
        "Economics",
        "Optimization",
    ]

    for page_name in analysis_pages:

        if st.button(
            page_name,
            key=f"nav_{page_name}",
            width="stretch",
            type=(
                "primary"
                if st.session_state.current_page == page_name
                else "secondary"
            ),
        ):

            navigate(page_name)
            st.rerun()

    # ========================================================
    # RESOURCES
    # ========================================================

    st.markdown(
        '<div class="nav-section">Resources</div>',
        unsafe_allow_html=True,
    )

    resource_pages = [
        "Equipment Library",
        "Learning Centre",
    ]

    for page_name in resource_pages:

        if st.button(
            page_name,
            key=f"nav_{page_name}",
            width="stretch",
            type=(
                "primary"
                if st.session_state.current_page == page_name
                else "secondary"
            ),
        ):

            navigate(page_name)
            st.rerun()

    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
<div class="sidebar-footer">

<div class="sidebar-footer-title">
MineOpsLab
</div>

<div class="sidebar-footer-text">
Surface Mining Teaching &amp; Analysis Environment
Development Build | 2026
</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE ROUTER
# ============================================================

page = st.session_state.current_page


# ============================================================
# HOME
# ============================================================

if page == "Home":

    show_home(
        logo_path=LOGO_PATH
    )


# ============================================================
# MATERIAL & PRODUCTION
# ============================================================

elif page == "Material & Production":

    show_material_production()


# ============================================================
# LOADING SYSTEM
# ============================================================

elif page == "Loading System":

    show_loading_system()


# ============================================================
# HAULAGE SYSTEM
# ============================================================

elif page == "Haulage System":

    show_haulage_system()


# ============================================================
# FLEET MATCHING
# ============================================================

elif page == "Fleet Matching":

    show_fleet_matching()


# ============================================================
# SENSITIVITY ANALYSIS
# ============================================================

elif page == "Sensitivity Analysis":

    show_analysis_lab()


# ============================================================
# SCENARIO COMPARISON
#
# ACTIVE MODULE
# ============================================================

elif page == "Scenario Comparison":

    show_scenario_comparison()


# ============================================================
# ECONOMICS
#
# UNDER DEVELOPMENT
# ============================================================

elif page == "Economics":

    show_coming_soon(
        icon="💰",
        eyebrow="Economic Analysis Module",
        title="Economics",
        subtitle=(
            "Connect equipment performance with operating "
            "and fleet economics."
        ),
        description=(
            "The Economics module will extend the engineering "
            "analysis into equipment ownership, operating "
            "costs and material handling cost evaluation."
        ),
        features=[
            "Equipment ownership cost",
            "Operating cost",
            "Cost per tonne",
            "Fleet cost comparison",
            "Productivity-cost relationships",
        ],
    )


# ============================================================
# OPTIMIZATION
#
# ACTIVE MODULE
# ============================================================

elif page == "Optimization":

    show_optimization()


# ============================================================
# EQUIPMENT LIBRARY
#
# UNDER DEVELOPMENT
# ============================================================

elif page == "Equipment Library":

    show_coming_soon(
        icon="📚",
        eyebrow="Equipment Resource",
        title="Equipment Library",
        subtitle=(
            "Explore equipment specifications used in "
            "MineOpsLab analyses."
        ),
        description=(
            "The Equipment Library will provide structured "
            "loader and haul-truck specifications that can "
            "later populate engineering inputs automatically."
        ),
        features=[
            "Loader specifications",
            "Truck specifications",
            "Payload capacities",
            "Bucket capacities",
            "Equipment operating ranges",
        ],
    )


# ============================================================
# LEARNING CENTRE
#
# UNDER DEVELOPMENT
# ============================================================

elif page == "Learning Centre":

    show_coming_soon(
        icon="🎓",
        eyebrow="Learning Resource",
        title="Learning Centre",
        subtitle=(
            "Connect MineOpsLab calculations with mining "
            "engineering concepts."
        ),
        description=(
            "The Learning Centre will provide explanations, "
            "worked examples and guided exercises linked "
            "directly to the MineOpsLab laboratory."
        ),
        features=[
            "Worked examples",
            "Engineering equations",
            "Concept explanations",
            "Student exercises",
            "Interpretation guides",
        ],
    )


# ============================================================
# FALLBACK
# ============================================================

else:

    st.error(
        "The selected MineOpsLab page could not be found."
    )
