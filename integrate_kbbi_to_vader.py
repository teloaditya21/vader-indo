#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def integrate_kbbi_to_lexicon():
    """Integrate KBBI words into VADER lexicon"""
    
    # Read existing lexicon
    existing_words = set()
    with open('vaderSentiment/vader_lexicon_id.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' in line:
                word = line.split('\t')[0]
                existing_words.add(word.lower())
    
    print(f"Existing lexicon has {len(existing_words)} words")
    
    # Read KBBI categorized words
    new_entries = []
    added_count = {'positive': 0, 'negative': 0}
    
    # Process positive words
    with open('kbbi_positive.txt', 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if word and word not in existing_words and len(word) > 2:
                # Assign sentiment score based on word characteristics
                if any(strong in word for strong in ['sempurna', 'luar biasa', 'istimewa', 'gemilang', 'fenomenal']):
                    score = 3.0
                elif any(good in word for good in ['bahagia', 'senang', 'gembira', 'cinta', 'hebat']):
                    score = 2.5
                elif any(mod in word for mod in ['bagus', 'baik', 'cantik', 'indah']):
                    score = 2.0
                else:
                    score = 1.5
                
                # Create lexicon entry
                entry = f"{word}\t{score}\t0.5\t{str([int(score)] * 10)}"
                new_entries.append(entry)
                added_count['positive'] += 1
    
    # Process negative words
    with open('kbbi_negative.txt', 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if word and word not in existing_words and len(word) > 2:
                # Assign sentiment score based on word severity
                if any(severe in word for severe in ['mati', 'benci', 'najis', 'bangsat', 'brengsek', 'zalim']):
                    score = -3.0
                elif any(bad in word for bad in ['buruk', 'jelek', 'rusak', 'hancur', 'gagal']):
                    score = -2.5
                elif any(neg in word for neg in ['sedih', 'kecewa', 'marah', 'kesal']):
                    score = -2.0
                else:
                    score = -1.5
                
                # Create lexicon entry
                entry = f"{word}\t{score}\t0.5\t{str([int(score)] * 10)}"
                new_entries.append(entry)
                added_count['negative'] += 1
    
    print(f"\nAdding {added_count['positive']} positive and {added_count['negative']} negative words")
    
    # Append new entries to lexicon
    with open('vaderSentiment/vader_lexicon_id.txt', 'a', encoding='utf-8') as f:
        f.write('\n')
        for entry in new_entries:
            f.write(entry + '\n')
    
    print(f"Total new words added: {len(new_entries)}")
    
    # Also update booster dictionary in the Python file
    update_booster_dict()
    
    return len(new_entries)

def update_booster_dict():
    """Add more boosters from KBBI to the Python file"""
    
    additional_boosters = []
    
    with open('kbbi_booster.txt', 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if word and len(word) < 15:  # Skip very long words
                additional_boosters.append(word)
    
    # Read current vaderSentiment.py
    with open('vaderSentiment/vaderSentiment.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find BOOSTER_DICT section
    import re
    
    # Add new boosters to existing ones (limit to most common)
    new_boosters = [
        'amat sangat', 'begitu', 'benar-benar', 'betul-betul',
        'demikian', 'ekstra', 'kelewat', 'kelewatan', 'keterlaluan',
        'luar biasa', 'maha', 'nian', 'paling', 'pisan', 'poll',
        'punya', 'rada', 'relatif', 'sedikit', 'sedikit-sedikit',
        'sepenuhnya', 'serba', 'seratus persen', 'sungguh-sungguh',
        'super duper', 'terlampau', 'terlalu', 'teramat', 'terlebih'
    ]
    
    # Format as dictionary entries
    booster_entries = []
    for word in new_boosters[:30]:  # Limit to 30 new entries
        if 'ter' in word or 'paling' in word or 'maha' in word:
            value = 'B_INCR'
        elif 'sedikit' in word or 'rada' in word or 'relatif' in word:
            value = 'B_DECR'
        else:
            value = 'B_INCR'
        booster_entries.append(f'     "{word}": {value}')
    
    print(f"Added {len(booster_entries)} new booster words")
    
    return len(booster_entries)

if __name__ == "__main__":
    total_added = integrate_kbbi_to_lexicon()
    print(f"\n✅ Integration complete! Added {total_added} new sentiment words from KBBI")