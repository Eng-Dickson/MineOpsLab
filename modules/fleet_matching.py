import streamlit as st

from calculations.fleet_matching import (
    calculate_fleet_matching,
)


def show_fleet_matching():

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        """
<div class="mineops-page-header">
<div class="mineops-eyebrow">
System Integration Module
</div>

<div class="mineops-page-title">
⚙️ Fleet Matching
</div>

<div class="mineops-page-subtitle">
Integrate the selected loading and haulage systems to evaluate
loader-truck compatibility, complete truck cycle time,
MPI-adjusted fleet productivity, fleet requirements,
system capacity and operational balance.
</div>
</div>
""",
        unsafe_allow_html=True,
    )


    # ========================================================
    # CHECK REQUIRED MODULES
    # ========================================================

    required_keys = [
        "material_type",
        "required_production_tph",
        "loader_results",
        "haulage_results",
        "loaders_required",
        "loader_effective_productivity",
        "loader_mpi",
        "bucket_payload_t",
        "loader_cycle_time",
        "truck_payload",
        "truck_mpi",
    ]

    missing_keys = [
        key
        for key in required_keys
        if key not in st.session_state
    ]

    if missing_keys:

        st.warning(
            "Fleet Matching requires completed Material & "
            "Production, Loading System and Haulage System "
            "modules."
        )

        st.info(
            "Complete the upstream modules first, then return "
            "to Fleet Matching."
        )

        return


    # ========================================================
    # INHERITED VALUES
    # ========================================================

    material_type = (
        st.session_state.material_type
    )

    required_production_tph = (
        st.session_state.required_production_tph
    )

    loader_results = (
        st.session_state.loader_results
    )

    haulage_results = (
        st.session_state.haulage_results
    )

    loaders_required = (
        st.session_state.loaders_required
    )

    loader_productivity = (
        st.session_state.loader_effective_productivity
    )

    loader_mpi = (
        st.session_state.loader_mpi
    )

    truck_mpi = (
        st.session_state.truck_mpi
    )

    bucket_payload_t = (
        st.session_state.bucket_payload_t
    )

    loader_cycle_time_sec = (
        st.session_state.loader_cycle_time
    )

    truck_payload_t = (
        st.session_state.truck_payload
    )

    loader_type = st.session_state.get(
        "loader_type",
        "Selected Loader",
    )

    truck_manufacturer = st.session_state.get(
        "truck_manufacturer",
        "Custom",
    )

    truck_model = st.session_state.get(
        "truck_model",
        "Custom Truck",
    )


    # ========================================================
    # SYSTEM CONFIGURATION
    # ========================================================

    st.subheader(
        "Selected Material Handling System"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Material",
            material_type,
        )

    with c2:

        st.metric(
            "Production Requirement",
            f"{required_production_tph:,.0f} t/h",
        )

    with c3:

        st.metric(
            "Loading Equipment",
            loader_type,
        )

    with c4:

        st.metric(
            "Haul Truck",
            truck_model,
        )

    st.caption(
        "Equipment specifications and operating conditions "
        "are inherited from the Loading and Haulage modules."
    )


    # ========================================================
    # PRODUCTIVITY HEALTH
    # ========================================================

    st.write("")
    st.subheader("⛏️ Equipment Productivity Health")

    st.caption(
        "Loader and truck productivity are independently "
        "adjusted using their respective Mine Productivity "
        "Indices."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Loader MPI",
            f"{loader_mpi * 100:.1f}%",
        )

    with c2:

        st.metric(
            "Loader Productivity",
            f"{loader_productivity:,.0f} t/h",
        )

    with c3:

        st.metric(
            "Truck MPI",
            f"{truck_mpi * 100:.1f}%",
        )

    with c4:

        st.metric(
            "Production Target",
            f"{required_production_tph:,.0f} t/h",
        )


    # ========================================================
    # RUN FLEET MATCHING ENGINE
    # ========================================================

    try:

        results = calculate_fleet_matching(
            truck_payload_t=truck_payload_t,
            bucket_payload_t=bucket_payload_t,
            loader_cycle_time_sec=(
                loader_cycle_time_sec
            ),
            non_loading_cycle_time_min=(
                haulage_results[
                    "non_loading_cycle_time_min"
                ]
            ),
            required_production_tph=(
                required_production_tph
            ),
            truck_mpi=truck_mpi,
            loaders_required=loaders_required,
            loader_effective_productivity_tph=(
                loader_productivity
            ),
        )

    except ValueError as error:

        st.error(str(error))
        return


    # ========================================================
    # STORE RESULTS
    # ========================================================

    st.session_state.fleet_matching_results = (
        results
    )

    st.session_state.trucks_required = (
        results["trucks_required"]
    )

    st.session_state.truck_theoretical_productivity = (
        results[
            "theoretical_truck_productivity_tph"
        ]
    )

    st.session_state.truck_effective_productivity = (
        results[
            "effective_truck_productivity_tph"
        ]
    )

    st.session_state.complete_truck_cycle_time = (
        results["complete_cycle_time_min"]
    )

    st.session_state.system_capacity_tph = (
        results["system_capacity_tph"]
    )

    st.session_state.match_factor = (
        results["match_factor"]
    )


    # ========================================================
    # PRIMARY FLEET RESULTS
    # ========================================================

    st.write("")
    st.subheader("Fleet Requirement")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Required Loaders",
            f"{loaders_required}",
        )

    with c2:

        st.metric(
            "Required Trucks",
            f"{results['trucks_required']}",
        )

    with c3:

        st.metric(
            "Passes per Truck",
            f"{results['passes_per_truck']}",
        )

    with c4:

        st.metric(
            "Truck Cycle Time",
            (
                f"{results['complete_cycle_time_min']:.2f} "
                "min"
            ),
        )


    # ========================================================
    # LOADER-TRUCK INTERACTION
    # ========================================================

    st.write("")
    st.subheader("Loader-Truck Interaction")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Bucket Payload",
            f"{bucket_payload_t:.2f} t",
        )

    with c2:

        st.metric(
            "Truck Payload",
            f"{truck_payload_t:.1f} t",
        )

    with c3:

        st.metric(
            "Loading Time",
            (
                f"{results['truck_loading_time_min']:.2f} "
                "min"
            ),
        )

    with c4:

        st.metric(
            "Final Pass Fill",
            (
                f"{results['final_pass_fill_fraction'] * 100:.0f}%"
            ),
        )


    # ========================================================
    # TRUCK PRODUCTIVITY TRANSFORMATION
    # ========================================================

    st.write("")
    st.subheader("🚛 Truck Productivity")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Theoretical Trips",
            (
                f"{results['theoretical_trips_per_hour']:.2f} "
                "trips/h"
            ),
        )

    with c2:

        st.metric(
            "Theoretical Productivity",
            (
                f"{results['theoretical_truck_productivity_tph']:,.0f} "
                "t/h"
            ),
        )

    with c3:

        st.metric(
            "Truck MPI",
            f"{truck_mpi * 100:.1f}%",
        )

    with c4:

        st.metric(
            "Effective Productivity",
            (
                f"{results['effective_truck_productivity_tph']:,.0f} "
                "t/h"
            ),
        )


    # ========================================================
    # MPI PRODUCTIVITY TRANSFORMATION
    # ========================================================

    st.write("")
    st.markdown("#### Productivity Transformation")

    st.latex(
        r"""
        P_{T,effective}
        =
        P_{T,theoretical}
        \times
        MPI_T
        """
    )

    st.write(
        f"The selected truck has a theoretical productivity "
        f"of **{results['theoretical_truck_productivity_tph']:,.0f} "
        f"t/h**. Applying a Truck MPI of "
        f"**{truck_mpi * 100:.1f}%** gives an effective "
        f"productivity of "
        f"**{results['effective_truck_productivity_tph']:,.0f} "
        f"t/h per truck**."
    )


    # ========================================================
    # TRUCK FLEET CAPACITY
    # ========================================================

    st.write("")
    st.subheader("Truck Fleet Capacity")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Required Trucks",
            f"{results['trucks_required']}",
        )

    with c2:

        st.metric(
            "Effective Trips",
            (
                f"{results['effective_trips_per_hour']:.2f} "
                "trips/h"
            ),
        )

    with c3:

        st.metric(
            "Installed Truck Capacity",
            (
                f"{results['installed_truck_capacity_tph']:,.0f} "
                "t/h"
            ),
        )

    with c4:

        st.metric(
            "Installed Capacity Use",
            (
                f"{results['truck_capacity_utilization'] * 100:.1f}%"
            ),
        )


    # ========================================================
    # SYSTEM PERFORMANCE
    # ========================================================

    st.write("")
    st.subheader("⚙️ Integrated System Performance")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Loading Capacity",
            (
                f"{results['installed_loader_capacity_tph']:,.0f} "
                "t/h"
            ),
        )

    with c2:

        st.metric(
            "Haulage Capacity",
            (
                f"{results['installed_truck_capacity_tph']:,.0f} "
                "t/h"
            ),
        )

    with c3:

        st.metric(
            "System Capacity",
            (
                f"{results['system_capacity_tph']:,.0f} "
                "t/h"
            ),
        )

    with c4:

        st.metric(
            "Match Factor",
            f"{results['match_factor']:.2f}",
        )


    # ========================================================
    # SYSTEM DIAGNOSIS
    # ========================================================

    st.write("")
    st.subheader("System Diagnosis")

    col1, col2 = st.columns(
        2,
        gap="large",
    )

    with col1:

        st.markdown(
            f"""
<div class="mineops-card">

<h3>⚙️ Fleet Match</h3>

<p>

Match factor:
<strong>{results['match_factor']:.2f}</strong>

<br><br>

Interpretation:
<strong>{results['match_status']}</strong>

<br><br>

Loader-to-truck capacity ratio:
<strong>{results['loader_to_truck_capacity_ratio']:.2f}</strong>

</p>

</div>
""",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
<div class="mineops-card">

<h3>🔍 Capacity Constraint</h3>

<p>

Current capacity bottleneck:
<strong>{results['capacity_bottleneck']}</strong>

<br><br>

System capacity:
<strong>{results['system_capacity_tph']:,.0f} t/h</strong>

<br><br>

Required production:
<strong>{required_production_tph:,.0f} t/h</strong>

</p>

</div>
""",
            unsafe_allow_html=True,
        )


    # ========================================================
    # TARGET CHECK
    # ========================================================

    st.write("")

    balance = results[
        "system_capacity_balance_tph"
    ]

    if balance >= 0:

        st.success(
            f"✓ The selected material handling system has "
            f"sufficient installed capacity for the production "
            f"requirement. The calculated system capacity is "
            f"{results['system_capacity_tph']:,.0f} t/h, "
            f"providing a capacity margin of "
            f"{balance:,.0f} t/h."
        )

    else:

        st.error(
            f"The selected material handling system does not "
            f"meet the production requirement. The calculated "
            f"capacity shortfall is "
            f"{abs(balance):,.0f} t/h."
        )


    # ========================================================
    # COMPLETE CALCULATION BASIS
    # ========================================================

    st.write("")

    with st.expander(
        "🔎 Complete Fleet Matching & Calculation Basis"
    ):

        # ----------------------------------------------------
        # 1. EQUIPMENT
        # ----------------------------------------------------

        st.markdown(
            "#### 1. Selected Equipment"
        )

        st.write(
            f"Selected loader: **{loader_type}**"
        )

        st.write(
            f"Selected truck: "
            f"**{truck_manufacturer} {truck_model}**"
        )

        st.write(
            f"Production requirement: "
            f"**{required_production_tph:,.0f} t/h**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # 2. LOADER MPI
        # ----------------------------------------------------

        st.markdown(
            "#### 2. Loader Productivity"
        )

        st.write(
            f"Loader Availability: "
            f"**{loader_results['availability'] * 100:.1f}%**"
        )

        st.write(
            f"Loader Performance: "
            f"**{loader_results['performance'] * 100:.1f}%**"
        )

        st.write(
            f"Loader Utilization: "
            f"**{loader_results['utilization'] * 100:.1f}%**"
        )

        st.write(
            f"Loader MPI: "
            f"**{loader_mpi * 100:.1f}%**"
        )

        st.write(
            f"Theoretical loader productivity: "
            f"**{loader_results['theoretical_productivity_tph']:,.0f} "
            f"t/h**"
        )

        st.write(
            f"Effective loader productivity: "
            f"**{loader_productivity:,.0f} t/h**"
        )

        st.latex(
            r"""
            P_{L,effective}
            =
            P_{L,theoretical}
            \times
            MPI_L
            """
        )

        st.markdown("---")


        # ----------------------------------------------------
        # 3. LOADER-TRUCK MATCH
        # ----------------------------------------------------

        st.markdown(
            "#### 3. Loader-Truck Compatibility"
        )

        st.write(
            f"Bucket payload: "
            f"**{bucket_payload_t:.2f} t/pass**"
        )

        st.write(
            f"Truck payload: "
            f"**{truck_payload_t:.2f} t**"
        )

        st.latex(
            r"""
            N_{passes}
            =
            \frac{Q_T}{Q_B}
            """
        )

        st.write(
            f"Exact bucket requirement: "
            f"**{results['exact_passes']:.2f} passes**"
        )

        st.write(
            f"Operational bucket passes: "
            f"**{results['passes_per_truck']} passes**"
        )

        st.write(
            f"Final pass payload: "
            f"**{results['final_pass_payload_t']:.2f} t**"
        )

        st.write(
            f"Final pass fill: "
            f"**{results['final_pass_fill_fraction'] * 100:.1f}%**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # 4. LOADING TIME
        # ----------------------------------------------------

        st.markdown(
            "#### 4. Truck Loading Time"
        )

        st.write(
            f"Loader cycle time: "
            f"**{loader_cycle_time_sec:.1f} seconds**"
        )

        st.write(
            f"Loader cycle time: "
            f"**{results['loader_cycle_time_min']:.3f} minutes**"
        )

        st.latex(
            r"""
            T_{load}
            =
            N_{passes}
            \times
            T_{loader\ cycle}
            """
        )

        st.write(
            f"Truck loading time: "
            f"**{results['truck_loading_time_min']:.2f} min**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # 5. COMPLETE CYCLE
        # ----------------------------------------------------

        st.markdown(
            "#### 5. Complete Truck Cycle"
        )

        st.write(
            f"Loading: "
            f"**{results['truck_loading_time_min']:.2f} min**"
        )

        st.write(
            f"Loaded haul: "
            f"**{haulage_results['loaded_haul_time_min']:.2f} min**"
        )

        st.write(
            f"Spotting: "
            f"**{haulage_results['spotting_time_min']:.2f} min**"
        )

        st.write(
            f"Dumping: "
            f"**{haulage_results['dumping_time_min']:.2f} min**"
        )

        st.write(
            f"Empty return: "
            f"**{haulage_results['empty_return_time_min']:.2f} min**"
        )

        st.latex(
            r"""
            T_C
            =
            T_{load}
            +
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
            f"Complete cycle: "
            f"**{results['complete_cycle_time_min']:.2f} min**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # 6. TRUCK MPI
        # ----------------------------------------------------

        st.markdown(
            "#### 6. Truck Mine Productivity Index"
        )

        st.write(
            f"Truck Availability: "
            f"**{haulage_results['truck_availability'] * 100:.1f}%**"
        )

        st.write(
            f"Truck Performance: "
            f"**{haulage_results['truck_performance'] * 100:.1f}%**"
        )

        st.write(
            f"Truck Utilization: "
            f"**{haulage_results['truck_utilization'] * 100:.1f}%**"
        )

        st.latex(
            r"""
            MPI_T
            =
            Av_T^{0.3}
            \times
            PP_T^{0.5}
            \times
            U_T^{0.2}
            """
        )

        st.write(
            f"Truck MPI: "
            f"**{truck_mpi * 100:.1f}%**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # 7. TRUCK PRODUCTIVITY
        # ----------------------------------------------------

        st.markdown(
            "#### 7. Truck Productivity"
        )

        st.latex(
            r"""
            N_{trips}
            =
            \frac{60}{T_C}
            """
        )

        st.write(
            f"Theoretical trips per hour: "
            f"**{results['theoretical_trips_per_hour']:.2f} "
            f"trips/h**"
        )

        st.latex(
            r"""
            P_{T,theoretical}
            =
            N_{trips}
            \times
            Q_T
            """
        )

        st.write(
            f"Theoretical truck productivity: "
            f"**{results['theoretical_truck_productivity_tph']:,.0f} "
            f"t/h**"
        )

        st.latex(
            r"""
            P_{T,effective}
            =
            P_{T,theoretical}
            \times
            MPI_T
            """
        )

        st.write(
            f"Effective truck productivity: "
            f"**{results['effective_truck_productivity_tph']:,.0f} "
            f"t/h**"
        )

        st.write(
            f"Productivity loss relative to theoretical: "
            f"**{results['truck_productivity_loss_tph']:,.0f} "
            f"t/h**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # 8. FLEET SIZING
        # ----------------------------------------------------

        st.markdown(
            "#### 8. Fleet Sizing"
        )

        st.latex(
            r"""
            N_T
            =
            \frac{P_{required}}
            {P_{T,effective}}
            """
        )

        st.write(
            f"Exact truck requirement: "
            f"**{results['exact_trucks_required']:.2f} trucks**"
        )

        st.write(
            f"Required whole trucks: "
            f"**{results['trucks_required']} trucks**"
        )

        st.write(
            f"Required loaders: "
            f"**{loaders_required} loaders**"
        )

        st.write(
            f"Installed loading capacity: "
            f"**{results['installed_loader_capacity_tph']:,.0f} "
            f"t/h**"
        )

        st.write(
            f"Installed haulage capacity: "
            f"**{results['installed_truck_capacity_tph']:,.0f} "
            f"t/h**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # 9. SYSTEM CAPACITY
        # ----------------------------------------------------

        st.markdown(
            "#### 9. Integrated System Capacity"
        )

        st.latex(
            r"""
            P_{system}
            =
            \min
            \left(
            P_{loader\ fleet},
            P_{truck\ fleet}
            \right)
            """
        )

        st.write(
            f"Loading capacity: "
            f"**{results['installed_loader_capacity_tph']:,.0f} "
            f"t/h**"
        )

        st.write(
            f"Haulage capacity: "
            f"**{results['installed_truck_capacity_tph']:,.0f} "
            f"t/h**"
        )

        st.write(
            f"System capacity: "
            f"**{results['system_capacity_tph']:,.0f} t/h**"
        )

        st.write(
            f"Capacity bottleneck: "
            f"**{results['capacity_bottleneck']}**"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # 10. MATCH FACTOR
        # ----------------------------------------------------

        st.markdown(
            "#### 10. Loader-Truck Match"
        )

        st.latex(
            r"""
            MF
            =
            \frac{
            N_T
            \times
            T_{load}
            }{
            N_L
            \times
            T_C
            }
            """
        )

        st.write(
            f"Match factor: "
            f"**{results['match_factor']:.2f}**"
        )

        st.write(
            f"Match interpretation: "
            f"**{results['match_status']}**"
        )

        st.write(
            f"Loader-to-truck capacity ratio: "
            f"**{results['loader_to_truck_capacity_ratio']:.2f}**"
        )


    # ========================================================
    # TEACHING NOTE
    # ========================================================

    st.write("")

    st.info(
        "🎓 Learning point: Fleet Matching integrates the "
        "physical loader-truck relationship with operational "
        "productivity. Loader productivity is adjusted by "
        "Loader MPI, while truck productivity is adjusted by "
        "Truck MPI. The resulting installed capacities "
        "determine whether the material handling system can "
        "satisfy the mine production requirement and which "
        "subsystem forms the current capacity constraint."
    )