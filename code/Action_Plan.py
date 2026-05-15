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

def print_row(c1, c2, c3, c4, color=Color.END):
    print(f"{color}{c1:<32} {c2:<18} {c3:<18} {c4:<22}{Color.END}")

# ---------------------------------------------------------
# 2. LOAD DATA
# ---------------------------------------------------------
clear_screen()
filename = 'FinalDataset.csv'

try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    print(f"{Color.RED}Error: '{filename}' not found.{Color.END}")
    sys.exit()

if 'GradeChange' not in df.columns:
    df['GradeChange'] = df['FinalGrade'] - df['PreviousGrade']

# ---------------------------------------------------------
# 3. DASHBOARD ENGINE
# ---------------------------------------------------------
def run_dashboard():

    print(f"{Color.BOLD}=============================================================={Color.END}")
    print(f"{Color.BOLD}   🎓 DATA-DRIVEN SCHOOL INTERVENTION DASHBOARD               {Color.END}")
    print(f"{Color.BOLD}=============================================================={Color.END}")
    print(f"{Color.GREY}This system suggests actionable interventions, not predictions.{Color.END}\n")

    # =====================================================
    # MODULE 1: ADAPTIVE PEER MENTORSHIP
    # =====================================================
    print_header("1. ADAPTIVE PEER MENTORSHIP PROGRAM")

    print(f"{Color.GREY}[GOAL]: Transfer effective study behavior through peer pairing.{Color.END}")
    print(f"{Color.GREY}[METHOD]: Percentile-based selection (scales with dataset size).{Color.END}\n")

    PAIR_PERCENT = 0.15
    pair_count = max(1, int(len(df) * PAIR_PERCENT))

    top_students = df.sort_values(by='FinalGrade', ascending=False).head(pair_count).reset_index(drop=True)
    bottom_students = df.sort_values(by='FinalGrade', ascending=True).head(pair_count).reset_index(drop=True)

    print_row("MENTOR (Final Grade)", "MENTEE (Final Grade)", "ID PAIR", "INTERVENTION", Color.BOLD)
    print("-" * 95)

    for i in range(pair_count):
        mentor = f"{top_students.iloc[i]['Name']} ({top_students.iloc[i]['FinalGrade']:.1f})"
        mentee = f"{bottom_students.iloc[i]['Name']} ({bottom_students.iloc[i]['FinalGrade']:.1f})"
        ids = f"{top_students.iloc[i]['StudentID']} → {bottom_students.iloc[i]['StudentID']}"
        action = "Weekly Guided Mentoring"
        print_row(mentor, mentee, ids, action,  Color.CYAN)

    # =====================================================
    # MODULE 2: HIDDEN GEMS (DATA-RELATIVE)
    # =====================================================
    print_header("2. HIDDEN GEMS — UNEXPECTED HIGH GROWTH")

    growth_threshold = df['GradeChange'].quantile(0.75)

    print(f"{Color.GREY}[DEFINITION]: Students starting below 75 who outperform 75% of peers in growth.{Color.END}")
    print(f"{Color.GREY}[THRESHOLD]: GradeChange > {growth_threshold:.2f} (75th percentile).{Color.END}\n")

    gems = df[
        (df['PreviousGrade'] < 75) &
        (df['GradeChange'] > growth_threshold)
    ].sort_values(by=['GradeChange', 'PreviousGrade'], ascending=[False, True])

    print_row("STUDENT NAME", "PREVIOUS", "FINAL", "GRADE CHANGE", Color.BOLD)
    print("-" * 95)

    if gems.empty:
        print(f"{Color.YELLOW}No students met the Hidden Gem criteria.{Color.END}")
    else:
        for _, row in gems.iterrows():
            print_row(
                row['Name'],
                f"{row['PreviousGrade']:.1f}",
                f"{row['FinalGrade']:.1f}",
                f"+{row['GradeChange']:.1f}",
                Color.GREEN
            )

    # =====================================================
    # MODULE 3: EARLY WARNING SYSTEM
    # =====================================================
    print_header("3. EARLY WARNING — PERFORMANCE DECLINE")

    drop_threshold = df['GradeChange'].mean() - df['GradeChange'].std()

    print(f"{Color.GREY}[LOGIC]: Statistical decline OR behavioral risk.{Color.END}")
    print(f"{Color.GREY}[THRESHOLD]: GradeChange < {drop_threshold:.2f} (mean − 1 SD).{Color.END}\n")

    risks = df[
        (df['AttendanceRate'] < 65) |
        (df['GradeChange'] < drop_threshold)
    ].sort_values(by=['GradeChange', 'PreviousGrade'], ascending=[True, False])

    print_row("STUDENT NAME", "ATTENDANCE", "GRADE CHANGE", "RISK DRIVER", Color.BOLD)
    print("-" * 95)

    if risks.empty:
        print(f"{Color.GREEN}No critical risk patterns detected.{Color.END}")
    else:
        for _, row in risks.iterrows():
            if row['AttendanceRate'] < 65 and row['GradeChange'] < drop_threshold:
                reason = "CRITICAL (Academic + Attendance)"
            elif row['AttendanceRate'] < 65:
                reason = "Low Attendance"
            else:
                reason = "Sharp Grade Decline"

            print_row(
                row['Name'],
                f"{row['AttendanceRate']}%",
                f"{row['GradeChange']:.1f}",
                reason,
                Color.RED
            )

    # =====================================================
    # MODULE 4: STRATEGIC RESOURCE SIGNAL
    # =====================================================
    print_header("4. STRATEGIC RESOURCE SIGNAL")

    avg_study = df['StudyHoursPerWeek'].mean()

    print(f"   Class Average Study Time: {Color.BOLD}{avg_study:.1f} hours/week{Color.END}")
    print(f"   {Color.GREY}Threshold defined as class mean study behavior.{Color.END}\n")

    if avg_study < 15:
        print(f"   {Color.RED}🔴 SIGNAL:{Color.END} Study effort below expected baseline.")
        print("      → Recommend structured after-school study sessions.")
        print("      → Increase supervised academic spaces.")
    else:
        print(f"   {Color.GREEN}🟢 SIGNAL:{Color.END} Study effort within healthy range.")
        print("      → Redirect resources toward enrichment & well-being.")

# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------
run_dashboard()
print("\n")

