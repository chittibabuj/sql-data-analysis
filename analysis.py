import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV and create SQLite database
df = pd.read_csv('heart_disease.csv')
conn = sqlite3.connect(':memory:')
df.to_sql('heart_disease', conn, index=False, if_exists='replace')

# Execute all 10 queries
queries = {
    'Q1_Overview': "SELECT COUNT() as total_patients, SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_count, ROUND(SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(), 2) as disease_percentage FROM heart_disease;",
    'Q2_Age_Analysis': "SELECT target, ROUND(AVG(age), 2) as avg_age, MIN(age) as min_age, MAX(age) as max_age FROM heart_disease GROUP BY target;",
    'Q3_Gender_Distribution': "SELECT sex, COUNT() as count, ROUND(COUNT() * 100.0 / (SELECT COUNT(*) FROM heart_disease), 2) as percentage FROM heart_disease GROUP BY sex;",
    'Q4_Cholesterol': "SELECT target, ROUND(AVG(chol), 2) as avg_cholesterol FROM heart_disease GROUP BY target;",
    'Q5_Blood_Pressure': "SELECT target, ROUND(AVG(trestbps), 2) as avg_bp FROM heart_disease GROUP BY target;",
    'Q6_Age_Groups': "SELECT CASE WHEN age < 40 THEN 'Under 40' WHEN age BETWEEN 40 AND 50 THEN '40-50' WHEN age BETWEEN 51 AND 60 THEN '51-60' ELSE 'Over 60' END as age_group, COUNT(*) as total, SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as with_disease FROM heart_disease GROUP BY age_group;",
    'Q7_Chest_Pain': "SELECT cp as chest_pain_type, COUNT(*) as count FROM heart_disease GROUP BY cp;",
    'Q8_High_Risk': "SELECT COUNT(*) as high_risk_patients FROM heart_disease WHERE chol > 240 AND trestbps > 140;",
    'Q9_Heart_Rate': "SELECT target, ROUND(AVG(thalach), 2) as avg_rate FROM heart_disease GROUP BY target;",
    'Q10_Summary': "SELECT COUNT(*) as total, ROUND(AVG(age), 2) as avg_age, ROUND(AVG(chol), 2) as avg_chol FROM heart_disease;"
}

# Print results
print("=" * 60)
print("HEART DISEASE DATA ANALYSIS - SQL QUERY RESULTS")
print("=" * 60)

for name, query in queries.items():
    result = pd.read_sql_query(query, conn)
    print(f"\n{name}:")
    print(result.to_string())

# Create visualizations
plt.figure(figsize=(15, 10))

# Plot 1: Disease Distribution
plt.subplot(2, 3, 1)
disease_counts = df['target'].value_counts()
plt.pie(disease_counts, labels=['No Disease', 'Disease'], autopct='%1.1f%%', colors=['green', 'red'])
plt.title('Heart Disease Distribution')

# Plot 2: Age Distribution
plt.subplot(2, 3, 2)
plt.hist(df[df['target'] == 0]['age'], alpha=0.6, label='No Disease', bins=15)
plt.hist(df[df['target'] == 1]['age'], alpha=0.6, label='Disease', bins=15)
plt.xlabel('Age')
plt.ylabel('Count')
plt.title('Age Distribution by Disease Status')
plt.legend()

# Plot 3: Cholesterol by Disease
plt.subplot(2, 3, 3)
df.boxplot(column='chol', by='target', ax=plt.gca())
plt.title('Cholesterol Levels by Disease Status')
plt.suptitle('')

# Plot 4: Gender Distribution
plt.subplot(2, 3, 4)
gender_counts = df['sex'].value_counts()
plt.bar(['Female', 'Male'], gender_counts.values, color=['pink', 'blue'])
plt.title('Gender Distribution')
plt.ylabel('Count')

# Plot 5: Average Age by Disease
plt.subplot(2, 3, 5)
age_by_disease = df.groupby('target')['age'].mean()
plt.bar(['No Disease', 'Disease'], age_by_disease.values, color=['green', 'red'])
plt.title('Average Age by Disease Status')
plt.ylabel('Age')

# Plot 6: Blood Pressure
plt.subplot(2, 3, 6)
df.boxplot(column='trestbps', by='target', ax=plt.gca())
plt.title('Blood Pressure by Disease Status')
plt.suptitle('')

plt.tight_layout()
plt.savefig('analysis_results.png', dpi=300, bbox_inches='tight')
print("\n" + "=" * 60)
print("✅ Visualizations saved to analysis_results.png")
print("=" * 60)

conn.close()
