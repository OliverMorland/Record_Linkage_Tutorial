from training import linker
from prediction import df_predictions, df_clusters

linker.visualisations.waterfall_chart(df_predictions.as_pandas_dataframe().to_dict(orient="records")[:2])

linker.visualisations.cluster_studio_dashboard(
    df_predictions, 
    df_clusters, 
    out_path="nass_cluster_studio.html", 
    overwrite=True
)