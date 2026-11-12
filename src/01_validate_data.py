"""
Script 01: Validasi Kualitas Data (ETL - Extract & Validate)
Proyek Human Mobility DIY - Rekayasa Data
"""
import os
import pandas as pd
import numpy as np

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")
OUTPUT_TABLES_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
os.makedirs(OUTPUT_TABLES_DIR, exist_ok=True)

def validate_datasets():
    print("=" * 60)
    print("TAHAP 1: VALIDASI KUALITAS DATA")
    print("=" * 60)
    
    files = {
        "presence_kapanewon_hourly": "presence_kapanewon_hourly.csv",
        "od_home_visits_kapanewon_monthly": "od_home_visits_kapanewon_monthly.csv",
        "od_origin_homes_monthly": "od_origin_homes_monthly.csv",
        "home_maids_vs_population_kapanewon": "home_maids_vs_population_kapanewon.csv",
        "presence_cell500m_daily": "presence_cell500m_daily.csv",
        "validation_night_presence_kapanewon": "validation_night_presence_kapanewon.csv",
        "tier1_summary": "tier1_summary.csv",
        "od_summary": "od_summary.csv"
    }
    
    report_rows = []
    
    for name, filename in files.items():
        filepath = os.path.join(DATASET_DIR, filename)
        if not os.path.exists(filepath):
            print(f"File {filename} tidak ditemukan!")
            continue
            
        df = pd.read_csv(filepath)
        n_rows, n_cols = df.shape
        n_null = df.isnull().sum().sum()
        n_dup = df.duplicated().sum()
        
        print(f"\n[+] {filename}:")
        print(f"    - Ukuran: {n_rows:,} baris x {n_cols} kolom")
        print(f"    - Missing values: {n_null:,}")
        print(f"    - Duplikasi: {n_dup:,}")
        
        report_rows.append({
            "File": filename,
            "Baris": n_rows,
            "Kolom": n_cols,
            "Missing Values": n_null,
            "Duplikasi": n_dup,
            "Status": "Valid" if n_dup == 0 else "Ada Duplikasi"
        })
        
    report_df = pd.DataFrame(report_rows)
    report_path = os.path.join(OUTPUT_TABLES_DIR, "data_quality_report.csv")
    report_df.to_csv(report_path, index=False)
    print(f"\n[OK] Laporan kualitas data disimpan ke: {report_path}")
    return report_df

if __name__ == "__main__":
    validate_datasets()
