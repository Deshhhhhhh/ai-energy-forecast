"""Create an illustrative GPU instance price table by region."""
import pandas as pd

# Illustrative on-demand prices (USD/hour) for an 8x H100-class instance.
# Not official quotes. Verify against AWS pricing before citing.
rows = [
    ("ap-southeast-2", "p5.48xlarge", 8, 55.0, 0.35),
    ("us-east-1",      "p5.48xlarge", 8, 49.0, 0.40),
    ("eu-north-1",     "p5.48xlarge", 8, 52.0, 0.38),
    ("ap-south-1",     "p5.48xlarge", 8, 53.0, 0.30),
]
df = pd.DataFrame(rows, columns=["region", "instance_type", "gpus_per_instance",
                                 "on_demand_usd_per_hour", "spot_discount"])
df["spot_usd_per_hour"] = (df["on_demand_usd_per_hour"] * (1 - df["spot_discount"])).round(2)
df["on_demand_usd_per_gpu_hour"] = (df["on_demand_usd_per_hour"] / df["gpus_per_instance"]).round(2)
df["spot_usd_per_gpu_hour"] = (df["spot_usd_per_hour"] / df["gpus_per_instance"]).round(2)

df.to_csv("data/cloud_pricing.csv", index=False)
print(df)
