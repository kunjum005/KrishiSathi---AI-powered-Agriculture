import pandas as pd
from services.smart_diary import save_fertilizer_activity

fertilizer_data = pd.read_csv(r"C:\Users\Hp\Documents\KrishiSathi\datasets\Fertilizer Prediction.csv")


def suggest_fertilizer(crop_name, N, P, K):
    # Example rule-based logic
    if N < 50:
        return "Urea (High Nitrogen)"
    elif P < 50:
        return "DAP (High Phosphorus)"
    elif K < 50:
        return "MOP (High Potassium)"
    else:
        # If NPK is good, suggest based on crop
        crop_data = fertilizer_data[fertilizer_data['Crop Type'].str.lower() == crop_name.lower()]
        if not crop_data.empty:
            return crop_data.iloc[0]['Fertilizer Name']
        else:
            return "NPK 19:19:19 (Balanced Fertilizer)"

if __name__ == "__main__":
    fert = suggest_fertilizer("rice", 40, 60, 70)
    print(f"💧 Suggested Fertilizer: {fert}")


save_fertilizer_activity({
    "crop": crop_name,
    "soil": soil_type,
    "N": nitrogen,
    "P": phosphorus,
    "K": potassium,
    "recommendation": result
})
