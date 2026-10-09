import streamlit as st


def show_coming_soon(
    icon,
    eyebrow,
    title,
    subtitle,
    description,
    features,
):

    st.markdown(
f"""<div class="mineops-page-header">
<div class="mineops-eyebrow">
{eyebrow}
</div>

<div class="mineops-page-title">
{icon} {title}
</div>

<div class="mineops-page-subtitle">
{subtitle}
</div>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
"""<div class="development-panel">
🚧 <strong>Module currently under development.</strong>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
f"""<div class="mineops-card">
<h3>{icon} {title}</h3>
<p>{description}</p>
</div>""",
        unsafe_allow_html=True,
    )

    st.write("")
    st.subheader("Planned Capabilities")

    midpoint = (len(features) + 1) // 2

    left_features = features[:midpoint]
    right_features = features[midpoint:]

    col1, col2 = st.columns(2)

    with col1:
        for feature in left_features:
            st.markdown(f"✓ **{feature}**")

    with col2:
        for feature in right_features:
            st.markdown(f"✓ **{feature}**")

    st.write("")

    st.caption(
        "This module will be activated as MineOpsLab development progresses."
    )