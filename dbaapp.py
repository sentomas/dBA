import streamlit as st
import numpy as np
import plotly.graph_objects as go

def calculate_L_plus(delta_L):
    if delta_L >= 10:
        return 0
    return 10 * np.log10(1 + 10 ** (-delta_L / 10))

def combine_SPL(Lp1, Lp2):
    louder = max(Lp1, Lp2)
    quieter = min(Lp1, Lp2)
    delta_L = louder - quieter
    L_plus = calculate_L_plus(delta_L)
    combined = louder + L_plus
    return combined, delta_L, L_plus

st.title("Sound Pressure Level (SPL) Addition Calculator")
st.markdown("""
This app calculates the combined SPL from multiple noise sources using standard acoustic procedures.
""")

spl_values = st.text_input("Enter SPL values (comma-separated, e.g. 90,85,88):", "90,85,88")

try:
    spl_list = [float(val.strip()) for val in spl_values.split(",") if val.strip().replace('.', '', 1).isdigit()]
    if len(spl_list) < 2:
        st.warning("Please enter at least two SPL values.")
    else:
        combined = spl_list[0]
        steps = []
        for i in range(1, len(spl_list)):
            combined, delta_L, L_plus = combine_SPL(combined, spl_list[i])
            steps.append((combined, delta_L, L_plus))

        st.subheader("Calculation Steps")
        for i, (result, delta, lplus) in enumerate(steps):
            st.write(f"Step {i+1}: ΔL = {delta:.2f} dB, L+ = {lplus:.2f} dB → Combined SPL = {result:.2f} dB")

        st.success(f"Final Combined SPL: {combined:.2f} dB")

        delta_range = np.linspace(0, 10, 100)
        lplus_values = [calculate_L_plus(d) for d in delta_range]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=delta_range, y=lplus_values, mode='lines', name='L+ vs ΔL'))
        fig.update_layout(title='ΔL vs L+ Chart', xaxis_title='ΔL (dB)', yaxis_title='L+ (dB)')

        st.plotly_chart(fig)

except ValueError:
    st.error("Invalid input. Please enter numeric SPL values separated by commas.")
