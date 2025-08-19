# VADER Sentiment Indonesia

VADER (Valence Aware Dictionary and sEntiment Reasoner) untuk Bahasa Indonesia.

## Deskripsi

Adaptasi VADER Sentiment Analysis untuk mendukung analisis sentimen dalam Bahasa Indonesia. Proyek ini merupakan modifikasi dari [vaderSentiment](https://github.com/cjhutto/vaderSentiment) yang disesuaikan dengan karakteristik dan kosakata Bahasa Indonesia.

## Fitur

- Analisis sentimen untuk teks Bahasa Indonesia
- Mendukung bahasa gaul dan singkatan Indonesia
- Mengenali emoticon dan emoji
- Menangani negasi dalam Bahasa Indonesia

## Instalasi

```bash
pip install -e .
```

## Penggunaan

```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
kalimat = "Hari ini sangat menyenangkan!"
skor = analyzer.polarity_scores(kalimat)
print(skor)
```

## Kontribusi

Kontribusi sangat diterima! Silakan buat pull request atau buka issue untuk saran dan perbaikan.

## Lisensi

MIT License - Lihat file LICENSE.txt untuk detail.

## Kredit

Berdasarkan VADER Sentiment Analysis oleh C.J. Hutto