"""
MineOpsLab Material Library

IMPORTANT:
The values below are demonstration defaults for application
development. They are editable by the user and should not be
treated as authoritative material constants.

A sourced engineering material database will replace these
defaults in a later MineOpsLab build.
"""


MATERIAL_LIBRARY = {

    "Waste Rock": {
        "bank_density": 2.70,
        "swell_factor": 35.0,
    },

    "Iron Ore": {
        "bank_density": 3.00,
        "swell_factor": 30.0,
    },

    "Copper Ore": {
        "bank_density": 2.70,
        "swell_factor": 30.0,
    },

    "Gold Ore": {
        "bank_density": 2.70,
        "swell_factor": 30.0,
    },

    "Coal": {
        "bank_density": 1.30,
        "swell_factor": 25.0,
    },

    "Limestone": {
        "bank_density": 2.50,
        "swell_factor": 35.0,
    },

    "Sand": {
        "bank_density": 1.70,
        "swell_factor": 12.0,
    },

    "Gravel": {
        "bank_density": 1.90,
        "swell_factor": 12.0,
    },

    "Custom Material": {
        "bank_density": 2.50,
        "swell_factor": 30.0,
    },
}


def get_material_names():
    """
    Return the names of materials available in the library.
    """

    return list(MATERIAL_LIBRARY.keys())


def get_material_properties(material_name):
    """
    Return the default properties for a selected material.
    """

    if material_name not in MATERIAL_LIBRARY:
        raise ValueError(
            f"Material '{material_name}' is not available "
            "in the MineOpsLab material library."
        )

    return MATERIAL_LIBRARY[material_name].copy()