"""
Script 04: Visualisasi Grafik Analisis Mobilitas
Proyek Human Mobility DIY - Rekayasa Data
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="tab10")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "figure.titlesize": 15,
    "figure.dpi": 300
})

def generate_visualizations():
    print("=" * 60)
    print("TAHAP 4: GENERASI VISUALISASI PUBLIKASI")
    print("=" * 60)
    
    # 1. Load data
    df_presence = pd.read_csv(os.path.join(DATASET_DIR, "presence_kapanewon_hourly.csv"))
    df_od = pd.read_csv(os.path.join(DATASET_DIR, "od_home_visits_kapanewon_monthly.csv"))
    df_od["reduced_quality"] = df_od["reduced_quality"].astype(bool)
    
    # Visual 1: Profil 24 Jam DIY
    print("\n[1/4] Membuat Gambar 1: Profil 24 Jam Kehadiran Perangkat...")
    profil_jam = df_presence.groupby("hour")["n_maids"].mean().reset_index()
    plt.figure(figsize=(10, 5))
    plt.plot(profil_jam["hour"], profil_jam["mean_n_maids"], marker="o", color="#1f77b4", linewidth=2.5, markersize=6)
    plt.title("Profil Rata-rata Kehadiran Perangkat per Jam di Seluruh Kapanewon DIY\n(Desember 2021 – April 2022)")
    plt.xlabel("Jam (WIB, 0–23)")
    plt.ylabel("Rata-rata n_maids per Kapanewon")
    plt.xticks(range(0, 24))
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.figtext(0.12, -0.04, "Sumber: JogjaPulse Zenodo (DOI: 10.5281/zenodo.23157460)\nCatatan: n_maids adalah perangkat unik per jam, bukan jumlah orang.", fontsize=9, color="#555555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "01_profil_kehadiran_24jam_diy.png"), bbox_inches="tight")
    plt.close()
    
    # Visual 2: Top 15 Destinasi Inter-zonal
    print("[2/4] Membuat Gambar 5: Top 15 Kapanewon Tujuan Inter-zonal...")
    od_clean = df_od[(~df_od["reduced_quality"]) & (df_od["origin_code"] != df_od["dest_code"])]
    top15 = od_clean.groupby("dest_kapanewon")["n_maids"].sum().reset_index().sort_values("n_maids", ascending=False).head(15)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top15, x="n_maids", y="dest_kapanewon", palette="viridis")
    plt.title("Top 15 Kapanewon Tujuan Kunjungan Inter-zonal di DIY\n(Periode Kualitas Tinggi: Desember 2021 – Februari 2022)")
    plt.xlabel("Total Akumulasi Perangkat Pengunjung Bulanan (n_maids)")
    plt.ylabel("Kapanewon Tujuan")
    plt.figtext(0.12, -0.04, "Sumber: JogjaPulse Zenodo | Catatan: Arus intrazonal (asal=tujuan) telah dikeluarkan. Unit: visitor counts.", fontsize=9, color="#555555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "05_top15_kapanewon_tujuan_interzonal.png"), bbox_inches="tight")
    plt.close()
    
    # Visual 3: Heatmap Matriks OD Antar-Kabupaten
    print("[3/4] Membuat Gambar 7: Matriks Arus Antar-Kabupaten...")
    od_kab = od_clean.groupby(["origin_kab_kota", "dest_kab_kota"])["n_maids"].sum().unstack(fill_value=0)
    plt.figure(figsize=(9, 7))
    sns.heatmap(od_kab, annot=True, fmt="d", cmap="YlGnBu", cbar_kws={'label': 'Akumulasi Pengunjung (n_maids)'})
    plt.title("Matriks Arus Kunjungan Lintas Kabupaten/Kota di DIY\n(Desember 2021 – Februari 2022)")
    plt.xlabel("Kabupaten/Kota Tujuan")
    plt.ylabel("Kabupaten/Kota Asal")
    plt.xticks(rotation=45, ha="right")
    plt.figtext(0.12, -0.05, "Sumber: JogjaPulse Zenodo (Agregasi Kabupaten/Kota)", fontsize=9, color="#555555")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "07_arus_od_antar_kabupaten.png"), bbox_inches="tight")
    plt.close()
    
    print("\n[OK] Visualisasi berhasil diperbarui di outputs/figures/")

if __name__ == "__main__":
    generate_visualizations()
