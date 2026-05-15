import pandas as pd
import numpy as np
import os
import sys

# ---------------------------------------------------------
# 1. VISUAL SETUP
# ---------------------------------------------------------
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_step(message):
    print(f"{Color.BLUE}[STEP]{Color.END} {message}")

def print_success(message):
    print(f"{Color.GREEN}[SUCCESS]{Color.END} {message}")

# ---------------------------------------------------------
# 2. DATA CLEANING MODULE
# ---------------------------------------------------------
def clean_data(input_file):
    print_step(f"Loading raw data from '{input_file}'...")
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"{Color.RED}Error: '{input_file}' not found.{Color.END}")
        sys.exit()

    # A. Remove Unwanted Columns
    cols_to_remove = ['Attendance', 'StudyHours', 'Attendance (%)']
    df = df.drop(columns=cols_to_remove, errors='ignore')
    df = df.loc[:, ~df.columns.duplicated()] # Remove duplicate columns
    
    # B. Reset ID
    df['StudentID'] = range(1, len(df) + 1)

    # C. Define Types
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()
    
    # Handle mixed types explicitly
    if 'ExtracurricularActivities' in numerical_cols:
        numerical_cols.remove('ExtracurricularActivities')
        categorical_cols.append('ExtracurricularActivities')
    if 'StudentID' in numerical_cols:
        numerical_cols.remove('StudentID')

    # D. Impute Numerical (Mean)
    for col in numerical_cols:
        if df[col].isnull().sum() > 0:
            mean_val = round(df[col].mean(), 1)
            df[col] = df[col].fillna(mean_val)

    # E. Impute Categorical (Weighted Random)
    np.random.seed(42)
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            valid_data = df[col].dropna()
            if not valid_data.empty:
                probs = valid_data.value_counts(normalize=True)
                missing_mask = df[col].isnull()
                random_values = np.random.choice(probs.index, size=missing_mask.sum(), p=probs.values)
                df.loc[missing_mask, col] = random_values

    print_success("Data cleaning & imputation complete.")
    return df

# ---------------------------------------------------------
# 3. LOGIC & FINE-TUNING MODULE (Optimized)
# ---------------------------------------------------------
def apply_academic_logic(df):
    # print_step("Applying academic logic and adjusting grades...")

    # --- VECTORIZED CALCULATION (Faster than .apply) ---
    
    # 1. Base Score (60% of Previous)
    base_score = df['PreviousGrade'] * 0.60
    
    # 2. Study Impact (0.8 points per hour)
    study_score = df['StudyHoursPerWeek'] * 0.8
    
    # 3. Attendance Impact (0.1 points per percentage)
    attendance_score = df['AttendanceRate'] * 0.1
    
    # 4. Parental Support Bonus (Using np.where for conditional logic)
    # High = +5, Others = 0
    support_bonus = np.where(df['ParentalSupport'] == 'High', 5, 0)
    
    # 5. Extracurricular Bonus
    # Activities > 0 = +2
    activity_bonus = np.where(df['ExtracurricularActivities'] > 0, 2, 0)
    
    # 6. Random Noise (Normal Distribution)
    noise = np.random.normal(0, 3, size=len(df))
    
    # --- SUMMATION ---
    final_grade = base_score + study_score + attendance_score + support_bonus + activity_bonus + noise
    
    # --- CLIPPING & ROUNDING ---
    # Enforce constraints: Minimum 50, Maximum 100
    df['FinalGrade'] = final_grade.clip(50, 100).round(1)

    # print_success("Grades recalculated based on logic formula.")
    return df

# ---------------------------------------------------------
# 4. MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Color.BOLD}Starting Data Processing Pipeline...{Color.END}\n")

    # Step 1: Clean
    df_clean = clean_data('Raw_Dataset.csv')
    
    # Save Intermediate (Optional, but good for the 'Investigation' script comparison)
    # df_clean.to_csv('Cleaned_Dataset.csv', index=False)
    # print(f"   -> Saved intermediate file: {Color.YELLOW}Cleaned_Dataset.csv{Color.END}")

    # Step 2: Fine Tune
    df_final = apply_academic_logic(df_clean)

    # Step 3: Save Final
    output_filename = 'FinalDataset.csv'
    df_final.to_csv(output_filename, index=False)

    print("\n" + "="*50)
    print(f"{Color.GREEN}PIPELINE COMPLETE!{Color.END}")
    print(f"Final Optimized Data Saved As: {Color.BOLD}{output_filename}{Color.END}")
    print("="*50 + "\n")