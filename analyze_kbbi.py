#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import defaultdict

def load_kbbi_words():
    """Load words from KBBI files"""
    words = set()
    
    # Load from the latest version
    with open('/tmp/kumpulan-kata-bahasa-indonesia-KBBI/list_1.0.0.txt', 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if word and len(word) > 2:  # Skip very short words
                words.add(word)
    
    print(f"Loaded {len(words)} unique words from KBBI")
    return words

def categorize_sentiment_words(words):
    """Categorize words based on sentiment patterns"""
    
    # Sentiment patterns for Indonesian words
    positive_patterns = [
        # Prefix patterns
        r'^mem(bahagia|banggakan|bantu|bela|berkat|beri|besarkan)',
        r'^me(muji|mulia|naik|nikmat|nyaman|nang)',
        r'^ber(bahagia|hasil|jaya|kat|manfaat|untung|kembang)',
        r'^ter(baik|bagus|hebat|indah|padu|tinggi|puji)',
        
        # Root word patterns - Positive
        r'(senang|gembira|suka|cinta|kasih|sayang)',
        r'(baik|bagus|hebat|keren|mantap|super)',
        r'(indah|cantik|elok|permai|asri)',
        r'(pintar|cerdas|pandai|bijak|arif)',
        r'(sukses|berhasil|jaya|menang|unggul)',
        r'(sehat|segar|bugar|prima|fit)',
        r'(aman|tenteram|damai|rukun|harmonis)',
        r'(mudah|gampang|lancar|mulus)',
        r'(murah|hemat|untung|laba|surplus)',
        r'(bersih|rapi|teratur|tertib)',
        r'(rajin|tekun|ulet|gigih)',
        r'(berani|gagah|perkasa|tangguh)',
        r'(ramah|sopan|santun|baik\shati)',
        r'(makmur|sejahtera|kaya|berlimpah)',
        r'(nikmat|lezat|enak|sedap|gurih)',
        r'(harum|wangi|semerbak)',
        r'(cepat|kilat|sigap|tangkas)',
        r'(baru|segar|modern|mutakhir)',
        r'(mewah|megah|istana|elit)',
        r'(sempurna|ideal|prima|utama)',
        
        # Suffix patterns  
        r'(an|kan|i).*(bahagia|senang|suka|cinta)',
    ]
    
    negative_patterns = [
        # Prefix patterns
        r'^mem(benci|babi\sbuta|bahayakan|binasakan|bodoh)',
        r'^me(rusak|rugikan|nyakitkan|nangis|ngecewakan)',
        r'^ter(buruk|jelek|hina|luka|sakit|susah)',
        
        # Root word patterns - Negative
        r'(sedih|duka|susah|sulit|sengsara|derita)',
        r'(buruk|jelek|busuk|rusak|hancur)',
        r'(benci|dengki|iri|dendam|marah|kesal)',
        r'(bodoh|dungu|tolol|goblok|bebal|bego)',
        r'(jahat|kejam|keji|bengis|biadab|zalim)',
        r'(gagal|kalah|rugi|bangkrut|jatuh)',
        r'(sakit|luka|nyeri|pedih|perih)',
        r'(takut|cemas|gelisah|panik|gugup)',
        r'(kotor|jorok|kumuh|dekil)',
        r'(malas|males|enggan|ogah)',
        r'(sulit|susah|rumit|ruwet|pelik)',
        r'(mahal|boros|rugi|bangkrut)',
        r'(bahaya|ancam|risiko|bencana)',
        r'(lemah|loyo|lemas|letih|lesu)',
        r'(mati|tewas|wafat|meninggal)',
        r'(bau|busuk|amis|apek|pesing)',
        r'(lambat|lelet|telat|terlambat)',
        r'(lama|usang|basi|kuno)',
        r'(miskin|papa|melarat|fakir)',
        r'(hina|rendah|nista|aib)',
        r'(sia-sia|mubazir|percuma)',
        r'(palsu|bohong|dusta|tipu)',
        r'(bingung|kacau|kusut|berantakan)',
    ]
    
    # Words that should be boosters/dampeners
    booster_patterns = [
        r'^(sangat|amat|sungguh|benar|betul|banget|sekali|nian)',
        r'^(ter|paling|maha|serba|se)',
        r'^(terlalu|kelewat|keterlaluan)',
        r'^(super|ultra|mega|ekstra)',
    ]
    
    categorized = {
        'positive': [],
        'negative': [],
        'booster': [],
        'neutral': []
    }
    
    for word in words:
        # Check if word matches positive patterns
        is_positive = any(re.search(pattern, word) for pattern in positive_patterns)
        
        # Check if word matches negative patterns  
        is_negative = any(re.search(pattern, word) for pattern in negative_patterns)
        
        # Check if word is a booster
        is_booster = any(re.search(pattern, word) for pattern in booster_patterns)
        
        if is_booster:
            categorized['booster'].append(word)
        elif is_positive and not is_negative:
            categorized['positive'].append(word)
        elif is_negative and not is_positive:
            categorized['negative'].append(word)
        # Skip neutral words for now (too many)
    
    return categorized

def filter_relevant_words(categorized):
    """Filter to keep only the most relevant sentiment words"""
    
    # Additional specific words to include
    additional_positive = [
        'afiat', 'akrab', 'amanah', 'ampuh', 'anggun', 'antusias',
        'apik', 'asyik', 'asoy', 'bahagia', 'berjaya', 'berkah',
        'bestari', 'bijaksana', 'brilian', 'cakap', 'cemerlang', 'cermat',
        'cerah', 'ceria', 'dahsyat', 'dinamis', 'efektif', 'efisien',
        'elegan', 'energik', 'fantastis', 'fenomenal', 'gembira', 'gemilang',
        'gesit', 'handal', 'harmoni', 'ikhlas', 'inovatif', 'inspiratif',
        'istimewa', 'jempolan', 'jujur', 'juara', 'kompeten', 'kreatif',
        'lincah', 'loyal', 'mahir', 'makbul', 'maksimal', 'menarik',
        'menawan', 'mengagumkan', 'mengesankan', 'mentereng', 'meriah', 'modern',
        'mujarab', 'mulia', 'optimal', 'optimis', 'pahlawan', 'patut',
        'piawai', 'positif', 'prestisius', 'prima', 'produktif', 'profesional',
        'progresif', 'ramah', 'riang', 'romantis', 'sakti', 'saleh',
        'sejuk', 'semangat', 'solutif', 'spektakuler', 'stabil', 'subur',
        'sukacita', 'syahdu', 'takjub', 'tawadhu', 'tegas', 'teladan',
        'teliti', 'tenang', 'terbaik', 'terbaru', 'tercinta', 'terdepan',
        'terkemuka', 'terpadu', 'terpercaya', 'terpilih', 'tersohor', 'tertinggi',
        'teruji', 'terampil', 'trendy', 'tulus', 'tuntas', 'ulung',
        'unggul', 'unik', 'utama', 'valid', 'visioner', 'wahid',
        'wibawa', 'yakin', 'yakjud', 'zuhud'
    ]
    
    additional_negative = [
        'abai', 'absurd', 'acuh', 'aib', 'ambruk', 'amburadul',
        'anarkis', 'angkuh', 'aral', 'arogan', 'bakhil', 'banal',
        'bandel', 'bangsat', 'basi', 'bebal', 'bebel', 'belingsatan',
        'bejat', 'bengal', 'bengis', 'berantakan', 'berisik', 'bimbang',
        'bobrok', 'bodoh', 'bohong', 'bosan', 'brutal', 'bubar',
        'buncah', 'buntu', 'buruk', 'busuk', 'cabul', 'cacat',
        'cacad', 'candu', 'celaka', 'cemar', 'cemas', 'cengeng',
        'congkak', 'curang', 'dekil', 'dengki', 'dosa', 'durhaka',
        'dzalim', 'egois', 'fana', 'fasik', 'fatal', 'fitnah',
        'frustasi', 'gaduh', 'ganas', 'gawat', 'geram', 'gersang',
        'gondok', 'gusar', 'hambar', 'hampa', 'hancur', 'haram',
        'heran', 'hina', 'hoax', 'iblis', 'jahil', 'jail',
        'jelek', 'jengkel', 'jijik', 'jorok', 'kafir', 'kacau',
        'kalut', 'kandas', 'kasar', 'keji', 'kelam', 'keliru',
        'keruh', 'khianat', 'khilaf', 'kikir', 'korupsi', 'kumuh',
        'kufur', 'kusam', 'kusut', 'labil', 'lacur', 'laknat',
        'lalai', 'lambat', 'lancung', 'leceh', 'lecet', 'lelah',
        'lemah', 'lengah', 'lesu', 'licik', 'luka', 'lumpur',
        'lunglai', 'makar', 'maki', 'maksiat', 'malang', 'malas',
        'mampus', 'maruk', 'masam', 'merana', 'mubazir', 'muak',
        'muram', 'murka', 'musibah', 'mustahil', 'nahas', 'nakal',
        'najis', 'nestapa', 'ngawur', 'nisbi', 'nista', 'ompong',
        'panik', 'papa', 'parno', 'payah', 'pecah', 'pedih',
        'pelit', 'pengecut', 'penyakit', 'pesimis', 'picik', 'pilu',
        'punah', 'pupus', 'pucat', 'racun', 'ragu', 'rancu',
        'rapuh', 'retak', 'resah', 'ricuh', 'ringkih', 'risau',
        'rongsokan', 'rosak', 'rumit', 'runtuh', 'rusuh', 'ruwet',
        'sadis', 'salah', 'saru', 'sedih', 'segan', 'sepi',
        'seram', 'serampangan', 'sesak', 'sesat', 'sial', 'sialan',
        'sia-sia', 'sinting', 'sombong', 'stagnan', 'stress', 'sumbang',
        'sumpek', 'sundal', 'suram', 'susah', 'syirik', 'takabur',
        'tandus', 'tawar', 'tegang', 'tengik', 'tepuk', 'terbelakang',
        'terlantar', 'terpuruk', 'tertinggal', 'timpang', 'tolol', 'tragis',
        'tua', 'tumpul', 'tunggang', 'usang', 'uzur', 'waswas',
        'yatim', 'zalim', 'zina', 'zonk'
    ]
    
    # Combine with categorized words
    final_positive = list(set(categorized['positive'] + additional_positive))
    final_negative = list(set(categorized['negative'] + additional_negative))
    
    return {
        'positive': sorted(final_positive),
        'negative': sorted(final_negative),
        'booster': sorted(categorized['booster'])
    }

def main():
    print("Loading KBBI words...")
    words = load_kbbi_words()
    
    print("\nCategorizing words by sentiment...")
    categorized = categorize_sentiment_words(words)
    
    print("\nFiltering relevant sentiment words...")
    filtered = filter_relevant_words(categorized)
    
    print(f"\nResults:")
    print(f"Positive words: {len(filtered['positive'])}")
    print(f"Negative words: {len(filtered['negative'])}")
    print(f"Booster words: {len(filtered['booster'])}")
    
    # Save to files for review
    with open('kbbi_positive.txt', 'w', encoding='utf-8') as f:
        for word in filtered['positive']:
            f.write(f"{word}\n")
    
    with open('kbbi_negative.txt', 'w', encoding='utf-8') as f:
        for word in filtered['negative']:
            f.write(f"{word}\n")
    
    with open('kbbi_booster.txt', 'w', encoding='utf-8') as f:
        for word in filtered['booster']:
            f.write(f"{word}\n")
    
    print("\nFiles saved: kbbi_positive.txt, kbbi_negative.txt, kbbi_booster.txt")
    
    return filtered

if __name__ == "__main__":
    sentiment_words = main()