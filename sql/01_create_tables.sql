-- Replace YOUR-BUCKET-NAME with your S3 bucket. Run each statement separately in Athena.
CREATE EXTERNAL TABLE ai_energy_db.gpu_usage (
  `timestamp` string, region string, gpus_in_use int, energy_kwh double,
  price_per_kwh double, energy_cost_usd double, carbon_kg double
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION 's3://YOUR-BUCKET-NAME/raw/gpu_usage/'
TBLPROPERTIES ('skip.header.line.count'='1');

CREATE EXTERNAL TABLE ai_energy_db.cloud_pricing (
  region string, instance_type string, gpus_per_instance int,
  on_demand_usd_per_hour double, spot_discount double, spot_usd_per_hour double,
  on_demand_usd_per_gpu_hour double, spot_usd_per_gpu_hour double
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION 's3://YOUR-BUCKET-NAME/raw/pricing/'
TBLPROPERTIES ('skip.header.line.count'='1');
