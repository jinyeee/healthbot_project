import pandas as pd
import logging
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from annoy import AnnoyIndex
from tqdm import tqdm
import os



# Setup logging
logging.basicConfig(level=logging.INFO)

# Constants
MODEL_NAME = "dmis-lab/biobert-v1.1"
MAX_LENGTH = 512
N_TREES = 10
ANN_FILE = 'sibum1.ann'
EMBEDDINGS_FILE = 'sibum1.npy'

class BioBERTEmbedding:
    def __init__(self, model_name=MODEL_NAME):
        self.model_name = model_name
        self.tokenizer, self.model = self.load_model()
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model loading failed.")

    def load_model(self):
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModel.from_pretrained(self.model_name)
            logging.info("Model loaded successfully.")
            return tokenizer, model
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            return None, None

    def get_embeddings(self, docs, batch_size=10):
        self.model = self.model.to('cuda' if torch.cuda.is_available() else 'cpu')
        embeddings = []
        logging.info("Starting embedding generation.")

        for i in tqdm(range(0, len(docs), batch_size), desc="Generating embeddings"):
            batch = docs[i:i+batch_size]
            inputs = self.tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=MAX_LENGTH)
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model(**inputs)
            batch_embeddings = outputs.last_hidden_state.mean(dim=1).cpu().detach().numpy()
            embeddings.extend(batch_embeddings)
        
        logging.info("Embedding generation complete.")
        return np.array(embeddings)

class AnnoyIndexBuilder:
    def __init__(self, embedding_dim, n_trees=N_TREES, ann_file=ANN_FILE):
        self.embedding_dim = embedding_dim
        self.n_trees = n_trees
        self.ann_file = ann_file

    def build_and_save(self, embeddings):
        if embeddings is None or len(embeddings) == 0:
            raise ValueError("No embeddings provided.")
        
        t = AnnoyIndex(self.embedding_dim, 'angular')
        logging.info("Building Annoy index.")

        for i, vec in enumerate(tqdm(embeddings, desc="Building Annoy Index")):
            t.add_item(i, vec)
        
        t.build(self.n_trees)
        t.save(self.ann_file)
        logging.info("Annoy index built and saved.")
        return t

    def load(self):
        u = AnnoyIndex(self.embedding_dim, 'angular')
        if not u.load(self.ann_file):
            raise IOError(f"Could not load Annoy index from {self.ann_file}")
        logging.info("Annoy index loaded.")
        return u

def save_embeddings(embeddings, filename=EMBEDDINGS_FILE):
    np.save(filename, embeddings)
    logging.info("Embeddings saved.")

def load_embeddings(filename=EMBEDDINGS_FILE):
    if os.path.exists(filename):
        return np.load(filename)
    else:
        logging.error(f"Embeddings file {filename} not found.")
        return None

def query_index(query, embedding_model, annoy_index, top_n=5):
    query_vec = embedding_model.get_embeddings([query])[0]
    nns = annoy_index.get_nns_by_vector(query_vec, top_n)
    return nns

def main():
    # Initialize BioBERT model for embeddings
    embedding_model = BioBERTEmbedding()
    
    # Paths to your CSV files
    csv_file_paths = ["C:/Users/user/Desktop/파프/아산병원데이터.csv", 
                      "C:/Users/user/Desktop/파프/asanshort.csv"]
    
    # Read and concatenate the specified columns for each document
    docs = []
    for csv_file_path in csv_file_paths:  # This line is changed
        df = pd.read_csv(csv_file_path)
        for index, row in df.iterrows():
            # Combine the text from all relevant columns into a single document string
            document = ' '.join(str(row[col]) if not pd.isnull(row[col]) else '' for col in ["질병명", "진료과", "증상", "관련질환", "동의어", "부위"])
            docs.append(document)
    
    # Generate or load embeddings
    if os.path.exists(EMBEDDINGS_FILE):
        embeddings = load_embeddings()
    else:
        embeddings = embedding_model.get_embeddings(docs)
        save_embeddings(embeddings)

    # Build or load Annoy index
    annoy_builder = AnnoyIndexBuilder(embedding_dim=embeddings.shape[1])
    if os.path.exists(ANN_FILE):
        annoy_index = annoy_builder.load()
    else:
        annoy_index = annoy_builder.build_and_save(embeddings)

    # Querying
    query = input("Enter your query text: ")
    top_n = int(input("Enter number of top results to fetch: "))
    nearest_neighbors = query_index(query, embedding_model, annoy_index, top_n)

    for nn in nearest_neighbors:
        print(f"Document {nn+1}: {docs[nn]}")

if __name__ == "__main__":
    main()