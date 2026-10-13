from pathlib import Path

import streamlit as st

# ============================================================
# MODULE IMPORTS
# ============================================================

from modules.home import show_home
from modules.material_production import show_material_production
from modules.loading_system import show_loading_system
from modules.haulage_system import show_haulage_system
from modules.fleet_matching import show_fleet_matching
from modules.analysis_lab import show_analysis_lab
from modules.scenario_comparison import show_scenario_comparison
from modules.optimization import show_optimization
from modules.coming_soon import show_coming_soon

from modules.authentication import (
    initialize_auth,
    is_logged_in,
    logout_student,
    show_login,
    show_register,
    show_forgot_password,
    show_student_dashboard,
)


# ============================================================
# APPLICATION PATHS
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
    page_title="MineOpsLab | Student Edition",
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

/* APPLICATION */

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


/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #081426 0%,
        #0D2038 55%,
        #142B49 100%
    );
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

[data-testid="stSidebar"] img {
    border-radius: 14px;
}

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

.nav-section {
    color: #8298B1 !important;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin-top: 20px;
    margin-bottom: 8px;
}


/* SIDEBAR BUTTONS */

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    border-radius: 8px;
    text-align: left;
    justify-content: flex-start;
    font-size: 14px;
    font-weight: 600;
    min-height: 40px;
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.15s ease;
}

[data-testid="stSidebar"]
.stButton > button[kind="secondary"] {
    background: transparent;
    color: #DCE6F0;
}

[data-testid="stSidebar"]
.stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.07);
    border-color: rgba(255,255,255,0.15);
}

[data-testid="stSidebar"]
.stButton > button[kind="primary"] {
    background: #F4A261;
    color: #14213D;
    border-color: #F4A261;
    font-weight: 750;
}

.sidebar-footer {
    margin-top: 30px;
    padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.10);
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


/* PAGE HEADERS */

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


/* CARDS */

.mineops-card {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 1px 2px rgba(16,24,40,0.04);
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


/* METRICS */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 12px;
    padding: 14px 16px;
    box-shadow: 0 1px 2px rgba(16,24,40,0.03);
}

[data-testid="stMetricLabel"] {
    color: #667085;
}

[data-testid="stMetricValue"] {
    color: #14213D;
}


/* DATAFRAMES AND EXPANDERS */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 12px;
}


/* WORKSPACE NAVIGATION BUTTONS */

.st-key-workspace_nav button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #14213D !important;
    border: 1px solid #E0E6EF !important;
    border-radius: 12px !important;
    min-height: 65px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    justify-content: flex-start !important;
    padding: 15px 20px !important;
    text-align: left !important;
    box-shadow: 0 2px 5px rgba(16,24,40,0.035);
    transition: all 0.18s ease;
}

.st-key-workspace_nav button[kind="secondary"] p {
    color: #14213D !important;
    font-weight: 700 !important;
}

.st-key-workspace_nav button[kind="secondary"]:hover {
    background: #FFF7EF !important;
    border-color: #F4A261 !important;
    color: #14213D !important;
    box-shadow: 0 4px 12px rgba(16,24,40,0.08);
}


/* RESPONSIVE DESIGN */

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

initialize_auth()

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "access_mode" not in st.session_state:
    st.session_state.access_mode = "public"


# ============================================================
# NAVIGATION FUNCTIONS
# ============================================================

def navigate(page_name):
    st.session_state.current_page = page_name


def enter_guest_workspace():
    if is_logged_in():
        st.session_state.access_mode = "student"
    else:
        st.session_state.access_mode = "guest"

    st.session_state.current_page = "Workspace"


def return_to_public_home():
    st.session_state.access_mode = "public"
    st.session_state.current_page = "Home"


def go_to_login():
    st.session_state.current_page = "Login"


def go_to_register():
    st.session_state.current_page = "Register"


def go_to_dashboard():
    if is_logged_in():
        st.session_state.current_page = "Student Dashboard"
    else:
        st.session_state.current_page = "Login"


def sign_out_to_home():
    logout_student()
    st.session_state.access_mode = "public"
    st.session_state.current_page = "Home"


def sidebar_navigation_button(page_name):
    active = st.session_state.current_page == page_name

    st.button(
        page_name,
        key=f"nav_{page_name}",
        width="stretch",
        type="primary" if active else "secondary",
        on_click=navigate,
        args=(page_name,),
    )


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.current_page

public_pages = {
    "Home",
    "Login",
    "Register",
    "Forgot Password",
}

is_public_home = page in public_pages


# ============================================================
# PUBLIC PAGE LAYOUT
# ============================================================

if is_public_home:
    st.markdown(
        """
<style>

[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

[data-testid="stMain"] .block-container {
    max-width: 1160px;
}

</style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ENGINEERING WORKSPACE SIDEBAR
# ============================================================

if not is_public_home:

    with st.sidebar:

        # BRAND ICON

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

        # BRAND

        st.markdown(
            """
<div class="sidebar-brand-name">
    Mine<span>Ops</span>Lab
</div>

<div class="sidebar-brand-tagline">
    Mining Operations Optimization &amp;
    Learning Platform
</div>
            """,
            unsafe_allow_html=True,
        )

        if is_logged_in():
            st.caption("Student Workspace")
        else:
            st.caption("Guest Workspace")

        # PLATFORM

        st.markdown(
            '<div class="nav-section">Platform</div>',
            unsafe_allow_html=True,
        )

        if is_logged_in():
            sidebar_navigation_button("Student Dashboard")

        sidebar_navigation_button("Workspace")

        st.button(
            "← Public Homepage",
            key="nav_public_home",
            width="stretch",
            on_click=return_to_public_home,
        )

        # MATERIAL HANDLING

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
            sidebar_navigation_button(page_name)

        # ANALYSIS

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
            sidebar_navigation_button(page_name)

        # RESOURCES

        st.markdown(
            '<div class="nav-section">Resources</div>',
            unsafe_allow_html=True,
        )

        resource_pages = [
            "Equipment Library",
            "Learning Centre",
        ]

        for page_name in resource_pages:
            sidebar_navigation_button(page_name)

        # STUDENT ACCOUNT

        st.markdown(
            '<div class="nav-section">Student Account</div>',
            unsafe_allow_html=True,
        )

        st.button(
            "🔒 My Projects",
            key="nav_my_projects",
            width="stretch",
            disabled=True,
            help="Project saving is coming soon.",
        )

        if is_logged_in():

            st.button(
                "Log Out",
                key="sidebar_logout",
                width="stretch",
                on_click=sign_out_to_home,
            )

        else:

            st.button(
                "Log In / Register",
                key="sidebar_login",
                width="stretch",
                on_click=go_to_login,
            )

        # FOOTER

        st.markdown(
            """
<div class="sidebar-footer">

    <div class="sidebar-footer-title">
        MineOpsLab
    </div>

    <div class="sidebar-footer-text">
        Surface Mining Teaching &amp;
        Analysis Environment<br>
        Student Edition | 2026
    </div>

</div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# PUBLIC HOMEPAGE
# ============================================================

if page == "Home":

    show_home(
        logo_path=LOGO_PATH,
        on_explore=enter_guest_workspace,
        on_login=go_to_login,
        on_register=go_to_register,
        is_authenticated=is_logged_in(),
        on_dashboard=go_to_dashboard,
    )


# ============================================================
# AUTHENTICATION PAGES
# ============================================================

elif page == "Login":
    show_login()

elif page == "Register":
    show_register()

elif page == "Forgot Password":
    show_forgot_password()


# ============================================================
# STUDENT DASHBOARD
# ============================================================

elif page == "Student Dashboard":

    if not is_logged_in():
        st.session_state.current_page = "Login"
        st.warning(
            "Please log in to access your student dashboard."
        )

        if st.button("Go to Login"):
            st.rerun()

    else:
        show_student_dashboard()


# ============================================================
# ENGINEERING WORKSPACE
# ============================================================

elif page == "Workspace":

    # Native Streamlit components prevent raw HTML
    # from appearing as a Markdown code block.

    st.caption("MINEOPSLAB STUDENT EDITION")

    st.title("Engineering Workspace")

    st.write(
        "Explore mining engineering calculations, "
        "equipment performance and operational analysis. "
        "Select a module to begin."
    )

    if is_logged_in():

        st.success(
            "Student account active. "
            "Engineering tools are ready to use."
        )

    else:

        st.info(
            "You are exploring MineOpsLab as a guest. "
            "Engineering tools are freely accessible. "
            "Student accounts are optional; "
            "saved projects are coming soon."
        )

    # WORKSPACE NAVIGATION

    with st.container(key="workspace_nav"):

        st.subheader("Material Handling")

        st.caption(
            "Explore production requirements, loading equipment, "
            "haulage systems and fleet configuration."
        )

        col1, col2 = st.columns(2, gap="medium")

        with col1:

            st.button(
                "🪨  Material & Production",
                key="workspace_material",
                width="stretch",
                on_click=navigate,
                args=("Material & Production",),
            )

            st.button(
                "🚜  Loading System",
                key="workspace_loading",
                width="stretch",
                on_click=navigate,
                args=("Loading System",),
            )

        with col2:

            st.button(
                "🚛  Haulage System",
                key="workspace_haulage",
                width="stretch",
                on_click=navigate,
                args=("Haulage System",),
            )

            st.button(
                "⚙️  Fleet Matching",
                key="workspace_fleet",
                width="stretch",
                on_click=navigate,
                args=("Fleet Matching",),
            )

        st.subheader("Analysis & Optimization")

        st.caption(
            "Investigate operating scenarios, analyse performance "
            "and explore alternative configurations."
        )

        col3, col4 = st.columns(2, gap="medium")

        with col3:

            st.button(
                "📊  Sensitivity Analysis",
                key="workspace_sensitivity",
                width="stretch",
                on_click=navigate,
                args=("Sensitivity Analysis",),
            )

            st.button(
                "📑  Scenario Comparison",
                key="workspace_scenarios",
                width="stretch",
                on_click=navigate,
                args=("Scenario Comparison",),
            )

        with col4:

            st.button(
                "🎯  Optimization",
                key="workspace_optimization",
                width="stretch",
                on_click=navigate,
                args=("Optimization",),
            )

            st.button(
                "🎓  Learning Centre",
                key="workspace_learning",
                width="stretch",
                on_click=navigate,
                args=("Learning Centre",),
            )

    st.caption(
        "Learning Centre resources are currently under development."
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
# ============================================================

elif page == "Scenario Comparison":
    show_scenario_comparison()


# ============================================================
# ECONOMICS - UNDER DEVELOPMENT
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
# ============================================================

elif page == "Optimization":
    show_optimization()


# ============================================================
# EQUIPMENT LIBRARY - UNDER DEVELOPMENT
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
# LEARNING CENTRE - UNDER DEVELOPMENT
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

    st.button(
        "Return to Homepage",
        on_click=return_to_public_home,
    )