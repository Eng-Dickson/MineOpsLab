
"""
MineOpsLab
Fleet Optimization Calculation Engine

Student Edition

Optimization objectives:
1. Minimum fleet size
2. Best fleet matching
3. Maximum system capacity

Uses the existing MineOpsLab calculation engines.
No economic calculations are required.

IMPORTANT:
This is a deterministic, preliminary planning model.
It does not simulate queues, equipment dispatch, road
congestion, or stochastic equipment downtime.
"""

import math

from calculations.loader import calculate_loader_performance
from calculations.haulage import calculate_haulage_performance
from calculations.fleet_matching import calculate_fleet_matching


OBJECTIVES = {
    "minimum_fleet": "Minimum Fleet Size",
    "best_match": "Best Fleet Matching",
    "maximum_capacity": "Maximum System Capacity",
}


def optimize_fleet(
    scenario,
    min_loaders=1,
    max_loaders=4,
    min_trucks=1,
    max_trucks=20,
    objective="minimum_fleet",
    minimum_match_factor=None,
    maximum_match_factor=None,
):
    """
    Evaluate integer loader-truck fleet combinations.

    Parameters
    ----------
    scenario : dict
        Operating inputs using the same structure as
        MineOpsLab Scenario Comparison.

    min_loaders, max_loaders : int
        Search bounds for installed loaders.

    min_trucks, max_trucks : int
        Search bounds for installed trucks.

    objective : str
        minimum_fleet, best_match, maximum_capacity

    minimum_match_factor : float or None
        Optional lower bound for fleet match factor.

    maximum_match_factor : float or None
        Optional upper bound for fleet match factor.

    Returns
    -------
    dict
        Recommended configuration, ranked feasible
        configurations, and all evaluated candidates.
    """

    if objective not in OBJECTIVES:
        raise ValueError(
            "Invalid optimization objective."
        )

    bounds = (
        min_loaders,
        max_loaders,
        min_trucks,
        max_trucks,
    )

    if any(
        isinstance(value, bool)
        or not isinstance(value, int)
        for value in bounds
    ):
        raise ValueError(
            "Fleet search bounds must be integers."
        )

    if min_loaders < 1 or max_loaders < min_loaders:
        raise ValueError(
            "Invalid loader search range."
        )

    if min_trucks < 1 or max_trucks < min_trucks:
        raise ValueError(
            "Invalid truck search range."
        )

    if max_loaders > 100 or max_trucks > 500:
        raise ValueError(
            "Search limits are too large for this "
            "student edition."
        )

    if (
        minimum_match_factor is not None
        and minimum_match_factor < 0
    ):
        raise ValueError(
            "Minimum match factor cannot be negative."
        )

    if (
        maximum_match_factor is not None
        and maximum_match_factor <= 0
    ):
        raise ValueError(
            "Maximum match factor must be positive."
        )

    if (
        minimum_match_factor is not None
        and maximum_match_factor is not None
        and minimum_match_factor > maximum_match_factor
    ):
        raise ValueError(
            "Minimum match factor cannot exceed "
            "maximum match factor."
        )

    required_keys = (
        "required_production_tph",
        "loose_density",
        "bucket_capacity_m3",
        "fill_factor",
        "loader_cycle_time_sec",
        "loader_availability",
        "loader_performance",
        "loader_utilization",
        "truck_payload_t",
        "haul_distance_km",
        "loaded_speed_kmh",
        "empty_speed_kmh",
        "spotting_time_min",
        "dumping_time_min",
        "truck_availability",
        "truck_performance",
        "truck_utilization",
    )

    missing = [
        key for key in required_keys
        if key not in scenario
    ]

    if missing:
        raise ValueError(
            "Missing scenario inputs: "
            + ", ".join(missing)
        )

    target = float(
        scenario["required_production_tph"]
    )

    if not math.isfinite(target) or target <= 0:
        raise ValueError(
            "Optimization requires a positive, finite "
            "production target."
        )

    # --------------------------------------------------------
    # EXISTING LOADER CALCULATION
    # --------------------------------------------------------

    loader = calculate_loader_performance(
        bucket_capacity_m3=scenario[
            "bucket_capacity_m3"
        ],
        fill_factor=scenario["fill_factor"],
        loose_density=scenario["loose_density"],
        bucket_cycle_time_sec=scenario[
            "loader_cycle_time_sec"
        ],
        availability=scenario[
            "loader_availability"
        ],
        utilization=scenario[
            "loader_utilization"
        ],
        performance=scenario[
            "loader_performance"
        ],
        required_production_tph=target,
    )

    # --------------------------------------------------------
    # EXISTING HAULAGE CALCULATION
    # --------------------------------------------------------

    haulage = calculate_haulage_performance(
        truck_payload_t=scenario["truck_payload_t"],
        haul_distance_km=scenario["haul_distance_km"],
        loaded_speed_kmh=scenario["loaded_speed_kmh"],
        empty_speed_kmh=scenario["empty_speed_kmh"],
        spotting_time_min=scenario["spotting_time_min"],
        dumping_time_min=scenario["dumping_time_min"],
        truck_availability=scenario[
            "truck_availability"
        ],
        truck_performance=scenario[
            "truck_performance"
        ],
        truck_utilization=scenario[
            "truck_utilization"
        ],
    )

    # --------------------------------------------------------
    # FLEET MATCHING REFERENCE
    #
    # This provides loading time, truck cycle time,
    # and per-truck effective productivity.
    #
    # Candidate fleet sizes are evaluated separately.
    # --------------------------------------------------------

    reference = calculate_fleet_matching(
        truck_payload_t=scenario["truck_payload_t"],
        bucket_payload_t=loader["bucket_payload_t"],
        loader_cycle_time_sec=scenario[
            "loader_cycle_time_sec"
        ],
        non_loading_cycle_time_min=haulage[
            "non_loading_cycle_time_min"
        ],
        required_production_tph=target,
        truck_mpi=haulage["truck_mpi"],
        loaders_required=loader["loaders_required"],
        loader_effective_productivity_tph=loader[
            "effective_productivity_tph"
        ],
    )

    loader_productivity = loader[
        "effective_productivity_tph"
    ]

    truck_productivity = reference[
        "effective_truck_productivity_tph"
    ]

    loading_time = reference[
        "truck_loading_time_min"
    ]

    complete_cycle = reference[
        "complete_cycle_time_min"
    ]

    # --------------------------------------------------------
    # ENUMERATE ALL INTEGER FLEET COMBINATIONS
    # --------------------------------------------------------

    candidates = []

    for loaders in range(
        min_loaders,
        max_loaders + 1,
    ):
        for trucks in range(
            min_trucks,
            max_trucks + 1,
        ):

            loading_capacity = (
                loaders * loader_productivity
            )

            haulage_capacity = (
                trucks * truck_productivity
            )

            system_capacity = min(
                loading_capacity,
                haulage_capacity,
            )

            capacity_balance = (
                system_capacity - target
            )

            production_met = (
                system_capacity + 1e-9 >= target
            )

            match_factor = (
                trucks * loading_time
            ) / (
                loaders * complete_cycle
            )

            match_deviation = abs(
                match_factor - 1.0
            )

            match_constraint_met = True

            if minimum_match_factor is not None:
                match_constraint_met = (
                    match_constraint_met
                    and match_factor + 1e-9
                    >= minimum_match_factor
                )

            if maximum_match_factor is not None:
                match_constraint_met = (
                    match_constraint_met
                    and match_factor - 1e-9
                    <= maximum_match_factor
                )

            feasible = (
                production_met
                and match_constraint_met
            )

            if abs(
                loading_capacity - haulage_capacity
            ) <= 1e-9:
                bottleneck = "Balanced capacity"
            elif loading_capacity < haulage_capacity:
                bottleneck = "Loading system"
            else:
                bottleneck = "Haulage system"

            if match_factor < 0.95:
                match_status = "Excess loader capacity"
            elif match_factor > 1.05:
                match_status = "Excess truck capacity"
            else:
                match_status = "Approximately balanced"

            candidates.append({
                "loaders": loaders,
                "trucks": trucks,
                "total_units": loaders + trucks,
                "loading_capacity_tph":
                    loading_capacity,
                "haulage_capacity_tph":
                    haulage_capacity,
                "system_capacity_tph":
                    system_capacity,
                "capacity_balance_tph":
                    capacity_balance,
                "match_factor":
                    match_factor,
                "match_deviation":
                    match_deviation,
                "match_status":
                    match_status,
                "bottleneck":
                    bottleneck,
                "production_target_met":
                    production_met,
                "match_constraint_met":
                    match_constraint_met,
                "feasible":
                    feasible,
            })

    feasible_candidates = [
        item for item in candidates
        if item["feasible"]
    ]

    # --------------------------------------------------------
    # RANK FEASIBLE CONFIGURATIONS
    # --------------------------------------------------------

    if objective == "minimum_fleet":

        ranking_key = lambda item: (
            item["total_units"],
            item["match_deviation"],
            item["capacity_balance_tph"],
            item["loaders"],
            item["trucks"],
        )

    elif objective == "best_match":

        ranking_key = lambda item: (
            item["match_deviation"],
            item["total_units"],
            item["capacity_balance_tph"],
            item["loaders"],
            item["trucks"],
        )

    else:

        ranking_key = lambda item: (
            -item["system_capacity_tph"],
            item["total_units"],
            item["match_deviation"],
            item["loaders"],
            item["trucks"],
        )

    ranked = sorted(
        feasible_candidates,
        key=ranking_key,
    )

    recommended = ranked[0] if ranked else None

    return {
        "objective": objective,
        "objective_label": OBJECTIVES[objective],
        "scenario_name": scenario.get(
            "name",
            "Operating Scenario",
        ),
        "required_production_tph": target,
        "recommended": recommended,
        "ranked_candidates": ranked,
        "all_candidates": candidates,
        "feasible_count": len(ranked),
        "evaluated_count": len(candidates),
        "loader_results": loader,
        "haulage_results": haulage,
        "fleet_reference": reference,
        "minimum_match_factor":
            minimum_match_factor,
        "maximum_match_factor":
            maximum_match_factor,
    }


def optimization_rows(candidates):
    """Convert candidate results into table records."""

    rows = []

    for item in candidates:
        rows.append({
            "Loaders": item["loaders"],
            "Trucks": item["trucks"],
            "Total units": item["total_units"],
            "Loading capacity (t/h)":
                item["loading_capacity_tph"],
            "Haulage capacity (t/h)":
                item["haulage_capacity_tph"],
            "System capacity (t/h)":
                item["system_capacity_tph"],
            "Capacity surplus (t/h)":
                item["capacity_balance_tph"],
            "Match factor":
                item["match_factor"],
            "Match deviation":
                item["match_deviation"],
            "Bottleneck":
                item["bottleneck"],
            "Production met":
                item["production_target_met"],
            "Match constraint met":
                item["match_constraint_met"],
            "Feasible":
                item["feasible"],
        })

    return rows


def optimization_interpretation(result):
    """Explain the recommended configuration."""

    best = result["recommended"]

    if best is None:
        return [
            "No feasible fleet was found within the "
            "specified search ranges and constraints.",
            "Consider increasing the available fleet "
            "limits or reviewing the match-factor bounds.",
        ]

    messages = [
        (
            f"The recommended fleet contains "
            f"{best['loaders']} loader(s) and "
            f"{best['trucks']} truck(s)."
        ),
        (
            f"The estimated system capacity is "
            f"{best['system_capacity_tph']:,.1f} t/h "
            f"against a production target of "
            f"{result['required_production_tph']:,.1f} t/h."
        ),
        (
            f"The fleet match factor is "
            f"{best['match_factor']:.3f}, classified as "
            f"{best['match_status'].lower()}."
        ),
        (
            f"The limiting subsystem is: "
            f"{best['bottleneck']}."
        ),
    ]

    if result["objective"] == "minimum_fleet":
        messages.append(
            "This solution minimizes the total number "
            "of equipment units within the evaluated "
            "configurations. It does not necessarily "
            "minimize ownership or operating cost."
        )

    elif result["objective"] == "best_match":
        messages.append(
            "This solution minimizes the absolute "
            "difference between the conventional match "
            "factor and 1.0 among feasible configurations."
        )

    else:
        messages.append(
            "This solution maximizes estimated system "
            "capacity within the specified equipment limits. "
            "It may involve more equipment than required "
            "to meet the production target."
        )

    return messages
