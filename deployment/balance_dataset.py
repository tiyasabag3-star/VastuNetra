import pandas as pd

# Load dataset
df = pd.read_csv("dataset_v2.csv")

print("Original Dataset:")
print(df["label"].value_counts())
print()

# Maximum samples to keep for scissors
MAX_SCISSORS = 100

# Separate scissors and others
scissors = df[df["label"] == "scissors"]
others = df[df["label"] != "scissors"]

# Randomly keep only 100 scissors samples
scissors = scissors.sample(
    n=min(MAX_SCISSORS, len(scissors)),
    random_state=42
)

# Merge back
balanced = pd.concat([others, scissors])

# Shuffle dataset
balanced = balanced.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
balanced.to_csv("dataset_v2_balanced.csv", index=False)

print("Balanced Dataset:")
print(balanced["label"].value_counts())

print("\nSaved as dataset_v2_balanced.csv")
