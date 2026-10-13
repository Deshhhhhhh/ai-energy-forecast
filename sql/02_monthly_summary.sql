CREATE TABLE ai_energy_db.monthly_summary
WITH (format = 'PARQUET',
      external_location = 's3://YOUR-BUCKET-NAME/processed/monthly_summary/') AS
SELECT
  substr(replace(timestamp, '"', ''), 1, 7) AS month,
  region,
  ROUND(AVG(gpus_in_use), 1) AS avg_gpus,
  ROUND(SUM(energy_kwh), 0) AS total_kwh,
  ROUND(SUM(energy_cost_usd), 0) AS total_cost_usd,
  ROUND(SUM(carbon_kg), 0) AS total_carbon_kg
FROM ai_energy_db.gpu_usage
GROUP BY 1, 2;
