import os
from Bio import SeqIO   
import pandas as pd
import itertools
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix




# insert Training Data
BASE_DIR = "Training_Data"
records = []

# Finds species directories
for species_dir in os.listdir(BASE_DIR):
    species_path = os.path.join(BASE_DIR, species_dir)
    if not os.path.isdir(species_path):
        continue
    
    for fname in os.listdir(species_path):
        if not fname.endswith(".txt"):
            continue
        
        fpath = os.path.join(species_path, fname)
        
        for record in SeqIO.parse(fpath, "fasta"):
            seq_str = str(record.seq).upper().replace("\n", "").replace(" ", "")
            # filters out barcodes
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

# 2. Convert sequences to k-mer vectors

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

X = np.array([kmer_counts(s) for s in df["sequence"]])
y = df["species"].values

# 3. Train kNN model

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)


# 4. Function: Predict species from query sequence

def predict_species(seq_query):
    feats = np.array(kmer_counts(seq_query.upper())).reshape(1, -1)
    return knn.predict(feats)[0]

user_input = input("Gimme your Sequence por favor:\n")
clean = user_input.replace("\n", "").replace(" ", "").upper()

print("Prediction:")
print(predict_species(clean))

