SELECT
  replace(m.region, '"', '') AS region,
  ROUND(SUM(m.total_cost_usd) / SUM(m.total_kwh), 4) AS energy_cost_per_kwh,
  ROUND(SUM(m.total_carbon_kg) / SUM(m.total_kwh), 3) AS carbon_kg_per_kwh,
  MAX(p.on_demand_usd_per_gpu_hour) AS on_demand_per_gpu_hr,
  MAX(p.spot_usd_per_gpu_hour) AS spot_per_gpu_hr
FROM ai_energy_db.monthly_summary m
JOIN ai_energy_db.cloud_pricing p
  ON replace(m.region, '"', '') = replace(p.region, '"', '')
GROUP BY 1
ORDER BY spot_per_gpu_hr;
