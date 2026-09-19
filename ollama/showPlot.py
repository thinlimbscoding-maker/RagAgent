#!/usr/bin/env python3
import numpy as np
from langchain_ollama import OllamaEmbeddings

# ✅ Reverted to the correct package path that originally worked!
from langchain_community.vectorstores import FAISS
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import plotly.figure_factory as ff

# 1. Initialize embeddings model
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

myDoc = [
    "india gets freedom in 1947",
    "india has poor roads",
    "india has more than 30 states",
    "india good developers",
]

# Build database index cleanly
print("🔄 Building local vector store index...")
db = FAISS.from_texts(myDoc, embeddings_model)

# 2. Get User Input Query from the terminal
print("\n📝 Context Loaded.")
user_query = input("🔍 Type a search query to plot: ")

# 3. Generate raw vectors for both documents and user query
print("🔄 Generating embeddings via nomic-embed-text...")
doc_vectors = embeddings_model.embed_documents(myDoc)
query_vector = embeddings_model.embed_query(user_query)
print(f"🔄 Generating embeddings via nomic-embed-text... {query_vector}")


# Combine them into a single matrix so they undergo the same PCA projection spacing
all_vectors = np.vstack([doc_vectors, query_vector])
all_texts = myDoc + [f"❓ QUERY: '{user_query}'"]

# Define styling rules (0 for documents, 1 for the query)
colors = ["Document"] * len(myDoc) + ["User Query"]
marker_symbols_2d = ["circle"] * len(myDoc) + ["x"]
marker_symbols_3d = ["circle"] * len(myDoc) + ["diamond"]

# 4. Dimensionality Reduction using PCA
print("📉 Reducing dimensions using PCA...")
pca_2d = PCA(n_components=2, random_state=42)
coords_2d = pca_2d.fit_transform(all_vectors)

pca_3d = PCA(n_components=3, random_state=42)
coords_3d = pca_3d.fit_transform(all_vectors)

# --- 1. 2D Plot with Query Position ---
print("📊 Launching 2D Plotly View...")
fig2d = px.scatter(
    x=coords_2d[:, 0],
    y=coords_2d[:, 1],
    text=all_texts,
    color=colors,
    color_discrete_map={"Document": "#1f77b4", "User Query": "#d62728"},
    title=f"2D Embedding Space Map (Query: '{user_query}')",
)
fig2d.update_traces(
    textposition="top center", marker=dict(size=14, symbol=marker_symbols_2d)
)
fig2d.show()

# --- 2. 3D Interactive Plot with Query Position ---
print("🌌 Launching 3D Interactive Plotly View...")
fig3d = px.scatter_3d(
    x=coords_3d[:, 0],
    y=coords_3d[:, 1],
    z=coords_3d[:, 2],
    text=all_texts,
    color=colors,
    color_discrete_map={"Document": "#1f77b4", "User Query": "#d62728"},
    title=f"3D Embedding Space Map (Query: '{user_query}')",
)
fig3d.update_traces(
    textposition="top center", marker=dict(size=10, symbol=marker_symbols_3d)
)
fig3d.show()

# --- 3. Similarity Heatmap (Including the Query) ---
print("🔥 Generating Cosine Similarity Heatmap...")
sim_matrix = cosine_similarity(all_vectors)
labels = [f"Doc {i+1}" for i in range(len(myDoc))] + ["User Query"]

fig_heat = ff.create_annotated_heatmap(
    z=sim_matrix.round(3),
    x=labels,
    y=labels,
    colorscale="RdBu",
    showscale=True,
)
fig_heat.update_layout(title="Cosine Similarity Grid (Documents vs User Query)")
fig_heat.show()
