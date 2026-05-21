from splink import SettingsCreator, block_on
import splink.comparison_library as cl

settings = SettingsCreator(
    link_type="dedupe_only",
    blocking_rules_to_generate_predictions=[
        block_on("state", "county"),
        block_on("operator_last_name")
    ],
    comparisons=[
        cl.JaroWinklerAtThresholds("farm_name", [0.9, 0.7]),
        cl.JaroWinklerAtThresholds("operator_first_name", [0.9, 0.7]),
        cl.ExactMatch("operator_last_name"),
        cl.ExactMatch("state"),
        cl.ExactMatch("county"),
        cl.ExactMatch("zip_code")
    ],
    retain_intermediate_calculation_columns=True
)