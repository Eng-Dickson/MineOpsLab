import math


def calculate_loader_performance(
    bucket_capacity_m3,
    fill_factor,
    loose_density,
    bucket_cycle_time_sec,
    availability,
    utilization,
    performance,
    required_production_tph,
):
    """
    Calculate loader productivity, Mine Productivity Index (MPI),
    and required loader fleet size.

    MineOpsLab productivity framework:

        MPI = Availability^0.3
              x Performance^0.5
              x Utilization^0.2

        Effective Productivity
            = Theoretical Productivity x MPI

    Parameters
    ----------
    bucket_capacity_m3 : float
        Rated bucket capacity, cubic metres.

    fill_factor : float
        Bucket fill factor expressed as a decimal.

    loose_density : float
        Loose bulk density, tonnes per cubic metre.

    bucket_cycle_time_sec : float
        Average loader bucket cycle time, seconds.

    availability : float
        Mechanical availability expressed as a decimal.

    utilization : float
        Loader utilization expressed as a decimal.

    performance : float
        Loader performance expressed as a decimal.

    required_production_tph : float
        Required material production rate, tonnes per hour.

    Returns
    -------
    dict
        Loader productivity, MPI and fleet-sizing results.
    """

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if bucket_capacity_m3 <= 0:
        raise ValueError(
            "Bucket capacity must be greater than zero."
        )

    if not 0 < fill_factor <= 1:
        raise ValueError(
            "Fill factor must be greater than 0 and not exceed 1."
        )

    if loose_density <= 0:
        raise ValueError(
            "Loose bulk density must be greater than zero."
        )

    if bucket_cycle_time_sec <= 0:
        raise ValueError(
            "Bucket cycle time must be greater than zero."
        )

    if not 0 < availability <= 1:
        raise ValueError(
            "Availability must be greater than 0 and not exceed 1."
        )

    if not 0 < utilization <= 1:
        raise ValueError(
            "Utilization must be greater than 0 and not exceed 1."
        )

    if not 0 < performance <= 1:
        raise ValueError(
            "Performance must be greater than 0 and not exceed 1."
        )

    if required_production_tph < 0:
        raise ValueError(
            "Required production cannot be negative."
        )


    # ========================================================
    # 1. EFFECTIVE BUCKET VOLUME
    # ========================================================

    effective_bucket_volume_m3 = (
        bucket_capacity_m3
        * fill_factor
    )


    # ========================================================
    # 2. EFFECTIVE BUCKET PAYLOAD
    # ========================================================

    bucket_payload_t = (
        effective_bucket_volume_m3
        * loose_density
    )


    # ========================================================
    # 3. THEORETICAL BUCKET CYCLES PER HOUR
    # ========================================================

    theoretical_cycles_per_hour = (
        3600.0
        / bucket_cycle_time_sec
    )


    # ========================================================
    # 4. THEORETICAL LOADER PRODUCTIVITY
    # ========================================================

    theoretical_productivity_tph = (
        bucket_payload_t
        * theoretical_cycles_per_hour
    )


    # ========================================================
    # 5. LOADER MINE PRODUCTIVITY INDEX
    #
    # MPI = Av^0.3 x PP^0.5 x U^0.2
    # ========================================================

    mpi = (
        (availability ** 0.3)
        * (performance ** 0.5)
        * (utilization ** 0.2)
    )


    # ========================================================
    # 6. EFFECTIVE LOADER PRODUCTIVITY
    #
    # Effective Productivity
    # = Theoretical Productivity x MPI
    # ========================================================

    effective_productivity_tph = (
        theoretical_productivity_tph
        * mpi
    )


    # ========================================================
    # 7. REQUIRED LOADERS
    # ========================================================

    if required_production_tph == 0:

        exact_loaders_required = 0.0
        loaders_required = 0

    else:

        exact_loaders_required = (
            required_production_tph
            / effective_productivity_tph
        )

        loaders_required = math.ceil(
            exact_loaders_required
        )


    # ========================================================
    # 8. INSTALLED LOADING CAPACITY
    # ========================================================

    installed_capacity_tph = (
        loaders_required
        * effective_productivity_tph
    )


    # ========================================================
    # 9. CAPACITY SURPLUS OR SHORTFALL
    # ========================================================

    capacity_surplus_tph = (
        installed_capacity_tph
        - required_production_tph
    )


    # ========================================================
    # 10. INSTALLED CAPACITY UTILIZATION
    #
    # This describes how much of the installed effective
    # loading capacity is required to meet the production
    # target. It is different from equipment utilization U.
    # ========================================================

    if installed_capacity_tph > 0:

        installed_capacity_utilization = (
            required_production_tph
            / installed_capacity_tph
        )

    else:

        installed_capacity_utilization = 0.0


    # ========================================================
    # 11. PRODUCTIVITY LOSS
    #
    # Difference between ideal theoretical productivity and
    # MPI-adjusted effective productivity.
    # ========================================================

    productivity_loss_tph = (
        theoretical_productivity_tph
        - effective_productivity_tph
    )


    # ========================================================
    # 12. PRODUCTIVITY RETENTION
    #
    # Under the MineOpsLab framework, MPI is the fraction of
    # theoretical productivity retained under the specified
    # availability, performance and utilization conditions.
    # ========================================================

    productivity_retention = mpi


    # ========================================================
    # 13. MPI COMPONENT CONTRIBUTIONS
    #
    # These are retained separately so future analysis modules
    # can examine sensitivity to Av, PP and U.
    # ========================================================

    availability_component = (
        availability ** 0.3
    )

    performance_component = (
        performance ** 0.5
    )

    utilization_component = (
        utilization ** 0.2
    )


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        # Bucket characteristics
        "effective_bucket_volume_m3":
            effective_bucket_volume_m3,

        "bucket_payload_t":
            bucket_payload_t,

        # Theoretical performance
        "theoretical_cycles_per_hour":
            theoretical_cycles_per_hour,

        "theoretical_productivity_tph":
            theoretical_productivity_tph,

        # MPI inputs
        "availability":
            availability,

        "utilization":
            utilization,

        "performance":
            performance,

        # MPI components
        "availability_component":
            availability_component,

        "performance_component":
            performance_component,

        "utilization_component":
            utilization_component,

        # Mine Productivity Index
        "mpi":
            mpi,

        # Effective performance
        "effective_productivity_tph":
            effective_productivity_tph,

        "productivity_loss_tph":
            productivity_loss_tph,

        "productivity_retention":
            productivity_retention,

        # Fleet sizing
        "exact_loaders_required":
            exact_loaders_required,

        "loaders_required":
            loaders_required,

        # Installed capacity
        "installed_capacity_tph":
            installed_capacity_tph,

        "capacity_surplus_tph":
            capacity_surplus_tph,

        "installed_capacity_utilization":
            installed_capacity_utilization,
    }