from challenge_dataset import df
from splink import SettingsCreator, block_on
from splink.comparison_library import JaroWinklerAtThresholds, ExactMatch
from splink import Linker, DuckDBAPI

print("Origin dataframe:" + str(df))

settings = SettingsCreator(
    link_type="dedupe_only",
    blocking_rules_to_generate_predictions=[
        block_on("state", "county"),
        block_on("operator_last_name")
    ],
    comparisons=[
        JaroWinklerAtThresholds("farm_name", [0.9, 0.7]),
        JaroWinklerAtThresholds("zip_code", [0.9, 0.7]),
        JaroWinklerAtThresholds("operator_first_name", [0.9, 0.7]),
        JaroWinklerAtThresholds("operator_last_name", [0.9, 0.7]),
    ]
)

db_api = DuckDBAPI()
linker = Linker(df, settings, db_api=db_api)
linker.training.estimate_u_using_random_sampling(max_pairs=1e5)
linker.training.estimate_parameters_using_expectation_maximisation(blocking_rule="l.state = r.state AND l.county = r.county")
linker.training.estimate_parameters_using_expectation_maximisation(blocking_rule="l.operator_last_name = r.operator_last_name")


# Prediction
df_predictions = linker.inference.predict(threshold_match_probability=0.5)

df_clusters = linker.clustering.cluster_pairwise_predictions_at_threshold(
    df_predictions,
    threshold_match_probability=0.9
)

final_df = df_clusters.as_pandas_dataframe()
cluster_sizes = final_df.groupby("cluster_id")["unique_id"].transform("count")
duplicates_df = final_df[cluster_sizes > 1].sort_values("cluster_id")
print(duplicates_df[["cluster_id", "unique_id", "farm_name", "operator_first_name", "operator_last_name", "state", "county", "zip_code"]])
