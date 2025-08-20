#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def test_vader_indonesia():
    analyzer = SentimentIntensityAnalyzer()
    
    # 30 kalimat test dengan label sentimen yang jelas
    # Format: (kalimat, sentimen_sebenarnya) 
    # sentimen_sebenarnya: 1=positif, -1=negatif, 0=netral
    test_sentences = [
        # Kalimat Positif (10)
        ("Hari ini sangat menyenangkan dan membahagiakan", 1),
        ("Makanan di restoran itu enak sekali", 1),
        ("Saya senang banget dengan hasilnya", 1),
        ("Film ini bagus dan menghibur", 1),
        ("Pemandangan di sini indah luar biasa", 1),
        ("Dia orang yang baik dan ramah", 1),
        ("Pelayanannya memuaskan", 1),
        ("Produk ini berkualitas tinggi", 1),
        ("Saya suka sekali dengan desainnya", 1),
        ("Mantap jiwa, keren abis!", 1),
        
        # Kalimat Negatif (10)
        ("Hari ini sangat menyebalkan", -1),
        ("Makanannya tidak enak dan mahal", -1),
        ("Saya kecewa dengan pelayanannya", -1),
        ("Film itu membosankan sekali", -1),
        ("Cuaca hari ini buruk banget", -1),
        ("Dia jahat dan tidak peduli", -1),
        ("Hasilnya mengecewakan", -1),
        ("Kualitasnya jelek dan tidak memuaskan", -1),
        ("Saya benci dengan sikapnya", -1),
        ("Payah banget, gagal total", -1),
        
        # Kalimat Netral (10)
        ("Saya pergi ke kantor hari ini", 0),
        ("Harga tiketnya lima puluh ribu rupiah", 0),
        ("Rapat dimulai pukul sembilan pagi", 0),
        ("Dia tinggal di Jakarta", 0),
        ("Buku itu tebalnya 300 halaman", 0),
        ("Mobilnya berwarna merah", 0),
        ("Toko buka dari jam 8 sampai jam 9 malam", 0),
        ("Perjalanan memakan waktu 2 jam", 0),
        ("Ada 20 orang dalam ruangan", 0),
        ("Dokumen sudah dikirim kemarin", 0)
    ]
    
    correct_predictions = 0
    total_predictions = len(test_sentences)
    
    print("=" * 80)
    print("TESTING VADER INDONESIA - 30 KALIMAT")
    print("=" * 80)
    print()
    
    # Analisis per kategori
    results_by_category = {
        "positif": {"correct": 0, "total": 0},
        "negatif": {"correct": 0, "total": 0},
        "netral": {"correct": 0, "total": 0}
    }
    
    for i, (sentence, actual_sentiment) in enumerate(test_sentences, 1):
        scores = analyzer.polarity_scores(sentence)
        
        # Tentukan prediksi berdasarkan compound score
        if scores['compound'] >= 0.05:
            predicted_sentiment = 1  # Positif
            predicted_label = "POSITIF"
        elif scores['compound'] <= -0.05:
            predicted_sentiment = -1  # Negatif
            predicted_label = "NEGATIF"
        else:
            predicted_sentiment = 0  # Netral
            predicted_label = "NETRAL"
        
        # Tentukan label aktual
        if actual_sentiment == 1:
            actual_label = "POSITIF"
            results_by_category["positif"]["total"] += 1
        elif actual_sentiment == -1:
            actual_label = "NEGATIF"
            results_by_category["negatif"]["total"] += 1
        else:
            actual_label = "NETRAL"
            results_by_category["netral"]["total"] += 1
        
        # Cek apakah prediksi benar
        is_correct = predicted_sentiment == actual_sentiment
        if is_correct:
            correct_predictions += 1
            if actual_sentiment == 1:
                results_by_category["positif"]["correct"] += 1
            elif actual_sentiment == -1:
                results_by_category["negatif"]["correct"] += 1
            else:
                results_by_category["netral"]["correct"] += 1
        
        # Print hasil
        status = "✓" if is_correct else "✗"
        print(f"{i:2}. [{status}] {sentence[:50]:<50}")
        print(f"    Aktual: {actual_label:<8} | Prediksi: {predicted_label:<8}")
        print(f"    Scores: neg={scores['neg']:.3f}, neu={scores['neu']:.3f}, pos={scores['pos']:.3f}, compound={scores['compound']:.4f}")
        print()
    
    # Hitung akurasi
    accuracy = (correct_predictions / total_predictions) * 100
    
    print("=" * 80)
    print("HASIL EVALUASI")
    print("=" * 80)
    print(f"\nAkurasi Keseluruhan: {accuracy:.2f}% ({correct_predictions}/{total_predictions} benar)")
    print()
    print("Akurasi per Kategori:")
    print("-" * 40)
    
    for category in ["positif", "negatif", "netral"]:
        cat_data = results_by_category[category]
        if cat_data["total"] > 0:
            cat_accuracy = (cat_data["correct"] / cat_data["total"]) * 100
            print(f"{category.upper():<8}: {cat_accuracy:6.2f}% ({cat_data['correct']}/{cat_data['total']} benar)")
    
    print()
    print("=" * 80)
    
    # Analisis kesalahan
    print("\nANALISIS KESALAHAN:")
    print("-" * 40)
    error_count = 0
    for i, (sentence, actual_sentiment) in enumerate(test_sentences, 1):
        scores = analyzer.polarity_scores(sentence)
        
        if scores['compound'] >= 0.05:
            predicted_sentiment = 1
        elif scores['compound'] <= -0.05:
            predicted_sentiment = -1
        else:
            predicted_sentiment = 0
        
        if predicted_sentiment != actual_sentiment:
            error_count += 1
            actual_label = "POSITIF" if actual_sentiment == 1 else ("NEGATIF" if actual_sentiment == -1 else "NETRAL")
            predicted_label = "POSITIF" if predicted_sentiment == 1 else ("NEGATIF" if predicted_sentiment == -1 else "NETRAL")
            print(f"{error_count}. \"{sentence}\"")
            print(f"   Seharusnya: {actual_label}, Diprediksi: {predicted_label}")
            print(f"   Compound score: {scores['compound']:.4f}")
            print()
    
    if error_count == 0:
        print("Tidak ada kesalahan prediksi!")
    
    return accuracy

if __name__ == "__main__":
    accuracy = test_vader_indonesia()
    print(f"\n🎯 Akurasi Final VADER Indonesia: {accuracy:.2f}%")