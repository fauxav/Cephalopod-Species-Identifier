# model_core.py
import os
from Bio import SeqIO
import pandas as pd
import itertools
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

BASE_DIR = "Training_Data"

# --- 1. Load training data ---
def load_dataset(base_dir=BASE_DIR):
    records = []

    for species_dir in os.listdir(base_dir):
        species_path = os.path.join(base_dir, species_dir)
        if not os.path.isdir(species_path):
            continue
        
        for fname in os.listdir(species_path):
            if not fname.endswith(".txt"):
                continue
            
            fpath = os.path.join(species_path, fname)
            
            for record in SeqIO.parse(fpath, "fasta"):
                seq_str = str(record.seq).upper().replace("\n", "").replace(" ", "")
                # filters out bad barcodes
                if len(seq_str) < 400:
                    continue
                
                records.append({
                    "species": species_dir,
                    "seq_id": record.id,
                    "sequence": seq_str
                })

    df = pd.DataFrame(records)
    print("\nLoaded dataset:")
    print(df["species"].value_counts())
    return df

# --- 2. k-mer features ---
import itertools
def all_kmers(k=3):
    bases = ["A", "C", "G", "T"]
    return ["".join(p) for p in itertools.product(bases, repeat=k)]

KMERS = all_kmers(3)

def kmer_counts(seq, k=3):
    counts = {kmer: 0 for kmer in KMERS}
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k]
        if kmer in counts:
            counts[kmer] += 1
    return [counts[k] for k in KMERS]

# --- 3. Train model ---
def train_model():
    df = load_dataset()
    X = np.array([kmer_counts(s) for s in df["sequence"]])
    y = df["species"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    return knn

# --- 4. Predict using trained model ---
def predict_species(model, seq_query):
    clean = seq_query.upper().replace("\n", "").replace(" ", "")
    feats = np.array(kmer_counts(clean)).reshape(1, -1)
    return model.predict(feats)[0]
