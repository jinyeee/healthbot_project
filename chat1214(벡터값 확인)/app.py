
import numpy as np
from sklearn.decomposition import PCA
import pinecone

# Initialize Pinecone
pinecone.init(
    api_key='PINECONE_API_KEY',
    environment='gcp-starter'
)

# Create a Pinecone index instance
index = pinecone.Index('health-dhver')

# Load the numpy array from the file (replace the file path with the actual path where your file is located)
file_path = r"C:\Users\user\Desktop\파프\chat\chat1213(multie5+annoy)\mteann3.npy"
vector = np.load(file_path)

# Assuming the loaded 'vector' variable is an array of vectors
if vector.ndim > 1 and vector.shape[1] != 1024:
    print("Reducing vector dimension to 1024...")
    # Reduce the dimensionality of each vector to 1024
    pca = PCA(n_components=1024)
    vectors_reduced = pca.fit_transform(vector)
else:
    vectors_reduced = vector

total_vectors = len(vectors_reduced)
last_successful_id = 9000  # Replace with the last successful vector_id you logged

# Resume uploading vectors from the last successful id
for i, vec in enumerate(vectors_reduced[last_successful_id:], start=last_successful_id):
    try:
        vector_id = f'vector-{i}'
        index.upsert(vectors=[(vector_id, vec.tolist())])

        # Check if the current index is a multiple of 50 to print progress
        if (i + 1) % 50 == 0 or i == total_vectors - 1:
            completion_percentage = (i + 1) / total_vectors * 100
            print(f"Uploading vector {i + 1}/{total_vectors} ({completion_percentage:.2f}%)")

    except Exception as e:
        # Log the error and break or continue as needed
        print(f"Error uploading vector {i}: {e}")
        # Optionally, handle the error by retrying, waiting, or skipping
        continue  # For example, just move on to the next vector

print("Upload complete.")
