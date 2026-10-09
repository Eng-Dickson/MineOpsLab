
"""
MineOpsLab
Fleet Optimization Module

Student Edition

Features:
- Select an existing operating scenario
- Set loader and truck fleet limits
- Choose an optimization objective
- Apply optional match-factor constraints
- Evaluate feasible equipment combinations
- Visualize results
- Interpret recommendations
- Export results to CSV

Uses calculations/optimization.py.
"""

import pandas as pd
import streamlit as st

from calculations.scenario_comparison import (
    DEFAULT_SCENARIO,
)

from calculations.optimization import (
    OBJECTIVES,
    optimize_fleet,
    optimization_rows,
    optimization_interpretation,
)


# ============================================================
# INITIALIZATION
# ============================================================

def initialize_optimization():

    if "mineops_optimization_results" not in st.session_state:
        st.session_state[
            "mineops_optimization_results"
        ] = None

    if "mineops_optimization_source" not in st.session_state:
        st.session_state[
            "mineops_optimization_source"
        ] = "Current Baseline"


# ============================================================
# AVAILABLE SCENARIOS
# ============================================================

def get_available_scenarios():

    available = {}

    saved_scenarios = st.session_state.get(
        "mineops_scenarios",
        [],
    )

    for index, scenario in enumerate(saved_scenarios):

        name = scenario.get(
            "name",
            f"Scenario {index + 1}",
        )

        available[name] = scenario

    if not available:

        available["Illustrative Baseline"] = dict(
            DEFAULT_SCENARIO
        )

    return available


# ============================================================
# SOURCE SELECTION
# ============================================================

def show_source_selection():

    st.subheader("1. Select Operating Scenario")

    available = get_available_scenarios()

    names = list(available.keys())

    selected_name = st.selectbox(
        "Operating scenario",
        options=names,
        help=(
            "Select a scenario previously created in "
            "Scenario Comparison."
        ),
    )

    scenario = dict(
        DEFAULT_SCENARIO
    )

    scenario.update(
        available[selected_name]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Production Target",
        f"{scenario['required_production_tph']:,.0f} t/h",
    )

    col2.metric(
        "Truck Payload",
        f"{scenario['truck_payload_t']:,.0f} t",
    )

    col3.metric(
        "Haul Distance",
        f"{scenario['haul_distance_km']:.2f} km",
    )

    with st.expander(
        "View Selected Scenario Inputs"
    ):

        rows = [
            {
                "Parameter": key.replace(
                    "_",
                    " ",
                ).title(),
                "Value": value,
            }
            for key, value in scenario.items()
            if key != "name"
        ]

        st.dataframe(
            pd.DataFrame(rows),
            width="stretch",
            hide_index=True,
        )

    if selected_name == "Illustrative Baseline":

        st.info(
            "No saved scenarios were found. "
            "Illustrative equipment and operating "
            "inputs are being used. Review these "
            "assumptions before interpreting results."
        )

    return scenario


# ============================================================
# OPTIMIZATION SETTINGS
# ============================================================

def show_optimization_settings():

    st.subheader("2. Optimization Configuration")

    st.write(
        "Define the available equipment fleet and "
        "select the engineering objective."
    )

    objective = st.selectbox(
        "Optimization objective",
        options=list(OBJECTIVES.keys()),
        format_func=lambda value: OBJECTIVES[value],
    )

    st.markdown("#### Available Loader Fleet")

    col1, col2 = st.columns(2)

    with col1:

        min_loaders = st.number_input(
            "Minimum loaders",
            min_value=1,
            max_value=100,
            value=1,
            step=1,
        )

    with col2:

        max_loaders = st.number_input(
            "Maximum loaders",
            min_value=1,
            max_value=100,
            value=4,
            step=1,
        )

    st.markdown("#### Available Truck Fleet")

    col1, col2 = st.columns(2)

    with col1:

        min_trucks = st.number_input(
            "Minimum trucks",
            min_value=1,
            max_value=500,
            value=1,
            step=1,
        )

    with col2:

        max_trucks = st.number_input(
            "Maximum trucks",
            min_value=1,
            max_value=500,
            value=20,
            step=1,
        )

    st.markdown("#### Engineering Constraints")

    apply_match_constraint = st.checkbox(
        "Apply match-factor limits",
        value=False,
    )

    minimum_match_factor = None
    maximum_match_factor = None

    if apply_match_constraint:

        left, right = st.columns(2)

        with left:

            minimum_match_factor = st.number_input(
                "Minimum match factor",
                min_value=0.0,
                max_value=10.0,
                value=0.80,
                step=0.05,
                format="%.2f",
            )

        with right:

            maximum_match_factor = st.number_input(
                "Maximum match factor",
                min_value=0.01,
                max_value=10.0,
                value=1.20,
                step=0.05,
                format="%.2f",
            )

    st.info(
        "Meeting the production target is mandatory "
        "for every feasible configuration. Match-factor "
        "limits are optional."
    )

    return {
        "objective": objective,
        "min_loaders": int(min_loaders),
        "max_loaders": int(max_loaders),
        "min_trucks": int(min_trucks),
        "max_trucks": int(max_trucks),
        "minimum_match_factor":
            minimum_match_factor,
        "maximum_match_factor":
            maximum_match_factor,
    }


# ============================================================
# RECOMMENDED CONFIGURATION
# ============================================================

def show_recommendation(result):

    st.subheader("3. Recommended Fleet Configuration")

    best = result["recommended"]

    if best is None:

        st.warning(
            "No feasible configuration was found "
            "within the selected fleet limits."
        )

        for message in optimization_interpretation(
            result
        ):
            st.write(message)

        return

    st.success(
        "A feasible configuration was identified."
    )

    left, middle, right = st.columns(3)

    left.metric(
        "Recommended Loaders",
        best["loaders"],
    )

    middle.metric(
        "Recommended Trucks",
        best["trucks"],
    )

    right.metric(
        "Total Equipment Units",
        best["total_units"],
    )

    left, middle, right = st.columns(3)

    left.metric(
        "System Capacity",
        f"{best['system_capacity_tph']:,.0f} t/h",
    )

    middle.metric(
        "Match Factor",
        f"{best['match_factor']:.3f}",
    )

    right.metric(
        "Capacity Surplus",
        f"{best['capacity_balance_tph']:,.0f} t/h",
    )

    st.markdown(
        f"**Optimization Objective:** "
        f"{result['objective_label']}"
    )

    st.markdown(
        f"**System Bottleneck:** "
        f"{best['bottleneck']}"
    )

    st.markdown(
        f"**Fleet Matching Status:** "
        f"{best['match_status']}"
    )


# ============================================================
# OPTIMIZATION SUMMARY
# ============================================================

def show_search_summary(result):

    st.subheader("4. Optimization Search Summary")

    left, middle, right = st.columns(3)

    left.metric(
        "Configurations Evaluated",
        result["evaluated_count"],
    )

    middle.metric(
        "Feasible Configurations",
        result["feasible_count"],
    )

    right.metric(
        "Infeasible Configurations",
        (
            result["evaluated_count"]
            - result["feasible_count"]
        ),
    )

    if result["evaluated_count"] > 0:

        feasibility_rate = (
            result["feasible_count"]
            / result["evaluated_count"]
        ) * 100

        st.write(
            f"**Feasible share of search space:** "
            f"{feasibility_rate:.1f}%"
        )


# ============================================================
# OPTIMIZATION TABLE
# ============================================================

def show_optimization_table(result):

    st.subheader("5. Evaluated Fleet Configurations")

    show_all = st.checkbox(
        "Show infeasible configurations",
        value=False,
    )

    if show_all:

        candidates = result["all_candidates"]

    else:

        candidates = result["ranked_candidates"]

    if not candidates:

        st.info(
            "No configurations meet the current "
            "constraints. Enable infeasible "
            "configurations to inspect the search space."
        )

        return

    dataframe = pd.DataFrame(
        optimization_rows(candidates)
    )

    st.dataframe(
        dataframe,
        width="stretch",
        hide_index=True,
    )

    st.download_button(
        "Download Optimization Results (CSV)",
        data=dataframe.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="mineopslab_optimization_results.csv",
        mime="text/csv",
    )


# ============================================================
# OPTIMIZATION CHARTS
# ============================================================

def show_optimization_charts(result):

    st.subheader("6. Optimization Visualizations")

    candidates = result["all_candidates"]

    if not candidates:
        return

    dataframe = pd.DataFrame(
        optimization_rows(candidates)
    )

    st.markdown(
        "#### System Capacity by Fleet Configuration"
    )

    chart_data = dataframe.copy()

    chart_data["Configuration"] = (
        chart_data["Loaders"].astype(str)
        + " loaders / "
        + chart_data["Trucks"].astype(str)
        + " trucks"
    )

    chart_data = chart_data.set_index(
        "Configuration"
    )

    st.bar_chart(
        chart_data[
            ["System capacity (t/h)"]
        ],
        width="stretch",
    )

    st.markdown(
        "#### Match Factor by Fleet Configuration"
    )

    st.line_chart(
        chart_data[
            ["Match factor"]
        ],
        width="stretch",
    )

    st.caption(
        "Charts show all evaluated configurations, "
        "including infeasible fleets. Use the results "
        "table to distinguish feasible solutions."
    )


# ============================================================
# ENGINEERING INTERPRETATION
# ============================================================

def show_interpretation(result):

    st.subheader("7. Engineering Interpretation")

    for message in optimization_interpretation(
        result
    ):

        st.write(message)

    st.info(
        "Optimization results depend on the equipment "
        "specifications, operating assumptions, fleet "
        "limits and selected objective. A configuration "
        "with the fewest units is not necessarily the "
        "configuration with the lowest cost."
    )


# ============================================================
# STUDENT LEARNING EXERCISE
# ============================================================

def show_learning_exercise():

    st.subheader("8. Student Engineering Exercise")

    st.write(
        "Use the optimization tool to investigate "
        "how fleet size and equipment matching affect "
        "mine production performance."
    )

    st.markdown(
        """
**Suggested investigations**

1. Determine the minimum fleet required to meet the
   specified production target.

2. Change the optimization objective to Best Fleet
   Matching. Does the recommended configuration change?

3. Apply match-factor limits between 0.80 and 1.20.
   How many configurations remain feasible?

4. Increase the maximum number of available trucks.
   Does the maximum achievable system capacity change?

5. Compare the minimum-fleet and maximum-capacity
   solutions. Which would you recommend for a mine
   operating under limited equipment availability?
"""
    )


# ============================================================
# MAIN OPTIMIZATION MODULE
# ============================================================

def show_optimization():

    st.caption(
        "MINEOPSLAB | ENGINEERING OPTIMIZATION"
    )

    st.title("Fleet Optimization")

    st.write(
        "Identify suitable loader-truck fleet "
        "configurations by evaluating production "
        "capacity, fleet requirements and equipment "
        "matching under defined engineering constraints."
    )

    initialize_optimization()

    st.divider()

    scenario = show_source_selection()

    st.divider()

    settings = show_optimization_settings()

    st.divider()

    if st.button(
        "Run Fleet Optimization",
        type="primary",
        width="stretch",
    ):

        try:

            result = optimize_fleet(
                scenario=scenario,
                **settings,
            )

            st.session_state[
                "mineops_optimization_results"
            ] = result

            st.success(
                "Fleet optimization completed."
            )

        except (
            ValueError,
            KeyError,
            TypeError,
            OverflowError,
        ) as error:

            st.session_state[
                "mineops_optimization_results"
            ] = None

            st.error(
                f"Optimization error: {error}"
            )

    result = st.session_state.get(
        "mineops_optimization_results"
    )

    if result is None:

        st.info(
            "Select an operating scenario, configure "
            "the optimization settings and click "
            "Run Fleet Optimization."
        )

        return

    st.divider()

    show_recommendation(result)

    st.divider()

    show_search_summary(result)

    st.divider()

    show_optimization_table(result)

    st.divider()

    show_optimization_charts(result)

    st.divider()

    show_interpretation(result)

    st.divider()

    show_learning_exercise()

    st.divider()

    st.caption(
        "MineOpsLab Student Edition. Optimization "
        "uses deterministic MPI-adjusted productivity "
        "estimates. Results are preliminary and do not "
        "represent detailed dispatch or queueing simulation."
    )
