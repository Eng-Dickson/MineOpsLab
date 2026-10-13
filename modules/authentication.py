
import streamlit as st
from supabase import create_client


# ============================================================
# SUPABASE CONNECTION
# ============================================================

def get_supabase():
    """Create a Supabase client using Streamlit secrets."""

    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)

    except (KeyError, FileNotFoundError):
        st.error(
            "Supabase configuration is missing. "
            "Check your Streamlit secrets."
        )
        return None


# ============================================================
# SESSION STATE
# ============================================================

def initialize_auth():
    """Initialize authentication state."""

    defaults = {
        "auth_user": None,
        "auth_session": None,
        "auth_page": "login",
        "auth_message": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def is_logged_in():
    """Check whether a user is currently authenticated."""

    initialize_auth()

    session = st.session_state.get("auth_session")
    user = st.session_state.get("auth_user")

    if not session or not user:
        return False

    return True


def get_current_user():
    """Return the current authenticated user."""

    if is_logged_in():
        return st.session_state.auth_user

    return None


# ============================================================
# REGISTRATION
# ============================================================

def register_student(
    full_name,
    email,
    password,
    institution="",
    programme="",
):
    """Register a new student using Supabase Auth."""

    client = get_supabase()

    if client is None:
        return False, "Supabase is not configured."

    try:
        response = client.auth.sign_up(
            {
                "email": email.strip().lower(),
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name.strip(),
                        "institution": institution.strip(),
                        "programme": programme.strip(),
                    }
                },
            }
        )

        if response.user is None:
            return False, "Registration could not be completed."

        return (
            True,
            "Registration request received. "
            "Please check your email for a verification link "
            "before logging in.",
        )

    except Exception as exc:
        return False, str(exc)


# ============================================================
# LOGIN
# ============================================================

def login_student(email, password):
    """Authenticate a student with Supabase."""

    client = get_supabase()

    if client is None:
        return False, "Supabase is not configured."

    try:
        response = client.auth.sign_in_with_password(
            {
                "email": email.strip().lower(),
                "password": password,
            }
        )

        if response.user is None or response.session is None:
            return False, "Login could not be completed."

        st.session_state.auth_user = response.user
        st.session_state.auth_session = response.session

        return True, "Login successful."

    except Exception:
        return (
            False,
            "Unable to log in. Check your email, password "
            "and email verification status.",
        )


# ============================================================
# LOGOUT
# ============================================================

def logout_student():
    """Sign out the current student."""

    initialize_auth()

    session = st.session_state.get("auth_session")

    if session is not None:
        client = get_supabase()

        if client is not None:
            try:
                client.auth.set_session(
                    session.access_token,
                    session.refresh_token,
                )
                client.auth.sign_out()
            except Exception:
                pass

    st.session_state.auth_user = None
    st.session_state.auth_session = None
    st.session_state.auth_page = "login"


# ============================================================
# PASSWORD RECOVERY REQUEST
# ============================================================

def request_password_reset(email):
    """Send a password recovery email."""

    client = get_supabase()

    if client is None:
        return False, "Supabase is not configured."

    try:
        client.auth.reset_password_email(
            email.strip().lower(),
            options={
                "redirect_to": (
                    "https://mineopslab.streamlit.app/"
                )
            },
        )

        return (
            True,
            "If an account exists for this email address, "
            "a password recovery email will be sent.",
        )

    except Exception:
        return (
            False,
            "The password recovery request could not "
            "be completed. Please try again later.",
        )


# ============================================================
# LOGIN PAGE
# ============================================================

def show_login():

    initialize_auth()

    st.title("Welcome Back")

    st.write(
        "Log in to your MineOpsLab student account."
    )

    with st.form("student_login_form"):

        email = st.text_input(
            "Email Address",
            placeholder="student@example.com",
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Log In",
            type="primary",
            use_container_width=True,
        )

        if submitted:

            if not email or not password:
                st.warning(
                    "Please enter your email and password."
                )

            else:
                success, message = login_student(
                    email,
                    password,
                )

                if success:
                    st.session_state.current_page = (
                        "Student Dashboard"
                    )
                    st.rerun()

                else:
                    st.error(message)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Create an Account",
            use_container_width=True,
        ):
            st.session_state.current_page = "Register"
            st.rerun()

    with col2:
        if st.button(
            "Forgot Password?",
            use_container_width=True,
        ):
            st.session_state.current_page = (
                "Forgot Password"
            )
            st.rerun()

    st.divider()

    if st.button("← Return to Homepage"):
        st.session_state.current_page = "Home"
        st.rerun()


# ============================================================
# REGISTRATION PAGE
# ============================================================

def show_register():

    initialize_auth()

    st.title("Create Your Free Account")

    st.write(
        "Join MineOpsLab to access your personal "
        "engineering workspace."
    )

    with st.form("student_registration_form"):

        full_name = st.text_input(
            "Full Name *",
        )

        email = st.text_input(
            "Email Address *",
        )

        institution = st.text_input(
            "University / Institution (Optional)",
        )

        programme = st.text_input(
            "Programme of Study (Optional)",
        )

        password = st.text_input(
            "Password *",
            type="password",
        )

        confirm_password = st.text_input(
            "Confirm Password *",
            type="password",
        )

        submitted = st.form_submit_button(
            "Create Free Account",
            type="primary",
            use_container_width=True,
        )

        if submitted:

            if not full_name.strip() or not email.strip():
                st.warning(
                    "Please provide your name and email."
                )

            elif not password:
                st.warning(
                    "Please create a password."
                )

            elif password != confirm_password:
                st.error(
                    "The passwords do not match."
                )

            elif len(password) < 8:
                st.warning(
                    "Use a password with at least 8 characters."
                )

            else:
                success, message = register_student(
                    full_name,
                    email,
                    password,
                    institution,
                    programme,
                )

                if success:
                    st.success(message)

                else:
                    st.error(message)

    st.divider()

    if st.button(
        "Already have an account? Log In",
        use_container_width=True,
    ):
        st.session_state.current_page = "Login"
        st.rerun()

    if st.button("← Return to Homepage"):
        st.session_state.current_page = "Home"
        st.rerun()


# ============================================================
# FORGOT PASSWORD PAGE
# ============================================================

def show_forgot_password():

    st.title("Reset Your Password")

    st.write(
        "Enter your registered email address to "
        "request a password recovery link."
    )

    with st.form("password_recovery_form"):

        email = st.text_input(
            "Email Address",
        )

        submitted = st.form_submit_button(
            "Send Recovery Email",
            type="primary",
            use_container_width=True,
        )

        if submitted:

            if not email.strip():
                st.warning(
                    "Please enter your email address."
                )

            else:
                success, message = request_password_reset(
                    email
                )

                if success:
                    st.success(message)

                else:
                    st.error(message)

    if st.button("← Back to Login"):
        st.session_state.current_page = "Login"
        st.rerun()


# ============================================================
# INITIAL STUDENT DASHBOARD
# ============================================================

def show_student_dashboard():

    initialize_auth()

    if not is_logged_in():
        st.warning(
            "Please log in to access your student dashboard."
        )

        if st.button("Go to Login"):
            st.session_state.current_page = "Login"
            st.rerun()

        return

    user = get_current_user()

    metadata = user.user_metadata or {}

    full_name = metadata.get(
        "full_name",
        "Student",
    )

    st.caption("MINEOPSLAB STUDENT EDITION")

    st.title(f"Welcome, {full_name}!")

    st.write(
        "Your personal mining engineering workspace."
    )

    st.success(
        "You are logged in to MineOpsLab."
    )

    st.subheader("Your Workspace")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "⚙️ Engineering Tools",
            use_container_width=True,
        ):
            st.session_state.current_page = "Workspace"
            st.rerun()

    with col2:
        st.button(
            "📁 My Projects — Coming Soon",
            use_container_width=True,
            disabled=True,
        )

    st.divider()

    st.write(
        "Project saving and personalized learning "
        "features will be introduced in the next phase."
    )

    if st.button("Log Out"):
        logout_student()
        st.session_state.current_page = "Home"
        st.rerun()
