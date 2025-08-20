# Hasil Analisis VADER Indonesia - 300 Kalimat

## Ringkasan Eksekutif
- **Total Kalimat Diuji**: 300 kalimat bahasa Indonesia
- **Akurasi Keseluruhan**: **82.33%** (247/300 benar)
- **Grade**: B (Decent Performance)
- **Tanggal Test**: 20 Agustus 2025

## Performa Per Kategori

| Kategori | Akurasi | Benar/Total | Skor Rata-rata | Rentang Skor |
|----------|---------|-------------|----------------|--------------|
| **Positif** | 79.0% | 79/100 | +0.385 | [-0.61, +0.82] |
| **Negatif** | 77.0% | 77/100 | -0.404 | [-0.82, +0.61] |
| **Netral** | 91.0% | 91/100 | +0.009 | [-0.70, +0.61] |

## Confusion Matrix

### Distribusi Prediksi
```
Aktual↓ / Prediksi→ | POSITIF | NEGATIF | NETRAL |
--------------------|---------|---------|---------|
POSITIF             |   79    |    3    |   18    |
NEGATIF             |    2    |   77    |   21    |
NETRAL              |    6    |    3    |   91    |
```

## Analisis Kesalahan

### Tipe Kesalahan Terbanyak:
1. **Negatif → Netral**: 21 kasus (39.6% dari total error)
   - Kalimat negatif yang kurang ekspresif sering dianggap netral
   
2. **Positif → Netral**: 18 kasus (34.0% dari total error)
   - Kalimat positif dengan kata-kata yang belum ada di lexicon

3. **Netral → Positif**: 6 kasus (11.3% dari total error)
   - Kalimat netral dengan kata yang bisa bermakna positif

## Metrik Evaluasi

### Precision, Recall, dan F1-Score

| Kategori | Precision | Recall | F1-Score |
|----------|-----------|--------|----------|
| Positif | 0.886 | 0.790 | 0.835 |
| Negatif | 0.927 | 0.770 | 0.841 |
| Netral | 0.697 | 0.910 | 0.789 |

## Kekuatan Model

1. **Deteksi Netral Sangat Baik** (91% akurasi)
   - Model sangat baik mengenali kalimat informatif dan deskriptif
   
2. **Precision Tinggi untuk Negatif** (92.7%)
   - Ketika model memprediksi negatif, kemungkinan besar benar
   
3. **Recall Tinggi untuk Netral** (91.0%)
   - Model jarang melewatkan kalimat netral

## Kelemahan Model

1. **Recall Rendah untuk Sentimen Positif/Negatif** (~77-79%)
   - Masih banyak kalimat bersentimen yang terdeteksi sebagai netral
   
2. **Precision Rendah untuk Netral** (69.7%)
   - Banyak kalimat bersentimen yang salah diklasifikasi sebagai netral

## Konteks Kalimat yang Bermasalah

### Positif yang Sering Salah Deteksi:
- Kalimat dengan kata informal/gaul yang belum ada di lexicon
- Kalimat dengan konteks implisit
- Kalimat dengan kata asing (worth it, fresh, dll)

### Negatif yang Sering Salah Deteksi:
- Kalimat dengan negasi tidak langsung
- Kalimat dengan sarkasme halus
- Kalimat komplain yang tidak menggunakan kata negatif eksplisit

## Rekomendasi Perbaikan

1. **Perkaya Lexicon**
   - Tambahkan lebih banyak kata gaul/slang Indonesia
   - Tambahkan kata-kata kontekstual (domain spesifik)
   - Tambahkan frasa umum Indonesia

2. **Tingkatkan Handling Negasi**
   - Perbaiki deteksi double negative
   - Tangani negasi implisit lebih baik

3. **Context Awareness**
   - Pertimbangkan n-gram (bigram/trigram) untuk konteks
   - Tambahkan rules untuk pattern kalimat Indonesia

4. **Domain Adaptation**
   - Buat lexicon khusus per domain (bisnis, kesehatan, dll)
   - Adjust booster weights untuk konteks Indonesia

## Kesimpulan

VADER Indonesia mencapai akurasi **82.33%** pada 300 kalimat test yang beragam. Performa ini termasuk kategori "Decent" (Grade B) dengan kekuatan utama pada deteksi kalimat netral (91%) namun masih perlu peningkatan pada deteksi sentimen positif dan negatif.

### Perbandingan Target:
- **Target Awal**: 95%
- **Hasil Test 50 kalimat**: 98% (kalimat sederhana)
- **Hasil Test 300 kalimat**: 82.33% (kalimat kompleks & beragam)

Model bekerja sangat baik untuk kalimat sederhana namun perlu optimasi lebih lanjut untuk menangani kompleksitas bahasa Indonesia dalam konteks real-world.