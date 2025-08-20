#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import csv
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

def extract_words_from_all_sources():
    """Extract words from all 7 KBBI sources"""
    
    all_words = set()
    source_stats = {}
    
    # Source 1: kbbi-qt (CSV file)
    print("Processing Source 1: kbbi-qt...")
    try:
        with open('/tmp/kbbi1/data-src/kbbi_data.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            words_s1 = set()
            for row in reader:
                if row and len(row) > 0:
                    word = row[0].lower().strip()
                    if word and len(word) > 1:
                        words_s1.add(word)
                        all_words.add(word)
            source_stats['kbbi-qt'] = len(words_s1)
            print(f"  Found {len(words_s1)} words")
    except Exception as e:
        print(f"  Error: {e}")
        source_stats['kbbi-qt'] = 0
    
    # Source 2: rizaumami/kbbi (TXT files A-Z)
    print("Processing Source 2: rizaumami/kbbi...")
    words_s2 = set()
    txt_dir = '/tmp/kbbi2/teks/hasil_akhir/'
    if os.path.exists(txt_dir):
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            txt_file = os.path.join(txt_dir, f'{letter}.txt')
            if os.path.exists(txt_file):
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            # Extract word from definition format
                            if line.strip():
                                parts = line.strip().split(None, 1)
                                if parts:
                                    word = parts[0].lower().strip()
                                    if word and len(word) > 1 and word.isalpha():
                                        words_s2.add(word)
                                        all_words.add(word)
                except:
                    pass
    source_stats['rizaumami'] = len(words_s2)
    print(f"  Found {len(words_s2)} words")
    
    # Source 3: damzaky (already processed)
    print("Processing Source 3: damzaky...")
    words_s3 = set()
    try:
        with open('/tmp/kumpulan-kata-bahasa-indonesia-KBBI/list_1.0.0.txt', 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                if word and len(word) > 1:
                    words_s3.add(word)
                    all_words.add(word)
    except:
        pass
    source_stats['damzaky'] = len(words_s3)
    print(f"  Found {len(words_s3)} words")
    
    # Source 4: muzavan/KBBI-Crawling
    print("Processing Source 4: KBBI-Crawling...")
    words_s4 = set()
    crawl_dir = '/tmp/kbbi4'
    if os.path.exists(crawl_dir):
        for root, dirs, files in os.walk(crawl_dir):
            for file in files:
                if file.endswith('.txt') or file.endswith('.json'):
                    try:
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Extract Indonesian words
                            words = re.findall(r'\b[a-z]+\b', content.lower())
                            for word in words:
                                if len(word) > 1 and len(word) < 20:
                                    words_s4.add(word)
                                    all_words.add(word)
                    except:
                        pass
    source_stats['KBBI-Crawling'] = len(words_s4)
    print(f"  Found {len(words_s4)} words")
    
    # Source 5: bbn-bernard/kbbi_dataset
    print("Processing Source 5: kbbi_dataset...")
    words_s5 = set()
    dataset_files = ['/tmp/kbbi5/kbbi_dataset.txt', '/tmp/kbbi5/data.txt', '/tmp/kbbi5/kbbi.txt']
    for filepath in dataset_files:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip().lower()
                        if word and len(word) > 1:
                            words_s5.add(word)
                            all_words.add(word)
            except:
                pass
    source_stats['kbbi_dataset'] = len(words_s5)
    print(f"  Found {len(words_s5)} words")
    
    # Source 6: bekicot/indonesian_words
    print("Processing Source 6: indonesian_words...")
    words_s6 = set()
    iw_dir = '/tmp/kbbi6'
    if os.path.exists(iw_dir):
        for root, dirs, files in os.walk(iw_dir):
            for file in files:
                if file.endswith(('.txt', '.csv', '.json')):
                    try:
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            for line in f:
                                # Try to extract words
                                words = re.findall(r'\b[a-z]+\b', line.lower())
                                for word in words:
                                    if len(word) > 1 and len(word) < 20:
                                        words_s6.add(word)
                                        all_words.add(word)
                    except:
                        pass
    source_stats['indonesian_words'] = len(words_s6)
    print(f"  Found {len(words_s6)} words")
    
    # Source 7: lufias69/KBBI2
    print("Processing Source 7: KBBI2...")
    words_s7 = set()
    kbbi2_dir = '/tmp/kbbi7'
    if os.path.exists(kbbi2_dir):
        for root, dirs, files in os.walk(kbbi2_dir):
            for file in files:
                if file.endswith(('.txt', '.csv', '.json', '.sql')):
                    try:
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            # Extract Indonesian words
                            words = re.findall(r'\b[a-z]+\b', content.lower())
                            for word in words:
                                if len(word) > 1 and len(word) < 20:
                                    words_s7.add(word)
                                    all_words.add(word)
                    except:
                        pass
    source_stats['KBBI2'] = len(words_s7)
    print(f"  Found {len(words_s7)} words")
    
    print("\n" + "="*50)
    print("SUMMARY:")
    for source, count in source_stats.items():
        print(f"  {source}: {count:,} words")
    print(f"\nTotal unique words: {len(all_words):,}")
    
    return all_words

def categorize_sentiment_words_advanced(words):
    """Advanced categorization of Indonesian words by sentiment"""
    
    # Extended sentiment patterns
    positive_patterns = [
        # Achievement & Success
        r'\b(berhasil|sukses|tercapai|terwujud|menang|juara|prestasi|gemilang|unggul|jaya)\b',
        r'\b(lulus|naik|promosi|terpilih|terbaik|teratas|terdepan|terkemuka|tersohor)\b',
        
        # Positive Emotions
        r'\b(senang|bahagia|gembira|riang|ceria|suka|cinta|kasih|sayang|rindu)\b',
        r'\b(bangga|puas|lega|tenang|damai|tenteram|nyaman|aman|tentram)\b',
        
        # Positive Qualities
        r'\b(bagus|baik|cantik|ganteng|tampan|indah|elok|molek|jelita|rupawan)\b',
        r'\b(pintar|cerdas|pandai|jenius|brilian|genius|mahir|ahli|pakar|piawai)\b',
        r'\b(kuat|tangguh|perkasa|gagah|berani|heroik|jantan|kesatria)\b',
        r'\b(rajin|tekun|ulet|giat|semangat|antusias|bersemangat|bergairah)\b',
        
        # Positive States
        r'\b(sehat|segar|bugar|fit|prima|optimal|maksimal|sempurna|ideal)\b',
        r'\b(bersih|rapi|teratur|tertib|apik|necis|kinclong|mengkilap)\b',
        r'\b(mewah|megah|glamor|elit|eksklusif|premium|berkelas|mentereng)\b',
        
        # Positive Actions
        r'\b(membantu|menolong|mendukung|menyokong|membangun|memperbaiki|meningkatkan)\b',
        r'\b(melindungi|menjaga|merawat|memelihara|menyelamatkan|mengatasi)\b',
        r'\b(menghargai|menghormati|memuji|mengagumi|menyanjung)\b',
        
        # Food & Taste Positive
        r'\b(enak|lezat|nikmat|sedap|gurih|mantap|maknyus|nendang|nagih)\b',
        r'\b(segar|fresh|crispy|renyah|empuk|lembut|pulen)\b',
        
        # Modern Positive
        r'\b(keren|cool|gaul|hits|viral|trending|populer|terkenal|fenomenal)\b',
        r'\b(canggih|modern|mutakhir|terkini|terbaru|inovatif|kreatif)\b'
    ]
    
    negative_patterns = [
        # Failure & Loss
        r'\b(gagal|kalah|rugi|bangkrut|jatuh|terpuruk|hancur|musnah|punah)\b',
        r'\b(hilang|lenyap|raib|sirna|lesap|kehilangan|kehabisan)\b',
        
        # Negative Emotions
        r'\b(sedih|duka|murung|muram|suram|galau|gundah|gulana|nelangsa)\b',
        r'\b(marah|kesal|jengkel|dongkol|sebal|benci|dendam|dengki|iri)\b',
        r'\b(takut|cemas|khawatir|waswas|gelisah|resah|gugup|grogi|panik)\b',
        r'\b(kecewa|menyesal|sesal|getir|pilu|pedih|perih|sakit)\b',
        
        # Negative Qualities
        r'\b(buruk|jelek|rusak|busuk|basi|lapuk|kropos|bobrok|reyot)\b',
        r'\b(bodoh|dungu|tolol|goblok|idiot|bego|pandir|bebal)\b',
        r'\b(lemah|lemas|loyo|letih|lesu|lelah|capek|payah)\b',
        r'\b(malas|pemalas|mager|ogah|enggan|segan)\b',
        
        # Negative States
        r'\b(sakit|nyeri|demam|flu|batuk|pilek|luka|cedera|cacat)\b',
        r'\b(kotor|jorok|kumuh|dekil|comberan|sampah|kotoran)\b',
        r'\b(miskin|melarat|papa|fakir|gembel|pengemis)\b',
        
        # Negative Actions
        r'\b(membunuh|menyakiti|melukai|memukul|menendang|menampar)\b',
        r'\b(mencuri|merampok|mencopet|menipu|membohongi|memperdaya)\b',
        r'\b(menghina|mencaci|memaki|mengejek|merendahkan|melecehkan)\b',
        
        # Problems & Issues
        r'\b(masalah|problem|kendala|hambatan|rintangan|halangan|gangguan)\b',
        r'\b(error|bug|crash|hang|lag|lemot|macet|stuck|mandek)\b',
        r'\b(bahaya|ancaman|risiko|bencana|musibah|malapetaka|tragedi)\b',
        
        # Negative Behavior
        r'\b(nakal|bandel|jail|iseng|usil|rewel|cengeng|manja)\b',
        r'\b(sombong|angkuh|congkak|takabur|arogan|tinggi\shati)\b',
        r'\b(kikir|pelit|bakhil|tamak|rakus|serakah)\b',
        
        # Crime & Violence
        r'\b(kriminal|kejahatan|korupsi|kolusi|nepotisme|mafia|preman)\b',
        r'\b(kekerasan|perkosaan|pembunuhan|perampokan|pencurian)\b'
    ]
    
    # Booster patterns
    booster_patterns = [
        r'^(sangat|amat|sungguh|benar|betul|banget|sekali|nian)$',
        r'^(ter|paling|maha|serba|se|super|ultra|mega|ekstra)$',
        r'^(terlalu|kelewat|keterlaluan|terlampau|teramat)$'
    ]
    
    categorized = {
        'positive': [],
        'negative': [],
        'booster': [],
        'potential_positive': [],
        'potential_negative': []
    }
    
    for word in words:
        word_lower = word.lower()
        
        # Check boosters first
        is_booster = any(re.match(pattern, word_lower) for pattern in booster_patterns)
        if is_booster:
            categorized['booster'].append(word)
            continue
        
        # Check positive
        is_positive = any(re.search(pattern, word_lower) for pattern in positive_patterns)
        
        # Check negative
        is_negative = any(re.search(pattern, word_lower) for pattern in negative_patterns)
        
        if is_positive and not is_negative:
            categorized['positive'].append(word)
        elif is_negative and not is_positive:
            categorized['negative'].append(word)
        elif is_positive and is_negative:
            # Words that could be both - need context
            if 'tidak' not in word_lower and 'bukan' not in word_lower:
                categorized['potential_positive'].append(word)
        
        # Check for potential sentiment words using prefix/suffix
        elif word_lower.startswith(('ke', 'pe', 'ter', 'ber', 'me')):
            # Check if it might be sentiment-bearing
            if any(root in word_lower for root in ['bahagia', 'sedih', 'senang', 'susah', 'baik', 'buruk']):
                if any(pos in word_lower for pos in ['bahagia', 'senang', 'baik', 'bagus', 'indah']):
                    categorized['potential_positive'].append(word)
                elif any(neg in word_lower for neg in ['sedih', 'susah', 'buruk', 'jelek']):
                    categorized['potential_negative'].append(word)
    
    return categorized

def create_comprehensive_lexicon(categorized_words):
    """Create comprehensive lexicon entries for new words"""
    
    new_entries = []
    
    # Process positive words
    for word in categorized_words['positive'][:1000]:  # Limit to top 1000
        # Assign scores based on word intensity
        if any(strong in word for strong in ['luar biasa', 'dahsyat', 'spektakuler', 'fenomenal']):
            score = 3.0
        elif any(good in word for good in ['bahagia', 'gemilang', 'sempurna', 'istimewa']):
            score = 2.5
        elif any(moderate in word for moderate in ['bagus', 'baik', 'senang', 'suka']):
            score = 2.0
        else:
            score = 1.5
        
        entry = f"{word}\t{score}\t0.5\t{str([int(score)] * 10)}"
        new_entries.append(entry)
    
    # Process negative words
    for word in categorized_words['negative'][:1000]:  # Limit to top 1000
        # Assign scores based on severity
        if any(severe in word for severe in ['mati', 'bunuh', 'hancur', 'musnah', 'bencana']):
            score = -3.0
        elif any(bad in word for bad in ['buruk', 'jelek', 'rusak', 'gagal', 'kalah']):
            score = -2.5
        elif any(moderate in word for moderate in ['sedih', 'kecewa', 'marah', 'kesal']):
            score = -2.0
        else:
            score = -1.5
        
        entry = f"{word}\t{score}\t0.5\t{str([int(score)] * 10)}"
        new_entries.append(entry)
    
    # Process potential words with lower scores
    for word in categorized_words['potential_positive'][:500]:
        score = 1.0
        entry = f"{word}\t{score}\t0.5\t{str([1] * 10)}"
        new_entries.append(entry)
    
    for word in categorized_words['potential_negative'][:500]:
        score = -1.0
        entry = f"{word}\t{score}\t0.5\t{str([-1] * 10)}"
        new_entries.append(entry)
    
    return new_entries

def main():
    print("="*60)
    print("COMPREHENSIVE KBBI INTEGRATION")
    print("="*60)
    
    # Step 1: Extract all words
    print("\n1. Extracting words from all sources...")
    all_words = extract_words_from_all_sources()
    
    # Step 2: Load existing lexicon to avoid duplicates
    print("\n2. Loading existing lexicon...")
    existing_words = set()
    try:
        with open('vaderSentiment/vader_lexicon_id.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if '\t' in line:
                    word = line.split('\t')[0].lower()
                    existing_words.add(word)
        print(f"   Existing lexicon has {len(existing_words)} words")
    except:
        print("   Could not load existing lexicon")
    
    # Step 3: Filter new words only
    new_words = all_words - existing_words
    print(f"\n3. Found {len(new_words):,} new unique words")
    
    # Step 4: Categorize words
    print("\n4. Categorizing words by sentiment...")
    categorized = categorize_sentiment_words_advanced(new_words)
    
    print(f"   Positive: {len(categorized['positive']):,}")
    print(f"   Negative: {len(categorized['negative']):,}")
    print(f"   Booster: {len(categorized['booster']):,}")
    print(f"   Potential Positive: {len(categorized['potential_positive']):,}")
    print(f"   Potential Negative: {len(categorized['potential_negative']):,}")
    
    # Step 5: Create lexicon entries
    print("\n5. Creating lexicon entries...")
    new_entries = create_comprehensive_lexicon(categorized)
    print(f"   Created {len(new_entries)} new entries")
    
    # Step 6: Save to file
    output_file = 'kbbi_comprehensive_additions.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in new_entries:
            f.write(entry + '\n')
    
    print(f"\n6. Saved to {output_file}")
    
    # Step 7: Save word lists for review
    with open('kbbi_positive_words.txt', 'w', encoding='utf-8') as f:
        for word in sorted(categorized['positive'][:500]):
            f.write(word + '\n')
    
    with open('kbbi_negative_words.txt', 'w', encoding='utf-8') as f:
        for word in sorted(categorized['negative'][:500]):
            f.write(word + '\n')
    
    print("\n7. Saved word lists for review:")
    print("   - kbbi_positive_words.txt")
    print("   - kbbi_negative_words.txt")
    
    return len(new_entries)

if __name__ == "__main__":
    total_added = main()
    print("\n" + "="*60)
    print(f"✅ COMPLETE! Ready to add {total_added} words to VADER Indonesia")
    print("="*60)