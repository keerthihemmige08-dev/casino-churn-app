import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load dataset
df = pd.read_csv('online_gaming_behavior_dataset.csv')

print("Columns:", df.columns.tolist())
print(df.head())

# 2. Drop rows with missing values
df = df.dropna()

# 3. Create binary target
df['is_churn'] = (df['EngagementLevel'] == 'Low').astype(int)

# 4. Encode categorical columns (except target source column)
cat_cols = df.select_dtypes(include='object').columns.tolist()
if 'EngagementLevel' in cat_cols:
    cat_cols.remove('EngagementLevel')

label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# 5. Features and target
drop_cols = ['PlayerID', 'EngagementLevel', 'is_churn']
X = df.drop(columns=[c for c in drop_cols if c in df.columns])
y = df['is_churn']

# 6. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 7. Train improved model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    random_state=42,
    class_weight='balanced'   # <-- MAIN FIX
)
model.fit(X_train, y_train)

# 8. Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Report:\n", classification_report(y_test, y_pred))

# Show feature importance (optional but useful)
import numpy as np
feat_imp = sorted(list(zip(X.columns, model.feature_importances_)), key=lambda x: x[1], reverse=True)
print("\nFeature Importance:")
for name, score in feat_imp:
    print(f"{name} : {score:.4f}")

# 9. Save artifacts
joblib.dump(model, 'casino_churn_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')
joblib.dump(X.columns.tolist(), 'feature_columns.pkl')

print("Saved casino_churn_model.pkl, label_encoders.pkl, feature_columns.pkl")
