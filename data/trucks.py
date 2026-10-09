"""
MineOpsLab Truck Library

The current entries are development placeholders.

Verified manufacturer specifications will be added later.
The purpose of this file is to establish the equipment-library
architecture without mixing equipment specifications with
operating conditions.
"""


TRUCK_LIBRARY = {

    "Custom Truck": {
        "manufacturer": "Custom",
        "payload_t": 90.0,
    },

}


def get_truck_names():
    """
    Return all trucks currently available in the library.
    """

    return list(TRUCK_LIBRARY.keys())


def get_truck_properties(truck_name):
    """
    Return specifications for the selected truck.
    """

    if truck_name not in TRUCK_LIBRARY:
        raise ValueError(
            f"Truck '{truck_name}' is not available "
            "in the MineOpsLab truck library."
        )

    return TRUCK_LIBRARY[truck_name].copy()