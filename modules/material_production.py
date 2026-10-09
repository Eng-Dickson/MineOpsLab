import streamlit as st

from calculations.material import calculate_material_production
from data.materials import (
    get_material_names,
    get_material_properties,
)


def show_material_production():

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
"""<div class="mineops-page-header">
<div class="mineops-eyebrow">
Mine Planning Input Module
</div>

<div class="mineops-page-title">
🪨 Material &amp; Production
</div>

<div class="mineops-page-subtitle">
Define the material characteristics and translate the annual
mine production target into the operating requirement for the
loading and haulage system.
</div>
</div>""",
        unsafe_allow_html=True,
    )


    # ========================================================
    # MATERIAL LIBRARY
    # ========================================================

    material_names = get_material_names()

    if "material_type" not in st.session_state:
        st.session_state.material_type = "Waste Rock"

    if "previous_material_type" not in st.session_state:
        st.session_state.previous_material_type = None


    # ========================================================
    # DEFAULT PRODUCTION PLAN
    # ========================================================

    if "annual_production_target" not in st.session_state:
        st.session_state.annual_production_target = 1_000_000.0

    if "operating_days_per_year" not in st.session_state:
        st.session_state.operating_days_per_year = 300

    if "shifts_per_day" not in st.session_state:
        st.session_state.shifts_per_day = 2

    if "shift_duration_hours" not in st.session_state:
        st.session_state.shift_duration_hours = 8.0


    # ========================================================
    # MATERIAL SELECTION
    # ========================================================

    st.subheader("🪨 Material Properties")

    material_type = st.selectbox(
        "Material type",
        material_names,
        index=material_names.index(
            st.session_state.material_type
        ),
        help=(
            "Selecting a material loads default engineering "
            "properties. These values remain editable."
        ),
    )


    # ========================================================
    # LOAD DEFAULTS WHEN MATERIAL CHANGES
    # ========================================================

    if (
        st.session_state.previous_material_type
        != material_type
    ):

        defaults = get_material_properties(
            material_type
        )

        st.session_state.bank_density = (
            defaults["bank_density"]
        )

        st.session_state.swell_factor_percent = (
            defaults["swell_factor"]
        )

        st.session_state.previous_material_type = (
            material_type
        )


    # ========================================================
    # MATERIAL INPUTS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.text_input(
            "Selected material",
            value=material_type,
            disabled=True,
        )

    with col2:

        bank_density = st.number_input(
            "Bank density (t/m³)",
            min_value=0.10,
            value=float(
                st.session_state.bank_density
            ),
            step=0.05,
            help=(
                "In-situ density before excavation. "
                "The library value is editable."
            ),
        )

    with col3:

        swell_factor_percent = st.number_input(
            "Swell factor (%)",
            min_value=0.0,
            max_value=200.0,
            value=float(
                st.session_state.swell_factor_percent
            ),
            step=1.0,
            help=(
                "Percentage increase in material volume "
                "after excavation."
            ),
        )


    # ========================================================
    # PRODUCTION PLAN
    # ========================================================

    st.write("")
    st.subheader("🎯 Production Plan")

    col1, col2 = st.columns(2, gap="large")

    with col1:

        annual_production_target = st.number_input(
            "Annual production target (tonnes/year)",
            min_value=0.0,
            value=float(
                st.session_state.annual_production_target
            ),
            step=50_000.0,
        )

        operating_days_per_year = st.number_input(
            "Operating days per year",
            min_value=1,
            max_value=366,
            value=int(
                st.session_state.operating_days_per_year
            ),
            step=1,
        )

    with col2:

        shifts_per_day = st.number_input(
            "Shifts per day",
            min_value=1,
            max_value=4,
            value=int(
                st.session_state.shifts_per_day
            ),
            step=1,
        )

        shift_duration_hours = st.number_input(
            "Shift duration (hours)",
            min_value=1.0,
            max_value=24.0,
            value=float(
                st.session_state.shift_duration_hours
            ),
            step=0.5,
        )


    # ========================================================
    # SAVE INPUTS
    # ========================================================

    st.session_state.material_type = (
        material_type
    )

    st.session_state.bank_density = (
        bank_density
    )

    st.session_state.swell_factor_percent = (
        swell_factor_percent
    )

    st.session_state.annual_production_target = (
        annual_production_target
    )

    st.session_state.operating_days_per_year = (
        operating_days_per_year
    )

    st.session_state.shifts_per_day = (
        shifts_per_day
    )

    st.session_state.shift_duration_hours = (
        shift_duration_hours
    )


    # ========================================================
    # RUN MATERIAL ENGINE
    # ========================================================

    try:

        results = calculate_material_production(
            annual_production_target=annual_production_target,
            operating_days_per_year=operating_days_per_year,
            shifts_per_day=shifts_per_day,
            shift_duration_hours=shift_duration_hours,
            bank_density=bank_density,
            swell_factor_percent=swell_factor_percent,
        )

    except ValueError as error:

        st.error(str(error))
        return


    # ========================================================
    # STORE RESULTS FOR DOWNSTREAM MODULES
    # ========================================================

    st.session_state.material_density = (
        results["loose_density"]
    )

    st.session_state.production_target = (
        results["shift_production"]
    )

    st.session_state.shift_hours = (
        shift_duration_hours
    )

    st.session_state.required_production_tph = (
        results["hourly_production"]
    )

    st.session_state.required_volume_m3ph = (
        results["hourly_loose_volume"]
    )

    st.session_state.material_results = results


    # ========================================================
    # MATERIAL RESULT
    # ========================================================

    st.write("")
    st.subheader("Material Behaviour")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Bank Density",
            f"{bank_density:.2f} t/m³",
        )

    with c2:

        st.metric(
            "Swell Factor",
            f"{swell_factor_percent:.0f}%",
        )

    with c3:

        st.metric(
            "Calculated Loose Density",
            f"{results['loose_density']:.2f} t/m³",
        )


    # ========================================================
    # PRODUCTION BASIS
    # ========================================================

    st.write("")
    st.subheader("Production Basis")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Annual Target",
            (
                f"{annual_production_target:,.0f} "
                "t/year"
            ),
        )

    with c2:

        st.metric(
            "Daily Production",
            (
                f"{results['daily_production']:,.0f} "
                "t/day"
            ),
        )

    with c3:

        st.metric(
            "Shift Production",
            (
                f"{results['shift_production']:,.0f} "
                "t/shift"
            ),
        )

    with c4:

        st.metric(
            "Required Production",
            (
                f"{results['hourly_production']:,.0f} "
                "t/h"
            ),
        )


    # ========================================================
    # OPERATING BASIS
    # ========================================================

    st.write("")
    st.subheader("Operating Basis")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Scheduled Shifts",
            (
                f"{results['shifts_per_year']:,.0f} "
                "shifts/year"
            ),
        )

    with c2:

        st.metric(
            "Scheduled Operating Hours",
            (
                f"{results['scheduled_hours_per_year']:,.0f} "
                "h/year"
            ),
        )

    with c3:

        st.metric(
            "Required Loose Volume",
            (
                f"{results['hourly_loose_volume']:,.0f} "
                "m³/h"
            ),
        )


    # ========================================================
    # ENGINEERING SUMMARY
    # ========================================================

    st.write("")

    st.markdown(
f"""<div class="mineops-card">
<h3>Engineering Basis</h3>
<p>
The selected <strong>{material_type}</strong> has a bank density
of <strong>{bank_density:.2f} t/m³</strong> and an assumed swell
factor of <strong>{swell_factor_percent:.0f}%</strong>.
After excavation, the calculated loose bulk density is
<strong>{results['loose_density']:.2f} t/m³</strong>.
<br><br>
To achieve an annual production target of
<strong>{annual_production_target:,.0f} tonnes</strong> over
<strong>{operating_days_per_year}</strong> operating days,
<strong>{shifts_per_day}</strong> shifts per day and
<strong>{shift_duration_hours:.1f}</strong> hours per shift,
the material handling system must provide approximately
<strong>{results['hourly_production']:,.0f} t/h</strong>.
</p>
</div>""",
        unsafe_allow_html=True,
    )

    st.write("")

    st.caption(
        "Material-library values are development defaults and "
        "should be replaced with site-specific or verified "
        "reference data where available."
    )

    st.success(
        "✓ Material and production requirements are available "
        "to the Loading System."
    )