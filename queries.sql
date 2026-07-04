-- Query 1: Count total patients and those with heart disease
SELECT 
  COUNT(*) as total_patients,
  SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_count,
  ROUND(SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as disease_percentage
FROM heart_disease;

-- Query 2: Average age by heart disease status
SELECT 
  target,
  ROUND(AVG(age), 2) as avg_age,
  MIN(age) as min_age,
  MAX(age) as max_age
FROM heart_disease
GROUP BY target;

-- Query 3: Gender distribution in dataset
SELECT 
  sex,
  COUNT(*) as count,
  ROUND(COUNT() * 100.0 / (SELECT COUNT() FROM heart_disease), 2) as percentage
FROM heart_disease
GROUP BY sex;

-- Query 4: Cholesterol levels - patients with heart disease vs without
SELECT 
  target,
  ROUND(AVG(chol), 2) as avg_cholesterol,
  ROUND(MAX(chol), 2) as max_cholesterol,
  ROUND(MIN(chol), 2) as min_cholesterol
FROM heart_disease
GROUP BY target;

-- Query 5: Blood pressure analysis
SELECT 
  target,
  ROUND(AVG(trestbps), 2) as avg_blood_pressure,
  COUNT(*) as patient_count
FROM heart_disease
GROUP BY target;

-- Query 6: Age groups at risk
SELECT 
  CASE 
    WHEN age < 40 THEN 'Under 40'
    WHEN age BETWEEN 40 AND 50 THEN '40-50'
    WHEN age BETWEEN 51 AND 60 THEN '51-60'
    ELSE 'Over 60'
  END as age_group,
  COUNT(*) as total,
  SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as with_disease,
  ROUND(SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as disease_rate
FROM heart_disease
GROUP BY age_group
ORDER BY age_group;

-- Query 7: Chest pain types distribution
SELECT 
  cp as chest_pain_type,
  COUNT(*) as count,
  SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as disease_count
FROM heart_disease
GROUP BY cp
ORDER BY disease_count DESC;

-- Query 8: High-risk patients (multiple risk factors)
SELECT 
  age,
  sex,
  chol,
  trestbps,
  target
FROM heart_disease
WHERE chol > 240 AND trestbps > 140 AND target = 1
ORDER BY age;

-- Query 9: Maximum heart rate achieved by disease status
SELECT 
  target,
  ROUND(AVG(thalach), 2) as avg_max_heart_rate,
  MAX(thalach) as highest_rate,
  MIN(thalach) as lowest_rate
FROM heart_disease
GROUP BY target;

-- Query 10: Summary statistics
SELECT 
  COUNT(*) as total_patients,
  ROUND(AVG(age), 2) as avg_age,
  ROUND(AVG(chol), 2) as avg_cholesterol,
  ROUND(AVG(trestbps), 2) as avg_blood_pressure,
  ROUND(AVG(thalach), 2) as avg_max_heart_rate,
  SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as patients_with_disease
FROM heart_disease;
