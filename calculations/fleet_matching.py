import math


def calculate_fleet_matching(
    truck_payload_t,
    bucket_payload_t,
    loader_cycle_time_sec,
    non_loading_cycle_time_min,
    required_production_tph,
    truck_mpi,
    loaders_required,
    loader_effective_productivity_tph,
):
    """
    Integrate the selected loading and haulage systems.

    The function calculates:

    1. Loader passes required per truck
    2. Truck loading time
    3. Complete truck cycle time
    4. Theoretical truck productivity
    5. MPI-adjusted effective truck productivity
    6. Production-based truck fleet requirement
    7. Installed loading and haulage capacities
    8. Integrated system capacity
    9. Conventional loader-truck Match Factor
    10. Balanced truck fleet requirement
    11. Capacity bottleneck

    MineOpsLab productivity framework
    ----------------------------------

    Effective Truck Productivity
        = Theoretical Truck Productivity x Truck MPI

    Conventional Match Factor
        = (N_trucks x T_loading)
          / (N_loaders x T_truck_cycle)

    A Match Factor close to 1 indicates an approximately
    balanced loader-truck fleet.

    The production truck requirement and balanced truck
    requirement answer two different engineering questions:

    Production trucks:
        How many trucks are required to satisfy the mine
        production target?

    Balanced trucks:
        How many trucks are approximately required to achieve
        a loader-truck Match Factor of 1.0?

    Parameters
    ----------
    truck_payload_t : float
        Rated truck payload in tonnes.

    bucket_payload_t : float
        Effective loader bucket payload in tonnes.

    loader_cycle_time_sec : float
        Loader bucket cycle time in seconds.

    non_loading_cycle_time_min : float
        Truck cycle time excluding loading, in minutes.

    required_production_tph : float
        Required mine production rate in tonnes per hour.

    truck_mpi : float
        Truck Mine Productivity Index expressed as a decimal.

    loaders_required : int
        Number of loaders installed.

    loader_effective_productivity_tph : float
        MPI-adjusted effective productivity of one loader,
        in tonnes per hour.

    Returns
    -------
    dict
        Integrated loader-truck fleet matching results.
    """

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if truck_payload_t <= 0:
        raise ValueError(
            "Truck payload must be greater than zero."
        )

    if bucket_payload_t <= 0:
        raise ValueError(
            "Bucket payload must be greater than zero."
        )

    if loader_cycle_time_sec <= 0:
        raise ValueError(
            "Loader cycle time must be greater than zero."
        )

    if non_loading_cycle_time_min < 0:
        raise ValueError(
            "Non-loading truck cycle time cannot be negative."
        )

    if required_production_tph < 0:
        raise ValueError(
            "Required production cannot be negative."
        )

    if not 0 < truck_mpi <= 1:
        raise ValueError(
            "Truck MPI must be greater than 0 "
            "and not exceed 1."
        )

    if loaders_required < 0:
        raise ValueError(
            "Number of loaders cannot be negative."
        )

    if loader_effective_productivity_tph <= 0:
        raise ValueError(
            "Loader effective productivity must be "
            "greater than zero."
        )


    # ========================================================
    # 1. EXACT LOADER PASSES PER TRUCK
    # ========================================================

    exact_passes = (
        truck_payload_t
        / bucket_payload_t
    )


    # ========================================================
    # 2. OPERATIONAL LOADER PASSES PER TRUCK
    #
    # Fractional loading passes are not operationally
    # possible. The exact requirement is therefore rounded
    # upward to the next whole loader pass.
    # ========================================================

    passes_per_truck = math.ceil(
        exact_passes
    )


    # ========================================================
    # 3. FINAL PASS REQUIREMENT
    #
    # The final loader pass may only require part of the
    # available bucket payload.
    # ========================================================

    full_passes_before_final = max(
        passes_per_truck - 1,
        0,
    )

    payload_before_final_pass = (
        full_passes_before_final
        * bucket_payload_t
    )

    final_pass_payload_t = max(
        truck_payload_t
        - payload_before_final_pass,
        0.0,
    )

    final_pass_fill_fraction = min(
        final_pass_payload_t
        / bucket_payload_t,
        1.0,
    )


    # ========================================================
    # 4. LOADER CYCLE TIME IN MINUTES
    # ========================================================

    loader_cycle_time_min = (
        loader_cycle_time_sec
        / 60.0
    )


    # ========================================================
    # 5. TRUCK LOADING TIME
    #
    # Loading time is calculated from the number of complete
    # loader cycles required to fill the truck.
    # ========================================================

    truck_loading_time_min = (
        passes_per_truck
        * loader_cycle_time_min
    )


    # ========================================================
    # 6. COMPLETE TRUCK CYCLE TIME
    #
    # Complete cycle =
    #
    # Loading
    # + Loaded haul
    # + Spotting
    # + Dumping
    # + Empty return
    #
    # The Haulage module already combines the non-loading
    # components.
    # ========================================================

    complete_cycle_time_min = (
        truck_loading_time_min
        + non_loading_cycle_time_min
    )


    # ========================================================
    # 7. THEORETICAL TRIPS PER HOUR
    # ========================================================

    theoretical_trips_per_hour = (
        60.0
        / complete_cycle_time_min
    )


    # ========================================================
    # 8. THEORETICAL TRUCK PRODUCTIVITY
    # ========================================================

    theoretical_truck_productivity_tph = (
        theoretical_trips_per_hour
        * truck_payload_t
    )


    # ========================================================
    # 9. EFFECTIVE TRUCK PRODUCTIVITY
    #
    # MineOpsLab productivity framework:
    #
    # P_effective = P_theoretical x MPI_T
    #
    # Availability, Performance and Utilization are already
    # incorporated within Truck MPI and must not be applied
    # again here.
    # ========================================================

    effective_truck_productivity_tph = (
        theoretical_truck_productivity_tph
        * truck_mpi
    )


    # ========================================================
    # 10. TRUCK PRODUCTIVITY LOSS
    # ========================================================

    truck_productivity_loss_tph = (
        theoretical_truck_productivity_tph
        - effective_truck_productivity_tph
    )


    # ========================================================
    # 11. EFFECTIVE TRIPS PER HOUR
    #
    # This is a productivity-equivalent indicator obtained
    # by applying Truck MPI to the theoretical trip rate.
    # ========================================================

    effective_trips_per_hour = (
        theoretical_trips_per_hour
        * truck_mpi
    )


    # ========================================================
    # 12. PRODUCTION-BASED TRUCK REQUIREMENT
    #
    # This answers:
    #
    # How many trucks are required to satisfy the production
    # target?
    # ========================================================

    if required_production_tph == 0:

        exact_trucks_required = 0.0
        trucks_required = 0

    else:

        exact_trucks_required = (
            required_production_tph
            / effective_truck_productivity_tph
        )

        trucks_required = math.ceil(
            exact_trucks_required
        )


    # ========================================================
    # 13. INSTALLED TRUCK CAPACITY
    #
    # Installed haulage capacity is based on the production
    # fleet calculated above.
    # ========================================================

    installed_truck_capacity_tph = (
        trucks_required
        * effective_truck_productivity_tph
    )


    # ========================================================
    # 14. TRUCK CAPACITY SURPLUS
    # ========================================================

    truck_capacity_surplus_tph = (
        installed_truck_capacity_tph
        - required_production_tph
    )


    # ========================================================
    # 15. INSTALLED TRUCK CAPACITY UTILIZATION
    #
    # This represents how much of the installed effective
    # haulage capacity is required to satisfy the production
    # target.
    #
    # It is NOT the Utilization component used in Truck MPI.
    # ========================================================

    if installed_truck_capacity_tph > 0:

        truck_capacity_utilization = (
            required_production_tph
            / installed_truck_capacity_tph
        )

    else:

        truck_capacity_utilization = 0.0


    # ========================================================
    # 16. INSTALLED LOADER CAPACITY
    # ========================================================

    installed_loader_capacity_tph = (
        loaders_required
        * loader_effective_productivity_tph
    )


    # ========================================================
    # 17. SYSTEM CAPACITY
    #
    # The integrated material handling system cannot
    # sustainably exceed the capacity of its limiting
    # subsystem.
    # ========================================================

    system_capacity_tph = min(
        installed_loader_capacity_tph,
        installed_truck_capacity_tph,
    )


    # ========================================================
    # 18. SYSTEM CAPACITY BALANCE
    #
    # Positive value = capacity surplus
    # Negative value = capacity shortfall
    # ========================================================

    system_capacity_balance_tph = (
        system_capacity_tph
        - required_production_tph
    )


    # ========================================================
    # 19. SYSTEM CAPACITY UTILIZATION
    # ========================================================

    if system_capacity_tph > 0:

        system_capacity_utilization = (
            required_production_tph
            / system_capacity_tph
        )

    else:

        system_capacity_utilization = 0.0


    # ========================================================
    # 20. CONVENTIONAL MATCH FACTOR
    #
    #                  N_T x T_loading
    # Match Factor = -------------------
    #                  N_L x T_cycle
    #
    # where:
    #
    # N_T = number of production trucks
    # N_L = number of loaders
    # T_loading = loading time per truck
    # T_cycle = complete truck cycle time
    #
    # Interpretation:
    #
    # MF < 1
    #     Excess loader capacity relative to the truck fleet.
    #     Loader idle or waiting time may occur.
    #
    # MF approximately 1
    #     Loader and truck fleet are approximately matched.
    #
    # MF > 1
    #     Excess truck capacity relative to the loader fleet.
    #     Truck queueing or waiting may occur.
    # ========================================================

    if (
        loaders_required > 0
        and complete_cycle_time_min > 0
    ):

        match_factor = (
            trucks_required
            * truck_loading_time_min
        ) / (
            loaders_required
            * complete_cycle_time_min
        )

    else:

        match_factor = 0.0


    # ========================================================
    # 21. MATCH INTERPRETATION
    #
    # A +/- 5% tolerance is used around unity.
    # ========================================================

    match_tolerance = 0.05

    if match_factor == 0:

        match_status = "Not applicable"

    elif match_factor < (
        1.0 - match_tolerance
    ):

        match_status = "Excess loader capacity"

    elif match_factor > (
        1.0 + match_tolerance
    ):

        match_status = "Excess truck capacity"

    else:

        match_status = "Approximately balanced"


    # ========================================================
    # 22. BALANCED TRUCK FLEET
    #
    # This answers a different question from production fleet
    # sizing:
    #
    # How many trucks would approximately produce MF = 1?
    #
    # Starting from:
    #
    #              N_T x T_loading
    # MF = -------------------------------
    #          N_L x T_complete_cycle
    #
    # For MF = 1:
    #
    #              N_L x T_complete_cycle
    # N_T = --------------------------------
    #                    T_loading
    #
    # The exact value is retained for learning and analysis.
    # The operational value is rounded upward.
    # ========================================================

    if (
        loaders_required > 0
        and truck_loading_time_min > 0
    ):

        exact_balanced_trucks = (
            loaders_required
            * complete_cycle_time_min
            / truck_loading_time_min
        )

        balanced_trucks = math.ceil(
            exact_balanced_trucks
        )

    else:

        exact_balanced_trucks = 0.0
        balanced_trucks = 0


    # ========================================================
    # 23. MATCH FACTOR OF BALANCED WHOLE-TRUCK FLEET
    #
    # Because trucks are discrete units, rounding the exact
    # balanced requirement upward will not always produce
    # exactly MF = 1.
    #
    # This indicator shows the resulting Match Factor when
    # the rounded balanced fleet is used.
    # ========================================================

    if (
        loaders_required > 0
        and complete_cycle_time_min > 0
    ):

        balanced_fleet_match_factor = (
            balanced_trucks
            * truck_loading_time_min
        ) / (
            loaders_required
            * complete_cycle_time_min
        )

    else:

        balanced_fleet_match_factor = 0.0


    # ========================================================
    # 24. ADDITIONAL TRUCKS TO BALANCED FLEET
    #
    # This is a teaching and diagnostic indicator.
    #
    # It does NOT mean the additional trucks are required to
    # satisfy the production target.
    # ========================================================

    additional_trucks_to_balance = max(
        balanced_trucks
        - trucks_required,
        0,
    )


    # ========================================================
    # 25. CAPACITY BOTTLENECK
    #
    # This diagnosis is separate from Match Factor.
    #
    # Match Factor evaluates loader-truck interaction.
    #
    # Capacity bottleneck identifies which installed
    # subsystem has the lower effective capacity.
    # ========================================================

    tolerance = 1e-9

    if abs(
        installed_loader_capacity_tph
        - installed_truck_capacity_tph
    ) <= tolerance:

        capacity_bottleneck = (
            "Balanced capacity"
        )

    elif (
        installed_loader_capacity_tph
        < installed_truck_capacity_tph
    ):

        capacity_bottleneck = (
            "Loading system"
        )

    else:

        capacity_bottleneck = (
            "Haulage system"
        )


    # ========================================================
    # 26. LOADER-TO-TRUCK CAPACITY RATIO
    #
    # Ratio > 1:
    #     Installed loading capacity exceeds haulage capacity.
    #
    # Ratio < 1:
    #     Installed haulage capacity exceeds loading capacity.
    #
    # Ratio approximately 1:
    #     Installed subsystem capacities are similar.
    # ========================================================

    if installed_truck_capacity_tph > 0:

        loader_to_truck_capacity_ratio = (
            installed_loader_capacity_tph
            / installed_truck_capacity_tph
        )

    else:

        loader_to_truck_capacity_ratio = 0.0


    # ========================================================
    # 27. PRODUCTION FLEET ADEQUACY
    # ========================================================

    production_target_met = (
        system_capacity_tph
        >= required_production_tph
    )


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        # ----------------------------------------------------
        # Loader-truck compatibility
        # ----------------------------------------------------

        "exact_passes":
            exact_passes,

        "passes_per_truck":
            passes_per_truck,

        "final_pass_payload_t":
            final_pass_payload_t,

        "final_pass_fill_fraction":
            final_pass_fill_fraction,


        # ----------------------------------------------------
        # Loading time
        # ----------------------------------------------------

        "loader_cycle_time_min":
            loader_cycle_time_min,

        "truck_loading_time_min":
            truck_loading_time_min,


        # ----------------------------------------------------
        # Complete truck cycle
        # ----------------------------------------------------

        "complete_cycle_time_min":
            complete_cycle_time_min,


        # ----------------------------------------------------
        # Truck theoretical performance
        # ----------------------------------------------------

        "theoretical_trips_per_hour":
            theoretical_trips_per_hour,

        "theoretical_truck_productivity_tph":
            theoretical_truck_productivity_tph,


        # ----------------------------------------------------
        # Truck MPI
        # ----------------------------------------------------

        "truck_mpi":
            truck_mpi,


        # ----------------------------------------------------
        # Truck effective performance
        # ----------------------------------------------------

        "effective_trips_per_hour":
            effective_trips_per_hour,

        "effective_truck_productivity_tph":
            effective_truck_productivity_tph,

        "truck_productivity_loss_tph":
            truck_productivity_loss_tph,


        # ----------------------------------------------------
        # Production-based truck fleet
        # ----------------------------------------------------

        "exact_trucks_required":
            exact_trucks_required,

        "trucks_required":
            trucks_required,


        # ----------------------------------------------------
        # Installed truck capacity
        # ----------------------------------------------------

        "installed_truck_capacity_tph":
            installed_truck_capacity_tph,

        "truck_capacity_surplus_tph":
            truck_capacity_surplus_tph,

        "truck_capacity_utilization":
            truck_capacity_utilization,


        # ----------------------------------------------------
        # Installed loader capacity
        # ----------------------------------------------------

        "installed_loader_capacity_tph":
            installed_loader_capacity_tph,


        # ----------------------------------------------------
        # Integrated system
        # ----------------------------------------------------

        "system_capacity_tph":
            system_capacity_tph,

        "system_capacity_balance_tph":
            system_capacity_balance_tph,

        "system_capacity_utilization":
            system_capacity_utilization,

        "production_target_met":
            production_target_met,


        # ----------------------------------------------------
        # Current fleet matching
        # ----------------------------------------------------

        "match_factor":
            match_factor,

        "match_status":
            match_status,


        # ----------------------------------------------------
        # Balanced fleet
        # ----------------------------------------------------

        "exact_balanced_trucks":
            exact_balanced_trucks,

        "balanced_trucks":
            balanced_trucks,

        "balanced_fleet_match_factor":
            balanced_fleet_match_factor,

        "additional_trucks_to_balance":
            additional_trucks_to_balance,


        # ----------------------------------------------------
        # Capacity diagnosis
        # ----------------------------------------------------

        "capacity_bottleneck":
            capacity_bottleneck,

        "loader_to_truck_capacity_ratio":
            loader_to_truck_capacity_ratio,
    }