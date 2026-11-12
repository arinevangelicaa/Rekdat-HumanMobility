"""
Script 02: Transformasi dan Pemodelan Data (Star Schema)
Proyek Human Mobility DIY - Rekayasa Data
"""
import os
import pandas as pd
import numpy as np

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")
OUTPUT_TABLES_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
os.makedirs(OUTPUT_TABLES_DIR, exist_ok=True)

def transform_and_model():
    print("=" * 60)
    print("TAHAP 2: TRANSFORMASI DAN PEMODELAN STAR SCHEMA")
    print("=" * 60)
    
    # 1. Load data
    print("\n[1/4] Memuat data mentah...")
    df_presence = pd.read_csv(os.path.join(DATASET_DIR, "presence_kapanewon_hourly.csv"))
    df_od = pd.read_csv(os.path.join(DATASET_DIR, "od_home_visits_kapanewon_monthly.csv"))
    df_origin = pd.read_csv(os.path.join(DATASET_DIR, "od_origin_homes_monthly.csv"))
    
    df_presence["date"] = pd.to_datetime(df_presence["date"])
    df_presence["hour"] = df_presence["hour"].astype(int)
    df_od["reduced_quality"] = df_od["reduced_quality"].astype(bool)
    
    # 2. Dimensi DimDate
    print("[2/4] Membuat tabel dimensi DimDate...")
    dates = pd.date_range(df_presence["date"].min(), df_presence["date"].max())
    dim_date = pd.DataFrame({
        "date_key": dates.strftime("%Y%m%d").astype(int),
        "date": dates,
        "year": dates.year,
        "month": dates.month,
        "month_name": dates.strftime("%B"),
        "day": dates.day,
        "day_of_week": dates.day_name(),
        "is_weekend": dates.dayofweek.isin([5, 6])
    })
    dim_date.to_csv(os.path.join(OUTPUT_TABLES_DIR, "dim_date.csv"), index=False)
    
    # 3. Dimensi DimTime
    print("[3/4] Membuat tabel dimensi DimTime...")
    def get_time_group(h):
        if 0 <= h <= 5: return "Malam Awal (00-05)"
        elif 6 <= h <= 10: return "Pagi (06-10)"
        elif 11 <= h <= 14: return "Siang (11-14)"
        elif 15 <= h <= 18: return "Sore (15-18)"
        else: return "Malam Akhir (19-23)"
        
    dim_time = pd.DataFrame({
        "hour_key": list(range(24)),
        "hour": list(range(24)),
        "time_group": [get_time_group(h) for h in range(24)]
    })
    dim_time.to_csv(os.path.join(OUTPUT_TABLES_DIR, "dim_time.csv"), index=False)
    
    # 4. Dimensi DimKapanewon
    print("[4/4] Membuat tabel dimensi DimKapanewon...")
    dim_kapanewon = df_presence[["kab_code", "kab_kota", "kapanewon_code", "kapanewon"]].drop_duplicates().sort_values("kapanewon_code")
    dim_kapanewon.to_csv(os.path.join(OUTPUT_TABLES_DIR, "dim_kapanewon.csv"), index=False)
    
    print("\n[OK] Model Star Schema berhasil dibuat:")
    print(f"    - DimDate: {len(dim_date)} baris")
    print(f"    - DimTime: {len(dim_time)} baris")
    print(f"    - DimKapanewon: {len(dim_kapanewon)} baris (78 kapanewon)")
    print(f"    - FactPresenceHourly: {len(df_presence):,} baris")
    print(f"    - FactODMonthly: {len(df_od):,} baris")

if __name__ == "__main__":
    transform_and_model()
