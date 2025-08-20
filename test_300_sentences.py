#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random
import json
from datetime import datetime

def generate_300_test_sentences():
    """Generate 300 diverse Indonesian sentences for testing"""
    
    sentences = []
    
    # 100 Positive sentences with various contexts
    sentences.extend([
        # Daily life positive
        ("Hari ini cuaca sangat cerah dan menyenangkan", 1),
        ("Sarapan pagi ini enak sekali", 1),
        ("Senang sekali bisa bertemu dengan teman lama", 1),
        ("Liburan kali ini benar-benar menyenangkan", 1),
        ("Akhirnya bisa istirahat dengan tenang", 1),
        ("Pemandangan di sini sangat indah", 1),
        ("Makanan di warung ini selalu enak", 1),
        ("Tidur nyenyak semalam, badan terasa segar", 1),
        ("Dapat kabar baik dari keluarga", 1),
        ("Hari ini produktif sekali", 1),
        
        # Work/Business positive
        ("Presentasi berjalan dengan lancar dan sukses", 1),
        ("Tim kita berhasil menyelesaikan proyek tepat waktu", 1),
        ("Klien sangat puas dengan hasil kerja kita", 1),
        ("Dapat bonus dari perusahaan", 1),
        ("Promosi jabatan akhirnya terwujud", 1),
        ("Kerjasama tim sangat solid", 1),
        ("Meeting hari ini sangat produktif", 1),
        ("Ide kreatif diterima dengan baik", 1),
        ("Penjualan meningkat drastis bulan ini", 1),
        ("Investor tertarik dengan proposal kita", 1),
        
        # Education positive
        ("Nilai ujian sangat memuaskan", 1),
        ("Berhasil lulus dengan predikat cumlaude", 1),
        ("Diterima di universitas impian", 1),
        ("Guru sangat sabar dan baik dalam mengajar", 1),
        ("Materi pelajaran mudah dipahami", 1),
        ("Dapat beasiswa penuh untuk kuliah", 1),
        ("Presentasi skripsi berjalan lancar", 1),
        ("Belajar jadi lebih menyenangkan", 1),
        ("Teman-teman sekelas sangat supportif", 1),
        ("Perpustakaan kampus sangat lengkap dan nyaman", 1),
        
        # Entertainment positive
        ("Film ini sangat bagus dan menghibur", 1),
        ("Konser musik tadi malam luar biasa", 1),
        ("Buku ini sangat menarik dan inspiratif", 1),
        ("Pertandingan sepak bola sangat seru", 1),
        ("Acara TV ini lucu dan menghibur", 1),
        ("Lagu baru ini enak didengar", 1),
        ("Game ini seru dan adiktif", 1),
        ("Drama Korea ini romantis sekali", 1),
        ("Stand up comedy tadi lucu banget", 1),
        ("Festival ini meriah dan penuh warna", 1),
        
        # Food positive
        ("Masakan ibu selalu yang terbaik", 1),
        ("Restoran ini pelayanannya sangat baik", 1),
        ("Kopi di cafe ini nikmat sekali", 1),
        ("Makanan tradisional ini lezat dan autentik", 1),
        ("Kue buatan teman sangat enak", 1),
        ("Seafood di sini segar dan lezat", 1),
        ("Nasi goreng ini juara rasanya", 1),
        ("Es krim ini menyegarkan sekali", 1),
        ("Bakso di sini legendaris enaknya", 1),
        ("Sate ayam ini empuk dan bumbu meresap sempurna", 1),
        
        # Technology positive
        ("Aplikasi baru ini sangat membantu", 1),
        ("Laptop baru bekerja dengan cepat", 1),
        ("Internet hari ini lancar sekali", 1),
        ("Fitur baru ini inovatif dan berguna", 1),
        ("Update sistem membuat performa lebih baik", 1),
        ("Smartphone ini kameranya bagus sekali", 1),
        ("Website ini user friendly dan informatif", 1),
        ("Teknologi AI sangat membantu pekerjaan", 1),
        ("Gadget ini worth it untuk dibeli", 1),
        ("Inovasi teknologi semakin canggih", 1),
        
        # Health/Sports positive
        ("Badan terasa sehat dan bugar", 1),
        ("Olahraga pagi membuat semangat", 1),
        ("Hasil medical checkup sangat baik", 1),
        ("Berhasil menurunkan berat badan", 1),
        ("Yoga membuat pikiran tenang", 1),
        ("Dokter bilang kondisi kesehatan prima", 1),
        ("Stamina meningkat setelah rutin olahraga", 1),
        ("Tidur lebih nyenyak setelah meditasi", 1),
        ("Pola makan sehat memberikan hasil positif", 1),
        ("Recovery dari cedera berjalan cepat", 1),
        
        # Relationship positive
        ("Hubungan dengan pasangan semakin harmonis", 1),
        ("Keluarga selalu mendukung setiap keputusan", 1),
        ("Teman-teman sangat perhatian dan peduli", 1),
        ("Komunikasi dengan orang tua semakin baik", 1),
        ("Dapat teman baru yang menyenangkan", 1),
        ("Reuni dengan sahabat lama sangat berkesan", 1),
        ("Kejutan ulang tahun dari teman-teman", 1),
        ("Pasangan sangat pengertian dan romantis", 1),
        ("Anak-anak tumbuh sehat dan cerdas", 1),
        ("Tetangga sangat ramah dan membantu", 1),
        
        # Shopping/Service positive
        ("Pelayanan toko sangat memuaskan", 1),
        ("Dapat diskon besar saat belanja", 1),
        ("Barang yang dibeli sesuai ekspektasi", 1),
        ("Customer service sangat responsif", 1),
        ("Pengiriman cepat dan aman", 1),
        ("Kualitas produk melebihi harga", 1),
        ("Promo hari ini sangat menguntungkan", 1),
        ("Toko online ini terpercaya", 1),
        ("Garansi produk sangat baik", 1),
        ("Belanja online jadi lebih mudah", 1),
        
        # Travel positive
        ("Perjalanan liburan sangat menyenangkan", 1),
        ("Hotel ini fasilitasnya lengkap dan nyaman", 1),
        ("Pemandangan gunung sangat memukau", 1),
        ("Pantai ini bersih dan indah", 1),
        ("Tour guide sangat informatif dan ramah", 1),
        ("Transportasi selama liburan lancar", 1),
        ("Kuliner lokal sangat lezat", 1),
        ("Pengalaman traveling tak terlupakan", 1),
        ("Destinasi wisata melebihi ekspektasi", 1),
        ("Suasana desa sangat asri dan tenang", 1)
    ])
    
    # 100 Negative sentences
    sentences.extend([
        # Daily life negative
        ("Hari ini benar-benar hari yang buruk", -1),
        ("Bangun kesiangan dan terlambat kerja", -1),
        ("Hujan deras membuat banjir di mana-mana", -1),
        ("Macet parah di jalan", -1),
        ("Listrik mati seharian", -1),
        ("Air di rumah tidak mengalir", -1),
        ("Tetangga berisik mengganggu istirahat", -1),
        ("Kehilangan dompet di jalan", -1),
        ("Motor mogok di tengah jalan", -1),
        ("Sakit kepala sejak pagi", -1),
        
        # Work/Business negative
        ("Proyek gagal total dan merugi", -1),
        ("Di PHK dari perusahaan", -1),
        ("Klien komplain dan kecewa", -1),
        ("Target penjualan tidak tercapai", -1),
        ("Meeting tidak produktif dan membuang waktu", -1),
        ("Rekan kerja tidak kooperatif", -1),
        ("Gaji dipotong tanpa alasan jelas", -1),
        ("Proposal ditolak investor", -1),
        ("Konflik dengan atasan", -1),
        ("Bisnis bangkrut karena pandemi", -1),
        
        # Education negative
        ("Nilai ujian sangat mengecewakan", -1),
        ("Tidak lulus ujian masuk universitas", -1),
        ("Skripsi ditolak dosen pembimbing", -1),
        ("Sulit memahami materi pelajaran", -1),
        ("Guru galak dan tidak sabar", -1),
        ("Beasiswa dibatalkan", -1),
        ("Diskors dari sekolah", -1),
        ("Tugas menumpuk dan deadline mepet", -1),
        ("Presentasi berantakan dan gagal", -1),
        ("Plagiarisme terdeteksi dalam tugas", -1),
        
        # Entertainment negative
        ("Film ini membosankan dan mengecewakan", -1),
        ("Konser dibatalkan mendadak", -1),
        ("Buku ini tidak menarik sama sekali", -1),
        ("Pertandingan kalah telak", -1),
        ("Acara TV ini tidak bermutu", -1),
        ("Lagu ini jelek dan tidak enak didengar", -1),
        ("Game ini penuh bug dan error", -1),
        ("Drama ini alurnya tidak masuk akal", -1),
        ("Stand up comedy tidak lucu sama sekali", -1),
        ("Festival gagal dan kacau", -1),
        
        # Food negative
        ("Makanan ini basi dan berbau", -1),
        ("Restoran ini jorok dan kotor", -1),
        ("Kopi ini pahit dan tidak enak", -1),
        ("Makanan terlalu asin dan pedas", -1),
        ("Kue ini keras dan tidak fresh", -1),
        ("Seafood tidak segar dan amis", -1),
        ("Nasi goreng gosong dan pahit", -1),
        ("Es krim sudah mencair dan tidak enak", -1),
        ("Bakso ini alot dan hambar", -1),
        ("Sate mentah dan berbahaya dimakan", -1),
        
        # Technology negative
        ("Aplikasi sering crash dan error", -1),
        ("Laptop rusak dan data hilang", -1),
        ("Internet lemot dan sering putus", -1),
        ("Fitur baru malah membuat ribet", -1),
        ("Update sistem membuat lag", -1),
        ("Smartphone cepat panas dan boros baterai", -1),
        ("Website susah diakses dan lambat", -1),
        ("Teknologi ini tidak berguna", -1),
        ("Gadget ini tidak worth it harganya", -1),
        ("Sistem error dan tidak bisa diperbaiki", -1),
        
        # Health/Sports negative
        ("Badan lemas dan tidak bertenaga", -1),
        ("Sakit flu sudah seminggu", -1),
        ("Hasil medical checkup mengkhawatirkan", -1),
        ("Berat badan naik drastis", -1),
        ("Cedera saat olahraga", -1),
        ("Dokter bilang harus operasi", -1),
        ("Stamina menurun drastis", -1),
        ("Insomnia mengganggu kesehatan", -1),
        ("Alergi makanan kambuh lagi", -1),
        ("Recovery sangat lambat dan menyakitkan", -1),
        
        # Relationship negative
        ("Putus dengan pasangan", -1),
        ("Bertengkar hebat dengan keluarga", -1),
        ("Dikhianati teman dekat", -1),
        ("Komunikasi dengan orang tua buruk", -1),
        ("Dijauhi teman-teman", -1),
        ("Konflik dengan sahabat", -1),
        ("Dibully di tempat kerja", -1),
        ("Pasangan selingkuh", -1),
        ("Anak-anak nakal dan susah diatur", -1),
        ("Tetangga suka gossip dan mengganggu", -1),
        
        # Shopping/Service negative
        ("Pelayanan toko sangat buruk", -1),
        ("Ditipu saat belanja online", -1),
        ("Barang yang dibeli rusak", -1),
        ("Customer service tidak responsif", -1),
        ("Pengiriman sangat lama dan rusak", -1),
        ("Kualitas produk mengecewakan", -1),
        ("Harga terlalu mahal tidak sesuai", -1),
        ("Toko online penipu", -1),
        ("Garansi tidak berlaku", -1),
        ("Komplain tidak ditanggapi", -1),
        
        # Travel negative
        ("Perjalanan penuh masalah", -1),
        ("Hotel kotor dan tidak nyaman", -1),
        ("Cuaca buruk merusak liburan", -1),
        ("Pantai kotor penuh sampah", -1),
        ("Tour guide tidak profesional", -1),
        ("Transportasi mogok di tengah jalan", -1),
        ("Makanan lokal menyebabkan sakit perut", -1),
        ("Kehilangan barang saat traveling", -1),
        ("Destinasi wisata mengecewakan", -1),
        ("Penginapan tidak sesuai foto", -1)
    ])
    
    # 100 Neutral/Mixed sentences
    sentences.extend([
        # Informational neutral
        ("Rapat dimulai pukul 9 pagi", 0),
        ("Dokumen sudah dikirim via email", 0),
        ("Harga tiket pesawat 500 ribu", 0),
        ("Jarak dari sini sekitar 10 kilometer", 0),
        ("Acara dimulai sesuai jadwal", 0),
        ("Pendaftaran dibuka mulai bulan depan", 0),
        ("Pembayaran bisa transfer atau tunai", 0),
        ("Kantor buka jam 8 sampai 5 sore", 0),
        ("Parkir tersedia di basement", 0),
        ("Menu makanan dalam bahasa Indonesia", 0),
        
        # Descriptive neutral
        ("Gedung ini memiliki 20 lantai", 0),
        ("Mobil berwarna putih", 0),
        ("Bukunya tebal 300 halaman", 0),
        ("Ruangan ber-AC", 0),
        ("Meja terbuat dari kayu", 0),
        ("Laptop merek terkenal", 0),
        ("Rumah menghadap ke selatan", 0),
        ("Tas berukuran sedang", 0),
        ("Sepatu nomor 42", 0),
        ("Baju warna biru", 0),
        
        # Mixed sentiment
        ("Makanan enak tapi pelayanan lambat", 0),
        ("Murah tapi kualitas biasa saja", 0),
        ("Bagus sih, tapi terlalu mahal", 0),
        ("Ada plus minusnya", 0),
        ("Tidak buruk tapi juga tidak istimewa", 0),
        ("Lumayan lah untuk harga segitu", 0),
        ("Biasa aja, nothing special", 0),
        ("50-50, kadang bagus kadang tidak", 0),
        ("Standar, sesuai ekspektasi", 0),
        ("Cukup, tidak lebih tidak kurang", 0),
        
        # Procedural neutral
        ("Isi formulir terlebih dahulu", 0),
        ("Ikuti petunjuk penggunaan", 0),
        ("Baca syarat dan ketentuan", 0),
        ("Tunggu konfirmasi lebih lanjut", 0),
        ("Simpan struk sebagai bukti", 0),
        ("Lakukan pembayaran sebelum tanggal 30", 0),
        ("Daftar melalui website resmi", 0),
        ("Ambil nomor antrian", 0),
        ("Tunjukkan kartu identitas", 0),
        ("Klik tombol submit", 0),
        
        # Factual statements
        ("Indonesia memiliki ribuan pulau", 0),
        ("Jakarta adalah ibu kota", 0),
        ("Hari ini tanggal 20", 0),
        ("Tahun ini tahun 2024", 0),
        ("Musim hujan dimulai Oktober", 0),
        ("Rupiah adalah mata uang Indonesia", 0),
        ("Bahasa resmi adalah Bahasa Indonesia", 0),
        ("Populasi Indonesia lebih dari 270 juta", 0),
        ("Indonesia terletak di Asia Tenggara", 0),
        ("Waktu Indonesia dibagi 3 zona", 0),
        
        # Questions (neutral tone)
        ("Apakah sudah makan?", 0),
        ("Dimana lokasi acaranya?", 0),
        ("Berapa harganya?", 0),
        ("Kapan mulai bekerjanya?", 0),
        ("Siapa yang bertanggung jawab?", 0),
        ("Bagaimana cara mendaftarnya?", 0),
        ("Mengapa harus begitu?", 0),
        ("Apa yang harus dibawa?", 0),
        ("Kemana harus pergi?", 0),
        ("Dari mana asalnya?", 0),
        
        # Activities neutral
        ("Sedang membaca buku", 0),
        ("Pergi ke pasar", 0),
        ("Menonton televisi", 0),
        ("Memasak untuk makan malam", 0),
        ("Mencuci pakaian", 0),
        ("Membersihkan kamar", 0),
        ("Mengerjakan tugas", 0),
        ("Berbelanja kebutuhan", 0),
        ("Menunggu teman", 0),
        ("Istirahat sejenak", 0),
        
        # Time/Schedule neutral
        ("Meeting dijadwalkan ulang", 0),
        ("Agenda hari ini penuh", 0),
        ("Libur tanggal merah", 0),
        ("Deadline minggu depan", 0),
        ("Shift malam mulai jam 10", 0),
        ("Break time 15 menit", 0),
        ("Lembur sampai malam", 0),
        ("Cuti mulai senin", 0),
        ("Semester baru dimulai", 0),
        ("Ujian bulan depan", 0),
        
        # Comparison neutral
        ("Sama saja dengan yang lain", 0),
        ("Tidak ada bedanya", 0),
        ("Mirip dengan sebelumnya", 0),
        ("Sebanding dengan harganya", 0),
        ("Setara dengan kompetitor", 0),
        ("Tidak lebih baik atau buruk", 0),
        ("Kurang lebih sama", 0),
        ("Hampir serupa", 0),
        ("Relatif sama", 0),
        ("Comparable dengan yang lain", 0),
        
        # Status updates neutral
        ("Dalam proses pengerjaan", 0),
        ("Masih menunggu konfirmasi", 0),
        ("Sedang dipertimbangkan", 0),
        ("Belum ada keputusan", 0),
        ("On progress", 0),
        ("Pending approval", 0),
        ("Under review", 0),
        ("To be determined", 0),
        ("Akan diinformasikan kemudian", 0),
        ("Status quo", 0)
    ])
    
    return sentences

def test_300_sentences():
    """Test VADER Indonesia with 300 sentences"""
    
    analyzer = SentimentIntensityAnalyzer()
    test_data = generate_300_test_sentences()
    
    # Shuffle for randomness
    random.shuffle(test_data)
    
    results = {
        'total': len(test_data),
        'correct': 0,
        'errors': [],
        'by_category': {
            'positive': {'total': 0, 'correct': 0, 'scores': [], 'errors': []},
            'negative': {'total': 0, 'correct': 0, 'scores': [], 'errors': []},
            'neutral': {'total': 0, 'correct': 0, 'scores': [], 'errors': []}
        },
        'confusion_matrix': {
            'positive': {'positive': 0, 'negative': 0, 'neutral': 0},
            'negative': {'positive': 0, 'negative': 0, 'neutral': 0},
            'neutral': {'positive': 0, 'negative': 0, 'neutral': 0}
        }
    }
    
    print("=" * 80)
    print("TESTING 300 INDONESIAN SENTENCES")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Sentences: {len(test_data)}")
    print("-" * 80)
    
    # Process each sentence
    for i, (sentence, actual_sentiment) in enumerate(test_data, 1):
        scores = analyzer.polarity_scores(sentence)
        
        # Determine predicted sentiment
        if scores['compound'] >= 0.05:
            predicted_sentiment = 1
            predicted_label = 'positive'
        elif scores['compound'] <= -0.05:
            predicted_sentiment = -1
            predicted_label = 'negative'
        else:
            predicted_sentiment = 0
            predicted_label = 'neutral'
        
        # Determine actual label
        if actual_sentiment == 1:
            actual_label = 'positive'
        elif actual_sentiment == -1:
            actual_label = 'negative'
        else:
            actual_label = 'neutral'
        
        # Update category totals
        results['by_category'][actual_label]['total'] += 1
        results['by_category'][actual_label]['scores'].append(scores['compound'])
        
        # Update confusion matrix
        results['confusion_matrix'][actual_label][predicted_label] += 1
        
        # Check if prediction is correct
        is_correct = predicted_sentiment == actual_sentiment
        
        if is_correct:
            results['correct'] += 1
            results['by_category'][actual_label]['correct'] += 1
        else:
            error_info = {
                'sentence': sentence,
                'actual': actual_label,
                'predicted': predicted_label,
                'compound_score': scores['compound'],
                'full_scores': scores
            }
            results['errors'].append(error_info)
            results['by_category'][actual_label]['errors'].append(error_info)
        
        # Progress indicator
        if i % 50 == 0:
            print(f"Processed {i}/{len(test_data)} sentences...")
    
    # Calculate overall accuracy
    results['accuracy'] = (results['correct'] / results['total']) * 100
    
    # Calculate per-category accuracy
    for category in ['positive', 'negative', 'neutral']:
        cat_data = results['by_category'][category]
        if cat_data['total'] > 0:
            cat_data['accuracy'] = (cat_data['correct'] / cat_data['total']) * 100
            cat_data['avg_score'] = sum(cat_data['scores']) / len(cat_data['scores'])
            cat_data['min_score'] = min(cat_data['scores'])
            cat_data['max_score'] = max(cat_data['scores'])
    
    return results

def print_analysis(results):
    """Print detailed analysis of results"""
    
    print("\n" + "=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    
    # Overall Results
    print(f"\n📊 OVERALL PERFORMANCE")
    print("-" * 40)
    print(f"Total Sentences: {results['total']}")
    print(f"Correct Predictions: {results['correct']}")
    print(f"Errors: {results['total'] - results['correct']}")
    print(f"ACCURACY: {results['accuracy']:.2f}%")
    
    # Category Performance
    print(f"\n📈 PERFORMANCE BY CATEGORY")
    print("-" * 40)
    print(f"{'Category':<10} {'Accuracy':<10} {'Correct':<12} {'Avg Score':<12} {'Score Range'}")
    print("-" * 70)
    
    for category in ['positive', 'negative', 'neutral']:
        cat_data = results['by_category'][category]
        if cat_data['total'] > 0:
            score_range = f"[{cat_data['min_score']:.2f}, {cat_data['max_score']:.2f}]"
            print(f"{category.upper():<10} {cat_data['accuracy']:>6.1f}%   {cat_data['correct']:>3}/{cat_data['total']:<3}      "
                  f"{cat_data['avg_score']:>+7.3f}      {score_range}")
    
    # Confusion Matrix
    print(f"\n📋 CONFUSION MATRIX")
    print("-" * 40)
    print(f"{'Actual↓/Predicted→':<20} {'POSITIVE':<12} {'NEGATIVE':<12} {'NEUTRAL':<12}")
    print("-" * 56)
    
    for actual in ['positive', 'negative', 'neutral']:
        row = results['confusion_matrix'][actual]
        total = sum(row.values())
        print(f"{actual.upper():<20} {row['positive']:>8} ({row['positive']/total*100:>5.1f}%)  "
              f"{row['negative']:>8} ({row['negative']/total*100:>5.1f}%)  "
              f"{row['neutral']:>8} ({row['neutral']/total*100:>5.1f}%)")
    
    # Error Analysis
    print(f"\n❌ ERROR ANALYSIS")
    print("-" * 40)
    
    # Most common error types
    error_types = {}
    for error in results['errors']:
        error_type = f"{error['actual']} → {error['predicted']}"
        if error_type not in error_types:
            error_types[error_type] = 0
        error_types[error_type] += 1
    
    print("Error Types Distribution:")
    for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(results['errors'])) * 100
        print(f"  {error_type:<20}: {count:>3} ({percentage:>5.1f}%)")
    
    # Sample errors from each category
    print(f"\n📝 SAMPLE ERRORS (First 3 from each category)")
    print("-" * 40)
    
    for category in ['positive', 'negative', 'neutral']:
        cat_errors = results['by_category'][category]['errors'][:3]
        if cat_errors:
            print(f"\n{category.upper()} sentences misclassified:")
            for error in cat_errors:
                print(f"  • \"{error['sentence'][:60]}...\"")
                print(f"    Expected: {error['actual']}, Got: {error['predicted']}, Score: {error['compound_score']:+.3f}")
    
    # Statistical Summary
    print(f"\n📊 STATISTICAL SUMMARY")
    print("-" * 40)
    
    # Calculate precision, recall, F1 for each class
    for category in ['positive', 'negative', 'neutral']:
        tp = results['confusion_matrix'][category][category]
        fp = sum(results['confusion_matrix'][other][category] 
                for other in ['positive', 'negative', 'neutral'] if other != category)
        fn = sum(results['confusion_matrix'][category][other] 
                for other in ['positive', 'negative', 'neutral'] if other != category)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"\n{category.upper()}:")
        print(f"  Precision: {precision:.3f}")
        print(f"  Recall: {recall:.3f}")
        print(f"  F1-Score: {f1:.3f}")
    
    # Final Assessment
    print(f"\n" + "=" * 80)
    print("FINAL ASSESSMENT")
    print("=" * 80)
    
    if results['accuracy'] >= 95:
        print("🎯 EXCELLENT! Accuracy exceeds 95% target!")
        grade = "A+"
    elif results['accuracy'] >= 90:
        print("✅ VERY GOOD! Accuracy is between 90-95%")
        grade = "A"
    elif results['accuracy'] >= 85:
        print("👍 GOOD! Accuracy is between 85-90%")
        grade = "B+"
    elif results['accuracy'] >= 80:
        print("📈 DECENT! Accuracy is between 80-85%")
        grade = "B"
    else:
        print("⚠️ NEEDS IMPROVEMENT! Accuracy is below 80%")
        grade = "C"
    
    print(f"\nGrade: {grade}")
    print(f"Overall Accuracy: {results['accuracy']:.2f}%")
    
    # Save results to JSON
    save_results = {
        'timestamp': datetime.now().isoformat(),
        'total_sentences': results['total'],
        'correct_predictions': results['correct'],
        'accuracy': results['accuracy'],
        'category_performance': {
            cat: {
                'accuracy': results['by_category'][cat]['accuracy'] if results['by_category'][cat]['total'] > 0 else 0,
                'total': results['by_category'][cat]['total'],
                'correct': results['by_category'][cat]['correct']
            }
            for cat in ['positive', 'negative', 'neutral']
        },
        'confusion_matrix': results['confusion_matrix'],
        'error_count': len(results['errors'])
    }
    
    with open('test_results_300.json', 'w', encoding='utf-8') as f:
        json.dump(save_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to test_results_300.json")
    
    return results['accuracy']

if __name__ == "__main__":
    print("Starting comprehensive 300-sentence test...")
    print("This may take a few moments...\n")
    
    results = test_300_sentences()
    final_accuracy = print_analysis(results)
    
    print(f"\n" + "=" * 80)
    print(f"🏁 TEST COMPLETE")
    print(f"Final Accuracy: {final_accuracy:.2f}%")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)