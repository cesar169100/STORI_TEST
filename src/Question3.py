import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import optuna

df = pd.read_csv('./data/data.csv')
df = df.drop(['Unnamed: 0'], axis=1)

# Function to optimize
def objective(trial):
    # hiperparameter values
    C = trial.suggest_loguniform('C', 1e-4, 1e2)
    penalty = trial.suggest_categorical('penalty', ['l1', 'l2'])
    max_iter = trial.suggest_int('max_iter', 100, 300)

    model = LogisticRegression(C=C, penalty=penalty, max_iter=max_iter, solver='liblinear', random_state=42)
    # CV and measure the selected metric
    score = cross_val_score(model, df.drop('fraud', axis=1), df['fraud'], cv=10, scoring='accuracy')
    return score.mean()

# Crear un estudio de Optuna y optimizar
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=30)

# Imprimir los mejores parámetros y la mejor precisión
print("Mejores parámetros:", study.best_params)
print("Mejor precisión:", study.best_value)