def calculate_material_production(
    annual_production_target,
    operating_days_per_year,
    shifts_per_day,
    shift_duration_hours,
    bank_density,
    swell_factor_percent,
):
    """
    Calculate material properties and scheduled production requirements.

    Parameters
    ----------
    annual_production_target : float
        Annual material production target, tonnes/year.

    operating_days_per_year : int
        Scheduled operating days per year.

    shifts_per_day : int
        Number of scheduled production shifts per day.

    shift_duration_hours : float
        Duration of one scheduled shift, hours.

    bank_density : float
        In-situ material density, tonnes per bank cubic metre.

    swell_factor_percent : float
        Increase in material volume after excavation,
        expressed as a percentage.

    Returns
    -------
    dict
        Material and production calculations.
    """

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if annual_production_target < 0:
        raise ValueError(
            "Annual production target cannot be negative."
        )

    if operating_days_per_year <= 0:
        raise ValueError(
            "Operating days per year must be greater than zero."
        )

    if shifts_per_day <= 0:
        raise ValueError(
            "Shifts per day must be greater than zero."
        )

    if shift_duration_hours <= 0:
        raise ValueError(
            "Shift duration must be greater than zero."
        )

    if bank_density <= 0:
        raise ValueError(
            "Bank density must be greater than zero."
        )

    if swell_factor_percent < 0:
        raise ValueError(
            "Swell factor cannot be negative."
        )


    # ========================================================
    # MATERIAL CALCULATIONS
    # ========================================================

    swell_factor_decimal = (
        swell_factor_percent / 100.0
    )

    swell_multiplier = (
        1.0 + swell_factor_decimal
    )

    loose_density = (
        bank_density / swell_multiplier
    )


    # ========================================================
    # SCHEDULED OPERATING TIME
    # ========================================================

    shifts_per_year = (
        operating_days_per_year
        * shifts_per_day
    )

    scheduled_hours_per_day = (
        shifts_per_day
        * shift_duration_hours
    )

    scheduled_hours_per_year = (
        shifts_per_year
        * shift_duration_hours
    )


    # ========================================================
    # PRODUCTION REQUIREMENTS
    # ========================================================

    daily_production = (
        annual_production_target
        / operating_days_per_year
    )

    shift_production = (
        annual_production_target
        / shifts_per_year
    )

    hourly_production = (
        annual_production_target
        / scheduled_hours_per_year
    )


    # ========================================================
    # VOLUMETRIC PRODUCTION REQUIREMENT
    # ========================================================

    hourly_loose_volume = (
        hourly_production
        / loose_density
    )


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        "annual_production_target":
            annual_production_target,

        "operating_days_per_year":
            operating_days_per_year,

        "shifts_per_day":
            shifts_per_day,

        "shift_duration_hours":
            shift_duration_hours,

        "bank_density":
            bank_density,

        "swell_factor_percent":
            swell_factor_percent,

        "loose_density":
            loose_density,

        "shifts_per_year":
            shifts_per_year,

        "scheduled_hours_per_day":
            scheduled_hours_per_day,

        "scheduled_hours_per_year":
            scheduled_hours_per_year,

        "daily_production":
            daily_production,

        "shift_production":
            shift_production,

        "hourly_production":
            hourly_production,

        "hourly_loose_volume":
            hourly_loose_volume,
    }