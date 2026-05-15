import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# =========================================================
# 1. LOAD & PREPARE DATA
# =========================================================
df = pd.read_csv("FinalDataset.csv")

df["GradeChange"] = df["FinalGrade"] - df["PreviousGrade"]


# =========================================================
# 2. OUTPUT SANITIZER (NUMPY → PYTHON NATIVE)
# =========================================================
def clean_value(x):
    if isinstance(x, (np.floating, np.integer)):
        return float(x)
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, dict):
        return {k: clean_value(v) for k, v in x.items()}
    return x


# =========================================================
# 3. NORMALITY ASSESSMENT
# =========================================================
def normality_assessment():
    results = {}

    for col in ["FinalGrade", "GradeChange"]:
        stat, p = stats.shapiro(df[col])
        results[col] = {
            "shapiro_p": p,
            "normal": p > 0.05,
            "skewness": stats.skew(df[col]),
            "kurtosis": stats.kurtosis(df[col])
        }

    conclusion = (
        "Parametric tests justified"
        if all(v["normal"] for v in results.values())
        else "Normality violated"
    )

    return {
        "metric": "Normality Assessment",
        "results": results,
        "conclusion": conclusion
    }


# =========================================================
# 4. VARIANCE HOMOGENEITY (GENDER)
# =========================================================
def variance_homogeneity_gender():
    males = df[df["Gender"] == "Male"]["FinalGrade"]
    females = df[df["Gender"] == "Female"]["FinalGrade"]

    stat, p = stats.levene(males, females)

    return {
        "metric": "Variance Homogeneity (Gender)",
        "levene_p": p,
        "homogeneous": p > 0.05,
        "interpretation": (
            "Standard t-test applicable"
            if p > 0.05
            else "Welch correction recommended"
        )
    }


# =========================================================
# 5. MULTICOLLINEARITY (VIF)
# =========================================================
def multicollinearity_diagnostics():
    X = df[["StudyHoursPerWeek", "AttendanceRate", "PreviousGrade"]]
    X = sm.add_constant(X)

    vif = {
        col: variance_inflation_factor(X.values, i)
        for i, col in enumerate(X.columns)
        if col != "const"
    }

    problematic = {
        k: v for k, v in vif.items() if v > 5
    }

    return {
        "metric": "Multicollinearity Diagnostics",
        "VIF": vif,
        "problematic_variables": problematic,
        "conclusion": (
            "No critical multicollinearity"
            if not problematic
            else "Multicollinearity detected"
        )
    }


# =========================================================
# 6. REGRESSION + RESIDUAL DIAGNOSTICS
# =========================================================
def regression_residual_diagnostics():
    X = df[["StudyHoursPerWeek", "AttendanceRate", "PreviousGrade"]]
    X = sm.add_constant(X)
    y = df["FinalGrade"]

    model = sm.OLS(y, X).fit()
    residuals = model.resid

    stat, p = stats.shapiro(residuals)

    return {
        "metric": "Residual Diagnostics",
        "residual_mean": residuals.mean(),
        "shapiro_p": p,
        "normal_residuals": p > 0.05,
        "model_valid": p > 0.05
    }


# =========================================================
# 7. MASTER REPORT
# =========================================================
def run_diagnostics():
    diagnostics = [
        normality_assessment(),
        variance_homogeneity_gender(),
        multicollinearity_diagnostics(),
        regression_residual_diagnostics()
    ]

    print("\n================ STATISTICAL DIAGNOSTICS ================\n")

    for d in diagnostics:
        print(f"▶ {d['metric']}")
        for k, v in d.items():
            if k != "metric":
                print(f"   - {k}: {clean_value(v)}")
        print()

    print("========================================================")
    print("\nINTERPRETATION GUIDE:")
    print("- Assumptions satisfied → inferential results reliable")
    print("- Violations detected → interpret with caution\n")


# =========================================================
# 8. RUN
# =========================================================
if __name__ == "__main__":
    run_diagnostics()
