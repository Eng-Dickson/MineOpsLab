
import streamlit as st


# ============================================================
# MINEOPSLAB PUBLIC HOMEPAGE
# ============================================================

def show_home(
    logo_path=None,
    on_explore=None,
    on_login=None,
    on_register=None,
    is_authenticated=False,
    on_dashboard=None,
):
    """
    MineOpsLab Student Edition public homepage.

    Uses native Streamlit elements for all visible content
    to prevent HTML from appearing as a code block.
    """

    # ========================================================
    # HOMEPAGE DESIGN
    # ========================================================

    st.markdown(
        """
<style>
.st-key-public_hero {
    background: linear-gradient(120deg, #081426, #142B49);
    border-radius: 20px;
    padding: 44px 42px;
    margin-top: 22px;
    margin-bottom: 18px;
}

.st-key-public_hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(32px, 4vw, 50px) !important;
    font-weight: 850 !important;
    line-height: 1.15 !important;
    letter-spacing: -1px;
}

.st-key-public_hero p {
    color: #D6E0EB !important;
    font-size: 16px;
    line-height: 1.75;
}

.st-key-public_hero .stCaptionContainer p {
    color: #F4A261 !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.st-key-public_hero [data-testid="stMarkdownContainer"] {
    color: #FFFFFF;
}

.st-key-home_brand h2 {
    color: #14213D !important;
    margin-bottom: 0;
    font-size: 26px;
}

.st-key-home_brand p {
    color: #667085 !important;
    font-size: 12px;
}

.st-key-home_feature_1,
.st-key-home_feature_2,
.st-key-home_feature_3 {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 16px;
    min-height: 220px;
}

.st-key-home_banner {
    background: #E8EEF5;
    border-radius: 14px;
    padding: 22px 25px;
    margin-top: 24px;
}

.st-key-home_banner p {
    color: #475467;
}

@media (max-width: 700px) {
    .st-key-public_hero {
        padding: 28px 22px;
    }

    .st-key-home_feature_1,
    .st-key-home_feature_2,
    .st-key-home_feature_3 {
        min-height: 0;
    }
}
</style>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # HEADER
    # ========================================================

    brand_col, account_col = st.columns([3, 2])

    with brand_col:
        with st.container(key="home_brand"):
            st.subheader("MineOpsLab")
            st.caption(
                "Student Edition | "
                "Mining Engineering Learning Platform"
            )

    with account_col:

        if is_authenticated:

            st.button(
                "👤 My Dashboard",
                key="public_dashboard",
                type="primary",
                width="stretch",
                on_click=on_dashboard,
            )

        else:

            login_col, register_col = st.columns(2)

            with login_col:
                st.button(
                    "Log In",
                    key="public_login",
                    width="stretch",
                    on_click=on_login,
                )

            with register_col:
                st.button(
                    "Register Free",
                    key="public_register",
                    type="primary",
                    width="stretch",
                    on_click=on_register,
                )

    # ========================================================
    # HERO SECTION
    # ========================================================

    with st.container(key="public_hero"):

        st.caption(
            "MINING ENGINEERING • SIMULATION • LEARNING"
        )

        st.title(
            "Design. Analyse. Optimize. Learn."
        )

        st.write(
            "An interactive engineering workspace for exploring "
            "mining operations, evaluating equipment performance, "
            "analysing operational scenarios and developing "
            "practical mining engineering skills."
        )

    # ========================================================
    # MAIN ACTIONS
    # ========================================================

    explore_col, info_col = st.columns([1, 2])

    with explore_col:

        st.button(
            "🚀 Open My Workspace"
            if is_authenticated
            else "🚀 Explore as Guest",
            key="public_explore",
            type="primary",
            width="stretch",
            on_click=on_explore,
        )

    with info_col:

        if is_authenticated:

            st.caption(
                "Welcome back! Continue exploring "
                "your mining engineering workspace."
            )

        else:

            st.caption(
                "No registration required. Explore engineering "
                "tools and learning resources freely."
            )

    # ========================================================
    # PLATFORM FEATURES
    # ========================================================

    st.subheader("Explore MineOpsLab")

    st.write(
        "Learn by doing. Apply engineering principles through "
        "interactive calculations, analysis and simulation."
    )

    feature_col1, feature_col2, feature_col3 = st.columns(
        3,
        gap="medium",
    )

    with feature_col1:

        with st.container(
            border=True,
            key="home_feature_1",
        ):

            st.markdown("### ⚙️ Engineering Tools")

            st.write(
                "Explore material production, loading, haulage, "
                "fleet matching, sensitivity analysis "
                "and optimization."
            )

            st.caption("OPEN ACCESS")

    with feature_col2:

        with st.container(
            border=True,
            key="home_feature_2",
        ):

            st.markdown("### 🎓 Learning Centre")

            st.write(
                "Access engineering concepts, worked examples "
                "and guided exercises as learning resources "
                "are introduced."
            )

            st.caption("OPEN ACCESS • IN DEVELOPMENT")

    with feature_col3:

        with st.container(
            border=True,
            key="home_feature_3",
        ):

            st.markdown("### 📁 My Projects")

            st.write(
                "Save engineering analyses, reopen previous work "
                "and manage projects from your personal dashboard."
            )

            st.caption("ACCOUNT REQUIRED • COMING SOON")

    # ========================================================
    # AVAILABLE ENGINEERING MODULES
    # ========================================================

    st.subheader("Start with Material Handling")

    st.write(
        "MineOpsLab currently focuses on surface mining "
        "material handling and loader-truck systems."
    )

    module_col1, module_col2 = st.columns(
        2,
        gap="large",
    )

    with module_col1:

        st.markdown("**🪨 Material & Production**")

        st.write(
            "Define material properties, operating conditions "
            "and production requirements."
        )

        st.markdown("**🚜 Loading System**")

        st.write(
            "Evaluate loader productivity, bucket payloads, "
            "loading cycles and equipment performance."
        )

    with module_col2:

        st.markdown("**🚛 Haulage System**")

        st.write(
            "Analyse haul-truck cycle times, payloads "
            "and transportation productivity."
        )

        st.markdown("**⚙️ Fleet Matching**")

        st.write(
            "Integrate loading and haulage systems to "
            "investigate fleet requirements."
        )

    st.button(
        "Open Engineering Workspace →",
        key="public_open_workspace",
        type="primary",
        on_click=on_explore,
    )

    # ========================================================
    # STUDENT ACCOUNT BANNER
    # ========================================================

    with st.container(key="home_banner"):

        if is_authenticated:

            st.markdown(
                "**Your personal engineering workspace.**"
            )

            st.write(
                "Your student account is active. Explore "
                "the engineering tools and access your "
                "student dashboard. Project saving and "
                "management features are under development."
            )

        else:

            st.markdown(
                "**Your engineering workspace, "
                "wherever you learn.**"
            )

            st.write(
                "Create a free MineOpsLab student account "
                "to access your personal dashboard, "
                "or continue exploring the engineering "
                "tools without registration. Project "
                "saving features are under development."
            )

    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()

    st.caption(
        "MineOpsLab Student Edition © 2026 | "
        "Mining Operations Optimization & Learning Platform"
    )
