
our_lap_times = [89.8, 89.9, 90.1, 90.4, 90.9, 91.6, 92.4, 93.3]

rivals = {
    "VER": [90.1, 90.2, 90.4, 90.7, 91.1, 91.6, 92.0],
    "NOR": [89.9, 90.0, 90.1, 90.3, 90.6, 91.0, 91.4],
    "HAM": [90.3, 90.4, 90.6, 90.9, 91.3, 91.9, 92.6]
}

pit_loss = 15
max_reasonable_laps = 10

def compute_metrics(laptimes):
    prev=None
    high_deltas=[]

    for lap in laptimes:
        if prev is None:
            delta=None
        else:
            delta=round(lap-prev,2)
        prev=lap

        if delta is not None and delta > 0.3:
            high_deltas.append(delta)
    
    if len(high_deltas) > 0:
        avg_deg_rate=sum(high_deltas) / len(high_deltas)
    else:
        avg_deg_rate = 0
    return avg_deg_rate

our_deg_rate = compute_metrics(our_lap_times)

best_target = None
best_recovery = float("inf")

for driver,laps in rivals.items():
    rival_deg_rate = compute_metrics(laps)

    per_lap_advantage = round(rival_deg_rate - our_deg_rate, 2)

    if per_lap_advantage <= 0:
        recovery_laps = float("inf")
        decision = "STAY OUT"
    else:
        recovery_laps = round(pit_loss / per_lap_advantage ,2)

        if recovery_laps <= max_reasonable_laps:
            decision = "PIT"
        else:
            decision ="STAY OUT"
    
    if recovery_laps < best_recovery:
        best_recovery = recovery_laps
        best_target = driver

    if per_lap_advantage <= 0:
        confidence = "LOW"
    elif recovery_laps <= 5 and per_lap_advantage > 1:
        confidence = "VERY HIGH"
    elif recovery_laps <= 8:
        confidence = "HIGH"
    elif recovery_laps <= 10:
        confidence = "MID"
    else:
        confidence = "LOW"
    

    #print(f"\nDriver: {driver}")
    #print("Our Degradation Rate :", round(our_deg_rate,2))
   # print(f"Rival Deg Rate: {round(rival_deg_rate,2)}")
    #print(f"Advantage: {per_lap_advantage}")
    #print(f"Recovery Laps: {recovery_laps}")
    #print(f"Decision: {decision}  (Confidence: {confidence})")

    print(f"{driver} -> {decision} (confidence: {confidence}) | Advanatge: {per_lap_advantage} | Recovery: {recovery_laps}")

if best_recovery <= max_reasonable_laps:
    print(f"\nBest Target: {best_target} (Recovery: {best_recovery})")
    print(f"Recommended Action -> PIT")

else:
    print("\nNo Viable undercut target")
    print("Recommended Action -> STAY OUT ")