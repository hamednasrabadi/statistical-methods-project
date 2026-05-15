import pandas as pd
import numpy as np
import os
import sys

# ---------------------------------------------------------
# 1. VISUAL SETUP
# ---------------------------------------------------------
class Color:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    GREY = '\033[90m'
    END = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print(f"\n{Color.HEADER}█▓▒░ {title} ░▒▓█{Color.END}")

def print_row(rank, name, student_id, prev, final, change, status):
    """Prints a perfectly aligned row."""
    # Define widths
    w_rank, w_name, w_id, w_prev, w_final, w_change = 5, 22, 8, 12, 12, 10
    
    row_str = (
        f"{rank:<{w_rank}} "
        f"{name:<{w_name}} "
        f"{student_id:<{w_id}} "
        f"{prev:<{w_prev}} "
        f"{final:<{w_final}} "
        f"{change:<{w_change}} "
        f"{status}"
    )
    print(row_str)

# ---------------------------------------------------------
# 2. LOAD & ALIGN DATA
# ---------------------------------------------------------
clear_screen()
clean_file = 'FinalDataset.csv'
raw_file = 'Raw_Dataset.csv'

try:
    # Load Clean Data
    df_clean = pd.read_csv(clean_file)
    df_clean['GradeChange'] = df_clean['FinalGrade'] - df_clean['PreviousGrade']
    # Set ID as index for accurate looking up
    df_clean.set_index('StudentID', inplace=True, drop=False) 
    print(f"{Color.GREEN}✔ Cleaned data loaded.{Color.END}")
except:
    print(f"{Color.RED}Error: '{clean_file}' not found.{Color.END}")
    sys.exit()

has_raw = False
try:
    # Load Raw Data
    df_raw = pd.read_csv(raw_file)
    df_raw.set_index('StudentID', inplace=True, drop=False)
    print(f"{Color.GREEN}✔ Raw data loaded for verification.{Color.END}")
    has_raw = True
except:
    print(f"{Color.YELLOW}⚠ Warning: '{raw_file}' not found. Cannot detect imputed values.{Color.END}")

# ---------------------------------------------------------
# 3. INSPECTION ENGINE
# ---------------------------------------------------------
def investigate_subset(subset_df, title, change_color):
    print_header(title)
    
    # Print Table Header
    print(f"{Color.BOLD}{'#':<5} {'NAME':<22} {'ID':<8} {'PREV':<12} {'FINAL':<12} {'CHANGE':<10} {'DATA STATUS'}{Color.END}")
    print(f"{Color.GREY}" + "-" * 95 + f"{Color.END}")

    rank_counter = 1
    
    for student_id, row in subset_df.iterrows():
        name = row['Name']
        # Values from CLEAN file
        clean_prev = row['PreviousGrade']
        clean_final = row['FinalGrade']
        change = row['GradeChange']

        # Check RAW file for NaNs (Imputation detection)
        is_prev_imputed = False
        is_final_imputed = False
        
        if has_raw and student_id in df_raw.index:
            raw_row = df_raw.loc[student_id]
            if pd.isna(raw_row['PreviousGrade']): is_prev_imputed = True
            if pd.isna(raw_row['FinalGrade']): is_final_imputed = True

        # --- Formatting Strings ---
        
        # 1. Previous Grade String
        prev_str = f"{clean_prev:.1f}"
        if is_prev_imputed:
            prev_str = f"{Color.YELLOW}{prev_str} (Imp){Color.END}"
        
        # 2. Final Grade String
        final_str = f"{clean_final:.1f}"
        if is_final_imputed:
            final_str = f"{Color.YELLOW}{final_str} (Imp){Color.END}"
            
        # 3. Change String
        sign = "+" if change > 0 else ""
        change_str = f"{change_color}{sign}{change:.1f}{Color.END}"

        # 4. Status String
        status_parts = []
        if is_prev_imputed: status_parts.append("PREV")
        if is_final_imputed: status_parts.append("FINAL")
        
        if status_parts:
            status_str = f"{Color.RED}⚠ IMPUTED: {', '.join(status_parts)}{Color.END}"
        else:
            status_str = f"{Color.GREEN}✔ Real Data{Color.END}"

        # Print using the aligned helper
        print_row(str(rank_counter), name, str(int(student_id)), prev_str, final_str, change_str, status_str)
        rank_counter += 1

# ---------------------------------------------------------
# 4. EXECUTE
# ---------------------------------------------------------

# Sort Data
df_sorted = df_clean.sort_values(by='GradeChange', ascending=False)

# Top 10 Growth
top_10 = df_sorted.head(10)
investigate_subset(top_10, "TOP 10 GROWTH INVESTIGATION", Color.GREEN)

print("\n")

# Bottom 10 Drop
bottom_10 = df_sorted.tail(10).sort_values(by='GradeChange', ascending=True)
investigate_subset(bottom_10, "WORST 10 FALL INVESTIGATION", Color.RED)

print("\n" + "="*95)
print(f" {Color.BOLD}LEGEND:{Color.END}")
print(f" {Color.YELLOW}(Imp){Color.END} = Value was missing in Raw Data and was auto-filled (Imputed) by Python.")
print(f" {Color.RED}⚠{Color.END}     = Be cautious interpreting these specific changes as they may be artificial.")
print("="*95 + "\n")