import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

loan_data = pd.read_csv('dataset/Task 3 and 4_Loan_Data.csv')

features = ['credit_lines_outstanding', 'loan_amt_outstanding', 'total_debt_outstanding',
            'income', 'years_employed', 'fico_score']
target = 'default'

X = loan_data[features]
y = loan_data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Logistic Regression Model
log_reg = LogisticRegression()
log_reg.fit(X_train_scaled, y_train)
log_reg_preds = log_reg.predict_proba(X_test_scaled)[:, 1]

# Random Forest Model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict_proba(X_test)[:, 1]

log_reg_auc = roc_auc_score(y_test, log_reg_preds)
rf_auc = roc_auc_score(y_test, rf_preds)

print(log_reg_auc, rf_auc)
