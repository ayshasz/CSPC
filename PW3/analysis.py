# ============================================================
# PW3 - Data, Distributions, Testing, and Causation
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from pathlib import Path


# ============================================================
# SETUP
# ============================================================

# Create a folder for all generated graphs.
Path("plots").mkdir(exist_ok=True)

# Significance level used in statistical tests.
ALPHA = 0.05


# ============================================================
# DATASET 1: HEART DISEASE
# ============================================================

print("\n" + "=" * 60)
print("DATASET 1: HEART DISEASE")
print("=" * 60)

# Task 1: Load the dataset.
heart = pd.read_csv("heart.csv")

print("\nDataset shape:")
print(heart.shape)

print("\nFirst five rows:")
print(heart.head())

print("\nDataset information:")
heart.info()

# Select the four continuous variables.
continuous_columns = [
    "age",
    "chol",
    "trestbps",
    "thalach"
]

continuous = heart[continuous_columns].apply(
    pd.to_numeric,
    errors="coerce"
)

print("\nSummary statistics:")
print(continuous.describe())

# Check missing values.
print("\nMissing values:")
print(heart[continuous_columns + ["target"]].isna().sum())


# ============================================================
# TASK 2: DISTRIBUTIONS
# ============================================================

print("\n" + "-" * 60)
print("TASK 2: DISTRIBUTIONS")
print("-" * 60)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

for column, ax in zip(continuous_columns, axes.flat):

    values = continuous[column].dropna()

    ax.hist(
        values,
        bins=20,
        edgecolor="black"
    )

    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")

fig.tight_layout()

fig.savefig(
    "plots/heart_distributions.png",
    dpi=300
)

plt.show()
plt.close(fig)


# ============================================================
# TASK 3: NORMALITY TESTS
# ============================================================

print("\n" + "-" * 60)
print("TASK 3: SHAPIRO-WILK NORMALITY TESTS")
print("-" * 60)

for column in continuous_columns:

    values = continuous[column].dropna()

    statistic, p_value = stats.shapiro(values)

    print(f"\nVariable: {column}")
    print(f"W statistic: {statistic:.4f}")
    print(f"p-value: {p_value:.6g}")

    if p_value < ALPHA:
        print("Verdict: Evidence against normality.")
    else:
        print("Verdict: Insufficient evidence against normality.")


# ============================================================
# TASK 4: COMPARE MAXIMUM HEART RATE
# ============================================================

print("\n" + "-" * 60)
print("TASK 4: HEART RATE COMPARISON")
print("-" * 60)

# Separate the two groups.
disease = heart.loc[
    heart["target"] == 1, "thalach"
].dropna()

healthy = heart.loc[
    heart["target"] == 0, "thalach"
].dropna()

# Calculate means and standard errors.
disease_mean = disease.mean()
healthy_mean = healthy.mean()

disease_se = stats.sem(disease)
healthy_se = stats.sem(healthy)

# Calculate 95% confidence intervals for each mean.
disease_ci = stats.t.interval(
    0.95,
    df=len(disease) - 1,
    loc=disease_mean,
    scale=disease_se
)

healthy_ci = stats.t.interval(
    0.95,
    df=len(healthy) - 1,
    loc=healthy_mean,
    scale=healthy_se
)

print("\nHeart disease group (target = 1):")
print(f"Number of patients: {len(disease)}")
print(f"Mean thalach: {disease_mean:.2f}")
print(f"Standard error: {disease_se:.2f}")
print(
    f"95% confidence interval: "
    f"{disease_ci[0]:.2f} to {disease_ci[1]:.2f}"
)

print("\nHealthy group (target = 0):")
print(f"Number of patients: {len(healthy)}")
print(f"Mean thalach: {healthy_mean:.2f}")
print(f"Standard error: {healthy_se:.2f}")
print(
    f"95% confidence interval: "
    f"{healthy_ci[0]:.2f} to {healthy_ci[1]:.2f}"
)

# Mann-Whitney U test.
mw_result = stats.mannwhitneyu(
    disease,
    healthy,
    alternative="two-sided"
)

print("\nMann-Whitney U test:")
print(f"U statistic: {mw_result.statistic:.2f}")
print(f"p-value: {mw_result.pvalue:.6g}")

if mw_result.pvalue < ALPHA:
    print("Conclusion: The group distributions differ significantly.")
else:
    print("Conclusion: Insufficient evidence of a group difference.")

# Plot the means and their 95% confidence intervals.
means = [disease_mean, healthy_mean]

lower_errors = [
    disease_mean - disease_ci[0],
    healthy_mean - healthy_ci[0]
]

upper_errors = [
    disease_ci[1] - disease_mean,
    healthy_ci[1] - healthy_mean
]

errors = np.array([lower_errors, upper_errors])

fig, ax = plt.subplots(figsize=(8, 5))

ax.errorbar(
    ["Heart disease", "Healthy"],
    means,
    yerr=errors,
    fmt="o",
    capsize=8
)

ax.set_title("Mean Maximum Heart Rate with 95% Confidence Intervals")
ax.set_xlabel("Patient group")
ax.set_ylabel("Maximum heart rate (thalach)")

fig.tight_layout()

fig.savefig(
    "plots/heart_rate_comparison.png",
    dpi=300
)

plt.show()
plt.close(fig)


# ============================================================
# TASK 5: AGE AND MAXIMUM HEART RATE CORRELATION
# ============================================================

print("\n" + "-" * 60)
print("TASK 5: AGE VS MAXIMUM HEART RATE")
print("-" * 60)

age_hr = heart[["age", "thalach"]].dropna()

# Spearman correlation.
spearman_result = stats.spearmanr(
    age_hr["age"],
    age_hr["thalach"]
)

print(f"Spearman correlation: {spearman_result.statistic:.4f}")
print(f"p-value: {spearman_result.pvalue:.6g}")

# Also report Pearson correlation for comparison.
pearson_result = stats.pearsonr(
    age_hr["age"],
    age_hr["thalach"]
)

print(f"Pearson correlation: {pearson_result.statistic:.4f}")
print(f"Pearson p-value: {pearson_result.pvalue:.6g}")

# Scatter plot.
fig, ax = plt.subplots(figsize=(8, 5))

ax.scatter(
    age_hr["age"],
    age_hr["thalach"],
    alpha=0.7
)

ax.set_title("Age vs Maximum Heart Rate")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Maximum heart rate (thalach)")

fig.tight_layout()

fig.savefig(
    "plots/age_vs_thalach.png",
    dpi=300
)

plt.show()
plt.close(fig)


# ============================================================
# DATASET 2: CHEMICAL EXPOSURE
# ============================================================

print("\n" + "=" * 60)
print("DATASET 2: CHEMICAL EXPOSURE")
print("=" * 60)

# Load the chemical dataset.
chemicals = pd.read_csv("chemicals_cancer.csv")

print("\nDataset shape:")
print(chemicals.shape)

print("\nFirst five rows:")
print(chemicals.head())

print("\nSummary statistics:")
print(chemicals.describe())


# ============================================================
# TASK 6: NAIVE CORRELATIONS
# ============================================================

print("\n" + "-" * 60)
print("TASK 6: NAIVE CHEMICAL CORRELATIONS")
print("-" * 60)

for chemical in ["benzene", "cadmium"]:

    result = stats.pearsonr(
        chemicals[chemical],
        chemicals["malignancy"]
    )

    print(f"\nChemical: {chemical}")
    print(f"Pearson correlation: {result.statistic:.4f}")
    print(f"p-value: {result.pvalue:.6g}")

# Examine the other variables' raw correlations with malignancy.
print("\nRaw correlations with malignancy:")
print(
    chemicals[
        ["benzene", "cadmium", "pollution_index", "age", "malignancy"]
    ].corr()["malignancy"]
)


# ============================================================
# TASK 7: ACCOUNT FOR THE CONFOUNDING VARIABLE
# ============================================================

print("\n" + "-" * 60)
print("TASK 7: CONTROL FOR POLLUTION AND AGE")
print("-" * 60)

# Method A: Restrict the pollution range.
middle_pollution = chemicals[
    (chemicals["pollution_index"] > 40)
    & (chemicals["pollution_index"] < 60)
]

print("\nPatients with pollution_index between 40 and 60:")
print(f"Number of patients: {len(middle_pollution)}")

for chemical in ["benzene", "cadmium"]:

    result = stats.pearsonr(
        middle_pollution[chemical],
        middle_pollution["malignancy"]
    )

    print(f"\n{chemical} in restricted group:")
    print(f"Correlation: {result.statistic:.4f}")
    print(f"p-value: {result.pvalue:.6g}")


# Method B: Partial correlation controlling for pollution and age.
#
# First, calculate the variation in each variable that remains
# after fitting a linear model with pollution and age.

controls = chemicals[["pollution_index", "age"]].to_numpy()

# Add an intercept column to the control variables.
controls = np.column_stack([
    np.ones(len(controls)),
    controls
])


def residuals_after_controls(values, control_matrix):
    """Return residuals after linear adjustment for control variables."""

    coefficients = np.linalg.lstsq(
        control_matrix,
        values,
        rcond=None
    )[0]

    predicted = control_matrix @ coefficients

    return values - predicted


malignancy_residuals = residuals_after_controls(
    chemicals["malignancy"].to_numpy(),
    controls
)

print("\nPartial correlations controlling for pollution and age:")

for chemical in ["benzene", "cadmium"]:

    chemical_residuals = residuals_after_controls(
        chemicals[chemical].to_numpy(),
        controls
    )

    result = stats.pearsonr(
        chemical_residuals,
        malignancy_residuals
    )

    print(f"\nChemical: {chemical}")
    print(f"Partial correlation: {result.statistic:.4f}")
    print(f"p-value: {result.pvalue:.6g}")


# ============================================================
# BONUS: CATEGORY BALANCE AND ENTROPY
# ============================================================

print("\n" + "-" * 60)
print("BONUS: TARGET CATEGORY BALANCE")
print("-" * 60)

proportions = heart["target"].value_counts(normalize=True)

print("\nTarget proportions:")
print(proportions)

# Shannon entropy in bits.
p = proportions.to_numpy()

entropy = -np.sum(
    p * np.log2(p)
)

print(f"\nTarget entropy: {entropy:.4f} bits")
print("Maximum entropy for two categories: 1 bit")


# ============================================================
# END OF ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("Check the plots/ folder for the saved graphs.")
print("=" * 60)