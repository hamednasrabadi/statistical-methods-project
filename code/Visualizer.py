import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Load Data
filename = 'FinalDataset.csv'
try:
    df = pd.read_csv(filename)
    print("Data loaded successfully.")
except FileNotFoundError:
    print(f"Error: '{filename}' not found.")
    exit()

# ---------------------------------------------------------
# SETUP: Colors & Style
# ---------------------------------------------------------
sns.set_theme(style="whitegrid", context="talk")

# رنگ‌های فیروزه‌ای و صورتی
COLOR_PRIOR = "#48D1CC"  # Cyan
COLOR_POSTERIOR = "#ff7373"  # Pink
MY_PALETTE = [COLOR_PRIOR, COLOR_POSTERIOR]

# ---------------------------------------------------------
# Graph 1: The PRETTY Matrix (Spectral + Normalized)
# ---------------------------------------------------------
cols_to_drop = ['StudentID']
numeric_df = df.select_dtypes(include=['number']).drop(columns=cols_to_drop, errors='ignore')

plt.figure(figsize=(12, 10))
mask = np.triu(np.ones_like(numeric_df.corr(), dtype=bool))

sns.heatmap(numeric_df.corr(), mask=mask, annot=True, fmt=".2f", 
            cmap='Spectral_r', vmin=-1, vmax=1, center=0, 
            square=True, linewidths=1, linecolor='black', 
            annot_kws={"size": 11, "weight": "bold"})

plt.title('Correlation Matrix', fontsize=18, weight='bold', pad=20)
plt.tight_layout()
plt.savefig('graph_1_matrix_final.png', bbox_inches='tight', dpi=300)
plt.show()
print("Graph 1 Created: Pretty Matrix.")

# ---------------------------------------------------------
# Helper Function: Bar Chart (Clean Legends)
# ---------------------------------------------------------
def draw_spread_chart(category_col, title, filename, order=None):
    plt.figure(figsize=(12, 7))
    temp_df = df[[category_col, 'PreviousGrade', 'FinalGrade']].dropna()
    df_melted = temp_df.melt(id_vars=[category_col], 
                             value_vars=['PreviousGrade', 'FinalGrade'], 
                             var_name='GradeType', value_name='Score')
    
    ax = sns.barplot(x=category_col, y='Score', hue='GradeType', data=df_melted, 
                     order=order, palette=MY_PALETTE,
                     errorbar=('sd', 2), capsize=0.1, 
                     edgecolor="white", linewidth=1)
    
    plt.title(title, fontsize=18, weight='bold', pad=20, color='#333333')
    plt.ylim(0, 119)
    plt.ylabel("Score (Mean ± 2 SD)")
    plt.xlabel(category_col)
    
    # --- CLEAN LEGEND ---
    # حذف نام رنگ‌ها از متن
    leg = plt.legend(loc='upper left', frameon=True, facecolor='white', framealpha=1)
    new_labels = ['Previous Grade', 'Final Grade']
    for t, l in zip(leg.texts, new_labels):
        t.set_text(l)
    
    sns.despine(left=True)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.show()
    print(f"Graph Created: {filename}")

# ---------------------------------------------------------
# Graph 2 & 3: Categorical
# ---------------------------------------------------------
draw_spread_chart('ParentalSupport', 
                  'Parental Support Impact', 
                  'graph_2_parent_spread.png', 
                  order=['Low', 'Medium', 'High'])

draw_spread_chart('ExtracurricularActivities', 
                  'Activities Impact', 
                  'graph_3_activities_spread.png')

# ---------------------------------------------------------
# Graph 4: Regression (Clean & Minimal)
# ---------------------------------------------------------
sns.set_context("talk", font_scale=1.0)
clean_reg_data = df.dropna(subset=['StudyHoursPerWeek', 'FinalGrade', 'Gender'])

g = sns.lmplot(x="StudyHoursPerWeek", y="FinalGrade", hue="Gender", data=clean_reg_data,
               height=7, aspect=1.4, 
               palette={"Male": COLOR_PRIOR, "Female": COLOR_POSTERIOR},
               markers=['o', 'D'],
               scatter_kws={'alpha': 0.3, 's': 25, 'linewidths': 0}, 
               line_kws={'linewidth': 2.5})

# تایتل ساده و تمیز
g.fig.suptitle('Study Hours Efficiency', fontsize=18, weight='bold', y=0.98)
g._legend.set_title("Gender")
sns.move_legend(g, "lower right", bbox_to_anchor=(.9, .15), frameon=True)

plt.tight_layout()
g.savefig('graph_4_regression_clean.png', bbox_inches='tight', dpi=300)
plt.show()
print("Graph 4 Created: Regression.")

# ---------------------------------------------------------
# Graph 5: Distribution (Clean Legends)
# ---------------------------------------------------------
plt.figure(figsize=(12, 7))
dist_data = df[['PreviousGrade', 'FinalGrade']].dropna()

# حذف نام رنگ‌ها از لیبل‌ها
sns.kdeplot(dist_data['PreviousGrade'], color=COLOR_PRIOR, label='Previous Grade', 
            fill=True, alpha=0.3, linewidth=2)
sns.kdeplot(dist_data['FinalGrade'], color=COLOR_POSTERIOR, label='Final Grade', 
            fill=True, alpha=0.3, linewidth=2)

plt.title('Grade Distribution Shift', fontsize=18, weight='bold', pad=20)
plt.xlabel('Grade Value')
plt.ylabel('Density')
plt.legend()
sns.despine()
plt.tight_layout()
plt.savefig('graph_5_distribution_smooth.png', bbox_inches='tight', dpi=300)
plt.show()
print("Graph 5 Created: Distribution.")

print("\nAll visuals generated successfully. Project Complete.")