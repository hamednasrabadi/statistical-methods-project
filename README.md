# Statistical Methods Project: Educational Performance Analysis

A comprehensive statistical analysis of factors influencing student academic performance, combining SPSS and Python pipelines for data preparation, hypothesis testing, modeling, and reporting.

> **Course:** Statistical Methods, University of Tehran, Statistics undergraduate program (3rd semester).
>
> **Report language:** Persian (Farsi). The Python code and SPSS output names are in English.

## Research Question

How do factors such as gender, study habits, attendance, family support, extracurricular activities, and online vs. in-person instruction relate to student academic performance, and which of these can be used to build a predictive model of final grades?

## Methodology Overview

The analysis follows a complete statistical workflow:

1. **Data architecture & preprocessing**: schema design, validation, and cleaning protocols.
2. **Exploratory data analysis**: distributional checks, group comparisons, and assumption testing.
3. **Inferential statistical testing**: a wide battery of parametric and nonparametric tests.
4. **Predictive modeling**: feature screening and multiple linear regression.
5. **Discussion & validation**: methodological critique and data-integrity audit.

### Tests Applied

**Parametric:**
- Paired-Samples *t*-Test (within-subject grade change)
- Independent-Samples *t*-Test (gender; class type)
- One-Way ANOVA (parental support)
- Two-Way ANOVA (interaction effects)
- ANCOVA (controlling for previous grade)
- Multiple Linear Regression (predictive modeling)

**Nonparametric:**
- Shapiro-Wilk Test (normality)
- Runs Test (randomness)
- Chi-Square Test (independence)
- One-Sample Binomial Test
- Mann-Whitney U Test
- Kruskal-Wallis Test
- Spearman's Rho (rank correlation)

### Modeling
Feature screening via correlation matrix and Spearman's Rho, followed by a multiple linear regression model fit on the selected predictors of final academic performance.

## Repository Structure

```
statistical-methods-project/
├── README.md
├── Data.sav                 # Primary SPSS dataset
├── Report.pdf               # Full 7-chapter research report (Persian)
├── Report_maker.md          # Source markdown for the report
├── code/                    # Python analysis pipeline + working CSVs
│   ├── Action_Plan.py            # Intervention-recommendation dashboard
│   ├── Data_Processor.py         # Data cleaning & feature engineering
│   ├── Investigation.py          # Data integrity & validation audit
│   ├── SPSS_Reporter.py          # SPSS output ingestion & summary
│   ├── Visualizer.py             # Plots & figures
│   ├── statistical_diagnostics.py # Normality, homogeneity, assumption checks
│   ├── Raw_Dataset.csv
│   └── FinalDataset.csv
├── spss-outputs/            # 15 SPSS test outputs (.spv) + SPSS data file
└── images/                  # Figures used in the report
```

## Report Structure (7 chapters)

1. **Introduction**: research questions and motivation
2. **Data architecture**: data dictionary, preprocessing protocols, validation
3. **Exploratory analysis**: distributions, group comparisons, normality & randomness checks
4. **Inferential analysis**: full battery of parametric and nonparametric tests
5. **Modeling**: feature screening and multiple linear regression
6. **Discussion**: interpretation, limitations, and methodological reflections (incl. Hawthorne effect)
7. **Validation & quality control**: audit of the data reconstruction pipeline

## Tech Stack

- **Python**: pandas, NumPy, SciPy, statsmodels, matplotlib
- **SPSS**: primary statistical testing platform
- **Markdown / HTML**: report authoring with custom styling

## Running the Code

The Python scripts in `code/` are designed to be run from inside that directory (they reference CSVs by relative path).

```bash
cd code/
pip install pandas numpy scipy statsmodels matplotlib
python statistical_diagnostics.py
```

## Note on Data

The dataset is **simulated**, not real student records. All names in the CSV are placeholder values. No personally identifiable information is included.

## Author

Hamed Nasrabadi, Statistics student at the University of Tehran.
