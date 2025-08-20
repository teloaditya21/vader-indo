# coding: utf-8
# Enhanced VADER for Indonesian with better complex sentence handling

import os
import re
import math
import string
import codecs
from itertools import product
from inspect import getsourcefile
from io import open

# Constants
B_INCR = 0.293
B_DECR = -0.293
C_INCR = 0.733
N_SCALAR = -0.74

# Indonesian Negation Words (Expanded)
NEGATE = [
    "tidak", "tak", "bukan", "bukanlah", "tiada", "tanpa", "belum",
    "jangan", "janganlah", "gak", "ga", "kagak", "engga", "enggak", "ngga", "nggak",
    "ogah", "gamau", "gkmau", "gakmau", "takmau", "takkan", "takada",
    "nihil", "kosong", "hampa", "sia-sia", "percuma", "mustahil",
    "jarang", "langka", "sulit", "susah", "minim", "kurang", "kekurangan",
    "meskipun", "walaupun", "walau", "sekalipun", "kendati", "kendatipun"
]

# Booster/Dampener Words (Enhanced)
BOOSTER_DICT = {
    # Strong boosters
    "sangat": B_INCR, "amat": B_INCR, "sungguh": B_INCR, "benar-benar": B_INCR,
    "betul-betul": B_INCR, "banget": B_INCR, "bgt": B_INCR, "bngt": B_INCR,
    "sekali": B_INCR, "nian": B_INCR, "teramat": B_INCR, "terlalu": B_INCR,
    "kelewat": B_INCR, "kelewatan": B_INCR, "keterlaluan": B_INCR,
    "luar biasa": B_INCR, "luarbiasa": B_INCR, "dahsyat": B_INCR, "hebat": B_INCR,
    "mantap": B_INCR, "mantul": B_INCR, "keren": B_INCR, "gila": B_INCR,
    "parah": B_INCR, "ekstrem": B_INCR, "ekstrim": B_INCR, "maksimal": B_INCR,
    "total": B_INCR, "sepenuhnya": B_INCR, "seutuhnya": B_INCR, "seluruhnya": B_INCR,
    "seratus persen": B_INCR, "100%": B_INCR, "paling": B_INCR, "ter": B_INCR,
    "super": B_INCR, "mega": B_INCR, "ultra": B_INCR, "ekstra": B_INCR,
    "lebih": B_INCR, "makin": B_INCR, "semakin": B_INCR, "kian": B_INCR,
    
    # Dampeners
    "hampir": B_DECR, "nyaris": B_DECR, "agak": B_DECR, "rada": B_DECR,
    "sedikit": B_DECR, "dikit": B_DECR, "cuma": B_DECR, "cuman": B_DECR,
    "hanya": B_DECR, "sekadar": B_DECR, "sekedar": B_DECR, "lumayan": B_DECR,
    "biasa aja": B_DECR, "biasa saja": B_DECR, "standar": B_DECR,
    "kurang": B_DECR, "minim": B_DECR, "tipis": B_DECR, "samar": B_DECR,
    "kadang": B_DECR, "kadang-kadang": B_DECR, "terkadang": B_DECR,
    "sesekali": B_DECR, "jarang": B_DECR, "langka": B_DECR
}

# Conjunction handlers for complex sentences
CONJUNCTIONS = {
    "tapi": -0.5,  # Reverses sentiment
    "tetapi": -0.5,
    "namun": -0.5,
    "akan tetapi": -0.5,
    "meskipun": -0.3,
    "walaupun": -0.3,
    "walau": -0.3,
    "sekalipun": -0.3,
    "kendati": -0.3,
    "padahal": -0.4,
    "sayangnya": -0.4,
    "malah": -0.3,
    "justru": 0.3,
    "bahkan": 0.3,
    "apalagi": 0.3,
    "terlebih": 0.3,
    "dan": 0.1,
    "serta": 0.1,
    "juga": 0.1,
    "atau": 0,
    "maupun": 0.1
}

# Indonesian idioms and special cases (Enhanced)
SENTIMENT_LADEN_IDIOMS = {
    "bintang lapangan": 3, "buah hati": 3, "jantung hati": 3,
    "makan hati": -3, "patah hati": -3, "sakit hati": -3,
    "naik daun": 2, "turun tangan": 2, "angkat tangan": -2,
    "buang muka": -2, "tutup mata": -2, "cuci tangan": -2,
    "darah daging": 2, "tulang punggung": 2, "tangan kanan": 2,
    "kambing hitam": -3, "air mata buaya": -3, "muka tembok": -2,
    "tinggi hati": -2, "besar kepala": -2, "keras kepala": -1,
    "ringan tangan": 2, "panjang tangan": -3, "tangan dingin": 2,
    "tidak apa-apa": 0.5, "tidak masalah": 0.5, "no problem": 0.5,
    "biasa saja": 0, "biasa aja": 0, "nothing special": 0,
    "lumayan lah": 0.3, "lumayan juga": 0.3, "not bad": 0.3
}

SPECIAL_CASES = {
    "mantap jiwa": 3, "keren abis": 3, "gokil abis": 3, "gila bener": 2.5,
    "parah banget": -3, "anjir banget": 2, "goks banget": 2.5,
    "ya kali": -2, "yeu kali": -2, "masa sih": -1.5, "ah masa": -2,
    "bohong banget": -3, "boong ah": -2, "ngaco banget": -3,
    "kacau balau": -3, "berantakan parah": -3, "hancur lebur": -3,
    "top markotop": 3, "joss gandos": 3, "mantul gan": 3,
    "sedih banget": -3, "seneng banget": 3, "bahagia banget": 3,
    "worth it": 2, "worth banget": 2.5, "not worth": -2,
    "on point": 2, "out of date": -1.5, "up to date": 1.5
}

def negated(input_words, include_nt=True):
    """Enhanced negation detection for Indonesian"""
    input_words = [str(w).lower() for w in input_words]
    
    # Check for explicit negation words
    for word in NEGATE:
        if word in input_words:
            return True
    
    # Check for negation patterns
    for i, word in enumerate(input_words):
        # Check prefixes
        if word.startswith(("tidak", "tak", "bukan", "belum")):
            return True
        # Check common informal negations
        if word in ["gak", "ga", "kagak", "engga", "enggak", "ngga", "nggak", "ogah"]:
            return True
        # Check for "tanpa" (without)
        if word == "tanpa":
            return True
            
    return False

def check_double_negative(words_and_emoticons, start_index, end_index):
    """Check for double negatives in Indonesian"""
    neg_count = 0
    for i in range(start_index, min(end_index, len(words_and_emoticons))):
        word = words_and_emoticons[i].lower()
        if word in NEGATE or word.startswith(("tidak", "tak", "bukan")):
            neg_count += 1
    
    # Double negative becomes positive
    return neg_count >= 2

def handle_conjunction(words_and_emoticons, valence_scores):
    """Handle conjunctions that change sentiment flow"""
    new_scores = valence_scores.copy()
    
    for i, word in enumerate(words_and_emoticons):
        word_lower = word.lower()
        
        if word_lower in CONJUNCTIONS:
            conj_weight = CONJUNCTIONS[word_lower]
            
            # Words like "tapi", "tetapi" reverse/dampen previous sentiment
            if conj_weight < 0:
                # Dampen all previous scores
                for j in range(i):
                    if new_scores[j] != 0:
                        new_scores[j] *= abs(conj_weight)
                
                # Boost scores after conjunction
                for j in range(i + 1, len(new_scores)):
                    if new_scores[j] != 0:
                        new_scores[j] *= 1.5
            
            # Words like "dan", "juga" maintain/boost sentiment
            elif conj_weight > 0:
                for j in range(i + 1, len(new_scores)):
                    if new_scores[j] != 0:
                        new_scores[j] *= (1 + conj_weight)
    
    return new_scores

def check_idiom_or_phrase(words_and_emoticons, current_index):
    """Check for multi-word idioms or phrases"""
    text = " ".join(words_and_emoticons).lower()
    
    # Check 3-word phrases
    if current_index <= len(words_and_emoticons) - 3:
        three_word = " ".join(words_and_emoticons[current_index:current_index+3]).lower()
        if three_word in SENTIMENT_LADEN_IDIOMS:
            return SENTIMENT_LADEN_IDIOMS[three_word]
        if three_word in SPECIAL_CASES:
            return SPECIAL_CASES[three_word]
    
    # Check 2-word phrases
    if current_index <= len(words_and_emoticons) - 2:
        two_word = " ".join(words_and_emoticons[current_index:current_index+2]).lower()
        if two_word in SENTIMENT_LADEN_IDIOMS:
            return SENTIMENT_LADEN_IDIOMS[two_word]
        if two_word in SPECIAL_CASES:
            return SPECIAL_CASES[two_word]
    
    return None

class SentiText(object):
    """Enhanced sentiment text processor for Indonesian"""
    
    def __init__(self, text):
        if not isinstance(text, str):
            text = str(text).encode('utf-8')
        self.text = text
        self.words_and_emoticons = self._words_and_emoticons()
        self.is_cap_diff = self._allcap_differential()
    
    def _words_and_emoticons(self):
        """Extract words and emoticons"""
        wes = self.text.split()
        stripped = []
        for word in wes:
            stripped_word = word.strip(string.punctuation)
            if len(stripped_word) <= 2:
                stripped.append(word)  # Keep emoticons
            else:
                stripped.append(stripped_word)
        return stripped
    
    def _allcap_differential(self):
        """Check if some words are in ALL CAPS"""
        allcap_words = sum(1 for w in self.words_and_emoticons if w.isupper())
        cap_differential = len(self.words_and_emoticons) - allcap_words
        return 0 < cap_differential < len(self.words_and_emoticons)

class SentimentIntensityAnalyzer(object):
    """Enhanced VADER for Indonesian complex sentences"""
    
    def __init__(self, lexicon_file="vader_lexicon_id.txt", emoji_lexicon="emoji_utf8_lexicon.txt"):
        _this_module_file_path_ = os.path.abspath(getsourcefile(lambda: 0))
        lexicon_full_filepath = os.path.join(os.path.dirname(_this_module_file_path_), lexicon_file)
        
        with codecs.open(lexicon_full_filepath, encoding='utf-8') as f:
            self.lexicon_full_filepath = f.read()
        
        self.lexicon = self.make_lex_dict()
        
        emoji_full_filepath = os.path.join(os.path.dirname(_this_module_file_path_), emoji_lexicon)
        with codecs.open(emoji_full_filepath, encoding='utf-8') as f:
            self.emoji_full_filepath = f.read()
        
        self.emojis = self.make_emoji_dict()
    
    def make_lex_dict(self):
        """Convert lexicon file to dictionary"""
        lex_dict = {}
        for line in self.lexicon_full_filepath.rstrip('\n').split('\n'):
            if not line:
                continue
            if '\t' in line:
                word, measure = line.strip().split('\t')[0:2]
                lex_dict[word] = float(measure)
        return lex_dict
    
    def make_emoji_dict(self):
        """Convert emoji lexicon to dictionary"""
        emoji_dict = {}
        for line in self.emoji_full_filepath.rstrip('\n').split('\n'):
            if not line:
                continue
            if '\t' in line:
                emoji, description = line.strip().split('\t')[0:2]
                emoji_dict[emoji] = description
        return emoji_dict
    
    def polarity_scores(self, text):
        """Enhanced sentiment scoring for complex Indonesian sentences"""
        
        # Pre-process text
        sentitext = SentiText(text)
        sentiments = []
        words_and_emoticons = sentitext.words_and_emoticons
        
        # Get base sentiment scores
        for i, item in enumerate(words_and_emoticons):
            valence = 0
            
            # Check for idioms first
            idiom_score = check_idiom_or_phrase(words_and_emoticons, i)
            if idiom_score is not None:
                valence = idiom_score
            else:
                # Check lexicon
                if item.lower() in self.lexicon:
                    valence = self.lexicon[item.lower()]
                
                # Check for emojis
                if item in self.emojis:
                    valence = 2.0  # Default positive for emojis
                
                # Apply ALL CAPS boost
                if item.isupper() and sentitext.is_cap_diff and valence != 0:
                    if valence > 0:
                        valence += C_INCR
                    else:
                        valence -= C_INCR
            
            # Check for boosters/dampeners
            if i > 0 and valence != 0:
                prev_word = words_and_emoticons[i-1].lower()
                if prev_word in BOOSTER_DICT:
                    scalar = BOOSTER_DICT[prev_word]
                    if valence < 0:
                        scalar *= -1
                    valence += scalar
            
            # Check for negation
            start_i = max(0, i-3)
            if negated([words_and_emoticons[j] for j in range(start_i, i)]):
                valence *= N_SCALAR
            
            # Check for double negative
            if check_double_negative(words_and_emoticons, start_i, i):
                valence *= -1  # Double negative becomes positive
            
            sentiments.append(valence)
        
        # Handle conjunctions
        sentiments = handle_conjunction(words_and_emoticons, sentiments)
        
        # Calculate compound score
        sum_s = sum(sentiments)
        
        # Compute compound score with normalization
        if sum_s != 0:
            compound = sum_s / math.sqrt(sum_s * sum_s + 15)
            if compound < -1.0:
                compound = -1.0
            elif compound > 1.0:
                compound = 1.0
        else:
            compound = 0.0
        
        # Calculate positive, negative, neutral ratios
        pos_sum = sum(s for s in sentiments if s > 0)
        neg_sum = abs(sum(s for s in sentiments if s < 0))
        neu_count = sum(1 for s in sentiments if s == 0)
        
        total = pos_sum + neg_sum + neu_count
        
        if total > 0:
            pos = pos_sum / total
            neg = neg_sum / total
            neu = neu_count / len(sentiments) if sentiments else 0
        else:
            pos = 0
            neg = 0
            neu = 1
        
        # Normalize scores
        total_sentiment = pos + neg + neu
        if total_sentiment > 1:
            pos /= total_sentiment
            neg /= total_sentiment
            neu /= total_sentiment
        
        return {
            "neg": round(neg, 3),
            "neu": round(neu, 3),
            "pos": round(pos, 3),
            "compound": round(compound, 4)
        }