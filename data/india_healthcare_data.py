import pandas as pd
import numpy as np

TOTAL_GAP = 6_500_000

AHP_CATEGORIES = {
    "Nurses & Midwives": {
        "current": 2_340_000,
        "required": 5_200_000,
        "gap": 2_860_000,
        "gap_percentage": 44.0,
        "avg_salary_inr": 420_000,
        "training_cost_inr": 350_000,
        "training_duration_years": 4,
        "attrition_rate": 0.12,
        "description": "General nurses, ANMs, staff nurses, midwives"
    },
    "Lab Technicians": {
        "current": 450_000,
        "required": 1_200_000,
        "gap": 750_000,
        "gap_percentage": 11.5,
        "avg_salary_inr": 360_000,
        "training_cost_inr": 280_000,
        "training_duration_years": 3,
        "attrition_rate": 0.08,
        "description": "Medical laboratory technicians, pathology assistants"
    },
    "Physiotherapists": {
        "current": 120_000,
        "required": 650_000,
        "gap": 530_000,
        "gap_percentage": 8.2,
        "avg_salary_inr": 480_000,
        "training_cost_inr": 400_000,
        "training_duration_years": 4.5,
        "attrition_rate": 0.10,
        "description": "Physical therapists, rehabilitation specialists"
    },
    "Pharmacists": {
        "current": 680_000,
        "required": 1_400_000,
        "gap": 720_000,
        "gap_percentage": 11.1,
        "avg_salary_inr": 400_000,
        "training_cost_inr": 320_000,
        "training_duration_years": 4,
        "attrition_rate": 0.09,
        "description": "Hospital pharmacists, clinical pharmacists"
    },
    "Radiographers": {
        "current": 85_000,
        "required": 450_000,
        "gap": 365_000,
        "gap_percentage": 5.6,
        "avg_salary_inr": 420_000,
        "training_cost_inr": 380_000,
        "training_duration_years": 3,
        "attrition_rate": 0.07,
        "description": "X-ray technicians, imaging specialists"
    },
    "Optometrists": {
        "current": 52_000,
        "required": 280_000,
        "gap": 228_000,
        "gap_percentage": 3.5,
        "avg_salary_inr": 450_000,
        "training_cost_inr": 350_000,
        "training_duration_years": 4,
        "attrition_rate": 0.06,
        "description": "Eye care professionals, vision specialists"
    },
    "Dental Hygienists": {
        "current": 38_000,
        "required": 320_000,
        "gap": 282_000,
        "gap_percentage": 4.3,
        "avg_salary_inr": 380_000,
        "training_cost_inr": 300_000,
        "training_duration_years": 3,
        "attrition_rate": 0.08,
        "description": "Dental assistants, oral health workers"
    },
    "Community Health Workers": {
        "current": 920_000,
        "required": 1_800_000,
        "gap": 880_000,
        "gap_percentage": 13.5,
        "avg_salary_inr": 240_000,
        "training_cost_inr": 150_000,
        "training_duration_years": 1,
        "attrition_rate": 0.15,
        "description": "ASHAs, health educators, community mobilizers"
    },
    "Medical Social Workers": {
        "current": 45_000,
        "required": 280_000,
        "gap": 235_000,
        "gap_percentage": 3.6,
        "avg_salary_inr": 350_000,
        "training_cost_inr": 250_000,
        "training_duration_years": 3,
        "attrition_rate": 0.10,
        "description": "Hospital social workers, counselors"
    },
    "Occupational Therapists": {
        "current": 18_000,
        "required": 180_000,
        "gap": 162_000,
        "gap_percentage": 2.5,
        "avg_salary_inr": 500_000,
        "training_cost_inr": 420_000,
        "training_duration_years": 4.5,
        "attrition_rate": 0.07,
        "description": "Rehabilitation specialists for daily living"
    },
    "Speech Therapists": {
        "current": 12_000,
        "required": 150_000,
        "gap": 138_000,
        "gap_percentage": 2.1,
        "avg_salary_inr": 480_000,
        "training_cost_inr": 400_000,
        "training_duration_years": 4,
        "attrition_rate": 0.06,
        "description": "Speech-language pathologists, audiologists"
    },
    "Nutritionists & Dietitians": {
        "current": 35_000,
        "required": 250_000,
        "gap": 215_000,
        "gap_percentage": 3.3,
        "avg_salary_inr": 420_000,
        "training_cost_inr": 280_000,
        "training_duration_years": 4,
        "attrition_rate": 0.08,
        "description": "Clinical dietitians, nutrition specialists"
    },
    "Emergency Medical Technicians": {
        "current": 65_000,
        "required": 400_000,
        "gap": 335_000,
        "gap_percentage": 5.2,
        "avg_salary_inr": 300_000,
        "training_cost_inr": 200_000,
        "training_duration_years": 2,
        "attrition_rate": 0.14,
        "description": "Paramedics, ambulance technicians"
    }
}

STATE_DATA = {
    "Uttar Pradesh": {
        "population": 231_502_578,
        "current_ahp": 285_000,
        "required_ahp": 925_000,
        "gap": 640_000,
        "urban_population_pct": 22.3,
        "rural_gap_pct": 78.5,
        "training_institutions": 145,
        "annual_graduates": 18_500,
        "lat": 26.8467,
        "lon": 80.9462,
        "region": "North"
    },
    "Maharashtra": {
        "population": 123_144_223,
        "current_ahp": 420_000,
        "required_ahp": 615_000,
        "gap": 195_000,
        "urban_population_pct": 45.2,
        "rural_gap_pct": 62.3,
        "training_institutions": 285,
        "annual_graduates": 42_000,
        "lat": 19.7515,
        "lon": 75.7139,
        "region": "West"
    },
    "Bihar": {
        "population": 119_520_000,
        "current_ahp": 142_000,
        "required_ahp": 598_000,
        "gap": 456_000,
        "urban_population_pct": 11.3,
        "rural_gap_pct": 89.2,
        "training_institutions": 68,
        "annual_graduates": 8_200,
        "lat": 25.0961,
        "lon": 85.3131,
        "region": "East"
    },
    "West Bengal": {
        "population": 99_609_303,
        "current_ahp": 285_000,
        "required_ahp": 498_000,
        "gap": 213_000,
        "urban_population_pct": 31.9,
        "rural_gap_pct": 71.4,
        "training_institutions": 156,
        "annual_graduates": 22_500,
        "lat": 22.9868,
        "lon": 87.8550,
        "region": "East"
    },
    "Madhya Pradesh": {
        "population": 82_232_000,
        "current_ahp": 165_000,
        "required_ahp": 412_000,
        "gap": 247_000,
        "urban_population_pct": 27.6,
        "rural_gap_pct": 76.8,
        "training_institutions": 98,
        "annual_graduates": 12_400,
        "lat": 23.2599,
        "lon": 77.4126,
        "region": "Central"
    },
    "Tamil Nadu": {
        "population": 77_841_267,
        "current_ahp": 385_000,
        "required_ahp": 390_000,
        "gap": 5_000,
        "urban_population_pct": 48.4,
        "rural_gap_pct": 45.2,
        "training_institutions": 312,
        "annual_graduates": 48_000,
        "lat": 11.1271,
        "lon": 78.6569,
        "region": "South"
    },
    "Rajasthan": {
        "population": 78_230_816,
        "current_ahp": 178_000,
        "required_ahp": 391_000,
        "gap": 213_000,
        "urban_population_pct": 24.9,
        "rural_gap_pct": 79.3,
        "training_institutions": 112,
        "annual_graduates": 14_200,
        "lat": 27.0238,
        "lon": 74.2179,
        "region": "North"
    },
    "Karnataka": {
        "population": 67_562_686,
        "current_ahp": 298_000,
        "required_ahp": 338_000,
        "gap": 40_000,
        "urban_population_pct": 38.6,
        "rural_gap_pct": 58.4,
        "training_institutions": 245,
        "annual_graduates": 35_500,
        "lat": 15.3173,
        "lon": 75.7139,
        "region": "South"
    },
    "Gujarat": {
        "population": 63_872_399,
        "current_ahp": 252_000,
        "required_ahp": 320_000,
        "gap": 68_000,
        "urban_population_pct": 42.6,
        "rural_gap_pct": 54.6,
        "training_institutions": 178,
        "annual_graduates": 24_800,
        "lat": 22.2587,
        "lon": 71.1924,
        "region": "West"
    },
    "Andhra Pradesh": {
        "population": 53_903_393,
        "current_ahp": 218_000,
        "required_ahp": 270_000,
        "gap": 52_000,
        "urban_population_pct": 33.5,
        "rural_gap_pct": 65.8,
        "training_institutions": 165,
        "annual_graduates": 21_200,
        "lat": 15.9129,
        "lon": 79.7400,
        "region": "South"
    },
    "Telangana": {
        "population": 37_220_000,
        "current_ahp": 165_000,
        "required_ahp": 186_000,
        "gap": 21_000,
        "urban_population_pct": 39.0,
        "rural_gap_pct": 52.4,
        "training_institutions": 142,
        "annual_graduates": 18_500,
        "lat": 18.1124,
        "lon": 79.0193,
        "region": "South"
    },
    "Odisha": {
        "population": 45_429_399,
        "current_ahp": 124_000,
        "required_ahp": 227_000,
        "gap": 103_000,
        "urban_population_pct": 16.7,
        "rural_gap_pct": 82.6,
        "training_institutions": 72,
        "annual_graduates": 9_800,
        "lat": 20.9517,
        "lon": 85.0985,
        "region": "East"
    },
    "Kerala": {
        "population": 35_330_888,
        "current_ahp": 195_000,
        "required_ahp": 176_000,
        "gap": -19_000,
        "urban_population_pct": 47.7,
        "rural_gap_pct": 38.2,
        "training_institutions": 198,
        "annual_graduates": 28_500,
        "lat": 10.8505,
        "lon": 76.2711,
        "region": "South"
    },
    "Jharkhand": {
        "population": 38_593_948,
        "current_ahp": 85_000,
        "required_ahp": 193_000,
        "gap": 108_000,
        "urban_population_pct": 24.0,
        "rural_gap_pct": 84.3,
        "training_institutions": 45,
        "annual_graduates": 5_800,
        "lat": 23.6102,
        "lon": 85.2799,
        "region": "East"
    },
    "Assam": {
        "population": 35_607_039,
        "current_ahp": 78_000,
        "required_ahp": 178_000,
        "gap": 100_000,
        "urban_population_pct": 14.1,
        "rural_gap_pct": 86.5,
        "training_institutions": 48,
        "annual_graduates": 6_200,
        "lat": 26.2006,
        "lon": 92.9376,
        "region": "Northeast"
    },
    "Punjab": {
        "population": 30_452_000,
        "current_ahp": 145_000,
        "required_ahp": 152_000,
        "gap": 7_000,
        "urban_population_pct": 37.5,
        "rural_gap_pct": 48.6,
        "training_institutions": 125,
        "annual_graduates": 16_500,
        "lat": 31.1471,
        "lon": 75.3412,
        "region": "North"
    },
    "Chhattisgarh": {
        "population": 29_436_231,
        "current_ahp": 68_000,
        "required_ahp": 147_000,
        "gap": 79_000,
        "urban_population_pct": 23.2,
        "rural_gap_pct": 81.4,
        "training_institutions": 52,
        "annual_graduates": 6_800,
        "lat": 21.2787,
        "lon": 81.8661,
        "region": "Central"
    },
    "Haryana": {
        "population": 28_672_000,
        "current_ahp": 112_000,
        "required_ahp": 143_000,
        "gap": 31_000,
        "urban_population_pct": 34.9,
        "rural_gap_pct": 58.7,
        "training_institutions": 95,
        "annual_graduates": 12_800,
        "lat": 29.0588,
        "lon": 76.0856,
        "region": "North"
    },
    "Uttarakhand": {
        "population": 11_250_858,
        "current_ahp": 52_000,
        "required_ahp": 56_000,
        "gap": 4_000,
        "urban_population_pct": 30.6,
        "rural_gap_pct": 62.4,
        "training_institutions": 68,
        "annual_graduates": 8_200,
        "lat": 30.0668,
        "lon": 79.0193,
        "region": "North"
    },
    "Himachal Pradesh": {
        "population": 7_451_955,
        "current_ahp": 42_000,
        "required_ahp": 37_000,
        "gap": -5_000,
        "urban_population_pct": 10.0,
        "rural_gap_pct": 45.8,
        "training_institutions": 42,
        "annual_graduates": 5_500,
        "lat": 31.1048,
        "lon": 77.1734,
        "region": "North"
    },
    "Jammu & Kashmir": {
        "population": 13_606_320,
        "current_ahp": 48_000,
        "required_ahp": 68_000,
        "gap": 20_000,
        "urban_population_pct": 27.4,
        "rural_gap_pct": 72.5,
        "training_institutions": 35,
        "annual_graduates": 4_200,
        "lat": 33.7782,
        "lon": 76.5762,
        "region": "North"
    },
    "Tripura": {
        "population": 4_169_794,
        "current_ahp": 18_000,
        "required_ahp": 21_000,
        "gap": 3_000,
        "urban_population_pct": 26.2,
        "rural_gap_pct": 68.4,
        "training_institutions": 12,
        "annual_graduates": 1_800,
        "lat": 23.9408,
        "lon": 91.9882,
        "region": "Northeast"
    },
    "Meghalaya": {
        "population": 3_366_710,
        "current_ahp": 12_000,
        "required_ahp": 17_000,
        "gap": 5_000,
        "urban_population_pct": 20.1,
        "rural_gap_pct": 78.6,
        "training_institutions": 8,
        "annual_graduates": 1_200,
        "lat": 25.4670,
        "lon": 91.3662,
        "region": "Northeast"
    },
    "Manipur": {
        "population": 3_091_545,
        "current_ahp": 14_000,
        "required_ahp": 15_000,
        "gap": 1_000,
        "urban_population_pct": 32.5,
        "rural_gap_pct": 65.2,
        "training_institutions": 10,
        "annual_graduates": 1_500,
        "lat": 24.6637,
        "lon": 93.9063,
        "region": "Northeast"
    },
    "Nagaland": {
        "population": 2_249_695,
        "current_ahp": 8_500,
        "required_ahp": 11_000,
        "gap": 2_500,
        "urban_population_pct": 28.9,
        "rural_gap_pct": 74.3,
        "training_institutions": 6,
        "annual_graduates": 850,
        "lat": 26.1584,
        "lon": 94.5624,
        "region": "Northeast"
    },
    "Goa": {
        "population": 1_586_250,
        "current_ahp": 12_500,
        "required_ahp": 8_000,
        "gap": -4_500,
        "urban_population_pct": 62.2,
        "rural_gap_pct": 28.4,
        "training_institutions": 18,
        "annual_graduates": 2_800,
        "lat": 15.2993,
        "lon": 74.1240,
        "region": "West"
    },
    "Arunachal Pradesh": {
        "population": 1_570_458,
        "current_ahp": 5_500,
        "required_ahp": 8_000,
        "gap": 2_500,
        "urban_population_pct": 22.7,
        "rural_gap_pct": 82.6,
        "training_institutions": 4,
        "annual_graduates": 520,
        "lat": 28.2180,
        "lon": 94.7278,
        "region": "Northeast"
    },
    "Mizoram": {
        "population": 1_239_244,
        "current_ahp": 6_200,
        "required_ahp": 6_000,
        "gap": -200,
        "urban_population_pct": 52.1,
        "rural_gap_pct": 42.5,
        "training_institutions": 7,
        "annual_graduates": 980,
        "lat": 23.1645,
        "lon": 92.9376,
        "region": "Northeast"
    },
    "Sikkim": {
        "population": 690_251,
        "current_ahp": 4_200,
        "required_ahp": 3_500,
        "gap": -700,
        "urban_population_pct": 25.2,
        "rural_gap_pct": 48.2,
        "training_institutions": 5,
        "annual_graduates": 650,
        "lat": 27.5330,
        "lon": 88.5122,
        "region": "Northeast"
    },
    "Delhi": {
        "population": 18_710_922,
        "current_ahp": 125_000,
        "required_ahp": 94_000,
        "gap": -31_000,
        "urban_population_pct": 97.5,
        "rural_gap_pct": 15.2,
        "training_institutions": 165,
        "annual_graduates": 22_500,
        "lat": 28.7041,
        "lon": 77.1025,
        "region": "North"
    }
}

DEMOGRAPHIC_DATA = {
    "urban_rural": {
        "Urban": {
            "population_pct": 35.0,
            "ahp_share": 58.0,
            "gap_share": 25.0,
            "density_per_10k": 38.2
        },
        "Rural": {
            "population_pct": 65.0,
            "ahp_share": 42.0,
            "gap_share": 75.0,
            "density_per_10k": 12.4
        }
    },
    "age_groups": {
        "0-14 years": {"population_pct": 26.2, "healthcare_need_index": 1.2},
        "15-24 years": {"population_pct": 17.9, "healthcare_need_index": 0.8},
        "25-44 years": {"population_pct": 29.5, "healthcare_need_index": 1.0},
        "45-59 years": {"population_pct": 14.8, "healthcare_need_index": 1.4},
        "60+ years": {"population_pct": 11.6, "healthcare_need_index": 2.5}
    },
    "socioeconomic": {
        "BPL (Below Poverty Line)": {
            "population_pct": 21.9,
            "ahp_access_pct": 28.0,
            "out_of_pocket_pct": 62.0
        },
        "Lower Middle": {
            "population_pct": 34.5,
            "ahp_access_pct": 45.0,
            "out_of_pocket_pct": 48.0
        },
        "Middle": {
            "population_pct": 28.2,
            "ahp_access_pct": 68.0,
            "out_of_pocket_pct": 35.0
        },
        "Upper Middle & Above": {
            "population_pct": 15.4,
            "ahp_access_pct": 92.0,
            "out_of_pocket_pct": 18.0
        }
    }
}

WHO_BENCHMARKS = {
    "nurses_per_10k": {"who_target": 30.0, "india_current": 17.2, "gap_pct": 42.7},
    "doctors_per_10k": {"who_target": 10.0, "india_current": 6.4, "gap_pct": 36.0},
    "ahp_per_10k": {"who_target": 44.5, "india_current": 28.8, "gap_pct": 35.3},
    "health_expenditure_gdp_pct": {"who_target": 5.0, "india_current": 2.1, "gap_pct": 58.0},
    "uhc_service_coverage_index": {"who_target": 80.0, "india_current": 55.0, "gap_pct": 31.25}
}

REGION_DATA = {
    "North": ["Uttar Pradesh", "Rajasthan", "Punjab", "Haryana", "Himachal Pradesh", 
              "Uttarakhand", "Jammu & Kashmir", "Delhi"],
    "South": ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Telangana", "Kerala"],
    "East": ["Bihar", "West Bengal", "Odisha", "Jharkhand"],
    "West": ["Maharashtra", "Gujarat", "Goa"],
    "Central": ["Madhya Pradesh", "Chhattisgarh"],
    "Northeast": ["Assam", "Tripura", "Meghalaya", "Manipur", "Nagaland", 
                  "Arunachal Pradesh", "Mizoram", "Sikkim"]
}

TRAINING_INFRASTRUCTURE = {
    "total_institutions": 2450,
    "nursing_colleges": 4520,
    "paramedical_institutes": 1850,
    "annual_seats": 485_000,
    "utilization_rate": 0.72,
    "quality_accredited_pct": 45.0,
    "faculty_shortage_pct": 35.0,
    "infrastructure_gap_pct": 42.0
}

CURRENT_FUNDING = {
    "central_budget_health_cr": 89155,
    "state_budgets_total_cr": 245000,
    "nhm_allocation_cr": 37159,
    "ayushman_bharat_cr": 7200,
    "human_resource_development_cr": 8500,
    "training_infrastructure_cr": 4200
}

INDIA_BUDGET_TREND = {
    "2015-16": {"health_budget_cr": 33152, "total_budget_cr": 1777477, "gdp_lakh_cr": 137.72, "health_pct_gdp": 0.24, "health_pct_budget": 1.87},
    "2016-17": {"health_budget_cr": 39879, "total_budget_cr": 1978060, "gdp_lakh_cr": 153.92, "health_pct_gdp": 0.26, "health_pct_budget": 2.02},
    "2017-18": {"health_budget_cr": 48878, "total_budget_cr": 2146735, "gdp_lakh_cr": 170.95, "health_pct_gdp": 0.29, "health_pct_budget": 2.28},
    "2018-19": {"health_budget_cr": 54667, "total_budget_cr": 2442213, "gdp_lakh_cr": 188.87, "health_pct_gdp": 0.29, "health_pct_budget": 2.24},
    "2019-20": {"health_budget_cr": 62659, "total_budget_cr": 2786349, "gdp_lakh_cr": 200.75, "health_pct_gdp": 0.31, "health_pct_budget": 2.25},
    "2020-21": {"health_budget_cr": 65012, "total_budget_cr": 3042230, "gdp_lakh_cr": 197.46, "health_pct_gdp": 0.33, "health_pct_budget": 2.14},
    "2021-22": {"health_budget_cr": 73932, "total_budget_cr": 3483236, "gdp_lakh_cr": 234.71, "health_pct_gdp": 0.31, "health_pct_budget": 2.12},
    "2022-23": {"health_budget_cr": 86201, "total_budget_cr": 3942589, "gdp_lakh_cr": 269.50, "health_pct_gdp": 0.32, "health_pct_budget": 2.19},
    "2023-24": {"health_budget_cr": 89155, "total_budget_cr": 4503097, "gdp_lakh_cr": 295.36, "health_pct_gdp": 0.30, "health_pct_budget": 1.98},
    "2024-25": {"health_budget_cr": 90959, "total_budget_cr": 4818085, "gdp_lakh_cr": 324.11, "health_pct_gdp": 0.28, "health_pct_budget": 1.89},
    "2025-26": {"health_budget_cr": 99859, "total_budget_cr": 5150000, "gdp_lakh_cr": 356.00, "health_pct_gdp": 0.28, "health_pct_budget": 1.94}
}

GLOBAL_HEALTH_SPENDING_COMPARISON = {
    "India": {"health_pct_gdp": 2.1, "govt_health_pct_gdp": 1.35, "out_of_pocket_pct": 48.0},
    "China": {"health_pct_gdp": 5.6, "govt_health_pct_gdp": 3.2, "out_of_pocket_pct": 35.0},
    "Brazil": {"health_pct_gdp": 10.3, "govt_health_pct_gdp": 4.1, "out_of_pocket_pct": 25.0},
    "USA": {"health_pct_gdp": 17.8, "govt_health_pct_gdp": 8.5, "out_of_pocket_pct": 11.0},
    "UK": {"health_pct_gdp": 12.0, "govt_health_pct_gdp": 10.2, "out_of_pocket_pct": 13.0},
    "Germany": {"health_pct_gdp": 12.8, "govt_health_pct_gdp": 10.9, "out_of_pocket_pct": 12.0},
    "Japan": {"health_pct_gdp": 11.1, "govt_health_pct_gdp": 9.2, "out_of_pocket_pct": 13.0},
    "Thailand": {"health_pct_gdp": 5.2, "govt_health_pct_gdp": 3.8, "out_of_pocket_pct": 11.0},
    "WHO Target": {"health_pct_gdp": 5.0, "govt_health_pct_gdp": 2.5, "out_of_pocket_pct": 15.0}
}

FUNDING_SOURCES = [
    {
        "source": "Central Government - Health Ministry",
        "potential_annual_cr": 45000,
        "current_annual_cr": 12700,
        "feasibility": "High",
        "mechanism": "Direct Budget Allocation",
        "timeline": "Immediate",
        "requirements": "Cabinet approval, Finance Ministry coordination"
    },
    {
        "source": "State Government Matching Funds",
        "potential_annual_cr": 35000,
        "current_annual_cr": 8000,
        "feasibility": "High",
        "mechanism": "60:40 Center-State Cost Sharing",
        "timeline": "1-2 Years",
        "requirements": "State health policy alignment, MoU signing"
    },
    {
        "source": "National Health Mission (NHM) Reallocation",
        "potential_annual_cr": 20000,
        "current_annual_cr": 5000,
        "feasibility": "High",
        "mechanism": "Program budget restructuring",
        "timeline": "Immediate",
        "requirements": "Mission steering committee approval"
    },
    {
        "source": "Ayushman Bharat Extended Coverage",
        "potential_annual_cr": 15000,
        "current_annual_cr": 2000,
        "feasibility": "Medium",
        "mechanism": "Provider network expansion incentives",
        "timeline": "2-3 Years",
        "requirements": "PMJAY policy amendments"
    },
    {
        "source": "Health Cess / Education Cess Extension",
        "potential_annual_cr": 25000,
        "current_annual_cr": 0,
        "feasibility": "Medium",
        "mechanism": "2% additional cess on income tax",
        "timeline": "1-2 Years",
        "requirements": "Parliamentary approval, Finance Bill amendment"
    },
    {
        "source": "Public-Private Partnerships (PPP)",
        "potential_annual_cr": 18000,
        "current_annual_cr": 3000,
        "feasibility": "Medium",
        "mechanism": "Viability gap funding, concession agreements",
        "timeline": "2-4 Years",
        "requirements": "PPP frameworks, bidding processes"
    },
    {
        "source": "International Aid (WHO, World Bank, ADB)",
        "potential_annual_cr": 8000,
        "current_annual_cr": 2500,
        "feasibility": "Medium",
        "mechanism": "Loans and grants for health systems strengthening",
        "timeline": "1-3 Years",
        "requirements": "Project proposals, government guarantees"
    },
    {
        "source": "Corporate Social Responsibility (CSR)",
        "potential_annual_cr": 5000,
        "current_annual_cr": 1200,
        "feasibility": "Low",
        "mechanism": "CSR mandate Section 135 - health focus",
        "timeline": "Ongoing",
        "requirements": "Corporate engagement, impact reporting"
    },
    {
        "source": "Skill India / PMKVY Allocation",
        "potential_annual_cr": 8000,
        "current_annual_cr": 1500,
        "feasibility": "High",
        "mechanism": "Healthcare skill development programs",
        "timeline": "Immediate",
        "requirements": "Ministry of Skill Development coordination"
    },
    {
        "source": "Medical Tourism Revenue Reinvestment",
        "potential_annual_cr": 6000,
        "current_annual_cr": 0,
        "feasibility": "Low",
        "mechanism": "Dedicated healthcare infrastructure fund",
        "timeline": "3-5 Years",
        "requirements": "New policy framework, revenue tracking"
    }
]

STRATEGY_PORTFOLIO = {
    "immediate": {
        "phase": "Immediate Priority (Years 1-2)",
        "description": "Critical interventions to address urgent shortages",
        "strategies": [
            {
                "name": "Emergency Skill Training Programs",
                "description": "6-month intensive certificate programs for community health workers, ANMs, and basic lab technicians",
                "target_professionals": 500000,
                "cost_cr_annual": 7500,
                "implementation_locations": ["Tier-2 Cities", "District Headquarters", "PHCs"],
                "expected_impact": "Immediate deployment of 500,000 workers to primary care",
                "gap_reduction_pct": 7.7,
                "key_actions": [
                    "Partner with existing nursing/medical colleges",
                    "Develop accelerated curriculum with NCAHP",
                    "Deploy mobile training units in rural areas",
                    "Offer stipends during training period"
                ],
                "success_metrics": ["Graduates per quarter", "Placement rate", "Rural deployment ratio"]
            },
            {
                "name": "Retention Incentive Package",
                "description": "Salary revision, housing allowance, and career progression for existing AHPs",
                "target_professionals": 4860000,
                "cost_cr_annual": 12000,
                "implementation_locations": ["All States", "Focus on Rural Areas"],
                "expected_impact": "Reduce attrition from 12% to 8%, retain 200,000 additional workers",
                "gap_reduction_pct": 3.1,
                "key_actions": [
                    "20% salary increase for rural postings",
                    "Housing allowance in underserved areas",
                    "Clear career progression pathways",
                    "Performance-based incentives"
                ],
                "success_metrics": ["Attrition rate", "Rural retention", "Job satisfaction index"]
            },
            {
                "name": "Infrastructure Emergency Fund",
                "description": "Rapid upgrade of existing training facilities and healthcare centers",
                "target_professionals": 0,
                "cost_cr_annual": 8000,
                "implementation_locations": ["100 priority districts", "Northeast states"],
                "expected_impact": "Double training capacity in 100 critical districts",
                "gap_reduction_pct": 0,
                "key_actions": [
                    "Equipment procurement for simulation labs",
                    "Digital learning infrastructure",
                    "Faculty housing in remote areas",
                    "Transportation support for students"
                ],
                "success_metrics": ["Facilities upgraded", "Seat utilization rate", "Faculty filled positions"]
            }
        ]
    },
    "intermediate": {
        "phase": "Intermediate Phase (Years 3-5)",
        "description": "Scaling up training capacity and systematic workforce development",
        "strategies": [
            {
                "name": "New Institution Establishment",
                "description": "Establish 500 new nursing schools, 200 paramedical institutes, 100 allied health colleges",
                "target_professionals": 0,
                "cost_cr_annual": 15000,
                "implementation_locations": ["High-gap states: UP, Bihar, MP, Rajasthan", "Aspirational districts"],
                "expected_impact": "Add 300,000 annual training seats, tripling current capacity",
                "gap_reduction_pct": 4.6,
                "key_actions": [
                    "Land acquisition in partnership with states",
                    "PPP models for construction and management",
                    "Faculty recruitment from retired professionals",
                    "International faculty exchange programs"
                ],
                "success_metrics": ["Institutions operational", "Accreditation status", "Graduate output"]
            },
            {
                "name": "Rural Deployment Mission",
                "description": "Mandatory 3-year rural service with enhanced benefits for all new graduates",
                "target_professionals": 900000,
                "cost_cr_annual": 18000,
                "implementation_locations": ["Rural PHCs", "CHCs", "Sub-centers in high-gap regions"],
                "expected_impact": "Deploy 300,000 professionals annually to rural areas, reducing rural gap by 40%",
                "gap_reduction_pct": 13.8,
                "key_actions": [
                    "Rural service bond in training agreements",
                    "3x salary for remote postings",
                    "Education support for children",
                    "Spouse employment assistance"
                ],
                "success_metrics": ["Rural deployment rate", "Service completion rate", "Patient coverage increase"]
            },
            {
                "name": "Quality Accreditation Drive",
                "description": "Upgrade all training institutions to meet NCAHP quality standards",
                "target_professionals": 0,
                "cost_cr_annual": 5000,
                "implementation_locations": ["All existing 2450+ institutions"],
                "expected_impact": "Increase quality-accredited institutions from 45% to 85%",
                "gap_reduction_pct": 0,
                "key_actions": [
                    "Mandatory NCAHP registration",
                    "Competency-based curriculum adoption",
                    "Regular quality audits",
                    "Faculty development programs"
                ],
                "success_metrics": ["Accreditation rate", "Graduate competency scores", "Employer satisfaction"]
            },
            {
                "name": "Digital Health Training Integration",
                "description": "Hybrid learning models combining online theory with hands-on clinical practice",
                "target_professionals": 600000,
                "cost_cr_annual": 4000,
                "implementation_locations": ["National platform", "Regional learning centers"],
                "expected_impact": "Enable 600,000 additional learners through flexible programs",
                "gap_reduction_pct": 9.2,
                "key_actions": [
                    "National e-learning platform development",
                    "VR/AR simulation modules",
                    "Clinical rotation partnerships",
                    "Continuous professional development credits"
                ],
                "success_metrics": ["Platform enrollment", "Course completion rate", "Skill certification rate"]
            }
        ]
    },
    "long_term": {
        "phase": "Long-term Sustainability (Years 6-15)",
        "description": "Achieving UHC goals and building self-sustaining healthcare workforce ecosystem",
        "strategies": [
            {
                "name": "Public-Private Training Partnership",
                "description": "Large-scale PPP for healthcare education with corporate hospitals",
                "target_professionals": 1500000,
                "cost_cr_annual": 12000,
                "implementation_locations": ["Metro cities", "Tier-1 cities with corporate hospitals"],
                "expected_impact": "Private sector contributes 1.5M trained professionals over 10 years",
                "gap_reduction_pct": 23.1,
                "key_actions": [
                    "Tax incentives for corporate training programs",
                    "Standardized curriculum across public-private",
                    "Employment guarantee post-training",
                    "Cross-deployment to public facilities"
                ],
                "success_metrics": ["Private sector training seats", "Public deployment ratio", "Quality parity"]
            },
            {
                "name": "International Collaboration & Exchange",
                "description": "Partnerships with WHO, foreign nursing schools for faculty and curriculum development",
                "target_professionals": 100000,
                "cost_cr_annual": 3000,
                "implementation_locations": ["Centers of Excellence", "Premier institutions"],
                "expected_impact": "World-class training standards, reduced brain drain through competitive salaries",
                "gap_reduction_pct": 1.5,
                "key_actions": [
                    "MoUs with UK, Australia, Philippines nursing councils",
                    "Faculty exchange programs",
                    "International certification pathways",
                    "Reverse brain drain incentives"
                ],
                "success_metrics": ["International partnerships", "Faculty trained abroad", "Returning professionals"]
            },
            {
                "name": "Autonomous Healthcare Workforce Authority",
                "description": "Independent body for planning, regulation, and continuous monitoring",
                "target_professionals": 0,
                "cost_cr_annual": 500,
                "implementation_locations": ["National level with state chapters"],
                "expected_impact": "Data-driven workforce planning, real-time gap monitoring, policy coordination",
                "gap_reduction_pct": 0,
                "key_actions": [
                    "Legislative framework for authority",
                    "National health workforce registry",
                    "Predictive analytics for workforce planning",
                    "Annual state-wise gap assessment"
                ],
                "success_metrics": ["Registry coverage", "Planning accuracy", "Policy implementation rate"]
            },
            {
                "name": "Career Ladder & Specialization Pathways",
                "description": "Advanced degrees, specializations, and leadership roles for AHPs",
                "target_professionals": 500000,
                "cost_cr_annual": 6000,
                "implementation_locations": ["Universities", "AIIMS", "State medical universities"],
                "expected_impact": "Create 500,000 specialized and leadership-level AHPs",
                "gap_reduction_pct": 7.7,
                "key_actions": [
                    "Master's and doctoral programs in allied health",
                    "Clinical specialist certifications",
                    "Management and leadership tracks",
                    "Research fellowships"
                ],
                "success_metrics": ["Advanced degree enrollments", "Specialist certifications", "Leadership positions filled"]
            }
        ]
    }
}

DATA_SOURCES = [
    {
        "title": "Allied Health Professionals Workforce Assessment",
        "publisher": "Ministry of Health and Family Welfare, Government of India",
        "year": 2012,
        "url": "https://mohfw.gov.in/",
        "data_used": "6.5 million AHP gap baseline, 139 allied health categories"
    },
    {
        "title": "National Health Workforce Account",
        "publisher": "WHO India / Ministry of Health",
        "year": 2018,
        "url": "https://www.who.int/india/health-topics/health-workforce",
        "data_used": "Health workforce stock estimates, density metrics"
    },
    {
        "title": "Union Budget Documents - Health Sector",
        "publisher": "Ministry of Finance, Government of India",
        "year": 2024,
        "url": "https://www.indiabudget.gov.in/",
        "data_used": "Health budget allocations, program-wise spending"
    },
    {
        "title": "Demand for Grants Analysis: Health and Family Welfare",
        "publisher": "PRS Legislative Research",
        "year": 2024,
        "url": "https://prsindia.org/budgets/parliament/demand-for-grants-2024-25-analysis-health-and-family-welfare",
        "data_used": "Budget trend analysis, program allocations"
    },
    {
        "title": "Human Resource Shortage in India's Health Sector",
        "publisher": "BMC Public Health",
        "year": 2024,
        "url": "https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-024-18850-x",
        "data_used": "Workforce shortage analysis, regional disparities"
    },
    {
        "title": "Size, Composition and Distribution of Health Workforce in India",
        "publisher": "Human Resources for Health Journal",
        "year": 2021,
        "url": "https://human-resources-health.biomedcentral.com/articles/10.1186/s12960-021-00575-2",
        "data_used": "State-wise workforce distribution, investment estimates"
    },
    {
        "title": "National Commission for Allied and Healthcare Professions",
        "publisher": "Government of India",
        "year": 2024,
        "url": "https://ncahp.gov.in/",
        "data_used": "57 allied health fields, regulatory framework"
    },
    {
        "title": "World Health Statistics",
        "publisher": "World Health Organization",
        "year": 2024,
        "url": "https://www.who.int/data/gho/publications/world-health-statistics",
        "data_used": "WHO benchmarks, global health workforce density standards"
    },
    {
        "title": "Census of India",
        "publisher": "Office of the Registrar General, India",
        "year": 2011,
        "url": "https://censusindia.gov.in/",
        "data_used": "State populations, urban-rural distribution"
    },
    {
        "title": "Economic Survey 2024-25",
        "publisher": "Ministry of Finance, Government of India",
        "year": 2025,
        "url": "https://www.indiabudget.gov.in/economicsurvey/",
        "data_used": "Health expenditure trends, GDP figures"
    }
]


def get_category_dataframe():
    data = []
    for category, info in AHP_CATEGORIES.items():
        data.append({
            "Category": category,
            "Current": info["current"],
            "Required": info["required"],
            "Gap": info["gap"],
            "Gap %": info["gap_percentage"],
            "Avg Salary (₹)": info["avg_salary_inr"],
            "Training Cost (₹)": info["training_cost_inr"],
            "Training Years": info["training_duration_years"],
            "Attrition Rate": info["attrition_rate"],
            "Description": info["description"]
        })
    return pd.DataFrame(data)


def get_state_dataframe():
    data = []
    for state, info in STATE_DATA.items():
        data.append({
            "State": state,
            "Population": info["population"],
            "Current AHP": info["current_ahp"],
            "Required AHP": info["required_ahp"],
            "Gap": info["gap"],
            "Urban %": info["urban_population_pct"],
            "Rural Gap %": info["rural_gap_pct"],
            "Training Institutions": info["training_institutions"],
            "Annual Graduates": info["annual_graduates"],
            "Region": info["region"],
            "Latitude": info["lat"],
            "Longitude": info["lon"],
            "AHP per 10K": round((info["current_ahp"] / info["population"]) * 10000, 2),
            "Required per 10K": round((info["required_ahp"] / info["population"]) * 10000, 2)
        })
    return pd.DataFrame(data)


def get_region_summary():
    region_data = []
    for region, states in REGION_DATA.items():
        total_pop = sum(STATE_DATA[s]["population"] for s in states if s in STATE_DATA)
        total_current = sum(STATE_DATA[s]["current_ahp"] for s in states if s in STATE_DATA)
        total_required = sum(STATE_DATA[s]["required_ahp"] for s in states if s in STATE_DATA)
        total_gap = sum(STATE_DATA[s]["gap"] for s in states if s in STATE_DATA)
        total_institutions = sum(STATE_DATA[s]["training_institutions"] for s in states if s in STATE_DATA)
        total_graduates = sum(STATE_DATA[s]["annual_graduates"] for s in states if s in STATE_DATA)
        
        region_data.append({
            "Region": region,
            "States": len(states),
            "Population": total_pop,
            "Current AHP": total_current,
            "Required AHP": total_required,
            "Gap": total_gap,
            "Gap %": round((total_gap / total_required) * 100, 1) if total_required > 0 else 0,
            "Training Institutions": total_institutions,
            "Annual Graduates": total_graduates,
            "AHP per 10K": round((total_current / total_pop) * 10000, 2) if total_pop > 0 else 0
        })
    return pd.DataFrame(region_data)


def calculate_cost_projection(
    target_gap_closure_pct: float,
    years: int,
    training_cost_multiplier: float = 1.0,
    salary_growth_rate: float = 0.05,
    infrastructure_investment_pct: float = 0.20,
    include_retention: bool = True,
    inflation_rate: float = 0.05
):
    target_reduction = int(TOTAL_GAP * (target_gap_closure_pct / 100))
    annual_target = target_reduction // years
    
    category_df = get_category_dataframe()
    total_gap = category_df["Gap"].sum()
    
    yearly_costs = []
    cumulative_hired = 0
    cumulative_cost = 0
    
    for year in range(1, years + 1):
        year_cost = 0
        year_training_cost = 0
        year_salary_cost = 0
        year_infrastructure_cost = 0
        year_retention_cost = 0
        
        inflation_multiplier = (1 + inflation_rate) ** (year - 1)
        
        for _, row in category_df.iterrows():
            category_share = row["Gap"] / total_gap if total_gap > 0 else 0
            category_target = int(annual_target * category_share)
            
            base_training_cost = row["Training Cost (₹)"] * training_cost_multiplier
            training_cost = category_target * base_training_cost * inflation_multiplier
            year_training_cost += training_cost
            
            salary_with_growth = row["Avg Salary (₹)"] * ((1 + salary_growth_rate) ** (year - 1))
            salary_cost = category_target * salary_with_growth
            year_salary_cost += salary_cost
            
            if include_retention:
                retention_cost = cumulative_hired * category_share * salary_with_growth * 0.15
                year_retention_cost += retention_cost
        
        year_infrastructure_cost = (year_training_cost + year_salary_cost) * infrastructure_investment_pct
        
        year_cost = year_training_cost + year_salary_cost + year_infrastructure_cost + year_retention_cost
        cumulative_hired += annual_target
        cumulative_cost += year_cost
        
        yearly_costs.append({
            "Year": year,
            "Calendar Year": 2024 + year,
            "Training Cost (₹ Cr)": float(round(year_training_cost / 1e7, 2)),
            "Salary Cost (₹ Cr)": float(round(year_salary_cost / 1e7, 2)),
            "Infrastructure Cost (₹ Cr)": float(round(year_infrastructure_cost / 1e7, 2)),
            "Retention Cost (₹ Cr)": float(round(year_retention_cost / 1e7, 2)),
            "Total Year Cost (₹ Cr)": float(round(year_cost / 1e7, 2)),
            "Cumulative Cost (₹ Cr)": float(round(cumulative_cost / 1e7, 2)),
            "Professionals Added": annual_target,
            "Cumulative Professionals": cumulative_hired,
            "Gap Remaining": TOTAL_GAP - cumulative_hired,
            "Gap Closure %": float(round((cumulative_hired / TOTAL_GAP) * 100, 2)),
            "Inflation Factor": float(round(inflation_multiplier, 3))
        })
    
    return pd.DataFrame(yearly_costs)


def get_budget_trend_dataframe():
    data = []
    for year, info in INDIA_BUDGET_TREND.items():
        data.append({
            "Financial Year": year,
            "Health Budget (₹ Cr)": info["health_budget_cr"],
            "Total Budget (₹ Cr)": info["total_budget_cr"],
            "GDP (₹ Lakh Cr)": info["gdp_lakh_cr"],
            "Health % of GDP": info["health_pct_gdp"],
            "Health % of Budget": info["health_pct_budget"]
        })
    return pd.DataFrame(data)


def get_funding_sources_dataframe():
    data = []
    for source in FUNDING_SOURCES:
        data.append({
            "Source": source["source"],
            "Potential (₹ Cr/Year)": source["potential_annual_cr"],
            "Current (₹ Cr/Year)": source["current_annual_cr"],
            "Additional Mobilizable": source["potential_annual_cr"] - source["current_annual_cr"],
            "Feasibility": source["feasibility"],
            "Mechanism": source["mechanism"],
            "Timeline": source["timeline"],
            "Requirements": source["requirements"]
        })
    return pd.DataFrame(data)


def get_global_comparison_dataframe():
    data = []
    for country, info in GLOBAL_HEALTH_SPENDING_COMPARISON.items():
        data.append({
            "Country": country,
            "Total Health % GDP": info["health_pct_gdp"],
            "Govt Health % GDP": info["govt_health_pct_gdp"],
            "Out-of-Pocket %": info["out_of_pocket_pct"]
        })
    return pd.DataFrame(data)


def get_strategy_summary():
    summary = []
    for phase_key, phase_data in STRATEGY_PORTFOLIO.items():
        for strategy in phase_data["strategies"]:
            summary.append({
                "Phase": phase_key.capitalize(),
                "Phase Description": phase_data["phase"],
                "Strategy": strategy["name"],
                "Description": strategy["description"],
                "Target Professionals": strategy["target_professionals"],
                "Annual Cost (₹ Cr)": strategy["cost_cr_annual"],
                "Gap Reduction %": strategy["gap_reduction_pct"],
                "Expected Impact": strategy["expected_impact"],
                "Locations": ", ".join(strategy["implementation_locations"])
            })
    return pd.DataFrame(summary)


def project_baseline_scenario(years: int = 15):
    current_annual_growth = 125_000
    current_gap = TOTAL_GAP
    
    projections = []
    for year in range(years + 1):
        projections.append({
            "Year": 2024 + year,
            "Scenario": "Baseline (Current Trend)",
            "Gap": current_gap,
            "Gap Closure %": round(((TOTAL_GAP - current_gap) / TOTAL_GAP) * 100, 2),
            "Annual Addition": current_annual_growth if year > 0 else 0
        })
        current_gap = max(0, current_gap - current_annual_growth + int(current_annual_growth * 0.12))
    
    return pd.DataFrame(projections)


def project_no_intervention_scenario(years: int = 15):
    annual_decline_rate = 0.02
    current_production = 485_000 * 0.72
    attrition = 0.10
    current_gap = TOTAL_GAP
    
    projections = []
    for year in range(years + 1):
        net_addition = int(current_production * (1 - attrition))
        
        projections.append({
            "Year": 2024 + year,
            "Scenario": "No Intervention",
            "Gap": current_gap,
            "Gap Closure %": round(((TOTAL_GAP - current_gap) / TOTAL_GAP) * 100, 2),
            "Annual Addition": net_addition if year > 0 else 0
        })
        
        current_gap = max(0, current_gap - net_addition)
        current_production *= (1 - annual_decline_rate)
    
    return pd.DataFrame(projections)


def project_proposed_strategy_scenario(
    years: int = 15,
    training_capacity_increase: float = 2.0,
    infrastructure_boost: float = 1.5,
    retention_improvement: float = 0.30
):
    base_production = 485_000 * 0.72
    enhanced_production = base_production * training_capacity_increase
    improved_attrition = 0.10 * (1 - retention_improvement)
    current_gap = TOTAL_GAP
    
    projections = []
    for year in range(years + 1):
        capacity_ramp = min(1.0, year / 3)
        year_production = base_production + (enhanced_production - base_production) * capacity_ramp
        net_addition = int(year_production * (1 - improved_attrition))
        
        projections.append({
            "Year": 2024 + year,
            "Scenario": "Proposed Strategy",
            "Gap": current_gap,
            "Gap Closure %": round(((TOTAL_GAP - current_gap) / TOTAL_GAP) * 100, 2),
            "Annual Addition": net_addition if year > 0 else 0
        })
        
        current_gap = max(0, current_gap - net_addition)
    
    return pd.DataFrame(projections)


def get_scenario_comparison(years: int = 15, **strategy_params):
    baseline = project_baseline_scenario(years)
    no_intervention = project_no_intervention_scenario(years)
    proposed = project_proposed_strategy_scenario(years, **strategy_params)
    
    return pd.concat([baseline, no_intervention, proposed], ignore_index=True)


def format_indian_number(num):
    if num >= 1e7:
        return f"₹{num/1e7:.2f} Cr"
    elif num >= 1e5:
        return f"₹{num/1e5:.2f} L"
    else:
        return f"₹{num:,.0f}"


def format_large_number(num):
    if abs(num) >= 1e7:
        return f"{num/1e6:.2f}M"
    elif abs(num) >= 1e5:
        return f"{num/1e5:.2f}L"
    elif abs(num) >= 1e3:
        return f"{num/1e3:.1f}K"
    else:
        return f"{num:,.0f}"
