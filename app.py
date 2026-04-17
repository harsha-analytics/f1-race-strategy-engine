import streamlit as st

# Title
st.title("F1 Race Strategy Engine")

# Input
our_lap_times = st.text_input("Enter our lap times (comma separated)", "89.8,89.9,90.1,90.4,90.9,91.6,92.4,93.3")

rival_lap_times = st.text_input("Enter rival lap times", "90.1,90.2,90.4,90.7,91.1,91.6,92.0")

pit_loss = st.number_input("Pit Loss", value=15)
max_reasonable_laps = st.number_input("Max Reasonable Laps", value=10)

def compute_metrics(laptimes):
    prev = None
    high_deltas = []

    for lap in laptimes:
        if prev is None:
            delta = None
        else:
            delta = round(lap - prev, 2)
        prev = lap

        if delta is not None and delta > 0.3:
            high_deltas.append(delta)

    if len(high_deltas) > 0:
        avg_deg_rate = sum(high_deltas) / len(high_deltas)
        return avg_deg_rate
    else:
        return 0

if st.button("Run Strategy"):

    our_laps = [float(x) for x in our_lap_times.split(",")]
    rival_laps = [float(x) for x in rival_lap_times.split(",")]

    our_deg = compute_metrics(our_laps)
    rival_deg = compute_metrics(rival_laps)

    advantage = rival_deg - our_deg

    if advantage <= 0:
        decision = "STAY OUT"
        recovery = float("inf")
        confidence = "LOW"
    else:
        recovery = pit_loss / advantage

        if recovery <= 5 and advantage > 1:
            decision = "PIT"
            confidence = "VERY HIGH"
        elif recovery <= 8:
            decision = "PIT"
            confidence = "HIGH"
        elif recovery <= 10:
            decision = "STAY OUT"
            confidence = "MID"
        else:
            decision = "STAY OUT"
            confidence = "LOW"

    st.write(f"Decision: {decision}")
    st.write(f"Confidence: {confidence}")
    st.write(f"Recovery Laps: {recovery}")
