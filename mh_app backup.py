import math
import streamlit as st

st.set_page_config(page_title="Material Handling Tool V1", layout="centered")

st.title("Material Handling Tool (Version 1)")
st.caption("Fleet sizing with loader inputs, outputs are trucks, production per shift, surplus")

# =========================
# SIDEBAR INPUTS
# =========================

st.sidebar.header("Loader inputs")

num_loaders = st.sidebar.number_input(
    "Number of loaders",
    min_value=1,
    value=1,
    step=1
)

B = st.sidebar.number_input(
    "Bucket capacity (tonnes)",
    min_value=0.1,
    value=15.0,
    step=0.5
)

F = st.sidebar.number_input(
    "Fill factor (0–1)",
    min_value=0.1,
    max_value=1.0,
    value=0.9,
    step=0.05
)

t_bucket_sec = st.sidebar.number_input(
    "Loader cycle time per bucket (seconds)",
    min_value=1.0,
    value=32.0,
    step=1.0
)

st.sidebar.header("Truck inputs")

Q = st.sidebar.number_input(
    "Truck payload (tonnes)",
    min_value=1.0,
    value=90.0,
    step=5.0
)

T_dump = st.sidebar.number_input(
    "Dumping and spotting time (minutes)",
    min_value=0.1,
    value=1.5,
    step=0.1
)

st.sidebar.header("Haulage inputs")

D = st.sidebar.number_input(
    "One-way haul distance (km)",
    min_value=0.1,
    value=3.0,
    step=0.1
)

V_l = st.sidebar.number_input(
    "Average speed loaded (km/h)",
    min_value=1.0,
    value=25.0,
    step=1.0
)

V_e = st.sidebar.number_input(
    "Average speed empty (km/h)",
    min_value=1.0,
    value=35.0,
    step=1.0
)

st.sidebar.header("Shift targets")

H = st.sidebar.number_input(
    "Shift duration (hours)",
    min_value=1.0,
    max_value=24.0,
    value=12.0,
    step=1.0
)

P_t = st.sidebar.number_input(
    "Production target (tonnes per shift)",
    min_value=0.0,
    value=15000.0,
    step=500.0
)

# =========================
# CALCULATIONS
# =========================

# Loader: passes and loading time for ONE loader
B_eff = B * F
if B_eff <= 0:
    st.error("Effective bucket capacity must be greater than 0.")
    st.stop()

passes = math.ceil(Q / B_eff)
t_bucket_min = t_bucket_sec / 60.0
T_load_single = passes * t_bucket_min  # minutes per truck for one loader

# Simplified multi-loader assumption (parallel loading)
T_load = T_load_single / num_loaders

# Travel times
t_haul = 60.0 * (D / V_l)
t_return = 60.0 * (D / V_e)

# Cycle time
T_cycle = t_haul + t_return + T_load + T_dump
if T_cycle <= 0:
    st.error("Total cycle time must be greater than 0.")
    st.stop()

# Production per truck per shift
trips_per_truck = (H * 60.0) / T_cycle
q_truck = trips_per_truck * Q
if q_truck <= 0:
    st.error("Production per truck must be greater than 0.")
    st.stop()

# Required trucks for target
N_req = (P_t / q_truck) if P_t > 0 else 0.0
N_fleet = math.ceil(N_req) if P_t > 0 else 0

# Achieved production per shift and surplus
P_achieved = q_truck * N_fleet
surplus = P_achieved - P_t

# =========================
# OUTPUTS (REDUCED)
# =========================

st.subheader("Key outputs")

c1, c2 = st.columns(2)
with c1:
    st.metric("Required number of trucks", f"{N_fleet}")
with c2:
    st.metric("Loaders (input)", f"{num_loaders}")

c3, c4 = st.columns(2)
with c3:
    st.metric("Production achieved (tonnes per shift)", f"{P_achieved:,.0f}")
with c4:
    st.metric("Surplus (tonnes per shift)", f"{surplus:,.0f}")

st.caption("Assumption: loading happens in parallel, so effective loading time per truck is divided by the number of loaders.")
