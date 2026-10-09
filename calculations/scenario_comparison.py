
"""
MineOpsLab
Scenario Comparison Calculation Engine

Reuses the existing loading, haulage and fleet-matching
calculation engines without modifying their formulas.
"""

from copy import deepcopy

from calculations.loader import calculate_loader_performance
from calculations.haulage import calculate_haulage_performance
from calculations.fleet_matching import calculate_fleet_matching


# ============================================================
# DEFAULT SCENARIO CONFIGURATION
# ============================================================

DEFAULT_SCENARIO = {
    "name": "Scenario",
    "required_production_tph": 980.0,
    "loose_density": 1.8,

    # Loading equipment
    "bucket_capacity_m3": 16.0,
    "fill_factor": 0.865,
    "loader_cycle_time_sec": 30.0,
    "loader_availability": 0.90,
    "loader_performance": 0.90,
    "loader_utilization": 0.85,

    # Haulage equipment
    "truck_payload_t": 90.0,
    "haul_distance_km": 3.0,
    "loaded_speed_kmh": 25.0,
    "empty_speed_kmh": 35.0,
    "spotting_time_min": 0.8,
    "dumping_time_min": 0.7,
    "truck_availability": 0.90,
    "truck_performance": 0.85,
    "truck_utilization": 0.85,
}


# ============================================================
# CREATE SCENARIO
# ============================================================

def make_scenario(name="Scenario", overrides=None):
    """
    Create an independent scenario using default inputs.
    """

    scenario = deepcopy(DEFAULT_SCENARIO)

    scenario["name"] = str(name)

    if overrides:
        scenario.update(overrides)

    return scenario


# ============================================================
# CALCULATE INDIVIDUAL SCENARIO
# ============================================================

def calculate_scenario(scenario):
    """
    Calculate an integrated loading and haulage scenario.

    Uses the existing MineOpsLab calculation engines:

    1. Loader performance
    2. Haulage performance
    3. Fleet matching

    Returns all engineering results for comparison.
    """

    data = deepcopy(DEFAULT_SCENARIO)
    data.update(scenario)

    # --------------------------------------------------------
    # 1. LOADER PERFORMANCE
    # --------------------------------------------------------

    loader = calculate_loader_performance(
        bucket_capacity_m3=data["bucket_capacity_m3"],
        fill_factor=data["fill_factor"],
        loose_density=data["loose_density"],
        bucket_cycle_time_sec=data["loader_cycle_time_sec"],
        availability=data["loader_availability"],
        utilization=data["loader_utilization"],
        performance=data["loader_performance"],
        required_production_tph=data["required_production_tph"],
    )

    # --------------------------------------------------------
    # 2. HAULAGE PERFORMANCE
    # --------------------------------------------------------

    haulage = calculate_haulage_performance(
        truck_payload_t=data["truck_payload_t"],
        haul_distance_km=data["haul_distance_km"],
        loaded_speed_kmh=data["loaded_speed_kmh"],
        empty_speed_kmh=data["empty_speed_kmh"],
        spotting_time_min=data["spotting_time_min"],
        dumping_time_min=data["dumping_time_min"],
        truck_availability=data["truck_availability"],
        truck_performance=data["truck_performance"],
        truck_utilization=data["truck_utilization"],
    )

    # --------------------------------------------------------
    # 3. FLEET MATCHING
    # --------------------------------------------------------

    fleet = calculate_fleet_matching(
        truck_payload_t=data["truck_payload_t"],
        bucket_payload_t=loader["bucket_payload_t"],
        loader_cycle_time_sec=data["loader_cycle_time_sec"],
        non_loading_cycle_time_min=haulage[
            "non_loading_cycle_time_min"
        ],
        required_production_tph=data["required_production_tph"],
        truck_mpi=haulage["truck_mpi"],
        loaders_required=loader["loaders_required"],
        loader_effective_productivity_tph=loader[
            "effective_productivity_tph"
        ],
    )

    # --------------------------------------------------------
    # 4. COMBINE ENGINEERING RESULTS
    # --------------------------------------------------------

    result = {
        "name": data["name"],

        "inputs": data,

        "loader": loader,
        "haulage": haulage,
        "fleet": fleet,

        # Production
        "required_production_tph":
            data["required_production_tph"],

        # Mine Productivity Index
        "loader_mpi":
            loader["mpi"],

        "truck_mpi":
            haulage["truck_mpi"],

        # Equipment productivity
        "loader_productivity_tph":
            loader["effective_productivity_tph"],

        "truck_productivity_tph":
            fleet["effective_truck_productivity_tph"],

        # Fleet requirements
        "loaders_required":
            loader["loaders_required"],

        "trucks_required":
            fleet["trucks_required"],

        "balanced_trucks":
            fleet["balanced_trucks"],

        # Loader-truck compatibility
        "passes_per_truck":
            fleet["passes_per_truck"],

        # Cycle times
        "truck_loading_time_min":
            fleet["truck_loading_time_min"],

        "complete_cycle_time_min":
            fleet["complete_cycle_time_min"],

        # Fleet matching
        "match_factor":
            fleet["match_factor"],

        "match_status":
            fleet["match_status"],

        # Integrated system
        "system_capacity_tph":
            fleet["system_capacity_tph"],

        "capacity_balance_tph":
            fleet["system_capacity_balance_tph"],

        "capacity_bottleneck":
            fleet["capacity_bottleneck"],

        "production_target_met":
            fleet["production_target_met"],
    }

    return result


# ============================================================
# COMPARE MULTIPLE SCENARIOS
# ============================================================

def compare_scenarios(scenarios):
    """
    Calculate multiple scenarios independently.
    """

    if not scenarios:
        raise ValueError(
            "At least one scenario is required."
        )

    names = [
        str(scenario.get("name", "")).strip()
        for scenario in scenarios
    ]

    if any(not name for name in names):
        raise ValueError(
            "Every scenario must have a name."
        )

    if len(names) != len(set(names)):
        raise ValueError(
            "Scenario names must be unique."
        )

    results = []

    for scenario in scenarios:
        result = calculate_scenario(scenario)
        results.append(result)

    return results


# ============================================================
# PREPARE COMPARISON TABLE
# ============================================================

def comparison_rows(results):
    """
    Convert scenario results into flat records suitable
    for tables, charts and CSV export.
    """

    rows = []

    for result in results:

        inputs = result["inputs"]

        rows.append({

            "Scenario":
                result["name"],

            "Production target (t/h)":
                result["required_production_tph"],

            "Bucket capacity (m3)":
                inputs["bucket_capacity_m3"],

            "Truck payload (t)":
                inputs["truck_payload_t"],

            "Haul distance (km)":
                inputs["haul_distance_km"],

            "Loader MPI (%)":
                result["loader_mpi"] * 100,

            "Truck MPI (%)":
                result["truck_mpi"] * 100,

            "Loader productivity (t/h)":
                result["loader_productivity_tph"],

            "Truck productivity (t/h)":
                result["truck_productivity_tph"],

            "Required loaders":
                result["loaders_required"],

            "Required trucks":
                result["trucks_required"],

            "Balanced trucks":
                result["balanced_trucks"],

            "Loader passes per truck":
                result["passes_per_truck"],

            "Truck cycle (min)":
                result["complete_cycle_time_min"],

            "Match factor":
                result["match_factor"],

            "System capacity (t/h)":
                result["system_capacity_tph"],

            "Capacity surplus (t/h)":
                result["capacity_balance_tph"],

            "Bottleneck":
                result["capacity_bottleneck"],

            "Production target met":
                result["production_target_met"],
        })

    return rows


# ============================================================
# ENGINEERING INTERPRETATION
# ============================================================

def interpret_scenario(result):
    """
    Generate engineering interpretations of the
    calculated loading and haulage configuration.
    """

    messages = []

    # --------------------------------------------------------
    # Production target
    # --------------------------------------------------------

    if result["production_target_met"]:

        messages.append(
            "The calculated fleet meets the specified "
            "production target under the model assumptions."
        )

    else:

        messages.append(
            "The calculated system does not meet the "
            "specified production target."
        )

    # --------------------------------------------------------
    # Fleet matching
    # --------------------------------------------------------

    match_factor = result["match_factor"]

    if match_factor == 0:

        messages.append(
            "Fleet matching is not applicable for this "
            "configuration."
        )

    elif match_factor < 0.95:

        messages.append(
            "The production fleet has excess loader "
            "capacity relative to its truck fleet."
        )

    elif match_factor > 1.05:

        messages.append(
            "The production fleet has excess truck "
            "capacity relative to its loader fleet."
        )

    else:

        messages.append(
            "The loader and truck fleet are approximately "
            "balanced by the conventional match factor."
        )

    # --------------------------------------------------------
    # Capacity bottleneck
    # --------------------------------------------------------

    messages.append(
        "The installed capacity bottleneck is: "
        f"{result['capacity_bottleneck']}."
    )

    # --------------------------------------------------------
    # Balanced fleet comparison
    # --------------------------------------------------------

    if (
        result["balanced_trucks"]
        > result["trucks_required"]
    ):

        messages.append(
            f"Approximately {result['balanced_trucks']} trucks "
            "would be required for a match factor near 1, "
            f"compared with {result['trucks_required']} trucks "
            "required for the production target. Additional "
            "trucks are not automatically necessary."
        )

    return messages
