# Record Linkage Challenge: NASS Agricultural Survey Deduplication

## Background

The USDA National Agricultural Statistics Service (NASS) conducts surveys across thousands of farm operations each year. A common data quality problem is that the same farm operation gets recorded more than once — under slightly different names, with nicknames instead of legal first names, or with minor address variations introduced by different data entry staff or survey forms.

Your job is to write Python and Splink code that identifies these duplicate records in a 2,000-record survey dataset.

---

## The Dataset

The dataset lives in `src/challenge_dataset.py`. Import it like this:

```python
from challenge_dataset import df
```

It contains the following columns:

| Column | Description |
|---|---|
| `unique_id` | Unique integer identifier (1–2000) |
| `farm_name` | Name of the farm or agricultural operation |
| `operator_first_name` | First name of the farm operator |
| `operator_last_name` | Last name of the farm operator |
| `state` | Two-letter state abbreviation |
| `county` | County name |
| `zip_code` | Five-digit ZIP code (stored as string) |

The dataset contains **7 duplicate pairs** — 14 records total — where the same real-world farm operation was entered twice with data entry variations. The other 1,986 records are unique.

---

## Your Task

Write three Python scripts (or adapt the existing ones in `src/`) to:

### 1. Configure Splink settings (`settings_creator.py`)

Define a `SettingsCreator` with:
- `link_type = "dedupe_only"`
- Appropriate **blocking rules** to limit candidate pairs
- **Comparisons** for each field that could contain variation

Think carefully about which comparisons to use for each field type. String similarity metrics like Jaro-Winkler work well for names that vary by typos or abbreviations. Should `zip_code` use exact match or something else?

### 2. Train the model (`training.py`)

- Initialize a `Linker` with your dataset and settings
- Estimate `u` probabilities using random sampling
- Run at least two rounds of Expectation-Maximisation with different blocking rules to train `m` probabilities

### 3. Generate predictions (`prediction.py`)

- Call `linker.inference.predict()` with an appropriate threshold
- Cluster the predictions with `linker.clustering.cluster_pairwise_predictions_at_threshold()`
- Print the resulting clusters showing `cluster_id`, `unique_id`, `farm_name`, `operator_first_name`, and `operator_last_name`

---

## What "Duplicate" Means Here

Two records are duplicates if they describe the **same farm operation** reported twice. The variations you will encounter include:

- **Nicknames**: Michael → Mike, Patricia → Pat, William → Bill, James → Jim, Susan → Sue, Elizabeth → Beth
- **First-name initials**: David → D.
- **Farm name abbreviations**: Agriculture → Ag, Company → Co
- **Corporate suffix added**: Ranch → Ranch LLC
- **Compound vs. spaced words**: Timber Creek → Timbercreek
- **Singular/plural variations**: Farm → Farms, Wind → Winds
- **Typos**: a dropped letter in a farm name
- **Minor address differences**: ZIP code off by one digit

A successful run will produce **7 clusters of size 2** (each cluster = one pair of duplicate records).

---

## Hints

<details>
<summary>Hint 1 — Blocking strategy</summary>

Two records from completely different states are almost certainly not duplicates. Blocking on `state` and `county` together is a good starting point. You may also want a second blocking rule on `operator_last_name` alone to catch pairs where the county field has minor differences.

</details>

<details>
<summary>Hint 2 — Choosing comparisons</summary>

`JaroWinklerAtThresholds` is well-suited to farm names and personal names because it handles transpositions and truncations. Use thresholds like `[0.9, 0.7]` to create three similarity levels (high / medium / non-match).

For `zip_code`, consider whether `ExactMatch` alone is sufficient, or whether you need a fuzzy comparison to catch a one-digit difference.

</details>

<details>
<summary>Hint 3 — The hardest pair</summary>

One pair has a zip code that differs by exactly 1 digit AND both first-name and farm-name variations. If your model misses it, check whether your `zip_code` comparison is too strict, and whether your blocking rules ensure these two records end up as a candidate pair at all.

</details>

<details>
<summary>Hint 4 — Evaluating your results</summary>

After clustering, filter for clusters where more than one `unique_id` appears. If you find exactly 7 such clusters, each containing exactly 2 records, you have found all the duplicates.

```python
cluster_sizes = final_df.groupby("cluster_id")["unique_id"].count()
duplicates_found = cluster_sizes[cluster_sizes > 1]
print(f"Duplicate clusters found: {len(duplicates_found)}")
print(duplicates_found)
```

</details>

---

## Stretch Goals

Once you have the basic pipeline working:

1. **Visualise match weights** — use `linker.visualisations.match_weights_chart()` to see which fields are the most discriminating predictors of a match.
2. **Waterfall chart** — pick one of your matched pairs and use `linker.visualisations.waterfall_chart()` to see exactly why Splink scored it as a match.
3. **Tune your thresholds** — experiment with `threshold_match_probability` values between 0.5 and 0.9. What happens to precision and recall?
4. **False positives** — are there any clusters of size 2 in your output that are NOT true duplicates? What field comparisons could you add or tighten to eliminate them?

---

---

---

## Answer Key

> **STOP — only read this after you have run your own pipeline.**

The 7 duplicate pairs and their `unique_id` values are:

| Pair | unique_id A | unique_id B | Difficulty | Variations |
|------|-------------|-------------|------------|------------|
| 1 | 47 | 311 | Easy | `Sunrise Valley Farm` → `Sunrise Valley Farms`; `Michael` → `Mike` |
| 2 | 88 | 441 | Easy-Medium | `Clearwater Ranch` → `Clearwater Ranch LLC`; `Patricia` → `Pat` |
| 3 | 133 | 601 | Medium | `Golden Acres Agriculture` → `Golden Acres Ag`; `David` → `D.` |
| 4 | 201 | 751 | Medium | `Timber Creek Organics` → `Timbercreek Organics`; `James` → `Jim` |
| 5 | 351 | 821 | Hard | `Prairie Wind Farm` → `Prairie Winds Farm`; `Susan` → `Sue`; ZIP `68801` → `68802` |
| 6 | 501 | 1051 | Medium | `Heartland Grain Company` → `Heartland Grain Co`; `William` → `Bill` |
| 7 | 701 | 1401 | Hard | `Blue Ridge Livestock` → `Blue Rdge Livestock` (typo); `Elizabeth` → `Beth` |

### Notes on each pair

**Pair 1** is the most straightforward. JaroWinkler on `farm_name` will score `Farm` vs `Farms` very high, and both blocking rules (state+county and last name) will include this pair.

**Pair 2** is easy if your `farm_name` comparison handles trailing suffixes — `Clearwater Ranch LLC` has a low Jaro-Winkler distance from `Clearwater Ranch`.

**Pair 3** is the first real test. `D.` vs `David` will score lower than you might expect on Jaro-Winkler — this pair relies heavily on the `farm_name` and location fields agreeing strongly. If you miss it, consider adding a comparison that checks whether one value is a prefix or initial of the other.

**Pair 4** — `Timbercreek` vs `Timber Creek` is a classic compound-word variation. Jaro-Winkler handles this well since the characters are all present.

**Pair 5** is the hardest. The ZIP codes differ by 1 digit, which means an `ExactMatch` on `zip_code` will actually count against this pair. Using `JaroWinklerAtThresholds("zip_code", [0.9])` instead will score `68801` vs `68802` as a near-match rather than a non-match, helping the model reach the right conclusion.

**Pair 6** — `Company` → `Co` is a heavy abbreviation that JaroWinkler scores lower than you might expect (~0.73). Make sure your lower threshold (e.g. 0.7) is set to include this level of similarity.

**Pair 7** is the trickiest farm-name variation: `Blue Ridge` vs `Blue Rdge` — a single dropped character. JaroWinkler handles single-character deletions well, so this should score around 0.97. The challenge is that `Elizabeth` → `Beth` is a short-form nickname with no character overlap, which will score low on JaroWinkler. The pair survives because the farm name, last name, state, county, and ZIP all agree strongly.
