import pandas as pd

df = pd.read_csv("dataset_v2.csv")

mapping = {
    "Knife": "knife",
    "usb": "usb_adapter",
    "batteries": "battery"
}

df["label"] = df["label"].replace(mapping)

df.to_csv("dataset_v2_clean.csv", index=False)

print(df["label"].value_counts())
print("\nClean dataset saved as dataset_v2_clean.csv")
