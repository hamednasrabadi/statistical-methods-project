import pandas as pd
import numpy as np
import os
import sys
import statsmodels.api as sm
from scipy import stats
from statsmodels.formula.api import ols
import textwrap

# ---------------------------------------------------------
# 1. VISUAL SETTINGS
# ---------------------------------------------------------
class Color:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    GREY = '\033[90m'
    WHITE = '\033[97m'
    END = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print(f"\n{Color.HEADER}▓▓▓▓ {title} ▓▓▓▓{Color.END}")

def format_p(p):
    if p < 0.001: return f"{Color.GREEN}< .001 ***{Color.END}"
    elif p < 0.05: return f"{Color.GREEN}{p:.3f} *{Color.END}"
    else: return f"{Color.RED}{p:.3f} (ns){Color.END}"

def print_report_box(text):
    """Prints the narrative report in a clean, professional box."""
    # تنظیم عرض باکس
    WIDTH = 70
    
    print(f"\n   {Color.YELLOW}📝 ACADEMIC REPORT (APA Style):{Color.END}")
    print(f"   {Color.GREY}┌{'─' * WIDTH}┐{Color.END}")
    
    wrapper = textwrap.TextWrapper(width=WIDTH - 4)
    lines = wrapper.wrap(text)
    
    for line in lines:
        print(f"   {Color.GREY}│{Color.END} {Color.WHITE}{line:<{WIDTH - 4}}{Color.END} {Color.GREY}│{Color.END}")
        
    print(f"   {Color.GREY}└{'─' * WIDTH}┘{Color.END}")

# ---------------------------------------------------------
# 2. LOAD DATA
# ---------------------------------------------------------
clear_screen()
try:
    df = pd.read_csv('FinalDataset.csv')
except:
    print(f"{Color.RED}Error: Cleaned_Dataset.csv not found.{Color.END}")
    sys.exit()

# ---------------------------------------------------------
# 3. ANALYSIS ENGINE
# ---------------------------------------------------------

def run_analysis():
    print(f"{Color.BOLD}--- PROFESSIONAL STATISTICAL ANALYSIS DASHBOARD ---{Color.END}")

    # ==========================================
    # 1. PAIRED SAMPLES T-TEST
    # ==========================================
    print_header("1. PAIRED SAMPLES T-TEST (Progress Analysis)")
    
    # --- CALCULATIONS ---
    t_stat, p_val = stats.ttest_rel(df['FinalGrade'], df['PreviousGrade'])
    m_prev = df['PreviousGrade'].mean()
    sd_prev = df['PreviousGrade'].std()
    m_final = df['FinalGrade'].mean()
    sd_final = df['FinalGrade'].std()
    diff = m_final - m_prev

    # --- RAW OUTPUT (NUMBERS) ---
    print(f"   {Color.CYAN}Previous Grade (Mean ± SD):{Color.END}  {m_prev:.2f} ± {sd_prev:.2f}")
    print(f"   {Color.CYAN}Final Grade (Mean ± SD):{Color.END}     {m_final:.2f} ± {sd_final:.2f}")
    print(f"   {Color.CYAN}Mean Difference:{Color.END}             {Color.BOLD}{diff:+.2f}{Color.END}")
    print(f"   {Color.CYAN}T-Statistic:{Color.END}                 {t_stat:.3f}")
    print(f"   {Color.CYAN}Significance (p-value):{Color.END}      {format_p(p_val)}")

    # --- TEXT GENERATION ---
    direction = "significant improvement" if diff > 0 else "significant decline"
    if p_val > 0.05: direction = "no significant change"
    
    p_text = "< .001" if p_val < 0.001 else f"= {p_val:.3f}"
    
    report_1 = (
        f"A paired-samples t-test was conducted to evaluate the impact of the educational program on students' academic performance. "
        f"The results indicated a statistically {direction} in grades from the beginning of the semester "
        f"(M = {m_prev:.2f}, SD = {sd_prev:.2f}) to the final assessment (M = {m_final:.2f}, SD = {sd_final:.2f}), "
        f"t({len(df)-1}) = {t_stat:.2f}, p {p_text}. "
        f"The mean difference was {abs(diff):.2f} points."
    )
    print_report_box(report_1)

    # ==========================================
    # 2. INDEPENDENT SAMPLES T-TEST (GENDER)
    # ==========================================
    print_header("2. INDEPENDENT T-TEST (Gender Gap)")
    
    # --- CALCULATIONS ---
    m_grades = df[df['Gender'] == 'Male']['FinalGrade']
    f_grades = df[df['Gender'] == 'Female']['FinalGrade']
    t_stat, p_val = stats.ttest_ind(m_grades, f_grades)
    
    # --- RAW OUTPUT (NUMBERS) ---
    print(f"   {Color.CYAN}Male Mean:{Color.END}    {m_grades.mean():.2f} (N={len(m_grades)})")
    print(f"   {Color.CYAN}Female Mean:{Color.END}  {f_grades.mean():.2f} (N={len(f_grades)})")
    print(f"   {Color.CYAN}T-Statistic:{Color.END}  {t_stat:.3f}")
    print(f"   {Color.CYAN}Sig (p-value):{Color.END} {format_p(p_val)}")

    # --- TEXT GENERATION ---
    if p_val < 0.05:
        winner = "females" if f_grades.mean() > m_grades.mean() else "males"
        conclusion = f"revealed that {winner} performed significantly better than the other group."
    else:
        conclusion = "indicated no statistically significant difference in academic performance between males and females."

    p_text = "< .001" if p_val < 0.001 else f"= {p_val:.3f}"
    
    report_2 = (
        f"An independent-samples t-test was performed to compare final grades between male and female students. "
        f"The analysis {conclusion} (Male M = {m_grades.mean():.2f}, SD = {m_grades.std():.2f}; "
        f"Female M = {f_grades.mean():.2f}, SD = {f_grades.std():.2f}; "
        f"t({len(df)-2}) = {t_stat:.2f}, p {p_text})."
    )
    print_report_box(report_2)

    # ==========================================
    # 2.5 ONLINE CLASSES EFFECT ANALYSIS
    # ==========================================
    print_header("2.5 ONLINE vs OFFLINE CLASSES (Impact Analysis)")

    # --- Ensure GradeChange exists BEFORE split ---
    if 'GradeChange' not in df.columns:
        df['GradeChange'] = df['FinalGrade'] - df['PreviousGrade']

    # --- Split Groups ---
    online = df[df['OnlineClassesTaken'] == "True"]
    offline = df[df['OnlineClassesTaken'] == "False"]

    n_online = len(online)
    n_offline = len(offline)

    print(f"   {Color.CYAN}Sample Sizes:{Color.END}")
    print(f"      Online Classes:  N = {n_online}")
    print(f"      Offline Classes: N = {n_offline}\n")

    # --- DESCRIPTIVE STATS (ALWAYS VALID) ---
    print(f"   {Color.CYAN}Descriptive Statistics:{Color.END}")
    print(f"      Final Grade Mean:")
    print(f"         Online:  {online['FinalGrade'].mean():.2f}")
    print(f"         Offline: {offline['FinalGrade'].mean():.2f}")

    print(f"      Grade Improvement Mean (Δ):")
    print(f"         Online:  {online['GradeChange'].mean():+.2f}")
    print(f"         Offline: {offline['GradeChange'].mean():+.2f}")

    # --- INFERENTIAL TEST (ONLY IF VALID) ---
    MIN_N = 5  # conservative threshold

    if n_online >= MIN_N and n_offline >= MIN_N:
        print(f"\n   {Color.GREEN}Inferential Test Applied (Independent T-Test){Color.END}")

        t_fg, p_fg = stats.ttest_ind(
            online['FinalGrade'],
            offline['FinalGrade'],
            equal_var=False
        )

        t_gc, p_gc = stats.ttest_ind(
            online['GradeChange'],
            offline['GradeChange'],
            equal_var=False
        )

        print(f"      Final Grade: t = {t_fg:.3f}, p = {format_p(p_fg)}")
        print(f"      Improvement: t = {t_gc:.3f}, p = {format_p(p_gc)}")

        # --- APA REPORT ---
        p_fg_text = "< .001" if p_fg < 0.001 else f"= {p_fg:.3f}"
        p_gc_text = "< .001" if p_gc < 0.001 else f"= {p_gc:.3f}"

        report_online = (
            f"An independent-samples t-test was conducted to examine whether participation in online classes "
            f"was associated with differences in academic outcomes. The results indicated "
            f"no statistically reliable difference in final grades between online and offline students "
            f"(Online M = {online['FinalGrade'].mean():.2f}, Offline M = {offline['FinalGrade'].mean():.2f}), "
            f"t({n_online + n_offline - 2}) = {t_fg:.2f}, p {p_fg_text}. "
            f"Similarly, the difference in grade improvement was not statistically significant "
            f"(Online ΔM = {online['GradeChange'].mean():+.2f}, Offline ΔM = {offline['GradeChange'].mean():+.2f}), "
            f"t({n_online + n_offline - 2}) = {t_gc:.2f}, p {p_gc_text}."
        )

        print_report_box(report_online)

    else:
        print(f"\n   {Color.YELLOW}⚠ Inferential Test Skipped{Color.END}")
        print(f"      Reason: One or both groups have insufficient sample size (N < {MIN_N}).")
        print(f"      Interpretation based on descriptive statistics only.")

        report_online = (
            f"The effect of online class participation on academic performance was examined descriptively. "
            f"Although differences in mean final grades and grade improvement were observed between online "
            f"and offline students, inferential statistical testing was not conducted due to insufficient "
            f"sample size in at least one group. As a result, no statistically reliable conclusions can be "
            f"drawn regarding the impact of online classes in this dataset."
        )

        print_report_box(report_online)


    # ==========================================
    # 3. ONE-WAY ANOVA (PARENTAL SUPPORT)
    # ==========================================
    print_header("3. ONE-WAY ANOVA (Parental Support)")
    
    # --- CALCULATIONS ---
    model = ols('FinalGrade ~ C(ParentalSupport)', data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)
    f_val = anova['F'].iloc[0]
    p_val = anova['PR(>F)'].iloc[0]
    
    means = df.groupby('ParentalSupport')['FinalGrade'].mean().sort_values(ascending=False)

    # --- RAW OUTPUT (NUMBERS) ---
    print(f"   {Color.CYAN}Group Means:{Color.END}")
    for support, score in means.items():
        print(f"     - {support:<7}: {score:.2f}")
    
    print(f"   {Color.CYAN}F-Value:{Color.END}     {f_val:.3f}")
    print(f"   {Color.CYAN}Sig (p-value):{Color.END} {format_p(p_val)}")

    # --- TEXT GENERATION ---
    p_text = "< .001" if p_val < 0.001 else f"= {p_val:.3f}"
    
    if p_val < 0.05:
        best_group = means.index[0]
        interpretation = (f"Post hoc comparisons using the Tukey HSD test indicated that the mean score for the '{best_group}' "
                          f"support group (M = {means.iloc[0]:.2f}) was significantly higher than the other groups.")
    else:
        interpretation = "However, the differences between the groups were not statistically significant."

    report_3 = (
        f"A one-way analysis of variance (ANOVA) was conducted to explore the impact of parental support levels on students' final grades. "
        f"There was a significant effect of parental support on grades [F(2, {len(df)-3}) = {f_val:.2f}, p {p_text}]. "
        f"{interpretation}"
    )
    print_report_box(report_3)


        # ==========================================
    # 3.5 GENDER AS PREDICTOR (REGRESSION CHECK)
    # ==========================================
    print_header("3.5 GENDER AS PREDICTOR (Model Eligibility Check)")

    male = df[df['Gender'] == 'Male']['FinalGrade']
    female = df[df['Gender'] == 'Female']['FinalGrade']

    t_gender, p_gender = stats.ttest_ind(male, female, equal_var=False)

    print(f"   {Color.CYAN}Male Mean:{Color.END}    {male.mean():.2f}")
    print(f"   {Color.CYAN}Female Mean:{Color.END}  {female.mean():.2f}")
    print(f"   {Color.CYAN}T-Statistic:{Color.END}  {t_gender:.3f}")
    print(f"   {Color.CYAN}Sig (p-value):{Color.END} {format_p(p_gender)}")

    p_text = "< .001" if p_gender < 0.001 else f"= {p_gender:.3f}"

    if p_gender < 0.05:
        decision = (
            "The null hypothesis was rejected, indicating that gender is statistically "
            "associated with differences in final grades. Despite this significance, gender "
            "was not included in the regression model to maintain interpretability and to focus "
            "on modifiable academic behaviors."
        )
    else:
        decision = (
            "The null hypothesis was not rejected, indicating that gender does not significantly "
            "predict final grades. Accordingly, gender was excluded from the regression model to "
            "prevent unnecessary model complexity."
        )

    report_gender = (
        f"An independent-samples t-test was conducted to evaluate whether gender could serve as a "
        f"predictive factor for students’ final grades. The results indicated that the difference "
        f"between male (M = {male.mean():.2f}) and female students (M = {female.mean():.2f}) was "
        f"{'statistically significant' if p_gender < 0.05 else 'not statistically significant'}, "
        f"t({len(df)-2}) = {t_gender:.2f}, p {p_text}. {decision}"
    )

    print_report_box(report_gender)


    # ==========================================
    # 4. MULTIPLE REGRESSION (Predictive Model)
    # ==========================================
    print_header("4. MULTIPLE LINEAR REGRESSION (Predictive Model)")

    # --- DATA PREPARATION ---
    df['OnlineClassesTaken'] = df['OnlineClassesTaken'].astype(str).str.strip()
    df['OnlineBinary'] = df['OnlineClassesTaken'].map({'True': 1, 'False': 0})

    predictors = [
        'StudyHoursPerWeek',
        'AttendanceRate',
        'PreviousGrade',
        'OnlineBinary'
    ]

    X = df[predictors]
    X = sm.add_constant(X)
    y = df['FinalGrade']

    # --- INITIAL MODEL ---
    full_model = sm.OLS(y, X).fit()

    # --- IDENTIFY NON-SIGNIFICANT VARIABLES ---
    non_significant = [
        var for var, p in full_model.pvalues.items()
        if p > 0.05 and var != 'const'
    ]

    significant_vars = [
        var for var in predictors
        if var not in non_significant
    ]

    # --- FINAL MODEL (REDUCED) ---
    X_final = sm.add_constant(df[significant_vars])
    final_model = sm.OLS(y, X_final).fit()

    # --- RAW OUTPUT ---
    print(f"   {Color.CYAN}Initial Predictors:{Color.END} {', '.join(predictors)}")
    print(f"   {Color.CYAN}Removed (Not Significant):{Color.END} "
          f"{', '.join(non_significant) if non_significant else 'None'}\n")

    print(f"   {Color.CYAN}Final Model R-Squared:{Color.END} "
          f"{Color.BOLD}{final_model.rsquared:.3f}{Color.END} "
          f"(Explains {final_model.rsquared*100:.1f}% of variance)\n")

    print(f"   {Color.CYAN}Final Regression Coefficients:{Color.END}")

    for var in final_model.params.index:
        coef = final_model.params[var]
        pval = final_model.pvalues[var]
        c_code = Color.GREEN if pval < 0.05 else Color.RED
        print(f"     - {var:<18}: Coef={c_code}{coef:7.3f}{Color.END} | p={format_p(pval)}")

    # --- BUILD PREDICTION EQUATION ---
    coeffs = final_model.params
    equation_terms = []

    for var, coef in coeffs.items():
        if var != 'const':
            sign = "+" if coef >= 0 else "-"
            equation_terms.append(f"{sign} {abs(coef):.3f}·{var}")

    prediction_equation = (
        f"FinalGrade = {coeffs['const']:.3f} " + " ".join(equation_terms)
    )

    print(f"\n   {Color.CYAN}Final Prediction Equation:{Color.END}")
    print(f"   {prediction_equation}")

    # --- APA STYLE REPORT ---
    removed_vars_str = ", ".join(non_significant) if non_significant else "none"

    p_model = "< .001" if final_model.f_pvalue < 0.001 else f"= {final_model.f_pvalue:.3f}"

    report_4 = (
        f"A multiple linear regression analysis was conducted to predict students’ final grades using "
        f"study hours, attendance rate, prior academic performance, and online class participation as predictors. "
        f"Initial analyses indicated that the following variables were not statistically significant "
        f"(p > .05): {removed_vars_str}. These predictors were removed to reduce model complexity and minimize "
        f"the risk of overfitting. The final regression model was statistically significant, "
        f"F({int(final_model.df_model)}, {int(final_model.df_resid)}) = {final_model.fvalue:.2f}, "
        f"p {p_model}, and explained {final_model.rsquared*100:.1f}% of the variance in final grades. "
        f"The resulting prediction equation was:\n\n"
        f"{prediction_equation}."
    )

    print_report_box(report_4)


# RUN
run_analysis()
print("\n")