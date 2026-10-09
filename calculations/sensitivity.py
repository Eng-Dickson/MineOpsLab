from calculations.haulage import (
    calculate_haulage_performance,
)

from calculations.fleet_matching import (
    calculate_fleet_matching,
)


def calculate_truck_performance_sensitivity(
    truck_payload_t,
    haul_distance_km,
    loaded_speed_kmh,
    empty_speed_kmh,
    spotting_time_min,
    dumping_time_min,
    truck_availability,
    truck_utilization,
    bucket_payload_t,
    loader_cycle_time_sec,
    required_production_tph,
    loaders_required,
    loader_effective_productivity_tph,
    performance_min,
    performance_max,
    performance_step,
    baseline_performance,
):
    """
    Perform sensitivity analysis on truck performance (PP).

    The analysis varies truck Performance while holding all
    other loading, haulage and production variables constant.

    For every test value, MineOpsLab re-runs the existing:

        Haulage Engine
              ↓
        Truck MPI
              ↓
        Fleet Matching Engine
              ↓
        Truck Productivity
              ↓
        Fleet Requirement
              ↓
        System Performance

    No haulage or fleet equations are duplicated here.

    Parameters
    ----------
    truck_payload_t : float
        Rated truck payload, tonnes.

    haul_distance_km : float
        One-way haul distance, kilometres.

    loaded_speed_kmh : float
        Average loaded truck speed, km/h.

    empty_speed_kmh : float
        Average empty return speed, km/h.

    spotting_time_min : float
        Truck spotting time at dump, minutes.

    dumping_time_min : float
        Truck dumping time, minutes.

    truck_availability : float
        Truck mechanical availability as a decimal.

    truck_utilization : float
        Truck utilization as a decimal.

    bucket_payload_t : float
        Effective loader bucket payload, tonnes.

    loader_cycle_time_sec : float
        Loader cycle time, seconds.

    required_production_tph : float
        Required mine production, tonnes per hour.

    loaders_required : int
        Installed loader fleet.

    loader_effective_productivity_tph : float
        Effective productivity of one loader, tonnes per hour.

    performance_min : float
        Minimum Truck PP to test, decimal.

    performance_max : float
        Maximum Truck PP to test, decimal.

    performance_step : float
        Truck PP increment, decimal.

    baseline_performance : float
        Current Truck PP, decimal.

    Returns
    -------
    dict
        Sensitivity results and baseline comparison.
    """

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if not 0 < performance_min <= 1:
        raise ValueError(
            "Minimum truck performance must be greater "
            "than 0 and not exceed 1."
        )

    if not 0 < performance_max <= 1:
        raise ValueError(
            "Maximum truck performance must be greater "
            "than 0 and not exceed 1."
        )

    if performance_min > performance_max:
        raise ValueError(
            "Minimum truck performance cannot exceed "
            "maximum truck performance."
        )

    if performance_step <= 0:
        raise ValueError(
            "Performance step must be greater than zero."
        )

    if performance_step > 1:
        raise ValueError(
            "Performance step cannot exceed 1."
        )

    if not 0 < baseline_performance <= 1:
        raise ValueError(
            "Baseline truck performance must be greater "
            "than 0 and not exceed 1."
        )


    # ========================================================
    # GENERATE TEST VALUES
    #
    # Floating-point increments are rounded to prevent values
    # such as 0.8500000000001 appearing in the analysis.
    # ========================================================

    performance_values = []

    current_value = performance_min

    while current_value <= (
        performance_max + 1e-9
    ):

        performance_values.append(
            round(current_value, 6)
        )

        current_value += performance_step


    # ========================================================
    # ENSURE BASELINE IS INCLUDED
    #
    # The current operating PP should appear in the analysis
    # even if it does not fall exactly on the selected step.
    # ========================================================

    if (
        performance_min
        <= baseline_performance
        <= performance_max
    ):

        baseline_exists = any(
            abs(
                value
                - baseline_performance
            ) < 1e-9
            for value in performance_values
        )

        if not baseline_exists:

            performance_values.append(
                round(
                    baseline_performance,
                    6,
                )
            )

            performance_values.sort()


    # ========================================================
    # SENSITIVITY ANALYSIS
    # ========================================================

    sensitivity_results = []

    for performance in performance_values:

        # ----------------------------------------------------
        # 1. RE-RUN HAULAGE ENGINE
        #
        # Only Truck PP changes.
        # ----------------------------------------------------

        haulage_result = (
            calculate_haulage_performance(
                truck_payload_t=(
                    truck_payload_t
                ),
                haul_distance_km=(
                    haul_distance_km
                ),
                loaded_speed_kmh=(
                    loaded_speed_kmh
                ),
                empty_speed_kmh=(
                    empty_speed_kmh
                ),
                spotting_time_min=(
                    spotting_time_min
                ),
                dumping_time_min=(
                    dumping_time_min
                ),
                truck_availability=(
                    truck_availability
                ),
                truck_performance=(
                    performance
                ),
                truck_utilization=(
                    truck_utilization
                ),
            )
        )


        # ----------------------------------------------------
        # 2. EXTRACT TRUCK MPI
        # ----------------------------------------------------

        truck_mpi = (
            haulage_result[
                "truck_mpi"
            ]
        )


        # ----------------------------------------------------
        # 3. RE-RUN FLEET MATCHING ENGINE
        # ----------------------------------------------------

        fleet_result = (
            calculate_fleet_matching(
                truck_payload_t=(
                    truck_payload_t
                ),
                bucket_payload_t=(
                    bucket_payload_t
                ),
                loader_cycle_time_sec=(
                    loader_cycle_time_sec
                ),
                non_loading_cycle_time_min=(
                    haulage_result[
                        "non_loading_cycle_time_min"
                    ]
                ),
                required_production_tph=(
                    required_production_tph
                ),
                truck_mpi=(
                    truck_mpi
                ),
                loaders_required=(
                    loaders_required
                ),
                loader_effective_productivity_tph=(
                    loader_effective_productivity_tph
                ),
            )
        )


        # ----------------------------------------------------
        # 4. IDENTIFY BASELINE
        # ----------------------------------------------------

        is_baseline = (
            abs(
                performance
                - baseline_performance
            )
            < 1e-9
        )


        # ----------------------------------------------------
        # 5. STORE SCENARIO RESULT
        # ----------------------------------------------------

        sensitivity_results.append(
            {
                "truck_performance":
                    performance,

                "truck_performance_percent":
                    performance * 100,

                "truck_mpi":
                    truck_mpi,

                "truck_mpi_percent":
                    truck_mpi * 100,

                "complete_cycle_time_min":
                    fleet_result[
                        "complete_cycle_time_min"
                    ],

                "theoretical_truck_productivity_tph":
                    fleet_result[
                        "theoretical_truck_productivity_tph"
                    ],

                "effective_truck_productivity_tph":
                    fleet_result[
                        "effective_truck_productivity_tph"
                    ],

                "exact_trucks_required":
                    fleet_result[
                        "exact_trucks_required"
                    ],

                "trucks_required":
                    fleet_result[
                        "trucks_required"
                    ],

                "balanced_trucks":
                    fleet_result[
                        "balanced_trucks"
                    ],

                "installed_truck_capacity_tph":
                    fleet_result[
                        "installed_truck_capacity_tph"
                    ],

                "system_capacity_tph":
                    fleet_result[
                        "system_capacity_tph"
                    ],

                "system_capacity_utilization":
                    fleet_result[
                        "system_capacity_utilization"
                    ],

                "match_factor":
                    fleet_result[
                        "match_factor"
                    ],

                "match_status":
                    fleet_result[
                        "match_status"
                    ],

                "capacity_bottleneck":
                    fleet_result[
                        "capacity_bottleneck"
                    ],

                "production_target_met":
                    fleet_result[
                        "production_target_met"
                    ],

                "is_baseline":
                    is_baseline,
            }
        )


    # ========================================================
    # FIND BASELINE RESULT
    # ========================================================

    baseline_result = None

    for result in sensitivity_results:

        if result["is_baseline"]:

            baseline_result = result
            break


    # ========================================================
    # FIND MINIMUM PP THAT MEETS PRODUCTION TARGET
    #
    # This gives the Analysis Lab its first diagnostic insight:
    #
    # What is the lowest tested Truck PP at which the selected
    # system still satisfies the production target?
    # ========================================================

    minimum_performance_meeting_target = None

    for result in sensitivity_results:

        if result["production_target_met"]:

            minimum_performance_meeting_target = (
                result["truck_performance"]
            )

            break


    # ========================================================
    # IDENTIFY FLEET-SIZE TRANSITIONS
    #
    # Example:
    #
    # 60% PP -> 5 trucks
    # 65% PP -> 5 trucks
    # 70% PP -> 4 trucks
    #
    # MineOpsLab records the point where the production fleet
    # requirement changes.
    # ========================================================

    fleet_transitions = []

    previous_trucks = None

    for result in sensitivity_results:

        current_trucks = (
            result["trucks_required"]
        )

        if previous_trucks is None:

            previous_trucks = (
                current_trucks
            )

            continue

        if current_trucks != previous_trucks:

            fleet_transitions.append(
                {
                    "truck_performance":
                        result[
                            "truck_performance"
                        ],

                    "truck_performance_percent":
                        result[
                            "truck_performance_percent"
                        ],

                    "previous_trucks":
                        previous_trucks,

                    "new_trucks":
                        current_trucks,
                }
            )

            previous_trucks = (
                current_trucks
            )


    # ========================================================
    # SUMMARY STATISTICS
    # ========================================================

    if sensitivity_results:

        lowest_mpi = min(
            result["truck_mpi"]
            for result
            in sensitivity_results
        )

        highest_mpi = max(
            result["truck_mpi"]
            for result
            in sensitivity_results
        )

        lowest_productivity = min(
            result[
                "effective_truck_productivity_tph"
            ]
            for result
            in sensitivity_results
        )

        highest_productivity = max(
            result[
                "effective_truck_productivity_tph"
            ]
            for result
            in sensitivity_results
        )

        minimum_trucks = min(
            result["trucks_required"]
            for result
            in sensitivity_results
        )

        maximum_trucks = max(
            result["trucks_required"]
            for result
            in sensitivity_results
        )

    else:

        lowest_mpi = 0.0
        highest_mpi = 0.0

        lowest_productivity = 0.0
        highest_productivity = 0.0

        minimum_trucks = 0
        maximum_trucks = 0


    # ========================================================
    # RETURN ANALYSIS
    # ========================================================

    return {

        "variable":
            "Truck Performance",

        "variable_symbol":
            "PP",

        "baseline_performance":
            baseline_performance,

        "baseline_performance_percent":
            baseline_performance * 100,

        "performance_min":
            performance_min,

        "performance_max":
            performance_max,

        "performance_step":
            performance_step,

        "results":
            sensitivity_results,

        "baseline_result":
            baseline_result,

        "minimum_performance_meeting_target":
            minimum_performance_meeting_target,

        "fleet_transitions":
            fleet_transitions,

        "lowest_mpi":
            lowest_mpi,

        "highest_mpi":
            highest_mpi,

        "lowest_productivity_tph":
            lowest_productivity,

        "highest_productivity_tph":
            highest_productivity,

        "minimum_trucks":
            minimum_trucks,

        "maximum_trucks":
            maximum_trucks,
    }