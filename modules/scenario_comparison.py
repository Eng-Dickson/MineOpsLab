
"""
MineOpsLab
Scenario Comparison Module

Interactive scenario creation, engineering comparison,
visualization, interpretation and data export.

Session-state management has been designed to avoid
modifying Streamlit widget keys after widget creation.
"""

from copy import deepcopy
import json

import pandas as pd
import streamlit as st

from calculations.scenario_comparison import (
    DEFAULT_SCENARIO,
    make_scenario,
    compare_scenarios,
    comparison_rows,
    interpret_scenario,
)


# ============================================================
# SCENARIO INPUT GROUPS
# ============================================================

FIELD_GROUPS = {
    "Production and Material": [
        ("required_production_tph", "Required production (t/h)"),
        ("loose_density", "Loose material density (t/m3)"),
    ],
    "Loading Equipment": [
        ("bucket_capacity_m3", "Bucket capacity (m3)"),
        ("fill_factor", "Bucket fill factor"),
        ("loader_cycle_time_sec", "Loader cycle time (seconds)"),
        ("loader_availability", "Loader availability"),
        ("loader_performance", "Loader performance"),
        ("loader_utilization", "Loader utilization"),
    ],
    "Haulage Equipment": [
        ("truck_payload_t", "Truck payload (tonnes)"),
        ("haul_distance_km", "One-way haul distance (km)"),
        ("loaded_speed_kmh", "Loaded speed (km/h)"),
        ("empty_speed_kmh", "Empty speed (km/h)"),
        ("spotting_time_min", "Spotting time (minutes)"),
        ("dumping_time_min", "Dumping time (minutes)"),
        ("truck_availability", "Truck availability"),
        ("truck_performance", "Truck performance"),
        ("truck_utilization", "Truck utilization"),
    ],
}


FACTOR_FIELDS = {
    "fill_factor",
    "loader_availability",
    "loader_performance",
    "loader_utilization",
    "truck_availability",
    "truck_performance",
    "truck_utilization",
}


NONNEGATIVE_FIELDS = {
    "required_production_tph",
    "spotting_time_min",
    "dumping_time_min",
}


# ============================================================
# SESSION INITIALIZATION
# ============================================================

def initialize_scenarios():

    if "mineops_scenarios" not in st.session_state:

        baseline = make_scenario(
            "Scenario A - Baseline"
        )

        loader = st.session_state.get(
            "loader_results", {}
        ) or {}

        haulage = st.session_state.get(
            "haulage_results", {}
        ) or {}

        production = st.session_state.get(
            "required_production_tph"
        )

        if production is not None:
            baseline["required_production_tph"] = float(
                production
            )

        if "availability" in loader:
            baseline["loader_availability"] = float(
                loader["availability"]
            )

        if "performance" in loader:
            baseline["loader_performance"] = float(
                loader["performance"]
            )

        if "utilization" in loader:
            baseline["loader_utilization"] = float(
                loader["utilization"]
            )

        for key in (
            "haul_distance_km",
            "loaded_speed_kmh",
            "empty_speed_kmh",
            "spotting_time_min",
            "dumping_time_min",
            "truck_availability",
            "truck_performance",
            "truck_utilization",
        ):
            if key in haulage:
                baseline[key] = float(haulage[key])

        if "truck_payload" in st.session_state:
            baseline["truck_payload_t"] = float(
                st.session_state["truck_payload"]
            )

        if "loader_cycle_time" in st.session_state:
            baseline["loader_cycle_time_sec"] = float(
                st.session_state["loader_cycle_time"]
            )

        st.session_state["mineops_scenarios"] = [
            baseline,
            make_scenario(
                "Scenario B - Alternative",
                {
                    "haul_distance_km":
                        baseline["haul_distance_km"] * 1.25
                },
            ),
        ]

        st.session_state["mineops_scenario_counter"] = 2

    if "mineops_selected_index" not in st.session_state:
        st.session_state["mineops_selected_index"] = 0

    if "mineops_scenario_results" not in st.session_state:
        st.session_state["mineops_scenario_results"] = None

    if "mineops_results_outdated" not in st.session_state:
        st.session_state["mineops_results_outdated"] = False


# ============================================================
# SCENARIO MANAGEMENT
# ============================================================

def add_scenario():

    scenarios = st.session_state["mineops_scenarios"]

    st.session_state["mineops_scenario_counter"] += 1

    number = st.session_state["mineops_scenario_counter"]

    source = deepcopy(scenarios[-1])
    source["name"] = f"Scenario {number}"

    scenarios.append(source)

    st.session_state["mineops_selected_index"] = (
        len(scenarios) - 1
    )

    st.session_state["mineops_results_outdated"] = True


def duplicate_scenario(index):

    scenarios = st.session_state["mineops_scenarios"]

    st.session_state["mineops_scenario_counter"] += 1

    number = st.session_state["mineops_scenario_counter"]

    scenario_copy = deepcopy(scenarios[index])
    scenario_copy["name"] = f"Scenario {number}"

    scenarios.append(scenario_copy)

    st.session_state["mineops_selected_index"] = (
        len(scenarios) - 1
    )

    st.session_state["mineops_results_outdated"] = True


def delete_scenario(index):

    scenarios = st.session_state["mineops_scenarios"]

    if len(scenarios) <= 2:
        return

    scenarios.pop(index)

    st.session_state["mineops_selected_index"] = min(
        index,
        len(scenarios) - 1,
    )

    st.session_state["mineops_results_outdated"] = True


# ============================================================
# SCENARIO EDITOR
# ============================================================

def edit_scenario(index):

    scenarios = st.session_state["mineops_scenarios"]
    scenario = scenarios[index]

    st.subheader("Scenario Configuration")

    with st.form(
        key=f"scenario_editor_{index}"
    ):

        name = st.text_input(
            "Scenario name",
            value=scenario["name"],
        )

        edited = deepcopy(scenario)

        for group_name, fields in FIELD_GROUPS.items():

            st.markdown(f"#### {group_name}")

            columns = st.columns(2)

            for position, (key, label) in enumerate(fields):

                with columns[position % 2]:

                    value = float(
                        scenario.get(
                            key,
                            DEFAULT_SCENARIO[key],
                        )
                    )

                    if key in FACTOR_FIELDS:

                        edited[key] = st.number_input(
                            label,
                            min_value=0.01,
                            max_value=1.0,
                            value=max(
                                0.01,
                                min(1.0, value),
                            ),
                            step=0.01,
                            format="%.2f",
                            key=f"sc_{index}_{key}",
                        )

                    elif key in NONNEGATIVE_FIELDS:

                        edited[key] = st.number_input(
                            label,
                            min_value=0.0,
                            value=max(0.0, value),
                            step=0.1,
                            key=f"sc_{index}_{key}",
                        )

                    else:

                        edited[key] = st.number_input(
                            label,
                            min_value=0.001,
                            value=max(0.001, value),
                            step=0.1,
                            key=f"sc_{index}_{key}",
                        )

        submitted = st.form_submit_button(
            "Save Scenario",
            type="primary",
        )

    if submitted:

        clean_name = name.strip()

        if not clean_name:
            st.error("Enter a scenario name.")
            return

        other_names = {
            item["name"]
            for i, item in enumerate(scenarios)
            if i != index
        }

        if clean_name in other_names:
            st.error(
                "Each scenario must have a unique name."
            )
            return

        edited["name"] = clean_name
        scenarios[index] = edited

        st.session_state["mineops_results_outdated"] = True

        st.success("Scenario saved successfully.")


# ============================================================
# COMPARISON TABLE
# ============================================================

def show_comparison_table(results):

    st.subheader("Engineering Comparison")

    dataframe = pd.DataFrame(
        comparison_rows(results)
    )

    st.dataframe(
        dataframe,
        width="stretch",
        hide_index=True,
    )

    st.download_button(
        "Download Comparison CSV",
        data=dataframe.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="mineopslab_scenario_comparison.csv",
        mime="text/csv",
    )

    return dataframe


# ============================================================
# COMPARISON CHARTS
# ============================================================

def show_comparison_charts(dataframe):

    st.subheader("Comparative Performance")

    chart_data = dataframe.set_index("Scenario")

    left, right = st.columns(2)

    with left:

        st.markdown("**Required Equipment**")

        st.bar_chart(
            chart_data[
                ["Required loaders", "Required trucks"]
            ],
            width="stretch",
        )

    with right:

        st.markdown("**Equipment Productivity**")

        st.bar_chart(
            chart_data[
                [
                    "Loader productivity (t/h)",
                    "Truck productivity (t/h)",
                ]
            ],
            width="stretch",
        )

    left, right = st.columns(2)

    with left:

        st.markdown("**System Capacity**")

        st.bar_chart(
            chart_data[
                ["System capacity (t/h)"]
            ],
            width="stretch",
        )

    with right:

        st.markdown("**Match Factor**")

        st.bar_chart(
            chart_data[
                ["Match factor"]
            ],
            width="stretch",
        )

    st.markdown("**Mine Productivity Index**")

    st.bar_chart(
        chart_data[
            ["Loader MPI (%)", "Truck MPI (%)"]
        ],
        width="stretch",
    )


# ============================================================
# ENGINEERING INTERPRETATION
# ============================================================

def show_scenario_interpretation(results):

    st.subheader("Engineering Interpretation")

    for result in results:

        with st.expander(
            result["name"],
            expanded=False,
        ):

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Required Loaders",
                result["loaders_required"],
            )

            col2.metric(
                "Required Trucks",
                result["trucks_required"],
            )

            col3.metric(
                "System Capacity",
                f"{result['system_capacity_tph']:,.0f} t/h",
            )

            st.markdown(
                f"**Match Factor:** "
                f"{result['match_factor']:.2f}"
            )

            for message in interpret_scenario(result):
                st.write(message)


# ============================================================
# LEARNING SECTION
# ============================================================

def show_learning_section(results):

    st.subheader("Engineering Learning Exercise")

    st.write(
        "Use the calculated scenarios to evaluate "
        "alternative mining equipment configurations."
    )

    st.markdown(
        """
**Questions for students**

1. Which scenario requires the fewest trucks?
2. How does haul distance influence truck productivity?
3. Which scenario has the highest system capacity?
4. Does a match factor close to 1 always indicate the
   best equipment configuration?
5. Which scenario would you recommend for the
   specified production target, and why?
"""
    )

    if results:

        fewest_trucks = min(
            results,
            key=lambda result: result["trucks_required"],
        )

        highest_capacity = max(
            results,
            key=lambda result: result["system_capacity_tph"],
        )

        with st.expander(
            "View Engineering Observations"
        ):

            st.write(
                "Fewest required trucks: "
                f"**{fewest_trucks['name']}**"
            )

            st.write(
                "Highest calculated system capacity: "
                f"**{highest_capacity['name']}**"
            )

            st.info(
                "Fleet size, production capacity and match "
                "factor are different engineering indicators. "
                "A final equipment recommendation should "
                "also consider operating costs, reliability "
                "and site-specific constraints."
            )


# ============================================================
# MAIN MODULE
# ============================================================

def show_scenario_comparison():

    st.caption("MINEOPSLAB | ENGINEERING ANALYSIS")
    st.title("Scenario Comparison")

    st.write(
        "Develop and compare alternative loading and "
        "haulage configurations. Evaluate equipment "
        "productivity, fleet requirements, system "
        "capacity and operational performance."
    )

    initialize_scenarios()

    scenarios = st.session_state["mineops_scenarios"]

    st.divider()

    st.subheader("Scenario Manager")

    # --------------------------------------------------------
    # CONTROL BUTTONS
    #
    # Callbacks run before Streamlit recreates the widgets.
    # This prevents the session-state modification error.
    # --------------------------------------------------------

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:

        scenario_options = list(range(len(scenarios)))

        current_index = st.session_state[
            "mineops_selected_index"
        ]

        current_index = min(
            current_index,
            len(scenarios) - 1,
        )

        selected_index = st.selectbox(
            "Select scenario",
            options=scenario_options,
            index=current_index,
            format_func=lambda index:
                scenarios[index]["name"],
            key="mineops_scenario_selector_widget",
        )

        st.session_state[
            "mineops_selected_index"
        ] = selected_index

    with col2:

        st.write("")
        st.write("")

        st.button(
            "Add Scenario",
            width="stretch",
            on_click=add_scenario,
        )

    with col3:

        st.write("")
        st.write("")

        st.button(
            "Duplicate Scenario",
            width="stretch",
            on_click=duplicate_scenario,
            args=(
                st.session_state["mineops_selected_index"],
            ),
        )

    # --------------------------------------------------------
    # DELETE SCENARIO
    # --------------------------------------------------------

    if len(scenarios) > 2:

        st.button(
            "Delete Selected Scenario",
            on_click=delete_scenario,
            args=(
                st.session_state["mineops_selected_index"],
            ),
        )

    # --------------------------------------------------------
    # EDIT SCENARIO
    # --------------------------------------------------------

    edit_scenario(
        st.session_state["mineops_selected_index"]
    )

    st.divider()

    # --------------------------------------------------------
    # RUN COMPARISON
    # --------------------------------------------------------

    st.subheader("Run Scenario Comparison")

    st.write(
        f"{len(scenarios)} scenarios are currently "
        "available for analysis."
    )

    if st.button(
        "Calculate and Compare Scenarios",
        type="primary",
        width="stretch",
    ):

        try:

            results = compare_scenarios(scenarios)

            st.session_state[
                "mineops_scenario_results"
            ] = results

            st.session_state[
                "mineops_results_outdated"
            ] = False

            st.success(
                "Scenario comparison completed."
            )

        except (ValueError, KeyError, TypeError) as error:

            st.error(
                f"Scenario calculation error: {error}"
            )

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    results = st.session_state.get(
        "mineops_scenario_results"
    )

    if not results:

        st.info(
            "Configure at least two scenarios, then "
            "select Calculate and Compare Scenarios."
        )

        return

    if st.session_state.get(
        "mineops_results_outdated",
        False,
    ):

        st.warning(
            "Scenario configurations have changed. "
            "Recalculate to update the comparison results."
        )

    st.divider()

    dataframe = show_comparison_table(results)

    st.divider()

    show_comparison_charts(dataframe)

    st.divider()

    show_scenario_interpretation(results)

    st.divider()

    show_learning_section(results)

    st.divider()

    # --------------------------------------------------------
    # EXPORT SCENARIO INPUTS
    # --------------------------------------------------------

    st.subheader("Export Scenario Inputs")

    export_data = json.dumps(
        scenarios,
        indent=4,
    )

    st.download_button(
        "Download Scenario Configuration (JSON)",
        data=export_data,
        file_name="mineopslab_scenarios.json",
        mime="application/json",
    )

    st.caption(
        "MineOpsLab Student Edition. Results are "
        "preliminary engineering estimates based on "
        "the MineOpsLab MPI productivity framework "
        "and specified operating assumptions."
    )
