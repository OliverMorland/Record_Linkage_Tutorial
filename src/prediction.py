from training import linker


df_predictions = linker.inference.predict(threshold_match_probability=0.5)

df_clusters = linker.clustering.cluster_pairwise_predictions_at_threshold(
    df_predictions,
    threshold_match_probability=0.7
)

final_df = df_clusters.as_pandas_dataframe()
print(final_df[["cluster_id", "unique_id", "farm_name", "operator_first_name", "operator_last_name"]])