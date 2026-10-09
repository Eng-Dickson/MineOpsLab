def calculate_haulage_performance(
    truck_payload_t,
    haul_distance_km,
    loaded_speed_kmh,
    empty_speed_kmh,
    spotting_time_min,
    dumping_time_min,
    truck_availability,
    truck_performance,
    truck_utilization,
):
    """
    Calculate independent haulage performance and Truck MPI.

    Loading time is deliberately excluded from this module
    because it depends on the selected loader-truck
    combination. Loading time is calculated in the
    Fleet Matching module.

    Mine Productivity Index:

        MPI = Av^0.3 x PP^0.5 x U^0.2

    Parameters
    ----------
    truck_payload_t : float
        Rated truck payload in tonnes.

    haul_distance_km : float
        One-way haul distance in kilometres.

    loaded_speed_kmh : float
        Average loaded truck speed in km/h.

    empty_speed_kmh : float
        Average empty return speed in km/h.

    spotting_time_min : float
        Spotting time at the dumping point in minutes.

    dumping_time_min : float
        Truck dumping time in minutes.

    truck_availability : float
        Mechanical availability expressed as a decimal.

    truck_performance : float
        Truck performance expressed as a decimal.

    truck_utilization : float
        Truck utilization expressed as a decimal.

    Returns
    -------
    dict
        Haulage performance, operating factors and Truck MPI.
    """

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if truck_payload_t <= 0:
        raise ValueError(
            "Truck payload must be greater than zero."
        )

    if haul_distance_km <= 0:
        raise ValueError(
            "Haul distance must be greater than zero."
        )

    if loaded_speed_kmh <= 0:
        raise ValueError(
            "Loaded speed must be greater than zero."
        )

    if empty_speed_kmh <= 0:
        raise ValueError(
            "Empty speed must be greater than zero."
        )

    if spotting_time_min < 0:
        raise ValueError(
            "Spotting time cannot be negative."
        )

    if dumping_time_min < 0:
        raise ValueError(
            "Dumping time cannot be negative."
        )

    if not 0 < truck_availability <= 1:
        raise ValueError(
            "Truck availability must be greater than 0 "
            "and not exceed 1."
        )

    if not 0 < truck_performance <= 1:
        raise ValueError(
            "Truck performance must be greater than 0 "
            "and not exceed 1."
        )

    if not 0 < truck_utilization <= 1:
        raise ValueError(
            "Truck utilization must be greater than 0 "
            "and not exceed 1."
        )


    # ========================================================
    # 1. LOADED HAUL TIME
    # ========================================================

    loaded_haul_time_min = (
        60.0
        * haul_distance_km
        / loaded_speed_kmh
    )


    # ========================================================
    # 2. EMPTY RETURN TIME
    # ========================================================

    empty_return_time_min = (
        60.0
        * haul_distance_km
        / empty_speed_kmh
    )


    # ========================================================
    # 3. ROUND-TRIP DISTANCE
    # ========================================================

    round_trip_distance_km = (
        2.0
        * haul_distance_km
    )


    # ========================================================
    # 4. TOTAL TRAVEL TIME
    # ========================================================

    total_travel_time_min = (
        loaded_haul_time_min
        + empty_return_time_min
    )


    # ========================================================
    # 5. DUMPING ACTIVITY TIME
    #
    # Includes truck positioning at the dump and the actual
    # dumping operation.
    # ========================================================

    dump_activity_time_min = (
        spotting_time_min
        + dumping_time_min
    )


    # ========================================================
    # 6. NON-LOADING TRUCK CYCLE TIME
    #
    # Loading is intentionally excluded.
    #
    # Complete truck cycle time is calculated later in the
    # Fleet Matching module once the selected loader is known.
    # ========================================================

    non_loading_cycle_time_min = (
        total_travel_time_min
        + dump_activity_time_min
    )


    # ========================================================
    # 7. MINE PRODUCTIVITY INDEX
    #
    # MPI = Av^0.3 x PP^0.5 x U^0.2
    #
    # Av = Availability
    # PP = Performance
    # U  = Utilization
    # ========================================================

    availability_component = (
        truck_availability ** 0.3
    )

    performance_component = (
        truck_performance ** 0.5
    )

    utilization_component = (
        truck_utilization ** 0.2
    )

    truck_mpi = (
        availability_component
        * performance_component
        * utilization_component
    )


    # ========================================================
    # 8. SIMPLE OPERATING FACTOR
    #
    # Retained as a diagnostic indicator.
    #
    # This value must NOT be applied again to productivity
    # where MPI is already being used.
    # ========================================================

    truck_operating_factor = (
        truck_availability
        * truck_utilization
    )


    # ========================================================
    # 9. TIME DISTRIBUTION
    #
    # Shows how the non-loading truck cycle is distributed
    # between haul, return, spotting and dumping activities.
    # ========================================================

    if non_loading_cycle_time_min > 0:

        loaded_haul_share = (
            loaded_haul_time_min
            / non_loading_cycle_time_min
        )

        empty_return_share = (
            empty_return_time_min
            / non_loading_cycle_time_min
        )

        spotting_share = (
            spotting_time_min
            / non_loading_cycle_time_min
        )

        dumping_share = (
            dumping_time_min
            / non_loading_cycle_time_min
        )

    else:

        loaded_haul_share = 0.0

        empty_return_share = 0.0

        spotting_share = 0.0

        dumping_share = 0.0


    # ========================================================
    # 10. TRAVEL SPEED RELATIONSHIP
    #
    # Diagnostic only.
    # ========================================================

    speed_ratio = (
        loaded_speed_kmh
        / empty_speed_kmh
    )


    # ========================================================
    # RETURN RESULTS
    #
    # Important operating inputs are deliberately returned
    # alongside calculated outputs.
    #
    # This allows downstream MineOpsLab modules such as:
    #
    # Sensitivity Analysis
    # Scenario Comparison
    # Economics
    # Optimization
    #
    # to reconstruct the current baseline scenario.
    # ========================================================

    return {

        # ----------------------------------------------------
        # Truck specification
        # ----------------------------------------------------

        "truck_payload_t":
            truck_payload_t,


        # ----------------------------------------------------
        # Haul profile inputs
        # ----------------------------------------------------

        "haul_distance_km":
            haul_distance_km,

        "loaded_speed_kmh":
            loaded_speed_kmh,

        "empty_speed_kmh":
            empty_speed_kmh,

        "round_trip_distance_km":
            round_trip_distance_km,


        # ----------------------------------------------------
        # Travel times
        # ----------------------------------------------------

        "loaded_haul_time_min":
            loaded_haul_time_min,

        "empty_return_time_min":
            empty_return_time_min,

        "total_travel_time_min":
            total_travel_time_min,


        # ----------------------------------------------------
        # Dumping cycle
        # ----------------------------------------------------

        "spotting_time_min":
            spotting_time_min,

        "dumping_time_min":
            dumping_time_min,

        "dump_activity_time_min":
            dump_activity_time_min,


        # ----------------------------------------------------
        # Independent haulage cycle
        # ----------------------------------------------------

        "non_loading_cycle_time_min":
            non_loading_cycle_time_min,


        # ----------------------------------------------------
        # Productivity factors
        # ----------------------------------------------------

        "truck_availability":
            truck_availability,

        "truck_performance":
            truck_performance,

        "truck_utilization":
            truck_utilization,


        # ----------------------------------------------------
        # MPI components
        # ----------------------------------------------------

        "availability_component":
            availability_component,

        "performance_component":
            performance_component,

        "utilization_component":
            utilization_component,

        "truck_mpi":
            truck_mpi,


        # ----------------------------------------------------
        # Diagnostic operating factor
        # ----------------------------------------------------

        "truck_operating_factor":
            truck_operating_factor,


        # ----------------------------------------------------
        # Cycle time distribution
        # ----------------------------------------------------

        "loaded_haul_share":
            loaded_haul_share,

        "empty_return_share":
            empty_return_share,

        "spotting_share":
            spotting_share,

        "dumping_share":
            dumping_share,


        # ----------------------------------------------------
        # Speed diagnostic
        # ----------------------------------------------------

        "speed_ratio":
            speed_ratio,
    }