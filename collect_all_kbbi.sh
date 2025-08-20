#!/bin/bash

# Script to collect all KBBI sources
echo "Collecting KBBI data from 7 sources..."

cd /tmp

# Source 1: kbbi-qt
echo "1. Cloning kbbi-qt..."
git clone --depth 1 https://github.com/bgli/kbbi-qt kbbi1 2>/dev/null || echo "Already exists"

# Source 2: KBBI from PDF
echo "2. Cloning rizaumami/kbbi..."
git clone --depth 1 https://github.com/rizaumami/kbbi kbbi2 2>/dev/null || echo "Already exists"

# Source 3: Already have this one (damzaky)
echo "3. Using existing damzaky/kumpulan-kata-bahasa-indonesia-KBBI..."

# Source 4: KBBI Crawling
echo "4. Cloning muzavan/KBBI-Crawling..."
git clone --depth 1 https://github.com/muzavan/KBBI-Crawling kbbi4 2>/dev/null || echo "Already exists"

# Source 5: KBBI Dataset
echo "5. Cloning bbn-bernard/kbbi_dataset..."
git clone --depth 1 https://github.com/bbn-bernard/kbbi_dataset kbbi5 2>/dev/null || echo "Already exists"

# Source 6: Indonesian Words
echo "6. Cloning bekicot/indonesian_words..."
git clone --depth 1 https://github.com/bekicot/indonesian_words kbbi6 2>/dev/null || echo "Already exists"

# Source 7: KBBI2
echo "7. Cloning lufias69/KBBI2..."
git clone --depth 1 https://github.com/lufias69/KBBI2 kbbi7 2>/dev/null || echo "Already exists"

echo "All sources collected!"