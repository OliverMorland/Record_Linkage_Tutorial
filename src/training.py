from splink import Linker, DuckDBAPI
from settings_creator import settings
from nass_data import df

db_api = DuckDBAPI()
linker = Linker(df, settings, db_api=db_api)
linker.training.estimate_u_using_random_sampling(max_pairs=1e5)
linker.training.estimate_parameters_using_expectation_maximisation(blocking_rule="l.state = r.state AND l.county = r.county")
linker.training.estimate_parameters_using_expectation_maximisation(blocking_rule="l.operator_last_name = r.operator_last_name")