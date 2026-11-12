# Dokumentasi Sumber Data dan Kamus Data

## Informasi Sumber Data

### Sumber Utama: JogjaPulse

| Atribut | Detail |
|---------|--------|
| **Penerbit** | Widyawan |
| **Tahun** | 2026 |
| **Judul** | JogjaPulse: An Aggregated Spatio-Temporal Mobility Dataset for Yogyakarta, Indonesia |
| **DOI** | [10.5281/zenodo.23157460](https://doi.org/10.5281/zenodo.23157460) |
| **URL** | https://zenodo.org/records/23157460 |
| **Platform** | Zenodo |
| **Lisensi** | CC BY 4.0 |
| **Cakupan Wilayah** | Daerah Istimewa Yogyakarta (DIY), Indonesia |
| **Cakupan Waktu** | 1 Desember 2021 – 30 April 2022 (151 hari) |
| **Sumber Asal** | 44.384.826 catatan lokasi GPS dari 594.223 perangkat seluler |

### Sumber Pendukung: BPS (Data Populasi)

| Atribut | Detail |
|---------|--------|
| **Penerbit** | Badan Pusat Statistik (BPS) |
| **Isi** | Populasi per kapanewon di DIY |
| **Referensi** | Kolom `pop_actual` pada `home_maids_vs_population_kapanewon.csv` |
| **Penggunaan** | Validasi representativitas spasial |

---

## Definisi Satuan Penting

| Istilah | Definisi |
|---------|----------|
| **Device / MAID** | Satu perangkat seluler, diidentifikasi oleh *mobile advertising identifier*. Satu perangkat **bukan** berarti satu orang. |
| **Ping** | Satu catatan lokasi GPS dari sebuah perangkat. |
| **Presence** | Perangkat dianggap "hadir" di suatu unit spasial jika memiliki minimal satu ping di unit tersebut selama periode tertentu. |
| **`n_maids`** | Jumlah perangkat **unik** yang hadir. **TIDAK ADITIF**: satu perangkat yang hadir di dua sel/jam dihitung sekali di masing-masing. Jangan menjumlahkan `n_maids` antar sel, kapanewon, jam, atau hari. |
| **`n_pings`** | Jumlah ping. Aditif, tetapi frekuensi ping bervariasi antar perangkat dan aplikasi. |
| **Visitor count** | Jumlah perangkat unik yang mengunjungi suatu tujuan dalam sebulan. **Bukan jumlah perjalanan** — perangkat yang mengunjungi tujuan setiap hari tetap dihitung sekali. |
| **Trip count** | (Tidak tersedia dalam dataset ini) Jumlah perjalanan individual. |
| **`n_homed_maids`** | Perangkat yang memiliki *home* bulanan di kapanewon tertentu. |
| **`n_homed_maids_daytime`** | Dari perangkat ber-*home*, yang teramati minimal sekali antara 08:00–17:59 WIB. |
| **Zona waktu** | Semua tanggal dan jam menggunakan WIB (UTC+7). |

---

## Catatan Privasi dan Supresi

### Mekanisme Proteksi

- **Hanya data agregat**: Tidak ada identifier perangkat, trajektori, atau lokasi individual.
- **Supresi k = 5**: Baris dengan kurang dari 5 perangkat unik dihapus.
- **Baris hilang ≠ nol**: Baris yang tidak ada berarti "kurang dari 5 perangkat", bukan tidak ada perangkat sama sekali.

### Statistik Supresi

| Produk | Baris Total | Baris Terpublikasi | % Baris Disupresi | % Kehadiran Disupresi |
|--------|-------------|--------------------|--------------------|----------------------|
| Grid sel 500m × hari | 518.176 | 183.548 | 64,6% | 6,6% |
| Kapanewon × jam | 273.979 | 230.418 | 15,9% | 0,7% |
| OD (kapanewon × kapanewon × bulan) | 19.263 | 9.894 | 48,6% | 4,7% (arus lintas-zona) |

---

## Kamus Data per File

### 1. `presence_kapanewon_hourly.csv`

**Deskripsi:** Jumlah perangkat unik dan ping per kapanewon (78 unit sub-distrik) per jam.  
**Jumlah baris:** 230.418  
**Ukuran:** ~12,2 MB

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `kab_code` | float64 | Kode kabupaten/kota, contoh: `34.01` |
| `kab_kota` | string | Nama kabupaten/kota: KULON PROGO, BANTUL, GUNUNGKIDUL, SLEMAN, YOGYAKARTA |
| `kapanewon_code` | string | Kode kapanewon, contoh: `34.01.01` |
| `kapanewon` | string | Nama kapanewon |
| `date` | string (YYYY-MM-DD) | Tanggal kalender (WIB) |
| `hour` | int64 | Jam, 0–23 (WIB); `8` berarti 08:00–08:59 |
| `n_maids` | int64 | Perangkat unik hadir di kapanewon pada jam tersebut (≥ 5) |
| `n_pings` | int64 | Jumlah ping tercatat di kapanewon pada jam tersebut |

**Keterbatasan:**
- Nilai malam hari di kapanewon pedesaan mungkin didasarkan pada sedikit baris terpublikasi (serendah 3,2% slot malam)
- 15,9% baris disupresi (mayoritas jam malam di area rural)

---

### 2. `presence_cell500m_daily.csv`

**Deskripsi:** Jumlah perangkat unik per grid sel 500m × 500m per hari. 5.715 sel unik, 151 hari.  
**Jumlah baris:** 183.548  
**Ukuran:** ~11,3 MB

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `cell_id` | string | Identifier sel `E{i}_N{j}`, di mana `i = floor(easting/500)` dan `j = floor(northing/500)` dalam UTM zona 49S (EPSG:32749). Contoh: `E790_N18255` |
| `x_min_utm` | int64 | Easting sudut kiri bawah sel (meter), EPSG:32749 |
| `y_min_utm` | int64 | Northing sudut kiri bawah sel (meter), EPSG:32749 |
| `centroid_lon` | float64 | Longitude pusat sel, WGS84 (EPSG:4326), 6 desimal |
| `centroid_lat` | float64 | Latitude pusat sel, WGS84 (EPSG:4326), 6 desimal |
| `date` | string (YYYY-MM-DD) | Tanggal kalender (WIB) |
| `n_maids` | int64 | Perangkat unik hadir di sel pada hari tersebut (≥ 5) |

**Keterbatasan:**
- 64,6% baris disupresi — sebagian besar sel pedesaan hilang banyak hari
- Tidak memiliki kolom `n_pings` (by design, untuk mencegah serangan diferensiasi)
- File ini **tidak** digunakan dalam analisis utama notebook (yang fokus pada level kapanewon)

---

### 3. `od_home_visits_kapanewon_monthly.csv`

**Deskripsi:** Arus kunjungan berbasis rumah (*home-based visitation flows*): jumlah perangkat unik yang rumah bulanannya di kapanewon asal *i* dan teramati di kapanewon tujuan *j* selama siang hari di bulan yang sama.  
**Jumlah baris:** 9.894  
**Ukuran:** ~0,8 MB

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `month` | string | Bulan format `YYYY-MM`, Desember 2021 – April 2022 |
| `origin_kab_code` | float64 | Kode kabupaten/kota asal (rumah) |
| `origin_kab_kota` | string | Nama kabupaten/kota asal |
| `origin_code` | string | Kode kapanewon asal |
| `origin_kapanewon` | string | Nama kapanewon asal |
| `dest_kab_code` | float64 | Kode kabupaten/kota tujuan |
| `dest_kab_kota` | string | Nama kabupaten/kota tujuan |
| `dest_code` | string | Kode kapanewon tujuan |
| `dest_kapanewon` | string | Nama kapanewon tujuan |
| `n_maids` | int64 | Perangkat unik dari asal yang teramati di tujuan selama siang hari (≥ 5) |
| `reduced_quality` | bool | `True` untuk Maret dan April 2022 (kualitas berkurang) |

**Definisi penting:**
- **Rumah bulanan:** Kapanewon dengan malam terbanyak (≥ 2 malam berbeda, ping 22:00–05:59 WIB)
- **Tujuan:** Kapanewon dengan minimal 1 ping siang hari (08:00–17:59 WIB)
- Baris dengan asal = tujuan (intra-zonal) **disertakan**
- Ini adalah **visitor counts, bukan trip counts**

**Keterbatasan:**
- Data Maret–April 2022 berkualitas rendah (`reduced_quality = True`)
- 48,6% baris disupresi (terutama pasangan OD di area rural)
- Kunjungan singkat kurang terepresentasi (hanya butuh 1 ping siang)

---

### 4. `od_origin_homes_monthly.csv`

**Deskripsi:** Denominator untuk produk OD. Digunakan untuk menghitung proporsi perangkat dari asal *i* yang mengunjungi *j*: `n_maids / n_homed_maids_daytime`.  
**Jumlah baris:** 390  
**Ukuran:** < 0,1 MB

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `month` | string | Bulan format `YYYY-MM` |
| `origin_kab_code` | float64 | Kode kabupaten/kota asal |
| `origin_kab_kota` | string | Nama kabupaten/kota asal |
| `origin_code` | string | Kode kapanewon asal |
| `origin_kapanewon` | string | Nama kapanewon asal |
| `n_homed_maids` | int64 | Perangkat dengan rumah bulanan di kapanewon tersebut (≥ 5) |
| `n_homed_maids_daytime` | int64 | Dari perangkat ber-rumah, yang teramati minimal sekali pada 08:00–17:59 WIB. Kosong jika < 5 |
| `reduced_quality` | bool | `True` untuk Maret dan April 2022 |

**Keterbatasan:**
- Definisi "rumah bulanan" berbeda dari definisi "rumah periode penuh" di `home_maids_vs_population_kapanewon.csv`
- Beberapa kapanewon memiliki `n_homed_maids_daytime` kosong pada bulan dengan sedikit perangkat

---

### 5. `home_maids_vs_population_kapanewon.csv`

**Deskripsi:** Perbandingan jumlah perangkat per kapanewon rumah vs populasi resmi BPS. Digunakan untuk validasi representativitas spasial.  
**Jumlah baris:** 78 (= jumlah kapanewon di DIY)  
**Ukuran:** < 0,1 MB

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `KAB_KOTA` | string | Nama kabupaten/kota |
| `KEC_KAPN` | string | Nama kecamatan/kapanewon |
| `n_users` | int64 | Perangkat dengan lokasi rumah di kapanewon tersebut (Des 2021 – Apr 2022) |
| `pop_actual` | float64 | Populasi resmi kapanewon menurut BPS |
| `ratio` | float64 | `n_users / pop_actual` |

**Catatan:**
- Definisi "rumah" di sini menggunakan seluruh periode (Des 2021–Apr 2022), berbeda dari definisi bulanan di file OD
- Gondomanan (Yogyakarta) memiliki rasio > 2.0, kemungkinan karena pengunjung/pariwisata
- Populasi BPS mungkin dari tahun sensus yang berbeda

---

### 6. `validation_night_presence_kapanewon.csv`

**Deskripsi:** Kehadiran malam hari per kapanewon, dihitung dari `presence_kapanewon_hourly.csv`. Digunakan untuk validasi teknis terhadap data populasi.  
**Jumlah baris:** 156 (78 kapanewon × 2 periode)  
**Ukuran:** < 0,1 MB

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `period` | string | `Dec 2021 - Apr 2022` atau `Dec 2021 - Jan 2022` |
| `kab_kota` | string | Nama kabupaten/kota |
| `kapanewon` | string | Nama kapanewon |
| `night_presence` | float64 | Rata-rata `n_maids` per jam untuk jam 00–05 WIB pada periode tersebut |
| `slots_published_pct` | float64 | Persentase slot malam (hari × 6 jam) yang terpublikasi (tidak disupresi) |
| `n_users` | int64 | Sama dengan di `home_maids_vs_population_kapanewon.csv` |
| `pop_actual` | float64 | Populasi resmi BPS |

**Keterbatasan:**
- Beberapa kapanewon rural memiliki `slots_published_pct` sangat rendah (serendah 3,2%)
- Nilai `night_presence` di kapanewon tersebut harus diinterpretasi dengan hati-hati

---

### 7. `tier1_summary.csv`

**Deskripsi:** Statistik baris dan supresi untuk dua produk presence.  
**Jumlah baris:** 2  
**Ukuran:** < 0,1 MB

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `pings_inside_diy_pct` | float64 | Persentase ping sumber di dalam batas DIY (100.0%) |
| `product` | string | `A_cell500m_daily` atau `B_kapanewon_hourly` |
| `k` | int64 | Ambang batas supresi (= 5) |
| `rows_total` | int64 | Baris sebelum supresi |
| `rows_published` | int64 | Baris setelah supresi |
| `rows_suppressed_pct` | float64 | Persentase baris yang disupresi |
| `maid_presence_suppressed_pct` | float64 | Persentase total `n_maids` yang ada di baris disupresi |
| `n_cells_published` | int64 | Jumlah sel (A) atau kapanewon (B) dengan minimal 1 baris terpublikasi |

---

### 8. `od_summary.csv`

**Deskripsi:** Statistik baris dan supresi untuk produk OD.  
**Jumlah baris:** 1  
**Ukuran:** < 0,1 MB

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `k` | int64 | Ambang batas supresi (= 5) |
| `min_nights` | int64 | Minimum malam untuk penentuan rumah (= 2) |
| `od_rows_total` | int64 | Baris OD sebelum supresi (19.263) |
| `od_rows_published` | int64 | Baris OD setelah supresi (9.894) |
| `od_rows_suppressed_pct` | float64 | Persentase baris OD yang disupresi (48,6%) |
| `inter_zonal_flow_kept_pct` | float64 | Persentase arus lintas-zona yang dipertahankan (95,3%) |
| `origin_rows_published` | int64 | Baris di `od_origin_homes_monthly.csv` (390) |

---

## Ringkasan Ukuran File

| File | Baris | Ukuran |
|------|-------|--------|
| `presence_cell500m_daily.csv` | 183.548 | 11,3 MB |
| `presence_kapanewon_hourly.csv` | 230.418 | 12,2 MB |
| `od_home_visits_kapanewon_monthly.csv` | 9.894 | 0,8 MB |
| `od_origin_homes_monthly.csv` | 390 | < 0,1 MB |
| `home_maids_vs_population_kapanewon.csv` | 78 | < 0,1 MB |
| `validation_night_presence_kapanewon.csv` | 156 | < 0,1 MB |
| `tier1_summary.csv` | 2 | < 0,1 MB |
| `od_summary.csv` | 1 | < 0,1 MB |
| **Total** | **~424.487** | **~24,4 MB** |
