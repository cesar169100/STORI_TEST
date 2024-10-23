import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix
import optuna

df = pd.read_csv('./data/data.csv')
df = df.drop(['Unnamed: 0'], axis=1)
df['activated_date'] = pd.to_datetime(df['activated_date'])
df['last_payment_date'] = pd.to_datetime(df['last_payment_date'])
# I assume that days<0 means that it is a reactivated credit
df['days'] = (df['last_payment_date'] - df['activated_date']).dt.days
df = df.drop(['cust_id','activated_date','last_payment_date','oneoff_purchases','purchases_installments_frequency'], axis=1)
# Split and imputation
X = df.drop(['fraud'], axis=1)
y = df['fraud']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
impute = SimpleImputer(strategy='median')
X_train_impute = impute.fit_transform(X_train) 
X_train = pd.DataFrame(X_train_impute, columns=X_train.columns, index=X_train.index)
X_test_impute = impute.transform(X_test)
X_test = pd.DataFrame(X_test_impute, columns=X_test.columns, index=X_test.index)
# Scaling to media zero and standard deviation 1
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_train = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
X_test_scaled = scaler.transform(X_test)
X_test = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)


# Function to optimize
def objective(trial):
    # hiperparameter values
    C = trial.suggest_loguniform('C', 1e-4, 1e2)
    penalty = trial.suggest_categorical('penalty', ['l1', 'l2'])
    max_iter = trial.suggest_int('max_iter', 100, 300)

    model = LogisticRegression(C=C, penalty=penalty, max_iter=max_iter, 
                               solver='liblinear', random_state=42, class_weight='balanced')
    # CV and measure the selected metric
    score = cross_val_score(model, X_train, y_train, cv=10, scoring='f1', n_jobs=-1)
    return score.mean()

# Crear un estudio de Optuna y optimizar
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=30)

# Imprimir los mejores parámetros y el mejor f1
print("Mejores parámetros:", study.best_params)
print("Mejor f1:", study.best_value)
best_params = study.best_params

# Entrenar modelo
best_model = LogisticRegression(
    C=best_params['C'],
    penalty=best_params['penalty'],
    max_iter=best_params['max_iter'],
    solver='liblinear',
    random_state=42,
    class_weight='balanced'
)

best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)
y_prob = best_model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
specificity = tn / (tn + fp)

print("Accuracy:", accuracy)
print("F1 Score:", f1)
print('Precision:', precision)
print('Recall:', recall)
print('Specificity:', specificity)
print('ROC AUC:', roc_auc)

# Feature importance
features = pd.DataFrame({
    'Feature': X_train.columns,
    'Coefficient': best_model.coef_[0]
})
features['Importance'] = features['Coefficient'].abs()
features = features.sort_values(by='Importance', ascending=False)
