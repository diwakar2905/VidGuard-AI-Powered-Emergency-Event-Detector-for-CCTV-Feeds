def classify_emergency(events):
    emergencies = []
    for event in events:
        label = event.get("label", "")
        if label in ["large_motion", "fire_detected", "no_motion_long", "water_leak_detected"]:
            emergencies.append({
                "label": label,
                "timestamp": event.get("timestamp", "Unknown"),
                "confidence": event.get("score", 0.0)
            })
    return emergencies
