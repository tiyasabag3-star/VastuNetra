import pandas as pd

df = pd.read_csv("dataset_v2.csv")

# Merge "key" into "keys"
df["label"] = df["label"].replace("key", "keys")

df.to_csv("dataset_v2.csv", index=False)

print(df["label"].value_counts())

