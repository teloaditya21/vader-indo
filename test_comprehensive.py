#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

def test_comprehensive():
    analyzer = SentimentIntensityAnalyzer()
    
    # 50 test sentences with various complexity levels
    test_sentences = [
        # Positive sentences (20)
        ("Hari ini sangat menyenangkan dan membahagiakan", 1),
        ("Makanan di restoran itu lezat dan nikmat sekali", 1),
        ("Pemandangan di sini sungguh indah dan menakjubkan", 1),
        ("Dia adalah orang yang baik, ramah, dan menyenangkan", 1),
        ("Pelayanannya memuaskan dan profesional", 1),
        ("Produk ini berkualitas tinggi dan tahan lama", 1),
        ("Saya sangat senang dengan hasil kerja tim", 1),
        ("Film ini bagus, menarik, dan menghibur", 1),
        ("Suasana di cafe ini nyaman dan romantis", 1),
        ("Prestasinya gemilang dan membanggakan", 1),
        ("Teknologi ini canggih dan inovatif", 1),
        ("Kerjasama tim sangat solid dan kompak", 1),
        ("Liburan kali ini benar-benar menyenangkan", 1),
        ("Makanan tradisional ini enak dan autentik", 1),
        ("Guru itu sabar dan telaten mengajar", 1),
        ("Hasilnya memuaskan dan sesuai harapan", 1),
        ("Acara ini meriah dan penuh kegembiraan", 1),
        ("Dia pintar, rajin, dan bertanggung jawab", 1),
        ("Cuaca hari ini cerah dan sejuk", 1),
        ("Pengalaman yang luar biasa dan tak terlupakan", 1),
        
        # Negative sentences (20)
        ("Hari ini benar-benar menyebalkan dan menjengkelkan", -1),
        ("Makanannya tidak enak, hambar, dan mahal", -1),
        ("Film itu membosankan dan mengecewakan", -1),
        ("Pelayanannya buruk, lambat, dan tidak ramah", -1),
        ("Kualitas produk ini jelek dan mudah rusak", -1),
        ("Saya kecewa dengan hasil yang mengecewakan ini", -1),
        ("Cuaca hari ini buruk, hujan, dan dingin", -1),
        ("Dia malas, bodoh, dan tidak bertanggung jawab", -1),
        ("Situasi ini kacau dan berantakan", -1),
        ("Hasilnya gagal total dan merugikan", -1),
        ("Tempat ini kotor, jorok, dan bau", -1),
        ("Kinerjanya payah dan mengecewakan", -1),
        ("Barang ini palsu dan tidak berkualitas", -1),
        ("Suasananya suram dan menyedihkan", -1),
        ("Dia jahat, kejam, dan tidak berperasaan", -1),
        ("Makanan ini basi dan berbahaya", -1),
        ("Proyeknya hancur dan merugi besar", -1),
        ("Kondisi jalan rusak parah dan berbahaya", -1),
        ("Sistem ini error dan tidak bisa diperbaiki", -1),
        ("Keputusan itu salah dan merugikan banyak pihak", -1),
        
        # Neutral/Mixed sentences (10)
        ("Harga tiket pesawat naik turun setiap hari", 0),
        ("Rapat dimulai pukul 10 pagi di ruang meeting", 0),
        ("Ada kelebihan dan kekurangannya", 0),
        ("Dokumen sudah dikirim via email kemarin", 0),
        ("Perjalanan memakan waktu sekitar 3 jam", 0),
        ("Buku ini tebalnya 500 halaman", 0),
        ("Dia tinggal di Jakarta sejak tahun 2020", 0),
        ("Menu makanan tersedia dalam bahasa Indonesia dan Inggris", 0),
        ("Pembayaran bisa dilakukan secara tunai atau transfer", 0),
        ("Acara dimulai tepat waktu sesuai jadwal", 0)
    ]
    
    # Shuffle for randomness
    random.shuffle(test_sentences)
    
    correct_predictions = 0
    total_predictions = len(test_sentences)
    
    print("=" * 80)
    print("COMPREHENSIVE TEST - 50 SENTENCES WITH KBBI INTEGRATION")
    print("=" * 80)
    print()
    
    # Track performance by category
    results_by_category = {
        "positif": {"correct": 0, "total": 0, "scores": []},
        "negatif": {"correct": 0, "total": 0, "scores": []},
        "netral": {"correct": 0, "total": 0, "scores": []}
    }
    
    # Test each sentence
    for i, (sentence, actual_sentiment) in enumerate(test_sentences, 1):
        scores = analyzer.polarity_scores(sentence)
        
        # Determine prediction
        if scores['compound'] >= 0.05:
            predicted_sentiment = 1
            predicted_label = "POSITIF"
        elif scores['compound'] <= -0.05:
            predicted_sentiment = -1
            predicted_label = "NEGATIF"
        else:
            predicted_sentiment = 0
            predicted_label = "NETRAL"
        
        # Determine actual label
        if actual_sentiment == 1:
            actual_label = "POSITIF"
            category = "positif"
        elif actual_sentiment == -1:
            actual_label = "NEGATIF"
            category = "negatif"
        else:
            actual_label = "NETRAL"
            category = "netral"
        
        results_by_category[category]["total"] += 1
        results_by_category[category]["scores"].append(scores['compound'])
        
        # Check if correct
        is_correct = predicted_sentiment == actual_sentiment
        if is_correct:
            correct_predictions += 1
            results_by_category[category]["correct"] += 1
        
        # Display result
        status = "✓" if is_correct else "✗"
        if not is_correct:  # Only show errors
            print(f"{i:2}. [{status}] {sentence[:60]}")
            print(f"    Expected: {actual_label:<8} | Got: {predicted_label:<8} | Score: {scores['compound']:+.4f}")
    
    # Calculate accuracy
    overall_accuracy = (correct_predictions / total_predictions) * 100
    
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    
    print(f"\n📊 Overall Accuracy: {overall_accuracy:.1f}% ({correct_predictions}/{total_predictions})")
    
    print("\n📈 Accuracy by Category:")
    print("-" * 40)
    for category in ["positif", "negatif", "netral"]:
        cat_data = results_by_category[category]
        if cat_data["total"] > 0:
            cat_accuracy = (cat_data["correct"] / cat_data["total"]) * 100
            avg_score = sum(cat_data["scores"]) / len(cat_data["scores"]) if cat_data["scores"] else 0
            print(f"{category.upper():<8}: {cat_accuracy:5.1f}% ({cat_data['correct']:2}/{cat_data['total']:2}) | Avg Score: {avg_score:+.3f}")
    
    # Performance assessment
    print("\n" + "=" * 80)
    if overall_accuracy >= 95:
        print("🎯 EXCELLENT! Target accuracy of 95% achieved!")
    elif overall_accuracy >= 90:
        print("✅ Very Good! Close to target (needs 5% more)")
    elif overall_accuracy >= 85:
        print("👍 Good performance, but needs improvement (10% to target)")
    else:
        print("⚠️ Needs significant improvement to reach 95% target")
    
    return overall_accuracy

def test_edge_cases():
    """Test specific edge cases and complex sentences"""
    analyzer = SentimentIntensityAnalyzer()
    
    edge_cases = [
        # Negation handling
        ("Tidak buruk, malah cukup bagus", 1),
        ("Bukan jelek, tapi juga tidak bagus", 0),
        ("Gak nyesel beli ini", 1),
        
        # Slang and informal
        ("Gokil abis bro, mantap jiwa!", 1),
        ("Anjir, keren parah!", 1),
        ("Kampret, gagal lagi", -1),
        
        # Mixed sentiment
        ("Bagus sih, tapi mahal banget", 0),
        ("Murah tapi kualitas jelek", -1),
        ("Awalnya susah, tapi akhirnya berhasil", 1),
        
        # Intensifiers
        ("Sangat amat luar biasa bagus sekali", 1),
        ("Jelek banget parah", -1),
        ("Biasa aja, nothing special", 0)
    ]
    
    print("\n" + "=" * 80)
    print("EDGE CASES TEST")
    print("=" * 80)
    
    for sentence, expected in edge_cases:
        scores = analyzer.polarity_scores(sentence)
        
        if scores['compound'] >= 0.05:
            predicted = 1
            label = "POS"
        elif scores['compound'] <= -0.05:
            predicted = -1
            label = "NEG"
        else:
            predicted = 0
            label = "NEU"
        
        exp_label = "POS" if expected == 1 else ("NEG" if expected == -1 else "NEU")
        status = "✓" if predicted == expected else "✗"
        
        print(f"[{status}] {sentence}")
        print(f"    Expected: {exp_label} | Got: {label} | Score: {scores['compound']:+.4f}")
        print()

if __name__ == "__main__":
    # Run comprehensive test
    accuracy = test_comprehensive()
    
    # Run edge cases test
    test_edge_cases()
    
    print("\n" + "=" * 80)
    print(f"🎯 FINAL ACCURACY WITH KBBI INTEGRATION: {accuracy:.1f}%")
    print("=" * 80)