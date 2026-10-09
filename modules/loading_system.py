import streamlit as st

from calculations.loader import calculate_loader_performance


def show_loading_system():

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        """
<div class="mineops-page-header">
<div class="mineops-eyebrow">
Equipment Performance Module
</div>

<div class="mineops-page-title">
🚜 Loading System
</div>

<div class="mineops-page-subtitle">
Configure the loading equipment and evaluate bucket performance,
theoretical productivity, Mine Productivity Index (MPI),
effective productivity and the loader fleet required to satisfy
the mine production target.
</div>
</div>
""",
        unsafe_allow_html=True,
    )


    # ========================================================
    # CHECK FOR MATERIAL & PRODUCTION DATA
    # ========================================================

    required_keys = [
        "material_type",
        "material_density",
        "required_production_tph",
        "production_target",
    ]

    missing_data = any(
        key not in st.session_state
        for key in required_keys
    )

    if missing_data:

        st.warning(
            "Material and production requirements have not yet "
            "been defined. Complete the Material & Production "
            "module first."
        )

        return


    # ========================================================
    # INHERITED DATA
    # ========================================================

    material_type = (
        st.session_state.material_type
    )

    loose_density = (
        st.session_state.material_density
    )

    required_production_tph = (
        st.session_state.required_production_tph
    )

    shift_production = (
        st.session_state.production_target
    )


    # ========================================================
    # SYSTEM REQUIREMENT
    # ========================================================

    st.subheader("Mine Production Requirement")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Material",
            material_type,
        )

    with c2:

        st.metric(
            "Loose Density",
            f"{loose_density:.2f} t/m³",
        )

    with c3:

        st.metric(
            "Shift Production",
            f"{shift_production:,.0f} t/shift",
        )

    with c4:

        st.metric(
            "Required Production",
            f"{required_production_tph:,.0f} t/h",
        )

    st.caption(
        "These values are inherited automatically from "
        "Material & Production."
    )


    # ========================================================
    # DEFAULT LOADER INPUTS
    # ========================================================

    if "loader_type" not in st.session_state:
        st.session_state.loader_type = "Wheel Loader"

    if "loader_bucket_capacity" not in st.session_state:
        st.session_state.loader_bucket_capacity = 12.0

    if "loader_fill_factor" not in st.session_state:
        st.session_state.loader_fill_factor = 90.0

    if "loader_cycle_time" not in st.session_state:
        st.session_state.loader_cycle_time = 32.0

    if "loader_availability" not in st.session_state:
        st.session_state.loader_availability = 90.0

    if "loader_performance" not in st.session_state:
        st.session_state.loader_performance = 85.0

    if "loader_utilization" not in st.session_state:
        st.session_state.loader_utilization = 85.0


    # ========================================================
    # LOADER SPECIFICATION
    # ========================================================

    st.write("")
    st.subheader("🚜 Loader Specification")

    col1, col2 = st.columns(2, gap="large")


    # --------------------------------------------------------
    # EQUIPMENT
    # --------------------------------------------------------

    with col1:

        loader_options = [
            "Wheel Loader",
            "Hydraulic Excavator",
            "Electric Rope Shovel",
            "Hydraulic Mining Shovel",
            "Custom Loader",
        ]

        loader_type = st.selectbox(
            "Loader type",
            loader_options,
            index=loader_options.index(
                st.session_state.loader_type
            )
            if st.session_state.loader_type
            in loader_options
            else 0,
        )

        bucket_capacity = st.number_input(
            "Rated bucket capacity (m³)",
            min_value=0.1,
            value=float(
                st.session_state.loader_bucket_capacity
            ),
            step=0.5,
            help=(
                "Rated volumetric capacity of the "
                "loading equipment bucket."
            ),
        )

        fill_factor_percent = st.number_input(
            "Bucket fill factor (%)",
            min_value=1.0,
            max_value=100.0,
            value=float(
                st.session_state.loader_fill_factor
            ),
            step=1.0,
            help=(
                "Actual bucket fill expressed as a percentage "
                "of rated bucket capacity."
            ),
        )

        cycle_time_sec = st.number_input(
            "Bucket cycle time (seconds)",
            min_value=1.0,
            value=float(
                st.session_state.loader_cycle_time
            ),
            step=1.0,
            help=(
                "Time required for one complete loading cycle "
                "under the specified operating conditions."
            ),
        )


    # --------------------------------------------------------
    # PRODUCTIVITY FACTORS
    # --------------------------------------------------------

    with col2:

        st.markdown("#### Productivity Factors")

        st.caption(
            "Availability, Performance and Utilization are "
            "combined to determine the loader Mine Productivity "
            "Index (MPI)."
        )

        availability_percent = st.number_input(
            "Mechanical availability, Av (%)",
            min_value=1.0,
            max_value=100.0,
            value=float(
                st.session_state.loader_availability
            ),
            step=1.0,
            help=(
                "The proportion of scheduled time during which "
                "the loader is mechanically available for operation."
            ),
        )

        performance_percent = st.number_input(
            "Performance, PP (%)",
            min_value=1.0,
            max_value=100.0,
            value=float(
                st.session_state.loader_performance
            ),
            step=1.0,
            help=(
                "Performance reflects the extent to which the "
                "loader performs relative to its expected "
                "operating performance."
            ),
        )

        utilization_percent = st.number_input(
            "Utilization, U (%)",
            min_value=1.0,
            max_value=100.0,
            value=float(
                st.session_state.loader_utilization
            ),
            step=1.0,
            help=(
                "The proportion of available time during which "
                "the loader is actually operating."
            ),
        )


    # ========================================================
    # SAVE INPUTS
    # ========================================================

    st.session_state.loader_type = (
        loader_type
    )

    st.session_state.loader_bucket_capacity = (
        bucket_capacity
    )

    st.session_state.loader_fill_factor = (
        fill_factor_percent
    )

    st.session_state.loader_cycle_time = (
        cycle_time_sec
    )

    st.session_state.loader_availability = (
        availability_percent
    )

    st.session_state.loader_performance = (
        performance_percent
    )

    st.session_state.loader_utilization = (
        utilization_percent
    )


    # ========================================================
    # CONVERT PERCENTAGES
    # ========================================================

    fill_factor = (
        fill_factor_percent / 100.0
    )

    availability = (
        availability_percent / 100.0
    )

    performance = (
        performance_percent / 100.0
    )

    utilization = (
        utilization_percent / 100.0
    )


    # ========================================================
    # RUN LOADER ENGINE
    # ========================================================

    try:

        results = calculate_loader_performance(
            bucket_capacity_m3=bucket_capacity,
            fill_factor=fill_factor,
            loose_density=loose_density,
            bucket_cycle_time_sec=cycle_time_sec,
            availability=availability,
            utilization=utilization,
            performance=performance,
            required_production_tph=required_production_tph,
        )

    except ValueError as error:

        st.error(str(error))
        return


    # ========================================================
    # STORE RESULTS
    # ========================================================

    st.session_state.loader_results = (
        results
    )

    st.session_state.loaders_required = (
        results["loaders_required"]
    )

    st.session_state.loader_effective_productivity = (
        results["effective_productivity_tph"]
    )

    st.session_state.loader_theoretical_productivity = (
        results["theoretical_productivity_tph"]
    )

    st.session_state.loader_mpi = (
        results["mpi"]
    )

    st.session_state.bucket_payload_t = (
        results["bucket_payload_t"]
    )


    # ========================================================
    # PRIMARY RESULTS
    # ========================================================

    st.write("")
    st.subheader("Loading System Results")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Required Loaders",
            f"{results['loaders_required']}",
        )

    with c2:

        st.metric(
            "Bucket Payload",
            f"{results['bucket_payload_t']:.2f} t",
        )

    with c3:

        st.metric(
            "Loader MPI",
            f"{results['mpi'] * 100:.1f}%",
        )

    with c4:

        st.metric(
            "Effective Productivity",
            (
                f"{results['effective_productivity_tph']:,.0f} "
                "t/h"
            ),
        )


    # ========================================================
    # PRODUCTIVITY TRANSFORMATION
    # ========================================================

    st.write("")
    st.subheader("📊 Productivity Performance")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Theoretical Productivity",
            (
                f"{results['theoretical_productivity_tph']:,.0f} "
                "t/h"
            ),
        )

    with c2:

        st.metric(
            "Productivity Retained",
            f"{results['mpi'] * 100:.1f}%",
        )

    with c3:

        st.metric(
            "Productivity Loss",
            (
                f"{results['productivity_loss_tph']:,.0f} "
                "t/h"
            ),
        )


    # ========================================================
    # MPI PANEL
    # ========================================================

    st.write("")
    st.subheader("⛏️ Mine Productivity Index")

    st.caption(
        "The Mine Productivity Index combines equipment "
        "availability, performance and utilization into a "
        "single operational productivity indicator."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Availability",
            f"{availability_percent:.1f}%",
        )

    with c2:

        st.metric(
            "Performance",
            f"{performance_percent:.1f}%",
        )

    with c3:

        st.metric(
            "Utilization",
            f"{utilization_percent:.1f}%",
        )

    with c4:

        st.metric(
            "Loader MPI",
            f"{results['mpi'] * 100:.1f}%",
        )

    st.latex(
        r"""
        MPI =
        Av^{0.3}
        \times
        PP^{0.5}
        \times
        U^{0.2}
        """
    )

    st.write(
        f"For the current loader, "
        f"**Av = {availability:.2f}**, "
        f"**PP = {performance:.2f}**, and "
        f"**U = {utilization:.2f}**."
    )

    st.write(
        f"The resulting loader Mine Productivity Index is "
        f"**{results['mpi'] * 100:.1f}%**."
    )


    # ========================================================
    # FLEET CAPACITY
    # ========================================================

    st.write("")
    st.subheader("Fleet Capacity")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Required Production",
            f"{required_production_tph:,.0f} t/h",
        )

    with c2:

        st.metric(
            "Effective Productivity / Loader",
            (
                f"{results['effective_productivity_tph']:,.0f} "
                "t/h"
            ),
        )

    with c3:

        st.metric(
            "Installed Loader Capacity",
            (
                f"{results['installed_capacity_tph']:,.0f} "
                "t/h"
            ),
        )

    with c4:

        capacity_utilization_percent = (
            results[
                "installed_capacity_utilization"
            ]
            * 100
        )

        st.metric(
            "Installed Capacity Utilization",
            f"{capacity_utilization_percent:.1f}%",
        )


    # ========================================================
    # CAPACITY MESSAGE
    # ========================================================

    st.write("")

    if results["loaders_required"] == 0:

        st.info(
            "No loader fleet is required because the current "
            "production target is zero."
        )

    else:

        st.success(
            f"MineOpsLab calculates that "
            f"{results['loaders_required']} "
            f"{loader_type.lower()}"
            f"{'s' if results['loaders_required'] != 1 else ''} "
            f"are required. Each loader has an effective "
            f"productivity of "
            f"{results['effective_productivity_tph']:,.0f} t/h "
            f"after applying a loader MPI of "
            f"{results['mpi'] * 100:.1f}%. "
            f"The installed loading capacity is "
            f"{results['installed_capacity_tph']:,.0f} t/h "
            f"against a requirement of "
            f"{required_production_tph:,.0f} t/h."
        )


    # ========================================================
    # ENGINEERING DETAILS
    # ========================================================

    st.write("")

    with st.expander(
        "🔎 Engineering Details & Calculation Basis"
    ):

        # ----------------------------------------------------
        # BUCKET PERFORMANCE
        # ----------------------------------------------------

        st.markdown("#### 1. Bucket Performance")

        st.write(
            f"Rated bucket capacity: "
            f"**{bucket_capacity:.2f} m³**"
        )

        st.write(
            f"Bucket fill factor: "
            f"**{fill_factor_percent:.1f}%**"
        )

        st.latex(
            r"""
            V_e = V_b \times F_f
            """
        )

        st.write(
            f"Effective bucket volume: "
            f"**{results['effective_bucket_volume_m3']:.2f} m³**"
        )

        st.write(
            f"Loose bulk density: "
            f"**{loose_density:.2f} t/m³**"
        )

        st.latex(
            r"""
            Q_b = V_e \times \rho_L
            """
        )

        st.write(
            f"Effective bucket payload: "
            f"**{results['bucket_payload_t']:.2f} t**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # THEORETICAL PRODUCTIVITY
        # ----------------------------------------------------

        st.markdown("#### 2. Theoretical Productivity")

        st.write(
            f"Bucket cycle time: "
            f"**{cycle_time_sec:.1f} seconds**"
        )

        st.latex(
            r"""
            N_c = \frac{3600}{T_c}
            """
        )

        st.write(
            f"Theoretical cycles per hour: "
            f"**{results['theoretical_cycles_per_hour']:.1f} cycles/h**"
        )

        st.latex(
            r"""
            P_{theoretical} = Q_b \times N_c
            """
        )

        st.write(
            f"Theoretical loader productivity: "
            f"**{results['theoretical_productivity_tph']:,.0f} t/h**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # MPI
        # ----------------------------------------------------

        st.markdown("#### 3. Mine Productivity Index")

        st.write(
            f"Availability, Av: "
            f"**{availability_percent:.1f}%**"
        )

        st.write(
            f"Performance, PP: "
            f"**{performance_percent:.1f}%**"
        )

        st.write(
            f"Utilization, U: "
            f"**{utilization_percent:.1f}%**"
        )

        st.latex(
            r"""
            MPI =
            Av^{0.3}
            \times
            PP^{0.5}
            \times
            U^{0.2}
            """
        )

        st.write(
            "Substituting the current operating factors:"
        )

        st.latex(
            rf"""
            MPI =
            ({availability:.2f})^{{0.3}}
            \times
            ({performance:.2f})^{{0.5}}
            \times
            ({utilization:.2f})^{{0.2}}
            =
            {results['mpi']:.3f}
            """
        )

        st.write(
            f"Loader MPI: "
            f"**{results['mpi'] * 100:.1f}%**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # EFFECTIVE PRODUCTIVITY
        # ----------------------------------------------------

        st.markdown("#### 4. Effective Productivity")

        st.latex(
            r"""
            P_{effective}
            =
            P_{theoretical}
            \times MPI
            """
        )

        st.latex(
            rf"""
            P_{{effective}}
            =
            {results['theoretical_productivity_tph']:.1f}
            \times
            {results['mpi']:.3f}
            =
            {results['effective_productivity_tph']:.1f}
            \text{{ t/h}}
            """
        )

        st.write(
            f"Productivity loss from theoretical conditions: "
            f"**{results['productivity_loss_tph']:,.0f} t/h**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # FLEET SIZING
        # ----------------------------------------------------

        st.markdown("#### 5. Fleet Sizing")

        st.latex(
            r"""
            N_L =
            \frac{P_{required}}
            {P_{effective}}
            """
        )

        st.write(
            f"Exact calculated loader requirement: "
            f"**{results['exact_loaders_required']:.2f} loaders**"
        )

        st.write(
            f"Required whole loaders: "
            f"**{results['loaders_required']}**"
        )

        st.write(
            f"Installed fleet capacity: "
            f"**{results['installed_capacity_tph']:,.0f} t/h**"
        )

        st.write(
            f"Capacity surplus: "
            f"**{results['capacity_surplus_tph']:,.0f} t/h**"
        )

        st.write(
            f"Installed capacity utilization: "
            f"**{capacity_utilization_percent:.1f}%**"
        )


    # ========================================================
    # LEARNING NOTE
    # ========================================================

    st.write("")

    st.info(
        "🎓 Learning point: Theoretical productivity describes "
        "what the loader could achieve under ideal operating "
        "conditions. MineOpsLab applies the Mine Productivity "
        "Index (MPI), derived from Availability, Performance "
        "and Utilization, to estimate effective productivity. "
        "The required loader fleet is then based on this "
        "MPI-adjusted productivity."
    )