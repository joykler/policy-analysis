import json

nb = json.load(open('A__dictionary_discovery_v24_unified_embedding.ipynb', encoding='utf-8'))

# ============================================================
# CELL 9.7: 2D DICTIONARY VISUALIZATION
# ============================================================

cell_97_source = """# ============================================================
# CELL 9.7: 2D DICTIONARY TERMS VISUALIZATION
# ============================================================

if VIZ_AVAILABLE and 'dict_viz_data' in globals():
    print(f"\\n{'='*70}")
    print("2D DICTIONARY VISUALIZATION")
    print(f"{'='*70}")

    df_dict_plot = dict_viz_data['df']

    # Color mapping for topics (same as chunks)
    topic_colors = {topic: color_palette[i % len(color_palette)]
                    for i, topic in enumerate(topics_viz)}

    # Additional colors for unknown/multi-topic
    topic_colors['Unknown'] = 'gray'
    topic_colors['Multi-topic'] = 'purple'

    # --------------------------------------------------------
    # Create Comparison Figure (Pre vs Post Training)
    # --------------------------------------------------------

    has_both = 'base' in dict_viz_data and 'trained' in dict_viz_data
    has_base_only = 'base' in dict_viz_data and 'trained' not in dict_viz_data
    has_trained_only = 'trained' in dict_viz_data and 'base' not in dict_viz_data

    if has_both:
        print(f"\\n  Creating side-by-side comparison (pre vs post training)...")

        # Create subplots
        from plotly.subplots import make_subplots

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['<b>Pre-Training</b> (Base BERTJE)', '<b>Post-Training</b> (Fine-tuned)'],
            horizontal_spacing=0.10
        )

        models = [('base', 1), ('trained', 2)]

    else:
        print(f"\\n  Creating single visualization...")
        fig = go.Figure()
        if has_base_only:
            models = [('base', None)]
            title_suffix = " (Pre-Training - Base BERTJE)"
        else:
            models = [('trained', None)]
            title_suffix = " (Post-Training - Fine-tuned)"

    # --------------------------------------------------------
    # Plot Dictionary Terms for Each Model
    # --------------------------------------------------------

    for model_type, col in models:
        data = dict_viz_data[model_type]
        coords_2d = data['pca_2d']
        var_exp = data['variance_2d']

        print(f"\\n  Plotting {model_type} model...")

        # Add coordinates to dataframe
        df_plot = df_dict_plot.copy()
        df_plot['pca_x'] = coords_2d[:, 0]
        df_plot['pca_y'] = coords_2d[:, 1]

        # Group by topic
        for topic in df_plot['topic_assigned'].unique():
            topic_df = df_plot[df_plot['topic_assigned'] == topic]

            if len(topic_df) == 0:
                continue

            # Separate seed and expanded terms
            if 'term_type' in topic_df.columns:
                seed_df = topic_df[topic_df['term_type'] == 'Seed']
                expanded_df = topic_df[topic_df['term_type'] == 'Expanded']
            else:
                seed_df = topic_df
                expanded_df = pd.DataFrame()

            # Build hover texts
            def build_hover(row):
                parts = [
                    f"<b>Term:</b> {row['term_text']}",
                    f"<b>Topic:</b> {row['topic_assigned']}",
                    f"<b>Type:</b> {row.get('term_type', 'Unknown')}",
                ]
                if 'weight' in row and pd.notna(row['weight']):
                    parts.append(f"<b>Weight:</b> {row['weight']:.2f}")
                if 'parent_seed' in row and pd.notna(row['parent_seed']):
                    parts.append(f"<b>Parent:</b> {row['parent_seed']}")
                return "<br>".join(parts)

            # Plot seed terms (larger, solid)
            if len(seed_df) > 0:
                hover_texts = [build_hover(row) for _, row in seed_df.iterrows()]

                trace = go.Scatter(
                    x=seed_df['pca_x'],
                    y=seed_df['pca_y'],
                    mode='markers+text',
                    name=f'{topic} (Seed)',
                    text=seed_df['term_text'].str[:15],  # Abbreviated labels
                    textposition='top center',
                    textfont=dict(size=8),
                    marker=dict(
                        size=12,
                        color=topic_colors.get(topic, 'gray'),
                        opacity=0.9,
                        symbol='diamond',
                        line=dict(width=2, color='black')
                    ),
                    hovertemplate='%{hovertext}<extra></extra>',
                    hovertext=hover_texts,
                    legendgroup=topic,
                    showlegend=(col == 1 or col is None),  # Show legend only once
                )

                if col is not None:
                    fig.add_trace(trace, row=1, col=col)
                else:
                    fig.add_trace(trace)

            # Plot expanded terms (smaller, hollow)
            if len(expanded_df) > 0:
                hover_texts = [build_hover(row) for _, row in expanded_df.iterrows()]

                trace = go.Scatter(
                    x=expanded_df['pca_x'],
                    y=expanded_df['pca_y'],
                    mode='markers',
                    name=f'{topic} (Expanded)',
                    marker=dict(
                        size=6,
                        color=topic_colors.get(topic, 'gray'),
                        opacity=0.6,
                        line=dict(width=1, color=topic_colors.get(topic, 'gray'))
                    ),
                    hovertemplate='%{hovertext}<extra></extra>',
                    hovertext=hover_texts,
                    legendgroup=topic,
                    showlegend=False,  # Don't clutter legend
                )

                if col is not None:
                    fig.add_trace(trace, row=1, col=col)
                else:
                    fig.add_trace(trace)

        print(f"    ✓ Plotted {len(df_plot)} terms")

        # Add variance annotation
        if col is not None:
            fig.add_annotation(
                text=f"<i>Variance: {var_exp.sum():.1%}</i>",
                xref=f'x{col}',
                yref=f'y{col}',
                x=0.02,
                y=0.98,
                xanchor='left',
                yanchor='top',
                showarrow=False,
                font=dict(size=10, color='gray'),
                row=1,
                col=col
            )

    # --------------------------------------------------------
    # Update Layout
    # --------------------------------------------------------

    if has_both:
        title_text = (
            '<b>Dictionary Terms: Pre vs Post Training Comparison</b><br>'
            '<sub>Diamonds = Seed terms | Circles = Expanded terms | '
            'Size indicates importance | Compare clustering between models</sub>'
        )
        height = 700
        width = 1600
    else:
        title_text = (
            f'<b>Dictionary Terms in Semantic Space{title_suffix}</b><br>'
            '<sub>Diamonds = Seed terms | Circles = Expanded terms | '
            'Hover for details</sub>'
        )
        height = 800
        width = 1200

    fig.update_layout(
        title_text=title_text,
        height=height,
        width=width,
        template='plotly_white',
        hovermode='closest',
        font=dict(size=11),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=9),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='lightgray',
            borderwidth=1
        )
    )

    # Update axes
    if has_both:
        for col in [1, 2]:
            fig.update_xaxes(
                title_text='PC1',
                showgrid=True,
                gridcolor='lightgray',
                zeroline=True,
                row=1,
                col=col
            )
            fig.update_yaxes(
                title_text='PC2',
                showgrid=True,
                gridcolor='lightgray',
                zeroline=True,
                row=1,
                col=col
            )
    else:
        fig.update_xaxes(
            title_text='PC1',
            showgrid=True,
            gridcolor='lightgray',
            zeroline=True
        )
        fig.update_yaxes(
            title_text='PC2',
            showgrid=True,
            gridcolor='lightgray',
            zeroline=True
        )

    # --------------------------------------------------------
    # Save Visualization
    # --------------------------------------------------------

    if has_both:
        output_path = visuals_path_viz / 'dictionary_terms_comparison_2d.html'
    elif has_trained_only:
        output_path = visuals_path_viz / 'dictionary_terms_trained_2d.html'
    else:
        output_path = visuals_path_viz / 'dictionary_terms_base_2d.html'

    fig.write_html(str(output_path))

    print(f"\\n{'='*70}")
    print(f"2D DICTIONARY VISUALIZATION COMPLETE")
    print(f"{'='*70}")
    print(f"  Saved to: {output_path.relative_to(fs.root)}")
    print(f"  Terms plotted: {len(df_dict_plot)}")
    if has_both:
        print(f"  Comparison: Pre-training vs Post-training")

    # Display
    try:
        fig.show()
    except:
        print(f"  (Interactive display not available)")

    print(f"\\n✓ Cell 9.7 Complete!")

else:
    print("⚠ Skipping 2D dictionary visualization - data not available")
"""

# ============================================================
# CELL 9.8: 3D DICTIONARY VISUALIZATION
# ============================================================

cell_98_source = """# ============================================================
# CELL 9.8: 3D DICTIONARY TERMS VISUALIZATION (WITH SHIFT ANALYSIS)
# ============================================================

if VIZ_AVAILABLE and 'dict_viz_data' in globals():
    print(f"\\n{'='*70}")
    print("3D DICTIONARY VISUALIZATION")
    print(f"{'='*70}")

    df_dict_plot = dict_viz_data['df']
    has_both = 'base' in dict_viz_data and 'trained' in dict_viz_data

    # --------------------------------------------------------
    # Create 3D Visualizations
    # --------------------------------------------------------

    if has_both:
        print(f"\\n  Creating 3D comparison with shift vectors...")

        # --------------------------------------------------------
        # Calculate Shifts (Pre to Post Training)
        # --------------------------------------------------------

        coords_pre = dict_viz_data['base']['pca_3d']
        coords_post = dict_viz_data['trained']['pca_3d']

        # Calculate shift vectors
        shifts = coords_post - coords_pre
        shift_magnitudes = np.linalg.norm(shifts, axis=1)

        # Add to dataframe
        df_dict_plot['shift_magnitude'] = shift_magnitudes
        df_dict_plot['shift_x'] = shifts[:, 0]
        df_dict_plot['shift_y'] = shifts[:, 1]
        df_dict_plot['shift_z'] = shifts[:, 2]

        print(f"    Shift statistics:")
        print(f"      Mean: {shift_magnitudes.mean():.3f}")
        print(f"      Median: {np.median(shift_magnitudes):.3f}")
        print(f"      Max: {shift_magnitudes.max():.3f}")

        # Identify top shifters
        top_shifters = df_dict_plot.nlargest(10, 'shift_magnitude')
        print(f"\\n    Top 10 terms with largest shifts:")
        for idx, row in top_shifters.iterrows():
            print(f"      {row['term_text']:30s}: {row['shift_magnitude']:.3f}")

        # --------------------------------------------------------
        # Create Figure with Both Positions + Shift Vectors
        # --------------------------------------------------------

        fig_3d = go.Figure()

        # Plot pre-training positions (lighter, smaller)
        print(f"\\n  Adding pre-training positions...")

        df_plot = df_dict_plot.copy()
        df_plot['pca_x'] = coords_pre[:, 0]
        df_plot['pca_y'] = coords_pre[:, 1]
        df_plot['pca_z'] = coords_pre[:, 2]

        for topic in df_plot['topic_assigned'].unique():
            topic_df = df_plot[df_plot['topic_assigned'] == topic]
            if len(topic_df) == 0:
                continue

            hover_texts = [
                f"<b>{row['term_text']}</b> (Pre-training)<br>"
                f"Topic: {row['topic_assigned']}<br>"
                f"Type: {row.get('term_type', 'Unknown')}<br>"
                f"Shift: {row['shift_magnitude']:.3f}"
                for _, row in topic_df.iterrows()
            ]

            fig_3d.add_trace(go.Scatter3d(
                x=topic_df['pca_x'],
                y=topic_df['pca_y'],
                z=topic_df['pca_z'],
                mode='markers',
                name=f'{topic} (Pre)',
                marker=dict(
                    size=4,
                    color=topic_colors.get(topic, 'gray'),
                    opacity=0.3,
                    symbol='circle'
                ),
                hovertemplate='%{hovertext}<extra></extra>',
                hovertext=hover_texts,
                legendgroup=topic,
                showlegend=True
            ))

        # Plot post-training positions (bolder, larger)
        print(f"  Adding post-training positions...")

        df_plot['pca_x'] = coords_post[:, 0]
        df_plot['pca_y'] = coords_post[:, 1]
        df_plot['pca_z'] = coords_post[:, 2]

        for topic in df_plot['topic_assigned'].unique():
            topic_df = df_plot[df_plot['topic_assigned'] == topic]
            if len(topic_df) == 0:
                continue

            # Separate seed vs expanded
            seed_df = topic_df[topic_df['term_type'] == 'Seed'] if 'term_type' in topic_df.columns else topic_df

            if len(seed_df) > 0:
                hover_texts = [
                    f"<b>{row['term_text']}</b> (Post-training)<br>"
                    f"Topic: {row['topic_assigned']}<br>"
                    f"Type: {row.get('term_type', 'Unknown')}<br>"
                    f"Shift: {row['shift_magnitude']:.3f}"
                    for _, row in seed_df.iterrows()
                ]

                fig_3d.add_trace(go.Scatter3d(
                    x=seed_df['pca_x'],
                    y=seed_df['pca_y'],
                    z=seed_df['pca_z'],
                    mode='markers+text',
                    name=f'{topic} (Post)',
                    text=seed_df['term_text'].str[:12],
                    textposition='top center',
                    textfont=dict(size=7),
                    marker=dict(
                        size=8,
                        color=topic_colors.get(topic, 'gray'),
                        opacity=0.9,
                        symbol='diamond',
                        line=dict(width=1, color='black')
                    ),
                    hovertemplate='%{hovertext}<extra></extra>',
                    hovertext=hover_texts,
                    legendgroup=topic,
                    showlegend=True
                ))

        # Plot shift vectors for significant shifts
        print(f"  Adding shift vectors...")

        significant_shifts = df_plot[df_plot['shift_magnitude'] > shift_magnitudes.median()]

        for _, row in significant_shifts.iterrows():
            # Arrow from pre to post
            fig_3d.add_trace(go.Scatter3d(
                x=[coords_pre[row.name, 0], coords_post[row.name, 0]],
                y=[coords_pre[row.name, 1], coords_post[row.name, 1]],
                z=[coords_pre[row.name, 2], coords_post[row.name, 2]],
                mode='lines',
                line=dict(color='red', width=2, dash='dash'),
                hovertemplate=f"<b>{row['term_text']}</b><br>Shift: {row['shift_magnitude']:.3f}<extra></extra>",
                showlegend=False
            ))

        print(f"    ✓ Added {len(significant_shifts)} shift vectors (above median)")

        var_exp = dict_viz_data['trained']['variance_3d']
        title_text = (
            f"<b>Dictionary Terms: Training-Induced Semantic Shifts (3D)</b><br>"
            f"<sub>Variance: {var_exp.sum():.1%} | "
            f"Light = Pre-training | Bold = Post-training | "
            f"Red arrows = Significant shifts | "
            f"Rotate to explore</sub>"
        )

    else:
        # Single model visualization
        print(f"\\n  Creating single 3D visualization...")

        fig_3d = go.Figure()

        model_type = 'base' if 'base' in dict_viz_data else 'trained'
        data = dict_viz_data[model_type]
        coords_3d = data['pca_3d']
        var_exp = data['variance_3d']

        df_plot = df_dict_plot.copy()
        df_plot['pca_x'] = coords_3d[:, 0]
        df_plot['pca_y'] = coords_3d[:, 1]
        df_plot['pca_z'] = coords_3d[:, 2]

        for topic in df_plot['topic_assigned'].unique():
            topic_df = df_plot[df_plot['topic_assigned'] == topic]
            if len(topic_df) == 0:
                continue

            hover_texts = [
                f"<b>{row['term_text']}</b><br>"
                f"Topic: {row['topic_assigned']}<br>"
                f"Type: {row.get('term_type', 'Unknown')}"
                for _, row in topic_df.iterrows()
            ]

            fig_3d.add_trace(go.Scatter3d(
                x=topic_df['pca_x'],
                y=topic_df['pca_y'],
                z=topic_df['pca_z'],
                mode='markers+text',
                name=topic,
                text=topic_df['term_text'].str[:12],
                textposition='top center',
                textfont=dict(size=7),
                marker=dict(
                    size=6,
                    color=topic_colors.get(topic, 'gray'),
                    opacity=0.8
                ),
                hovertemplate='%{hovertext}<extra></extra>',
                hovertext=hover_texts,
                legendgroup=topic
            ))

        model_name = "Pre-training" if model_type == 'base' else "Post-training"
        title_text = (
            f"<b>Dictionary Terms in 3D Semantic Space ({model_name})</b><br>"
            f"<sub>Variance: {var_exp.sum():.1%} | Rotate to explore</sub>"
        )

    # --------------------------------------------------------
    # Update Layout
    # --------------------------------------------------------

    fig_3d.update_layout(
        title=title_text,
        scene=dict(
            xaxis=dict(
                title=f'PC1 ({var_exp[0]:.1%})',
                backgroundcolor="rgb(245, 245, 245)",
                gridcolor="white",
                showbackground=True
            ),
            yaxis=dict(
                title=f'PC2 ({var_exp[1]:.1%})',
                backgroundcolor="rgb(245, 245, 245)",
                gridcolor="white",
                showbackground=True
            ),
            zaxis=dict(
                title=f'PC3 ({var_exp[2]:.1%})',
                backgroundcolor="rgb(245, 245, 245)",
                gridcolor="white",
                showbackground=True
            ),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        width=1400,
        height=900,
        font=dict(size=11),
        showlegend=True,
        legend=dict(
            x=1.0,
            y=1.0,
            font=dict(size=9),
            bgcolor='rgba(255,255,255,0.8)'
        ),
        template='plotly_white'
    )

    # --------------------------------------------------------
    # Save Visualization
    # --------------------------------------------------------

    if has_both:
        output_path = visuals_path_viz / 'dictionary_terms_shifts_3d.html'
    elif 'trained' in dict_viz_data:
        output_path = visuals_path_viz / 'dictionary_terms_trained_3d.html'
    else:
        output_path = visuals_path_viz / 'dictionary_terms_base_3d.html'

    fig_3d.write_html(str(output_path))

    print(f"\\n{'='*70}")
    print(f"3D DICTIONARY VISUALIZATION COMPLETE")
    print(f"{'='*70}")
    print(f"  Saved to: {output_path.relative_to(fs.root)}")
    if has_both:
        print(f"  Shows: Pre/Post training comparison with shift vectors")
        print(f"  Significant shifts: {len(significant_shifts)}")

    # Display
    try:
        fig_3d.show()
    except:
        print(f"  (Interactive display not available)")

    print(f"\\n✓ Cell 9.8 Complete!")

else:
    print("⚠ Skipping 3D dictionary visualization - data not available")
"""

# Create cells
new_cell_97 = {
    "cell_type": "code",
    "execution_count": None,
    "id": "dict_viz_2d",
    "metadata": {},
    "outputs": [],
    "source": cell_97_source.split('\n')
}

new_cell_98 = {
    "cell_type": "code",
    "execution_count": None,
    "id": "dict_viz_3d",
    "metadata": {},
    "outputs": [],
    "source": cell_98_source.split('\n')
}

# Insert at positions 82 and 83
print(f"Inserting dictionary visualization cells...")
nb['cells'].insert(82, new_cell_97)
nb['cells'].insert(83, new_cell_98)

# Save
with open('A__dictionary_discovery_v24_unified_embedding.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Dictionary visualization cells added!")
print(f"  Cell 9.7: 2D dictionary visualization (comparison if both models)")
print(f"  Cell 9.8: 3D dictionary with shift vectors")
print(f"Total cells: {len(nb['cells'])}")
