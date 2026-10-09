import streamlit as st

from calculations.haulage import calculate_haulage_performance

from data.trucks import (
    get_truck_names,
    get_truck_properties,
)


def show_haulage_system():

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
🚛 Haulage System
</div>

<div class="mineops-page-subtitle">
Select the haul truck and define the haul-road operating
conditions to analyse travel times, non-loading cycle components
and the truck Mine Productivity Index (MPI).
</div>
</div>
""",
        unsafe_allow_html=True,
    )


    # ========================================================
    # CHECK FOR PRODUCTION DATA
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

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Material",
            material_type,
        )

    with c2:

        st.metric(
            "Shift Production",
            f"{shift_production:,.0f} t/shift",
        )

    with c3:

        st.metric(
            "Required Production",
            f"{required_production_tph:,.0f} t/h",
        )

    st.caption(
        "Production requirements are inherited automatically "
        "from Material & Production."
    )


    # ========================================================
    # TRUCK LIBRARY
    # ========================================================

    truck_names = get_truck_names()

    if "selected_truck" not in st.session_state:
        st.session_state.selected_truck = (
            truck_names[0]
        )

    if "previous_truck" not in st.session_state:
        st.session_state.previous_truck = None


    # ========================================================
    # DEFAULT OPERATING CONDITIONS
    # ========================================================

    if "haul_distance" not in st.session_state:
        st.session_state.haul_distance = 3.0

    if "loaded_speed" not in st.session_state:
        st.session_state.loaded_speed = 25.0

    if "empty_speed" not in st.session_state:
        st.session_state.empty_speed = 35.0

    if "spotting_time" not in st.session_state:
        st.session_state.spotting_time = 0.8

    if "dumping_time" not in st.session_state:
        st.session_state.dumping_time = 0.7

    if "truck_availability" not in st.session_state:
        st.session_state.truck_availability = 90.0

    if "truck_performance" not in st.session_state:
        st.session_state.truck_performance = 85.0

    if "truck_utilization" not in st.session_state:
        st.session_state.truck_utilization = 85.0


    # ========================================================
    # TRUCK SELECTION
    # ========================================================

    st.write("")
    st.subheader("🚛 Truck Selection")

    selected_truck = st.selectbox(
        "Truck model",
        truck_names,
        index=(
            truck_names.index(
                st.session_state.selected_truck
            )
            if st.session_state.selected_truck
            in truck_names
            else 0
        ),
        help=(
            "Select a truck from the MineOpsLab equipment "
            "library. Equipment specifications can be edited "
            "for scenario analysis."
        ),
    )


    # ========================================================
    # LOAD SPECIFICATIONS WHEN TRUCK CHANGES
    # ========================================================

    if (
        st.session_state.previous_truck
        != selected_truck
    ):

        truck_defaults = (
            get_truck_properties(
                selected_truck
            )
        )

        st.session_state.truck_payload = (
            truck_defaults["payload_t"]
        )

        st.session_state.previous_truck = (
            selected_truck
        )


    # ========================================================
    # TRUCK SPECIFICATION
    # ========================================================

    truck_properties = (
        get_truck_properties(
            selected_truck
        )
    )

    manufacturer = truck_properties.get(
        "manufacturer",
        "Unknown",
    )

    st.write("")
    st.subheader("Truck Specification")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.text_input(
            "Manufacturer",
            value=manufacturer,
            disabled=True,
        )

    with c2:

        st.text_input(
            "Model",
            value=selected_truck,
            disabled=True,
        )

    with c3:

        truck_payload = st.number_input(
            "Rated payload (tonnes)",
            min_value=1.0,
            value=float(
                st.session_state.truck_payload
            ),
            step=5.0,
            help=(
                "Rated payload from the selected truck "
                "specification. This remains editable "
                "for scenario analysis."
            ),
        )


    # ========================================================
    # HAUL CONDITIONS
    # ========================================================

    st.write("")
    st.subheader("🛣️ Haul Conditions")

    col1, col2 = st.columns(
        2,
        gap="large",
    )


    # --------------------------------------------------------
    # HAUL PROFILE
    # --------------------------------------------------------

    with col1:

        haul_distance = st.number_input(
            "One-way haul distance (km)",
            min_value=0.1,
            value=float(
                st.session_state.haul_distance
            ),
            step=0.1,
            help=(
                "One-way distance between the loading "
                "and dumping locations."
            ),
        )

        loaded_speed = st.number_input(
            "Average loaded speed (km/h)",
            min_value=1.0,
            value=float(
                st.session_state.loaded_speed
            ),
            step=1.0,
            help=(
                "Average truck travel speed while loaded."
            ),
        )

        empty_speed = st.number_input(
            "Average empty speed (km/h)",
            min_value=1.0,
            value=float(
                st.session_state.empty_speed
            ),
            step=1.0,
            help=(
                "Average truck return speed while empty."
            ),
        )


    # --------------------------------------------------------
    # PRODUCTIVITY FACTORS
    # --------------------------------------------------------

    with col2:

        st.markdown(
            "#### Productivity Factors"
        )

        st.caption(
            "Availability, Performance and Utilization "
            "are combined to determine the truck Mine "
            "Productivity Index (MPI)."
        )

        availability_percent = (
            st.number_input(
                "Truck mechanical availability, Av (%)",
                min_value=1.0,
                max_value=100.0,
                value=float(
                    st.session_state.truck_availability
                ),
                step=1.0,
                help=(
                    "The proportion of scheduled time "
                    "during which the truck is mechanically "
                    "available for operation."
                ),
            )
        )

        performance_percent = (
            st.number_input(
                "Truck performance, PP (%)",
                min_value=1.0,
                max_value=100.0,
                value=float(
                    st.session_state.truck_performance
                ),
                step=1.0,
                help=(
                    "Performance reflects how closely the "
                    "truck performs relative to its expected "
                    "operating performance."
                ),
            )
        )

        utilization_percent = (
            st.number_input(
                "Truck utilization, U (%)",
                min_value=1.0,
                max_value=100.0,
                value=float(
                    st.session_state.truck_utilization
                ),
                step=1.0,
                help=(
                    "The proportion of available time during "
                    "which the truck is actually operating."
                ),
            )
        )


    # ========================================================
    # FIXED CYCLE COMPONENTS
    # ========================================================

    st.write("")
    st.subheader(
        "⏱️ Dumping Cycle Components"
    )

    c1, c2 = st.columns(2)

    with c1:

        spotting_time = st.number_input(
            "Spotting time at dump (minutes)",
            min_value=0.0,
            value=float(
                st.session_state.spotting_time
            ),
            step=0.1,
            help=(
                "Time required for the truck to position "
                "itself correctly at the dumping point."
            ),
        )

    with c2:

        dumping_time = st.number_input(
            "Dumping time (minutes)",
            min_value=0.0,
            value=float(
                st.session_state.dumping_time
            ),
            step=0.1,
            help=(
                "Time required to discharge the truck payload."
            ),
        )


    # ========================================================
    # SAVE INPUTS
    # ========================================================

    st.session_state.selected_truck = (
        selected_truck
    )

    st.session_state.truck_payload = (
        truck_payload
    )

    st.session_state.haul_distance = (
        haul_distance
    )

    st.session_state.loaded_speed = (
        loaded_speed
    )

    st.session_state.empty_speed = (
        empty_speed
    )

    st.session_state.spotting_time = (
        spotting_time
    )

    st.session_state.dumping_time = (
        dumping_time
    )

    st.session_state.truck_availability = (
        availability_percent
    )

    st.session_state.truck_performance = (
        performance_percent
    )

    st.session_state.truck_utilization = (
        utilization_percent
    )


    # ========================================================
    # CONVERT PERCENTAGES
    # ========================================================

    truck_availability = (
        availability_percent / 100.0
    )

    truck_performance = (
        performance_percent / 100.0
    )

    truck_utilization = (
        utilization_percent / 100.0
    )


    # ========================================================
    # RUN HAULAGE ENGINE
    # ========================================================

    try:

        results = (
            calculate_haulage_performance(
                truck_payload_t=truck_payload,
                haul_distance_km=haul_distance,
                loaded_speed_kmh=loaded_speed,
                empty_speed_kmh=empty_speed,
                spotting_time_min=spotting_time,
                dumping_time_min=dumping_time,
                truck_availability=(
                    truck_availability
                ),
                truck_performance=(
                    truck_performance
                ),
                truck_utilization=(
                    truck_utilization
                ),
            )
        )

    except ValueError as error:

        st.error(str(error))
        return


    # ========================================================
    # STORE RESULTS FOR FLEET MATCHING
    # ========================================================

    st.session_state.haulage_results = (
        results
    )

    st.session_state.truck_manufacturer = (
        manufacturer
    )

    st.session_state.truck_model = (
        selected_truck
    )

    st.session_state.truck_mpi = (
        results["truck_mpi"]
    )


    # ========================================================
    # PRIMARY RESULTS
    # ========================================================

    st.write("")
    st.subheader("Haulage Performance")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Loaded Haul",
            (
                f"{results['loaded_haul_time_min']:.2f} "
                "min"
            ),
        )

    with c2:

        st.metric(
            "Empty Return",
            (
                f"{results['empty_return_time_min']:.2f} "
                "min"
            ),
        )

    with c3:

        st.metric(
            "Non-loading Cycle",
            (
                f"{results['non_loading_cycle_time_min']:.2f} "
                "min"
            ),
        )

    with c4:

        st.metric(
            "Truck MPI",
            (
                f"{results['truck_mpi'] * 100:.1f}%"
            ),
        )


    # ========================================================
    # HAUL PROFILE
    # ========================================================

    st.write("")
    st.subheader("Haul Profile")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "One-way Distance",
            f"{haul_distance:.2f} km",
        )

    with c2:

        st.metric(
            "Round-trip Distance",
            (
                f"{results['round_trip_distance_km']:.2f} "
                "km"
            ),
        )

    with c3:

        st.metric(
            "Total Travel Time",
            (
                f"{results['total_travel_time_min']:.2f} "
                "min"
            ),
        )

    with c4:

        st.metric(
            "Dump Activities",
            (
                f"{results['dump_activity_time_min']:.2f} "
                "min"
            ),
        )


    # ========================================================
    # TRUCK CYCLE BREAKDOWN
    # ========================================================

    st.write("")
    st.subheader("Truck Cycle Breakdown")

    st.markdown(
        f"""
<div class="mineops-card">

<h3>🚛 Current Truck Cycle Components</h3>

<p>

Truck:
<strong>{manufacturer} {selected_truck}</strong><br>

Rated payload:
<strong>{truck_payload:.1f} t</strong><br><br>

Loading:
<strong>Pending Fleet Matching</strong><br><br>

Loaded haul:
<strong>{results['loaded_haul_time_min']:.2f} min</strong><br>

Spotting at dump:
<strong>{spotting_time:.2f} min</strong><br>

Dumping:
<strong>{dumping_time:.2f} min</strong><br>

Empty return:
<strong>{results['empty_return_time_min']:.2f} min</strong><br><br>

Non-loading cycle time:
<strong>{results['non_loading_cycle_time_min']:.2f} min</strong>

</p>

</div>
""",
        unsafe_allow_html=True,
    )


    # ========================================================
    # MINE PRODUCTIVITY INDEX
    # ========================================================

    st.write("")
    st.subheader("⛏️ Mine Productivity Index")

    st.caption(
        "The truck MPI combines mechanical availability, "
        "performance and utilization into a single "
        "operational productivity indicator."
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
            "Truck MPI",
            (
                f"{results['truck_mpi'] * 100:.1f}%"
            ),
        )

    st.latex(
        r"""
        MPI_T =
        Av_T^{0.3}
        \times
        PP_T^{0.5}
        \times
        U_T^{0.2}
        """
    )

    st.write(
        f"For the current truck, "
        f"**Av = {truck_availability:.2f}**, "
        f"**PP = {truck_performance:.2f}**, and "
        f"**U = {truck_utilization:.2f}**."
    )

    st.write(
        f"The resulting truck Mine Productivity Index is "
        f"**{results['truck_mpi'] * 100:.1f}%**."
    )

    st.info(
        "Truck MPI is calculated here, but it is not yet "
        "applied to truck productivity. Complete truck "
        "productivity requires loading time, which is "
        "determined when the truck is matched with the "
        "selected loader in Fleet Matching."
    )


    # ========================================================
    # ENGINEERING DETAILS
    # ========================================================

    st.write("")

    with st.expander(
        "🔎 Engineering Details & Calculation Basis"
    ):

        # ----------------------------------------------------
        # SELECTED TRUCK
        # ----------------------------------------------------

        st.markdown("#### 1. Selected Truck")

        st.write(
            f"Manufacturer: **{manufacturer}**"
        )

        st.write(
            f"Model: **{selected_truck}**"
        )

        st.write(
            f"Rated payload: **{truck_payload:.1f} t**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # LOADED TRAVEL
        # ----------------------------------------------------

        st.markdown("#### 2. Loaded Haul")

        st.latex(
            r"""
            T_{haul}
            =
            \frac{60D}{V_L}
            """
        )

        st.write(
            f"Haul distance: **{haul_distance:.2f} km**"
        )

        st.write(
            f"Loaded speed: **{loaded_speed:.1f} km/h**"
        )

        st.write(
            f"Loaded haul time: "
            f"**{results['loaded_haul_time_min']:.2f} min**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # EMPTY RETURN
        # ----------------------------------------------------

        st.markdown("#### 3. Empty Return")

        st.latex(
            r"""
            T_{return}
            =
            \frac{60D}{V_E}
            """
        )

        st.write(
            f"Return distance: **{haul_distance:.2f} km**"
        )

        st.write(
            f"Empty speed: **{empty_speed:.1f} km/h**"
        )

        st.write(
            f"Empty return time: "
            f"**{results['empty_return_time_min']:.2f} min**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # DUMP ACTIVITIES
        # ----------------------------------------------------

        st.markdown("#### 4. Dump Activities")

        st.write(
            f"Spotting time: "
            f"**{spotting_time:.2f} min**"
        )

        st.write(
            f"Dumping time: "
            f"**{dumping_time:.2f} min**"
        )

        st.latex(
            r"""
            T_{dump\ activities}
            =
            T_{spot}
            +
            T_{dump}
            """
        )

        st.write(
            f"Total dump activities: "
            f"**{results['dump_activity_time_min']:.2f} min**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # NON-LOADING CYCLE
        # ----------------------------------------------------

        st.markdown(
            "#### 5. Non-loading Truck Cycle"
        )

        st.latex(
            r"""
            T_{nonload}
            =
            T_{haul}
            +
            T_{spot}
            +
            T_{dump}
            +
            T_{return}
            """
        )

        st.write(
            f"Total travel time: "
            f"**{results['total_travel_time_min']:.2f} min**"
        )

        st.write(
            f"Non-loading cycle time: "
            f"**{results['non_loading_cycle_time_min']:.2f} min**"
        )

        st.write(
            "Complete truck cycle: "
            "**Pending loader-truck matching**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # MPI
        # ----------------------------------------------------

        st.markdown(
            "#### 6. Truck Mine Productivity Index"
        )

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
            MPI_T =
            Av_T^{0.3}
            \times
            PP_T^{0.5}
            \times
            U_T^{0.2}
            """
        )

        st.write(
            "Substituting the current operating factors:"
        )

        st.latex(
            rf"""
            MPI_T =
            ({truck_availability:.2f})^{{0.3}}
            \times
            ({truck_performance:.2f})^{{0.5}}
            \times
            ({truck_utilization:.2f})^{{0.2}}
            =
            {results['truck_mpi']:.3f}
            """
        )

        st.write(
            f"Truck MPI: "
            f"**{results['truck_mpi'] * 100:.1f}%**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # TIME DISTRIBUTION
        # ----------------------------------------------------

        st.markdown(
            "#### 7. Non-loading Time Distribution"
        )

        st.write(
            f"Loaded haul: "
            f"**{results['loaded_haul_share'] * 100:.1f}%**"
        )

        st.write(
            f"Empty return: "
            f"**{results['empty_return_share'] * 100:.1f}%**"
        )

        st.write(
            f"Spotting: "
            f"**{results['spotting_share'] * 100:.1f}%**"
        )

        st.write(
            f"Dumping: "
            f"**{results['dumping_share'] * 100:.1f}%**"
        )


    # ========================================================
    # LEARNING NOTE
    # ========================================================

    st.write("")

    st.info(
        "🎓 Learning point: The Haulage System determines the "
        "truck's travel and dumping components independently "
        "of the loader. Availability, Performance and "
        "Utilization determine the truck MPI. In Fleet "
        "Matching, loader loading time will complete the "
        "truck cycle, allowing theoretical truck productivity "
        "to be calculated and then adjusted using MPI."
    )