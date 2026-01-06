import json

nb = json.load(open('A__dictionary_discovery_v24_unified_embedding.ipynb', encoding='utf-8'))

# ============================================================
# NEW CELL 9.6: DICTIONARY TERMS VISUALIZATION
# ============================================================

cell_96_source = """# ============================================================
# CELL 9.6: DICTIONARY TERMS IN SEMANTIC SPACE
# ============================================================

if VIZ_AVAILABLE:
    print(f"\\n{'='*70}")
    print("DICTIONARY TERMS IN SEMANTIC SPACE")
    print(f"{'='*70}")

    # --------------------------------------------------------
    # Load Dictionary
    # --------------------------------------------------------

    print(f"\\nLoading dictionary...")

    dict_path = source_fs.folders.get('Dictionary') / 'Curated_dictionary.csv'
    if not dict_path.exists():
        print(f"  ✗ Dictionary not found: {dict_path}")
        VIZ_AVAILABLE = False
    else:
        df_dict = pd.read_csv(dict_path)
        print(f"  ✓ Loaded {len(df_dict)} dictionary terms")

        # Identify columns
        has_is_seed = 'is_seed' in df_dict.columns
        has_weight = 'weight' in df_dict.columns
        has_parent = 'parent_seed' in df_dict.columns

        if has_is_seed:
            n_seed = df_dict['is_seed'].sum()
            n_expanded = len(df_dict) - n_seed
            print(f"    - Seed terms: {n_seed}")
            print(f"    - Expanded terms: {n_expanded}")

    # --------------------------------------------------------
    # Load BERTJE Models for Embeddings
    # --------------------------------------------------------

    if VIZ_AVAILABLE:
        print(f"\\n{'='*70}")
        print("LOADING BERTJE MODELS FOR EMBEDDINGS")
        print(f"{'='*70}")

        from transformers import AutoModel, AutoTokenizer
        import torch

        # Check for trained model
        trained_model_path = source_fs.folders.get('Model_finetuning')
        base_model_path = source_fs.folders.get('Model_finetuning') / 'base_encoder' if trained_model_path else None

        has_trained_model = False
        has_base_model = False

        # Try to load trained (post-training) model
        if trained_model_path and (trained_model_path / 'trained_encoder').exists():
            try:
                print(f"\\n  Loading trained (post-training) BERTJE model...")
                tokenizer_trained = AutoTokenizer.from_pretrained(str(trained_model_path / 'trained_encoder'))
                model_trained = AutoModel.from_pretrained(str(trained_model_path / 'trained_encoder'))
                model_trained.eval()
                has_trained_model = True
                print(f"    ✓ Loaded: {trained_model_path / 'trained_encoder'}")
            except Exception as e:
                print(f"    ✗ Failed to load trained model: {e}")

        # Try to load base (pre-training) model
        if base_model_path and base_model_path.exists():
            try:
                print(f"\\n  Loading base (pre-training) BERTJE model...")
                tokenizer_base = AutoTokenizer.from_pretrained(str(base_model_path))
                model_base = AutoModel.from_pretrained(str(base_model_path))
                model_base.eval()
                has_base_model = True
                print(f"    ✓ Loaded: {base_model_path}")
            except Exception as e:
                print(f"    ✗ Failed to load base model: {e}")

        # If neither available, try default GroNLP/bert-base-dutch-cased
        if not has_trained_model and not has_base_model:
            try:
                print(f"\\n  Loading default GroNLP BERTJE model...")
                tokenizer_base = AutoTokenizer.from_pretrained('GroNLP/bert-base-dutch-cased')
                model_base = AutoModel.from_pretrained('GroNLP/bert-base-dutch-cased')
                model_base.eval()
                has_base_model = True
                print(f"    ✓ Loaded: GroNLP/bert-base-dutch-cased")
            except Exception as e:
                print(f"    ✗ Failed to load default BERTJE: {e}")
                VIZ_AVAILABLE = False

        if has_trained_model and has_base_model:
            print(f"\\n  ✓ Both pre and post-training models available for comparison")
        elif has_trained_model:
            print(f"\\n  ⚠ Only post-training model available (no comparison)")
        elif has_base_model:
            print(f"\\n  ⚠ Only pre-training model available (no comparison)")
        else:
            print(f"\\n  ✗ No models available for embedding")
            VIZ_AVAILABLE = False

    # --------------------------------------------------------
    # Generate Dictionary Term Embeddings
    # --------------------------------------------------------

    if VIZ_AVAILABLE:
        print(f"\\n{'='*70}")
        print("GENERATING DICTIONARY EMBEDDINGS")
        print(f"{'='*70}")

        def get_embeddings(texts, tokenizer, model, batch_size=32):
            \"\"\"Generate embeddings for list of texts using BERTJE model\"\"\"
            embeddings = []

            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i+batch_size]

                # Tokenize
                inputs = tokenizer(
                    batch_texts,
                    padding=True,
                    truncation=True,
                    max_length=128,
                    return_tensors='pt'
                )

                # Generate embeddings
                with torch.no_grad():
                    outputs = model(**inputs)
                    # Use CLS token embedding
                    batch_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
                    embeddings.append(batch_embeddings)

            return np.vstack(embeddings)

        # Get dictionary terms
        dict_terms = df_dict['term'].tolist() if 'term' in df_dict.columns else df_dict.iloc[:, 0].tolist()

        print(f"\\n  Embedding {len(dict_terms)} dictionary terms...")

        # Generate embeddings with available models
        embeddings_base = None
        embeddings_trained = None

        if has_base_model:
            print(f"\\n  Generating pre-training embeddings...")
            embeddings_base = get_embeddings(dict_terms, tokenizer_base, model_base)
            print(f"    ✓ Shape: {embeddings_base.shape}")

        if has_trained_model:
            print(f"\\n  Generating post-training embeddings...")
            embeddings_trained = get_embeddings(dict_terms, tokenizer_trained, model_trained)
            print(f"    ✓ Shape: {embeddings_trained.shape}")

        # --------------------------------------------------------
        # Dimensionality Reduction for Dictionary Terms
        # --------------------------------------------------------

        print(f"\\n{'='*70}")
        print("DIMENSIONALITY REDUCTION (PCA)")
        print(f"{'='*70}")

        # We'll project dictionary terms into same PCA space as chunks
        # This allows direct comparison

        dict_viz_data = {}

        if has_base_model and embeddings_base is not None:
            print(f"\\n  Projecting pre-training embeddings to PCA space...")

            # Note: We need to use the same scaler/PCA from chunk visualization
            # But dictionary embeddings are in different space than topic scores
            # So we'll do separate PCA for dictionary terms

            scaler_dict_base = StandardScaler()
            emb_scaled_base = scaler_dict_base.fit_transform(embeddings_base)

            pca_dict_2d_base = PCA(n_components=2, random_state=42)
            emb_pca_2d_base = pca_dict_2d_base.fit_transform(emb_scaled_base)

            pca_dict_3d_base = PCA(n_components=3, random_state=42)
            emb_pca_3d_base = pca_dict_3d_base.fit_transform(emb_scaled_base)

            var_2d_base = pca_dict_2d_base.explained_variance_ratio_
            var_3d_base = pca_dict_3d_base.explained_variance_ratio_

            print(f"    2D PCA: {var_2d_base.sum():.2%} variance")
            print(f"    3D PCA: {var_3d_base.sum():.2%} variance")

            dict_viz_data['base'] = {
                'embeddings': embeddings_base,
                'pca_2d': emb_pca_2d_base,
                'pca_3d': emb_pca_3d_base,
                'pca_model_2d': pca_dict_2d_base,
                'pca_model_3d': pca_dict_3d_base,
                'scaler': scaler_dict_base,
                'variance_2d': var_2d_base,
                'variance_3d': var_3d_base,
            }

        if has_trained_model and embeddings_trained is not None:
            print(f"\\n  Projecting post-training embeddings to PCA space...")

            scaler_dict_trained = StandardScaler()
            emb_scaled_trained = scaler_dict_trained.fit_transform(embeddings_trained)

            pca_dict_2d_trained = PCA(n_components=2, random_state=42)
            emb_pca_2d_trained = pca_dict_2d_trained.fit_transform(emb_scaled_trained)

            pca_dict_3d_trained = PCA(n_components=3, random_state=42)
            emb_pca_3d_trained = pca_dict_3d_trained.fit_transform(emb_scaled_trained)

            var_2d_trained = pca_dict_2d_trained.explained_variance_ratio_
            var_3d_trained = pca_dict_3d_trained.explained_variance_ratio_

            print(f"    2D PCA: {var_2d_trained.sum():.2%} variance")
            print(f"    3D PCA: {var_3d_trained.sum():.2%} variance")

            dict_viz_data['trained'] = {
                'embeddings': embeddings_trained,
                'pca_2d': emb_pca_2d_trained,
                'pca_3d': emb_pca_3d_trained,
                'pca_model_2d': pca_dict_2d_trained,
                'pca_model_3d': pca_dict_3d_trained,
                'scaler': scaler_dict_trained,
                'variance_2d': var_2d_trained,
                'variance_3d': var_3d_trained,
            }

        # --------------------------------------------------------
        # Prepare Dictionary DataFrame for Visualization
        # --------------------------------------------------------

        print(f"\\n  Preparing dictionary data for visualization...")

        # Add term info
        df_dict['term_text'] = dict_terms
        df_dict['term_length'] = df_dict['term_text'].str.len()

        # Identify seed vs expanded
        if has_is_seed:
            df_dict['term_type'] = df_dict['is_seed'].apply(lambda x: 'Seed' if x else 'Expanded')
        else:
            df_dict['term_type'] = 'Unknown'

        # Get topic assignment
        if 'topic' in df_dict.columns:
            df_dict['topic_assigned'] = df_dict['topic']
        elif 'category' in df_dict.columns:
            df_dict['topic_assigned'] = df_dict['category']
        else:
            df_dict['topic_assigned'] = 'Unknown'

        # Store in dict_viz_data
        dict_viz_data['df'] = df_dict

        print(f"\\n{'='*70}")
        print(f"✓ DICTIONARY EMBEDDINGS PREPARED")
        print(f"{'='*70}")
        print(f"  Terms: {len(df_dict)}")
        print(f"  Pre-training embeddings: {'Available' if 'base' in dict_viz_data else 'Not available'}")
        print(f"  Post-training embeddings: {'Available' if 'trained' in dict_viz_data else 'Not available'}")

        print(f"\\n✓ Cell 9.6 Complete - Ready for dictionary visualization!")

else:
    print("⚠ Skipping dictionary embeddings - visualization not available")
"""

# Create new cell
new_cell_96 = {
    "cell_type": "code",
    "execution_count": None,
    "id": "dict_embeddings",
    "metadata": {},
    "outputs": [],
    "source": cell_96_source.split('\n')
}

# Insert at position 81 (before training metrics)
print(f"Inserting new Cell 9.6 (Dictionary Embeddings) at position 81...")
nb['cells'].insert(81, new_cell_96)

# Save
with open('A__dictionary_discovery_v24_unified_embedding.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Cell 9.6 added successfully!")
print(f"Total cells: {len(nb['cells'])}")
