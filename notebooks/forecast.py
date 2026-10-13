"""Forecast 2026 energy, cost and carbon per region (run in a SageMaker notebook).
Reads the Athena-built monthly Parquet from S3 and writes results back to S3."""
import io
import boto3
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

BUCKET = "YOUR-BUCKET-NAME"
REGION = "ap-southeast-2"
s3 = boto3.client("s3", region_name=REGION)

objs = s3.list_objects_v2(Bucket=BUCKET, Prefix="processed/monthly_summary/")
frames = [pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()))
          for o in objs.get("Contents", []) if o["Size"] > 0]
df = pd.concat(frames)
df["region"] = df["region"].str.replace('"', "")
df = df.sort_values(["region", "month"]).reset_index(drop=True)

df["month_dt"] = pd.to_datetime(df["month"] + "-01")
metrics = ["total_kwh", "total_cost_usd", "total_carbon_kg"]
future_months = pd.date_range("2026-01-01", periods=12, freq="MS")

results = []
for region, g in df.groupby("region"):
    g = g.sort_values("month_dt").reset_index(drop=True)
    t = np.arange(len(g)).reshape(-1, 1)
    t_future = np.arange(len(g), len(g) + 12).reshape(-1, 1)
    out = pd.DataFrame({"month": future_months.strftime("%Y-%m"), "region": region})
    for m in metrics:
        out[m] = LinearRegression().fit(t, g[m]).predict(t_future).round(0)
    out["type"] = "forecast"
    results.append(out)

forecast = pd.concat(results, ignore_index=True)
actual = df[["month", "region"] + metrics].copy()
actual["type"] = "actual"
final = pd.concat([actual, forecast], ignore_index=True).sort_values(["region", "month"])

final.to_csv("forecast_results.csv", index=False)
s3.upload_file("forecast_results.csv", BUCKET, "processed/forecast/forecast_results.csv")
print(final.shape, "uploaded")
