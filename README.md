# Pola Kehadiran Perangkat dan Arus Kunjungan Antar-Kapanewon di DIY, Desember 2021–Februari 2022

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arinevangelicaa/Rekdat-HumanMobility/blob/main/notebooks/human_mobility_analysis.ipynb)

Link Google Colab : https://colab.research.google.com/github/arinevangelicaa/Rekdat-HumanMobility/blob/main/notebooks/human_mobility_analysis.ipynb

## Deskripsi Proyek

Proyek ini menganalisis **pola mobilitas manusia** di Daerah Istimewa Yogyakarta (DIY) menggunakan data agregat kehadiran perangkat seluler dan arus origin–destination (OD) antar-kapanewon. Data bersumber dari dataset [JogjaPulse](https://doi.org/10.5281/zenodo.23157460), yang berisi catatan lokasi GPS teragregasi dari 594.223 perangkat seluler selama periode Desember 2021 – April 2022.

Analisis difokuskan pada tiga pertanyaan riset utama terkait pola temporal kehadiran perangkat, arus kunjungan lintas-kapanewon, dan pengaruh normalisasi terhadap hasil analisis. Pendekatan yang digunakan mencakup pipeline ETL, konsep OLAP (roll-up, drill-down, slice, dice, pivot), dan pemodelan star schema.

> **Catatan Penting:** Jumlah perangkat (n_maids) **bukan** representasi jumlah penduduk. Satu perangkat belum tentu satu orang, dan data ini bukan sampel acak populasi.

---

## Anggota Kelompok

| No. | Nama | NIM |
|-----|------|-----|
| 1 | Arin Evangelica Patabang | 24/534030/TK/59182 |
| 2 | Nayla Thalita | 24/535820/TK/59467 |
| 3 | Arimbi Arum Sari | 24/541867/TK/60129 |
| 4 | Nabila Putri Barokah | 24/541890/TK/60132 |
| 5 | Stella Florencia Doulim | 24/542739/TK/60285 |

**Mata Kuliah:** Rekayasa Data — Semester 5  
**Program Studi:** Teknologi Informasi, Universitas Gadjah Mada

---

## Pertanyaan Riset

1. **Bagaimana pola kehadiran perangkat berubah menurut jam dan wilayah di DIY?**  
   Menganalisis profil 24-jam kehadiran perangkat, perbandingan hari kerja vs akhir pekan, dan perbedaan antar kabupaten/kota.

2. **Kapanewon mana yang menjadi tujuan kunjungan lintas-kapanewon terbesar pada Desember 2021–Februari 2022?**  
   Mengidentifikasi 15 kapanewon tujuan utama, membuat matriks OD heatmap, dan menganalisis arus antar kabupaten/kota.

3. **Bagaimana hasilnya berubah setelah jumlah perangkat yang menjadi sampel diperhitungkan?**  
   Membandingkan peringkat tujuan berdasarkan jumlah mentah vs proporsi ternormalisasi, dan menganalisis representativitas perangkat terhadap populasi.

---

## Sumber Data

### Sumber 1: JogjaPulse (Data Mobilitas)

- **Penerbit:** Widyawan (2026)
- **Judul:** JogjaPulse: An Aggregated Spatio-Temporal Mobility Dataset for Yogyakarta, Indonesia
- **DOI:** [10.5281/zenodo.23157460](https://doi.org/10.5281/zenodo.23157460)
- **Platform:** Zenodo
- **Lisensi:** CC BY 4.0
- **Cakupan:** DIY, 1 Desember 2021 – 30 April 2022 (151 hari)
- **Isi:** Data agregat kehadiran perangkat (harian per grid 500m, per jam per kapanewon) dan arus OD bulanan antar-kapanewon

### Sumber 2: BPS (Data Populasi)

- **Penerbit:** Badan Pusat Statistik (BPS)
- **Isi:** Data populasi per kapanewon di DIY
- **Referensi dalam dataset:** Kolom `pop_actual` pada file `home_maids_vs_population_kapanewon.csv`
- **Penggunaan:** Validasi representativitas spasial perangkat terhadap populasi aktual

---

## Metodologi

### Pipeline ETL

```
Extract → Validate → Transform → Model → Analyze → Visualize
```

1. **Extract:** Memuat 8 file CSV dari dataset JogjaPulse
2. **Validate:** Pengecekan null, duplikat, rentang tanggal/jam, jumlah kapanewon (78 unit), dan supresi (k=5)
3. **Transform:** Konversi tipe data, pembuatan tabel dimensi dan fakta
4. **Model:** Star schema dengan tabel dimensi (DimDate, DimTime, DimKapanewon) dan tabel fakta (FactPresenceHourly, FactODMonthly)

### Operasi OLAP

| Operasi | Contoh Penerapan |
|---------|------------------|
| **Roll-up** | Jam → kelompok waktu (pagi, siang, sore, malam); tanggal → bulan |
| **Drill-down** | Kabupaten/kota → kapanewon |
| **Slice** | Hanya data Desember 2021 |
| **Dice** | Filter beberapa bulan + beberapa wilayah |
| **Pivot** | Matriks OD origin × destination |

---

## Struktur Repositori

```
PROJECT AFTER UTS/
├── README.md                          # Dokumentasi utama (file ini)
├── requirements.txt                   # Dependensi Python
├── .gitignore                         # File yang diabaikan Git
│
├── dataset/                           # Data mentah dari JogjaPulse
│   ├── README.md                      # Dokumentasi asli dataset (dari Zenodo)
│   ├── presence_kapanewon_hourly.csv  # Kehadiran per kapanewon per jam (230K baris)
│   ├── presence_cell500m_daily.csv    # Kehadiran per grid 500m per hari (183K baris)
│   ├── od_home_visits_kapanewon_monthly.csv  # Arus OD bulanan (9.894 baris)
│   ├── od_origin_homes_monthly.csv    # Denominator OD (390 baris)
│   ├── home_maids_vs_population_kapanewon.csv  # Perangkat vs populasi (78 baris)
│   ├── validation_night_presence_kapanewon.csv # Validasi malam hari (156 baris)
│   ├── tier1_summary.csv             # Statistik supresi presence
│   └── od_summary.csv                # Statistik supresi OD
│
├── data/                              # Data olahan (jika ada)
│   └── README_data_sources.md         # Kamus data lengkap
│
├── notebooks/                         # Jupyter notebook analisis
│   └── human_mobility_analysis.ipynb  # Notebook utama
│
├── outputs/                           # Hasil analisis
│   ├── figures/                       # Visualisasi (PNG/SVG)
│   └── tables/                        # Tabel hasil (CSV)
│
└── src/                               # Skrip pipeline pembersihan & analisis modular
```

---

## Cara Menjalankan

### Prasyarat

- Python 3.8 atau lebih baru
- Jupyter Notebook / JupyterLab

### Langkah-langkah

1. **Clone repositori:**
   ```bash
   git clone <repository-url>
   cd "PROJECT AFTER UTS"
   ```

2. **Instal dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan notebook:**
   ```bash
   jupyter notebook notebooks/human_mobility_analysis.ipynb
   ```

4. **Jalankan semua sel** secara berurutan. Notebook bersifat self-contained dan akan:
   - Memuat semua data dari folder `dataset/`
   - Melakukan validasi dan transformasi data
   - Menghasilkan semua visualisasi di folder `outputs/figures/`
   - Menyimpan tabel ringkasan di folder `outputs/tables/`

---

## Temuan Utama

### Pola Temporal (RQ1)
- Kehadiran perangkat mengikuti siklus diurnal yang jelas: minimum sekitar pukul 03:00, naik dari 05:00, dan mencapai plateau antara 11:00–20:00 WIB.
- Akhir pekan (terutama Minggu) menunjukkan kehadiran yang sedikit lebih rendah dibandingkan hari kerja.
- Terdapat penurunan signifikan jumlah sampel perangkat dari ~87.000 (Desember 2021) menjadi ~9.000 (April 2022), dengan penurunan tajam pada 1 Januari 2022 dan 16 Februari 2022.

### Arus OD (RQ2)
- Kapanewon di pusat kota Yogyakarta dan Sleman mendominasi sebagai tujuan kunjungan lintas-kapanewon.
- Arus antar-kabupaten/kota menunjukkan interaksi kuat antara Kota Yogyakarta dan Kabupaten Sleman.
- Pola arus pada Desember 2021–Februari 2022 mengikuti model gravitasi (R² = 0.45–0.58).

### Normalisasi (RQ3)
- Normalisasi dengan jumlah perangkat sampel mengubah peringkat beberapa kapanewon tujuan.
- Rasio perangkat terhadap populasi bervariasi antar kapanewon (contoh: Gondomanan memiliki lebih banyak perangkat teramati daripada penduduk, kemungkinan karena pengunjung/pariwisata).

---

## Keterbatasan Data

1. **Perangkat ≠ Orang:** Data mencakup perangkat dengan aplikasi yang mengaktifkan lokasi, bukan sampel acak populasi. Satu perangkat belum tentu satu orang.

2. **Supresi (k = 5):** Baris dengan kurang dari 5 perangkat dihapus untuk perlindungan privasi. Baris yang hilang berarti "kurang dari 5 perangkat", **bukan nol**.
   - Grid sel × hari: 64,6% baris dihapus (6,6% total kehadiran perangkat)
   - Kapanewon × jam: 15,9% baris dihapus (0,7% total kehadiran perangkat)
   - OD: 48,6% baris dihapus (4,7% arus lintas-zona)

3. **Penurunan Sampel:** Rata-rata perangkat per hari turun dari ~87.000 (Des 2021) menjadi ~9.000 (Apr 2022). Perbandingan antar-waktu harus menggunakan nilai ternormalisasi.

4. **Kualitas Data Berkurang (Maret–April 2022):** Data OD pada Maret–April ditandai `reduced_quality = True`. Analisis kuantitatif difokuskan pada Desember 2021–Februari 2022.

5. **n_maids Tidak Aditif:** Jumlah perangkat unik tidak boleh dijumlahkan antar sel, kapanewon, jam, atau hari karena satu perangkat dapat terhitung di beberapa unit.

6. **Kunjungan vs Perjalanan:** Arus OD menghitung *visitor counts* (perangkat unik yang mengunjungi suatu tujuan dalam sebulan), bukan jumlah perjalanan.

---

## Lisensi

Dataset JogjaPulse dirilis di bawah lisensi **CC BY 4.0**. Kode analisis dalam repositori ini dibuat untuk keperluan tugas mata kuliah Rekayasa Data, Universitas Gadjah Mada.

---

## Referensi

1. Widyawan (2026). *JogjaPulse: An Aggregated Spatio-Temporal Mobility Dataset for Yogyakarta, Indonesia.* Zenodo. [https://doi.org/10.5281/zenodo.23157460](https://doi.org/10.5281/zenodo.23157460)

2. Deville, P. et al. (2014). Dynamic population mapping using mobile phone data. *PNAS*, 111, 15888–15893. [https://doi.org/10.1073/pnas.1408439111](https://doi.org/10.1073/pnas.1408439111)

3. Kang, Y. et al. (2020). Multiscale dynamic human mobility flow dataset in the U.S. during the COVID-19 epidemic. *Scientific Data*, 7, 390. [https://doi.org/10.1038/s41597-020-00734-5](https://doi.org/10.1038/s41597-020-00734-5)

4. de Montjoye, Y.-A. et al. (2013). Unique in the crowd: the privacy bounds of human mobility. *Scientific Reports*, 3, 1376. [https://doi.org/10.1038/srep01376](https://doi.org/10.1038/srep01376)

5. Pei, T. et al. (2014). A new insight into land use classification based on aggregated mobile phone data. *Int. J. Geogr. Inf. Sci.*, 28, 1988–2007. [https://doi.org/10.1080/13658816.2014.913794](https://doi.org/10.1080/13658816.2014.913794)

6. Pappalardo, L. et al. (2023). A dataset to assess mobility changes in Chile following local quarantines. *Scientific Data*, 10, 6. [https://doi.org/10.1038/s41597-022-01893-3](https://doi.org/10.1038/s41597-022-01893-3)
