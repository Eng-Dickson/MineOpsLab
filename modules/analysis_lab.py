
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from calculations.sensitivity import (
    calculate_truck_performance_sensitivity,
)


# ============================================================
# MINEOPSLAB CHART THEME
# ============================================================

NAVY = "#14213D"
BLUE = "#2378B8"
ORANGE = "#E68A36"
GREY = "#667085"
GRID = "#E7ECF2"
WHITE = "#FFFFFF"


def style_chart(fig, y_title, x_title="Truck Performance (%)"):
    """Apply a consistent light MineOpsLab chart style."""

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(
            family="Arial, sans-serif",
            color=NAVY,
            size=13,
        ),
        height=420,
        margin=dict(l=65, r=35, t=35, b=65),
        hovermode="x unified",
        showlegend=False,
    )

    fig.update_xaxes(
        title_text=x_title,
        title_font=dict(size=14, color=NAVY),
        tickfont=dict(size=12, color=GREY),
        showgrid=False,
        showline=True,
        linecolor="#CBD5E1",
        ticks="outside",
        tickcolor="#CBD5E1",
        zeroline=False,
    )

    fig.update_yaxes(
        title_text=y_title,
        title_font=dict(size=14, color=NAVY),
        tickfont=dict(size=12, color=GREY),
        showgrid=True,
        gridcolor=GRID,
        showline=False,
        zeroline=False,
    )

    return fig


def performance_ticks(minimum, maximum):
    """Choose readable percentage ticks."""

    span = maximum - minimum

    if span <= 10:
        interval = 2
    elif span <= 25:
        interval = 5
    elif span <= 60:
        interval = 10
    else:
        interval = 20

    start = math.ceil(minimum / interval) * interval

    ticks = list(
        range(start, math.floor(maximum / interval)
              * interval + 1, interval)
    )

    ticks = sorted(
        set([minimum, *ticks, maximum])
    )

    return ticks


def show_metric(label, value):
    st.metric(label, value)


def get_fleet_transitions(results):
    """Identify changes in required truck fleet."""

    ordered = sorted(
        results,
        key=lambda r: r["truck_performance_percent"],
    )

    transitions = []

    for previous, current in zip(
        ordered[:-1], ordered[1:]
    ):
        old_fleet = previous["trucks_required"]
        new_fleet = current["trucks_required"]

        if old_fleet != new_fleet:
            transitions.append({
                "lower_pp": previous[
                    "truck_performance_percent"
                ],
                "upper_pp": current[
                    "truck_performance_percent"
                ],
                "old_fleet": old_fleet,
                "new_fleet": new_fleet,
            })

    return transitions


# ============================================================
# PRODUCTIVITY GRAPH
# ============================================================

def show_productivity_chart(df, baseline_pp):

    x = df["Truck PP (%)"].tolist()
    y = df["Truck Productivity (t/h)"].tolist()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            name="Truck Productivity",
            line=dict(
                color=BLUE,
                width=3,
            ),
            marker=dict(
                color=BLUE,
                size=8,
                line=dict(
                    color=WHITE,
                    width=1.5,
                ),
            ),
            hovertemplate=(
                "Performance: %{x:.1f}%"
                "<br>Productivity: %{y:,.1f} t/h"
                "<extra></extra>"
            ),
        )
    )

    if min(x) <= baseline_pp * 100 <= max(x):
        fig.add_vline(
            x=baseline_pp * 100,
            line_dash="dash",
            line_color=ORANGE,
            line_width=2,
            annotation_text="Current PP",
            annotation_position="top left",
            annotation_font_color=ORANGE,
        )

    fig = style_chart(
        fig,
        y_title="Effective Truck Productivity (t/h)",
    )

    fig.update_xaxes(
        range=[min(x), max(x)],
        tickmode="array",
        tickvals=performance_ticks(min(x), max(x)),
        ticksuffix="%",
    )

    fig.update_yaxes(
        rangemode="tozero",
        tickformat=",.0f",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "mineopslab_truck_productivity",
                "scale": 2,
            },
        },
    )


# ============================================================
# FLEET REQUIREMENT GRAPH
# ============================================================

def show_fleet_chart(df, baseline_pp):

    x = df["Truck PP (%)"].tolist()
    y = df["Required Trucks"].tolist()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            name="Required Trucks",
            line=dict(
                color=ORANGE,
                width=3,
                shape="hv",
            ),
            marker=dict(
                color=ORANGE,
                size=8,
                symbol="circle",
                line=dict(
                    color=WHITE,
                    width=1.5,
                ),
            ),
            hovertemplate=(
                "Performance: %{x:.1f}%"
                "<br>Required Trucks: %{y:.0f}"
                "<extra></extra>"
            ),
        )
    )

    if min(x) <= baseline_pp * 100 <= max(x):
        fig.add_vline(
            x=baseline_pp * 100,
            line_dash="dash",
            line_color=BLUE,
            line_width=2,
            annotation_text="Current PP",
            annotation_position="top left",
            annotation_font_color=BLUE,
        )

    fig = style_chart(
        fig,
        y_title="Number of Trucks Required",
    )

    fig.update_xaxes(
        range=[min(x), max(x)],
        tickmode="array",
        tickvals=performance_ticks(min(x), max(x)),
        ticksuffix="%",
    )

    minimum_fleet = min(y)
    maximum_fleet = max(y)

    lower = max(0, minimum_fleet - 1)
    upper = maximum_fleet + 1

    fig.update_yaxes(
        range=[lower - 0.15, upper + 0.15],
        tickmode="linear",
        tick0=0,
        dtick=1,
    )

    if minimum_fleet == maximum_fleet:
        fig.add_annotation(
            x=(min(x) + max(x)) / 2,
            y=minimum_fleet,
            text=f"{minimum_fleet} truck(s) required",
            showarrow=False,
            yshift=24,
            font=dict(
                size=13,
                color=NAVY,
            ),
            bgcolor=WHITE,
            bordercolor=GRID,
            borderpad=5,
        )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "mineopslab_required_trucks",
                "scale": 2,
            },
        },
    )


# ============================================================
# MAIN ANALYSIS LAB
# ============================================================

def show_analysis_lab():

    st.caption("EXPERIMENTATION AND LEARNING")
    st.title("🧪 Sensitivity Analysis")

    st.write(
        "Investigate how changes in operating conditions "
        "affect equipment productivity and fleet requirements."
    )

    st.divider()

    # --------------------------------------------------------
    # REQUIRED BASELINE DATA
    # --------------------------------------------------------

    required_keys = [
        "required_production_tph",
        "loader_results",
        "haulage_results",
        "fleet_matching_results",
        "loaders_required",
        "loader_effective_productivity",
        "bucket_payload_t",
        "loader_cycle_time",
        "truck_payload",
    ]

    missing = [
        key for key in required_keys
        if key not in st.session_state
    ]

    if missing:
        st.warning(
            "Complete the Material & Production, Loading "
            "System, Haulage System and Fleet Matching "
            "modules before running Sensitivity Analysis."
        )
        return

    haulage = st.session_state.haulage_results
    fleet = st.session_state.fleet_matching_results

    required_production = (
        st.session_state.required_production_tph
    )

    baseline_pp = haulage["truck_performance"]
    baseline_mpi = haulage["truck_mpi"]
    baseline_trucks = fleet["trucks_required"]

    # --------------------------------------------------------
    # 1. RESEARCH QUESTION
    # --------------------------------------------------------

    st.subheader("1. What Are We Investigating?")

    st.info(
        "🎓 Research Question: How does changing Truck "
        "Performance (PP) affect truck productivity and "
        "the number of trucks required to achieve the "
        "mine production target?"
    )

    st.write(
        "In this experiment, we change only Truck "
        "Performance. Truck payload, haul distance, "
        "travel speeds, equipment availability, "
        "utilization and loader characteristics "
        "remain constant."
    )

    # --------------------------------------------------------
    # 2. BASELINE OPERATING CONDITIONS
    # --------------------------------------------------------

    st.write("")
    st.subheader("2. Current Operating Conditions")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        show_metric(
            "Production Target",
            f"{required_production:,.0f} t/h",
        )

    with c2:
        show_metric(
            "Truck Performance",
            f"{baseline_pp * 100:.1f}%",
        )

    with c3:
        show_metric(
            "Truck MPI",
            f"{baseline_mpi * 100:.1f}%",
        )

    with c4:
        show_metric(
            "Required Trucks",
            f"{baseline_trucks}",
        )

    st.caption(
        "These values represent the current mine "
        "operating scenario and provide the baseline "
        "for the sensitivity experiment."
    )

    # --------------------------------------------------------
    # 3. EXPERIMENT DESIGN
    # --------------------------------------------------------

    st.write("")
    st.subheader("3. Design Your Experiment")

    st.selectbox(
        "Operational variable",
        ["Truck Performance (PP)"],
        key="sensitivity_variable",
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        minimum_pp = st.number_input(
            "Minimum PP (%)",
            min_value=1.0,
            max_value=100.0,
            value=60.0,
            step=1.0,
            key="analysis_min_pp",
        )

    with c2:
        maximum_pp = st.number_input(
            "Maximum PP (%)",
            min_value=1.0,
            max_value=100.0,
            value=100.0,
            step=1.0,
            key="analysis_max_pp",
        )

    with c3:
        step_pp = st.number_input(
            "Step (%)",
            min_value=1.0,
            max_value=25.0,
            value=5.0,
            step=1.0,
            key="analysis_step_pp",
        )

    if minimum_pp >= maximum_pp:
        st.error(
            "Maximum PP must be greater than Minimum PP."
        )
        return

    st.caption(
        "For example, test Truck Performance from 60% "
        "to 100% in increments of 5 percentage points."
    )

    # --------------------------------------------------------
    # 4. RUN SENSITIVITY CALCULATION
    # --------------------------------------------------------

    try:
        analysis = calculate_truck_performance_sensitivity(
            truck_payload_t=st.session_state.truck_payload,
            haul_distance_km=haulage["haul_distance_km"],
            loaded_speed_kmh=haulage["loaded_speed_kmh"],
            empty_speed_kmh=haulage["empty_speed_kmh"],
            spotting_time_min=haulage["spotting_time_min"],
            dumping_time_min=haulage["dumping_time_min"],
            truck_availability=haulage["truck_availability"],
            truck_utilization=haulage["truck_utilization"],
            bucket_payload_t=st.session_state.bucket_payload_t,
            loader_cycle_time_sec=st.session_state.loader_cycle_time,
            required_production_tph=required_production,
            loaders_required=st.session_state.loaders_required,
            loader_effective_productivity_tph=(
                st.session_state.loader_effective_productivity
            ),
            performance_min=minimum_pp / 100,
            performance_max=maximum_pp / 100,
            performance_step=step_pp / 100,
            baseline_performance=baseline_pp,
        )

    except (ValueError, KeyError, TypeError) as error:
        st.error(
            f"Unable to complete analysis: {error}"
        )
        return

    results = analysis["results"]

    if not results:
        st.warning(
            "No sensitivity results were generated."
        )
        return

    st.session_state.analysis_results = analysis

    # --------------------------------------------------------
    # 5. CREATE DATAFRAME
    # --------------------------------------------------------

    df = pd.DataFrame([
        {
            "Truck PP (%)":
                result["truck_performance_percent"],
            "Truck MPI (%)":
                result["truck_mpi_percent"],
            "Truck Productivity (t/h)":
                result[
                    "effective_truck_productivity_tph"
                ],
            "Required Trucks":
                result["trucks_required"],
            "Baseline": (
                "Current"
                if result["is_baseline"]
                else ""
            ),
        }
        for result in results
    ])

    df = df.sort_values(
        by="Truck PP (%)"
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # 6. TRUCK PRODUCTIVITY ANALYSIS
    # --------------------------------------------------------

    st.write("")
    st.subheader(
        "4. What Happens to Truck Productivity?"
    )

    st.write(
        "This graph illustrates how the effective "
        "productivity of one truck changes when "
        "Truck Performance increases or decreases."
    )

    show_productivity_chart(df, baseline_pp)

    lowest = min(
        results,
        key=lambda r: r["truck_performance_percent"],
    )

    highest = max(
        results,
        key=lambda r: r["truck_performance_percent"],
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            (
                "Productivity at "
                f"{lowest['truck_performance_percent']:.0f}% PP"
            ),
            (
                f"{lowest['effective_truck_productivity_tph']:,.1f} "
                "t/h"
            ),
        )

    with c2:
        st.metric(
            (
                "Productivity at "
                f"{highest['truck_performance_percent']:.0f}% PP"
            ),
            (
                f"{highest['effective_truck_productivity_tph']:,.1f} "
                "t/h"
            ),
        )

    st.info(
        "🎓 Learning Point: Improving Truck Performance "
        "increases Truck MPI and effective truck productivity. "
        "In this experiment, physical cycle time remains "
        "constant because haul distance, speeds and "
        "loading conditions are unchanged."
    )

    # --------------------------------------------------------
    # 7. FLEET REQUIREMENT ANALYSIS
    # --------------------------------------------------------

    st.write("")
    st.subheader(
        "5. What Happens to the Required Truck Fleet?"
    )

    st.write(
        "The application recalculates the minimum number "
        "of trucks required to achieve the production "
        "target at each Performance level."
    )

    show_fleet_chart(df, baseline_pp)

    st.caption(
        "Truck fleet requirements change in whole units. "
        "A small improvement in Performance does not "
        "necessarily reduce the required fleet."
    )

    # --------------------------------------------------------
    # 8. FLEET TRANSITIONS
    # --------------------------------------------------------

    st.write("")
    st.subheader(
        "6. Where Does the Fleet Requirement Change?"
    )

    transitions = get_fleet_transitions(results)

    if transitions:
        for transition in transitions:
            old_fleet = transition["old_fleet"]
            new_fleet = transition["new_fleet"]
            lower_pp = transition["lower_pp"]
            upper_pp = transition["upper_pp"]

            st.info(
                f"Between {lower_pp:.1f}% and "
                f"{upper_pp:.1f}% Truck Performance, "
                f"the required fleet changes from "
                f"{old_fleet} to {new_fleet} trucks."
            )

        st.caption(
            "These intervals are based on the selected "
            "experiment step size. They do not represent "
            "exact fleet transition thresholds."
        )

    else:
        st.info(
            "The required truck fleet does not change "
            "within the selected Performance range."
        )

    # --------------------------------------------------------
    # 9. ENGINEERING INTERPRETATION
    # --------------------------------------------------------

    st.write("")
    st.subheader("7. What Have We Learned?")

    lowest_productivity = (
        lowest["effective_truck_productivity_tph"]
    )

    highest_productivity = (
        highest["effective_truck_productivity_tph"]
    )

    productivity_change = (
        highest_productivity - lowest_productivity
    )

    if lowest_productivity > 0:
        change_percent = (
            productivity_change
            / lowest_productivity
            * 100
        )
    else:
        change_percent = 0.0

    lowest_fleet = lowest["trucks_required"]
    highest_fleet = highest["trucks_required"]

    st.write(
        f"When Truck Performance increases from "
        f"{lowest['truck_performance_percent']:.1f}% "
        f"to {highest['truck_performance_percent']:.1f}%, "
        f"effective truck productivity increases from "
        f"{lowest_productivity:,.1f} t/h to "
        f"{highest_productivity:,.1f} t/h. "
        f"This represents a productivity increase "
        f"of {change_percent:.1f}%."
    )

    if highest_fleet < lowest_fleet:
        st.success(
            f"Across the tested range, the required "
            f"production fleet decreases from "
            f"{lowest_fleet} to {highest_fleet} trucks."
        )

    elif highest_fleet == lowest_fleet:
        st.info(
            f"Despite improved truck productivity, "
            f"the required fleet remains at "
            f"{highest_fleet} trucks throughout "
            f"the tested range."
        )

    else:
        st.warning(
            "The calculated fleet requirement increased "
            "as Performance improved. Review the "
            "calculation inputs and results."
        )

    st.write(
        "**Engineering Conclusion:** Improving equipment "
        "performance increases productive capacity and "
        "may reduce the number of trucks required to meet "
        "a fixed production target. However, the fleet "
        "requirement only changes when a whole-truck "
        "sizing threshold is crossed."
    )

    # --------------------------------------------------------
    # 10. COMPLETE RESULTS TABLE
    # --------------------------------------------------------

    st.write("")

    with st.expander(
        "📊 View Complete Experiment Results"
    ):
        st.dataframe(
            df.style.format({
                "Truck PP (%)": "{:.1f}",
                "Truck MPI (%)": "{:.1f}",
                "Truck Productivity (t/h)": "{:,.1f}",
                "Required Trucks": "{:.0f}",
            }),
            width="stretch",
            hide_index=True,
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Results as CSV",
            data=csv,
            file_name="mineopslab_sensitivity.csv",
            mime="text/csv",
            width="stretch",
        )

    # --------------------------------------------------------
    # 11. CALCULATION BASIS
    # --------------------------------------------------------

    with st.expander(
        "🔎 Understand the Engineering Calculations"
    ):
        st.markdown("#### Mine Productivity Index")

        st.latex(
            r"MPI_T = Av_T^{0.3} PP_T^{0.5} U_T^{0.2}"
        )

        st.write(
            "Truck Availability and Utilization remain "
            "constant. Only Truck Performance changes."
        )

        st.markdown(
            "#### Effective Truck Productivity"
        )

        st.latex(
            r"P_{\mathrm{effective}} = "
            r"P_{\mathrm{theoretical}} \times MPI_T"
        )

        st.markdown("#### Required Truck Fleet")

        st.latex(
            r"N_T = \left\lceil "
            r"\frac{P_{\mathrm{required}}}"
            r"{P_{\mathrm{effective}}} "
            r"\right\rceil"
        )

        st.write(
            "The ceiling function rounds the calculated "
            "fleet requirement upward to the next whole truck."
        )

        st.markdown("#### Assumptions")

        st.write(
            "Truck payload, haul distance, travel speeds, "
            "spotting time, dumping time, loader characteristics, "
            "Truck Availability and Truck Utilization "
            "are held constant."
        )

        st.write(
            "The sensitivity analysis uses deterministic "
            "calculations. It does not explicitly simulate "
            "truck queues, dispatching delays or random "
            "variations in operating cycles."
        )

    # --------------------------------------------------------
    # 12. STUDENT LEARNING EXERCISE
    # --------------------------------------------------------

    st.write("")
    st.subheader("🎓 Test Your Understanding")

    st.write(
        "**Question:** Why can Truck Performance improve "
        "without reducing the number of trucks required?"
    )

    with st.expander("Reveal Explanation"):
        st.write(
            "Truck productivity changes continuously, "
            "but fleet requirements consist of whole "
            "trucks. An improvement in Performance "
            "only reduces the required fleet when "
            "the productive capacity of one fewer truck "
            "becomes sufficient to meet the mine "
            "production target."
        )

    st.divider()

    st.caption(
        "MineOpsLab | Mining Operations Optimization "
        "& Learning Platform"
    )
