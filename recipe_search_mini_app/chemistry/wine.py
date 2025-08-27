import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNet
from sklearn.pipeline import Pipeline

df = pd.read_csv("winequality-red.csv", sep=";")
X, y = df.drop(columns=["quality"]), df["quality"]
pipe = Pipeline([("scaler", StandardScaler()), ("model", ElasticNet(alpha=0.05, l1_ratio=0.2, random_state=42))])

cv = KFold(n_splits=5, shuffle=True, random_state=42)
scores = -cross_val_score(pipe, X, y, cv=cv, scoring="neg_root_mean_squared_error")
print(f"RMSE: {scores.mean():.3f} ± {scores.std():.3f}")

