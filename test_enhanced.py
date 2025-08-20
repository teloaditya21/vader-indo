#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'vaderSentiment')

from vaderSentiment_enhanced import SentimentIntensityAnalyzer
import random
from datetime import datetime

def test_complex_sentences():
    """Test enhanced VADER with complex Indonesian sentences"""
    
    analyzer = SentimentIntensityAnalyzer()
    
    # Complex test cases that were problematic before
    complex_cases = [
        # Conjunction handling
        ("Makanan enak tapi pelayanan lambat", 0),  # Mixed
        ("Murah tapi kualitas jelek", -1),  # Negative dominates
        ("Awalnya susah tapi akhirnya berhasil", 1),  # Positive ending
        ("Bagus sih tapi terlalu mahal", 0),  # Mixed
        ("Tidak buruk malah cukup bagus", 1),  # Double negative to positive
        
        # Negation patterns
        ("Tidak jelek sama sekali", 1),  # Not bad at all = good
        ("Bukan tidak bagus", 1),  # Not not good = good
        ("Gak nyesel beli ini", 1),  # No regret = positive
        ("Tidak mengecewakan", 1),  # Not disappointing = good
        ("Belum puas dengan hasilnya", -1),  # Not satisfied = negative
        
        # Idioms and phrases
        ("Worth it banget", 1),
        ("Mantap jiwa bro", 1),
        ("Parah sih ini", -1),
        ("Gokil abis", 1),
        ("Kacau balau", -1),
        
        # Complex sentiment flow
        ("Pelayanan ramah, makanan enak, harga terjangkau", 1),
        ("Pelayanan buruk, makanan dingin, harga mahal", -1),
        ("Ada bagus ada jeleknya", 0),
        ("Lumayan lah untuk harga segitu", 0),
        ("Biasa aja nothing special", 0),
        
        # Real problematic sentences from test
        ("Keluarga selalu mendukung setiap keputusan", 1),
        ("Gadget ini worth it untuk dibeli", 1),
        ("Game ini seru dan adiktif", 1),
        ("Kehilangan barang saat traveling", -1),
        ("Macet parah di jalan", -1),
        ("Seafood tidak segar dan amis", -1),
        ("Murah tapi kualitas biasa saja", 0),
        ("Semester baru dimulai", 0),
        ("Membersihkan kamar", 0)
    ]
    
    print("=" * 80)
    print("TESTING ENHANCED VADER - COMPLEX SENTENCES")
    print("=" * 80)
    print()
    
    correct = 0
    total = len(complex_cases)
    
    for sentence, expected in complex_cases:
        scores = analyzer.polarity_scores(sentence)
        
        # Determine predicted sentiment
        if scores['compound'] >= 0.05:
            predicted = 1
            pred_label = "POSITIVE"
        elif scores['compound'] <= -0.05:
            predicted = -1
            pred_label = "NEGATIVE"
        else:
            predicted = 0
            pred_label = "NEUTRAL"
        
        # Determine expected label
        if expected == 1:
            exp_label = "POSITIVE"
        elif expected == -1:
            exp_label = "NEGATIVE"
        else:
            exp_label = "NEUTRAL"
        
        is_correct = predicted == expected
        if is_correct:
            correct += 1
        
        status = "✓" if is_correct else "✗"
        print(f"[{status}] {sentence}")
        print(f"    Expected: {exp_label:<8} | Got: {pred_label:<8}")
        print(f"    Scores: {scores}")
        print()
    
    accuracy = (correct / total) * 100
    print("=" * 80)
    print(f"Complex Sentences Accuracy: {accuracy:.1f}% ({correct}/{total})")
    print("=" * 80)
    
    return accuracy

def test_300_enhanced():
    """Test enhanced VADER with 300 sentences"""
    
    from test_300_sentences import generate_300_test_sentences
    
    analyzer = SentimentIntensityAnalyzer()
    test_data = generate_300_test_sentences()
    
    random.shuffle(test_data)
    
    results = {
        'total': len(test_data),
        'correct': 0,
        'by_category': {
            'positive': {'total': 0, 'correct': 0},
            'negative': {'total': 0, 'correct': 0},
            'neutral': {'total': 0, 'correct': 0}
        }
    }
    
    print("\n" + "=" * 80)
    print("TESTING ENHANCED VADER - 300 SENTENCES")
    print("=" * 80)
    print(f"Start: {datetime.now().strftime('%H:%M:%S')}")
    
    for i, (sentence, actual_sentiment) in enumerate(test_data, 1):
        scores = analyzer.polarity_scores(sentence)
        
        # Determine predicted sentiment
        if scores['compound'] >= 0.05:
            predicted_sentiment = 1
        elif scores['compound'] <= -0.05:
            predicted_sentiment = -1
        else:
            predicted_sentiment = 0
        
        # Determine actual category
        if actual_sentiment == 1:
            category = 'positive'
        elif actual_sentiment == -1:
            category = 'negative'
        else:
            category = 'neutral'
        
        results['by_category'][category]['total'] += 1
        
        # Check if correct
        if predicted_sentiment == actual_sentiment:
            results['correct'] += 1
            results['by_category'][category]['correct'] += 1
        
        # Progress
        if i % 100 == 0:
            print(f"Processed {i}/{len(test_data)}...")
    
    # Calculate accuracy
    overall_accuracy = (results['correct'] / results['total']) * 100
    
    print(f"\n{'='*80}")
    print("RESULTS - ENHANCED VADER")
    print("=" * 80)
    print(f"\n📊 Overall Accuracy: {overall_accuracy:.1f}% ({results['correct']}/{results['total']})")
    
    print("\n📈 Per Category:")
    for category in ['positive', 'negative', 'neutral']:
        cat_data = results['by_category'][category]
        if cat_data['total'] > 0:
            cat_accuracy = (cat_data['correct'] / cat_data['total']) * 100
            print(f"{category.upper():<8}: {cat_accuracy:>6.1f}% ({cat_data['correct']}/{cat_data['total']})")
    
    print("\n" + "=" * 80)
    
    # Compare with original
    print("\n📊 IMPROVEMENT ANALYSIS")
    print("-" * 40)
    print("Original VADER: 82.33% accuracy")
    print(f"Enhanced VADER: {overall_accuracy:.1f}% accuracy")
    improvement = overall_accuracy - 82.33
    if improvement > 0:
        print(f"✅ Improvement: +{improvement:.1f}%")
    else:
        print(f"❌ Decrease: {improvement:.1f}%")
    
    return overall_accuracy

if __name__ == "__main__":
    print("Testing Enhanced VADER Indonesia...")
    print()
    
    # Test complex sentences first
    complex_acc = test_complex_sentences()
    
    # Test 300 sentences
    overall_acc = test_300_enhanced()
    
    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print(f"Complex Sentences: {complex_acc:.1f}%")
    print(f"300 Sentences: {overall_acc:.1f}%")
    
    if overall_acc >= 95:
        print("\n🎯 TARGET ACHIEVED! Enhanced VADER reaches 95%+ accuracy!")
    elif overall_acc >= 90:
        print("\n✅ Excellent! Enhanced VADER achieves 90%+ accuracy!")
    elif overall_acc >= 85:
        print("\n👍 Good improvement! Enhanced VADER reaches 85%+ accuracy!")
    else:
        print("\n📈 Some improvement, but more work needed.")