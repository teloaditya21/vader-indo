#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def clean_lexicon():
    """Clean the lexicon file from malformed entries"""
    
    valid_entries = []
    invalid_count = 0
    
    with open('vaderSentiment/vader_lexicon_id.txt', 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            
            # Valid entry should have at least 3 parts: word, score, std_dev
            if len(parts) >= 3:
                word = parts[0]
                
                # Skip if word contains HTML or suspicious characters
                if '<' in word or '>' in word or '&' in word or len(word) > 50:
                    invalid_count += 1
                    continue
                
                # Skip if word is a number
                if word.isdigit():
                    invalid_count += 1
                    continue
                
                try:
                    score = float(parts[1])
                    std_dev = float(parts[2])
                    
                    # Keep valid entry
                    valid_entries.append(line)
                except ValueError:
                    invalid_count += 1
                    continue
            else:
                invalid_count += 1
    
    print(f"Found {len(valid_entries)} valid entries")
    print(f"Removed {invalid_count} invalid entries")
    
    # Write clean lexicon
    with open('vaderSentiment/vader_lexicon_id_clean.txt', 'w', encoding='utf-8') as f:
        for entry in valid_entries:
            f.write(entry + '\n')
    
    # Replace original with clean version
    import shutil
    shutil.move('vaderSentiment/vader_lexicon_id_clean.txt', 'vaderSentiment/vader_lexicon_id.txt')
    
    print("Lexicon cleaned and saved")
    
    return len(valid_entries)

if __name__ == "__main__":
    total = clean_lexicon()
    print(f"Final lexicon size: {total} words")