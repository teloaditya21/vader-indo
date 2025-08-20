#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def test_vader_advanced():
    analyzer = SentimentIntensityAnalyzer()
    
    # 30 kalimat test yang lebih kompleks dan realistis
    # Format: (kalimat, sentimen_sebenarnya) 
    # sentimen_sebenarnya: 1=positif, -1=negatif, 0=netral
    test_sentences = [
        # Kalimat Positif Kompleks (10)
        ("Walaupun awalnya sulit, akhirnya berhasil juga. Senang sekali!", 1),
        ("Tidak buruk, malah bagus banget hasilnya", 1),
        ("Gila, keren abis performanya tadi malam", 1),
        ("Meski harganya mahal, tapi kualitasnya luar biasa bagus", 1),
        ("Alhamdulillah, akhirnya lulus dengan nilai memuaskan", 1),
        ("Wow, tidak menyangka bisa sebagus ini", 1),
        ("Pelayanan ramah, makanan enak, harga terjangkau. Perfect!", 1),
        ("Awalnya ragu, tapi ternyata pilihan yang tepat", 1),
        ("Bangga banget sama prestasi anak-anak", 1),
        ("Suasananya nyaman, pemandangan indah, recommended!", 1),
        
        # Kalimat Negatif Kompleks (10)
        ("Bagus sih, tapi sayang sekali banyak kekurangan", -1),
        ("Katanya enak, ternyata biasa aja malah cenderung tidak enak", -1),
        ("Mahal tapi kualitas mengecewakan", -1),
        ("Sudah capek-capek datang, eh tutup. Kesal banget!", -1),
        ("Tidak sesuai ekspektasi, jauh dari yang dijanjikan", -1),
        ("Rugi banget beli ini, tidak worth it sama sekali", -1),
        ("Pelayanan lambat, makanan dingin, harga mahal pula", -1),
        ("Sia-sia waktu dan tenaga, hasilnya nihil", -1),
        ("Kecewa berat, padahal sudah berharap banyak", -1),
        ("Buang-buang uang saja, mending tidak usah", -1),
        
        # Kalimat Campuran/Ambigu (10)
        ("Lumayan lah, tidak jelek-jelek amat", 0),
        ("Ada bagusnya ada jeleknya juga", 0),
        ("Biasa saja, nothing special", 0),
        ("Tidak terlalu buruk tapi juga tidak terlalu bagus", 0),
        ("50-50 lah, kadang oke kadang tidak", 0),
        ("Standar aja sih menurut saya", 0),
        ("Gak gimana-gimana banget", 0),
        ("Ya gitu deh, no comment", 0),
        ("Bingung mau bilang bagus atau jelek", 0),
        ("Tergantung selera masing-masing sih", 0)
    ]
    
    correct_predictions = 0
    total_predictions = len(test_sentences)
    
    print("=" * 80)
    print("ADVANCED TESTING VADER INDONESIA - 30 KALIMAT KOMPLEKS")
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
        print(f"{i:2}. [{status}] {sentence[:55]:<55}")
        print(f"    Aktual: {actual_label:<8} | Prediksi: {predicted_label:<8}")
        print(f"    Compound: {scores['compound']:+.4f}")
        print()
    
    # Hitung akurasi
    accuracy = (correct_predictions / total_predictions) * 100
    
    print("=" * 80)
    print("HASIL EVALUASI ADVANCED")
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
    
    # Tampilkan ringkasan kesalahan
    error_count = 0
    print("\nRINGKASAN KESALAHAN PREDIKSI:")
    print("-" * 40)
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
            print(f"❌ Kalimat #{i}: Seharusnya {actual_label}, terprediksi {predicted_label}")
            print(f"   \"{sentence[:60]}...\"")
            print(f"   Compound: {scores['compound']:+.4f}")
            print()
    
    if error_count == 0:
        print("✅ Sempurna! Tidak ada kesalahan prediksi!")
    else:
        print(f"Total kesalahan: {error_count} dari {total_predictions} kalimat")
    
    return accuracy

if __name__ == "__main__":
    accuracy = test_vader_advanced()
    print(f"\n🎯 Akurasi Final VADER Indonesia (Advanced Test): {accuracy:.2f}%")