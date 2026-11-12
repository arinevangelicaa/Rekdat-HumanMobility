"""
Script 03: Analisis Mobilitas Manusia (OLAP & Indikator Kuantitatif)
Proyek Human Mobility DIY - Rekayasa Data
"""
import os
import pandas as pd
import numpy as np

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")
OUTPUT_TABLES_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
os.makedirs(OUTPUT_TABLES_DIR, exist_ok=True)

def run_analysis():
    print("=" * 60)
    print("TAHAP 3: EKSEKUSI ANALISIS OLAP & INDIKATOR")
    print("=" * 60)
    
    # 1. Load Data
    df_presence = pd.read_csv(os.path.join(DATASET_DIR, "presence_kapanewon_hourly.csv"))
    df_od = pd.read_csv(os.path.join(DATASET_DIR, "od_home_visits_kapanewon_monthly.csv"))
    df_origin = pd.read_csv(os.path.join(DATASET_DIR, "od_origin_homes_monthly.csv"))
    df_pop = pd.read_csv(os.path.join(DATASET_DIR, "home_maids_vs_population_kapanewon.csv"))
    
    df_presence["date"] = pd.to_datetime(df_presence["date"])
    df_presence["is_weekend"] = df_presence["date"].dt.dayofweek.isin([5, 6])
    df_od["reduced_quality"] = df_od["reduced_quality"].astype(bool)
    
    # RQ1: Pola Temporal
    print("\n[RQ1] Menghitung profil 24 jam kehadiran perangkat...")
    profil_jam = df_presence.groupby("hour")["n_maids"].mean().reset_index()
    profil_jam.columns = ["hour", "mean_n_maids"]
    profil_jam.to_csv(os.path.join(OUTPUT_TABLES_DIR, "rq1_profil_jam_diy.csv"), index=False)
    
    profil_weekend = df_presence.groupby(["hour", "is_weekend"])["n_maids"].mean().unstack().reset_index()
    profil_weekend.columns = ["hour", "Hari Kerja (Senin-Jumat)", "Akhir Pekan (Sabtu-Minggu)"]
    profil_weekend.to_csv(os.path.join(OUTPUT_TABLES_DIR, "rq1_profil_weekday_vs_weekend.csv"), index=False)
    
    # RQ2: Arus Kunjungan OD Antar-Kapanewon (Des 2021 - Feb 2022)
    print("\n[RQ2] Menganalisis arus kunjungan inter-zonal (Des 2021 - Feb 2022)...")
    # Filter kualitas baik dan inter-zonal (origin != dest)
    od_clean = df_od[(~df_od["reduced_quality"]) & (df_od["origin_code"] != df_od["dest_code"])].copy()
    
    top_dest = od_clean.groupby(["dest_kab_kota", "dest_kapanewon"])["n_maids"].sum().reset_index()
    top_dest = top_dest.sort_values("n_maids", ascending=False).reset_index(drop=True)
    top_dest.columns = ["Kabupaten/Kota", "Kapanewon Tujuan", "Total Pengunjung Teramati (n_maids)"]
    top_dest.head(15).to_csv(os.path.join(OUTPUT_TABLES_DIR, "rq2_top15_destinasi_interzonal.csv"), index=False)
    
    # Matriks Antar Kabupaten/Kota
    od_kab = od_clean.groupby(["origin_kab_kota", "dest_kab_kota"])["n_maids"].sum().unstack(fill_value=0)
    od_kab.to_csv(os.path.join(OUTPUT_TABLES_DIR, "rq2_matriks_od_kabupaten.csv"))
    
    # RQ3: Normalisasi dan Representativitas
    print("\n[RQ3] Menghitung proporsi ternormalisasi dan korelasi representativitas...")
    od_norm = pd.merge(
        od_clean,
        df_origin[["month", "origin_code", "n_homed_maids_daytime"]],
        on=["month", "origin_code"],
        how="inner"
    )
    od_norm["proporsi_kunjungan"] = od_norm["n_maids"] / od_norm["n_homed_maids_daytime"]
    
    top_dest_norm = od_norm.groupby("dest_kapanewon")["proporsi_kunjungan"].mean().reset_index()
    top_dest_norm = top_dest_norm.sort_values("proporsi_kunjungan", ascending=False).reset_index(drop=True)
    top_dest_norm.columns = ["Kapanewon Tujuan", "Rata-rata Proporsi Pengunjung Asal"]
    top_dest_norm.head(15).to_csv(os.path.join(OUTPUT_TABLES_DIR, "rq3_top15_destinasi_ternormalisasi.csv"), index=False)
    
    # Korelasi n_users vs pop_actual
    corr = df_pop["n_users"].corr(df_pop["pop_actual"])
    print(f"    - Korelasi Pearson (n_users vs pop_actual, n=78): {corr:.4f}")
    
    print("\n[OK] Analisis selesai. Semua tabel ringkasan tersimpan di outputs/tables/")

if __name__ == "__main__":
    run_analysis()
