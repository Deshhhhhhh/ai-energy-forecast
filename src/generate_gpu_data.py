"""Generate simulated hourly GPU usage, energy, cost and carbon data (2024-2025)."""
import numpy as np
import pandas as pd

np.random.seed(42)

dates = pd.date_range("2024-01-01", "2025-12-31 23:00", freq="h")
n = len(dates)

# Illustrative regional assumptions: electricity price (USD/kWh), carbon intensity (gCO2/kWh)
regions = {
    "ap-southeast-2": {"price": 0.12, "carbon": 540},
    "us-east-1":      {"price": 0.09, "carbon": 380},
    "eu-north-1":     {"price": 0.07, "carbon": 30},
    "ap-south-1":     {"price": 0.10, "carbon": 700},
}

GPU_KW = 0.7   # approx. power per H100-class GPU (kW)
PUE = 1.3      # data center overhead (cooling etc.)

frames = []
for region, info in regions.items():
    hour = dates.hour.to_numpy()
    dow = dates.dayofweek.to_numpy()
    days = np.arange(n) / 24

    growth = 1 + 0.0012 * days                      # AI demand growth
    daily = 1 + 0.35 * np.sin((hour - 8) / 24 * 2 * np.pi)
    weekly = np.where(dow < 5, 1.0, 0.7)
    noise = np.random.normal(1, 0.08, n)

    gpus_in_use = (200 * growth * daily * weekly * noise).clip(min=20).round()
    energy_kwh = gpus_in_use * GPU_KW * PUE
    peak = np.where((hour >= 9) & (hour <= 20), 1.25, 0.85)
    price_per_kwh = info["price"] * peak
    energy_cost = energy_kwh * price_per_kwh
    carbon_kg = energy_kwh * info["carbon"] / 1000

    frames.append(pd.DataFrame({
        "timestamp": dates,
        "region": region,
        "gpus_in_use": gpus_in_use.astype(int),
        "energy_kwh": energy_kwh.round(2),
        "price_per_kwh": price_per_kwh.round(4),
        "energy_cost_usd": energy_cost.round(2),
        "carbon_kg": carbon_kg.round(2),
    }))

result = pd.concat(frames, ignore_index=True)
result.to_csv("data/gpu_usage.csv", index=False)
print(result.shape)
print(result.head())
