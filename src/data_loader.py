import pandas as pd
import requests
import time
import os

# 1. PROFESSIONAL COORDINATE DATABASE (Every Major Indian State)
# We use the coordinates of state capitals as a proxy for the entire state's weather.
INDIAN_STATES = {
    "Andhra Pradesh": {"lat": 16.5412, "lon": 80.5154},
    "Arunachal Pradesh": {"lat": 27.0844, "lon": 93.6053},
    "Assam": {"lat": 26.1445, "lon": 91.7362},
    "Bihar": {"lat": 25.5941, "lon": 85.1376},
    "Chhattisgarh": {"lat": 21.2514, "lon": 81.6296},
    "Delhi": {"lat": 28.61, "lon": 77.20},
    "Goa": {"lat": 15.4909, "lon": 73.8278},
    "Gujarat": {"lat": 23.2156, "lon": 72.6369},
    "Haryana": {"lat": 30.7333, "lon": 76.7794},
    "Himachal Pradesh": {"lat": 31.1048, "lon": 77.1734},
    "Jharkhand": {"lat": 23.3441, "lon": 85.3094},
    "Karnataka": {"lat": 12.9716, "lon": 77.5946},
    "Kerala": {"lat": 8.5241, "lon": 76.9366},
    "Madhya Pradesh": {"lat": 23.2599, "lon": 77.4126},
    "Maharashtra": {"lat": 19.0760, "lon": 72.8777},
    "Manipur": {"lat": 24.8170, "lon": 93.9368},
    "Meghalaya": {"lat": 25.5788, "lon": 91.8933},
    "Mizoram": {"lat": 23.7271, "lon": 92.7176},
    "Nagaland": {"lat": 25.6751, "lon": 94.1086},
    "Odisha": {"lat": 20.2961, "lon": 85.8245},
    "Punjab": {"lat": 30.7333, "lon": 76.7794},
    "Rajasthan": {"lat": 26.9124, "lon": 75.7873},
    "Sikkim": {"lat": 27.3314, "lon": 88.6138},
    "Tamil Nadu": {"lat": 13.0827, "lon": 80.2707},
    "Telangana": {"lat": 17.3850, "lon": 78.4867},
    "Tripura": {"lat": 23.8315, "lon": 91.2868},
    "Uttar Pradesh": {"lat": 26.8467, "lon": 80.9462},
    "Uttarakhand": {"lat": 30.3165, "lon": 78.0322},
    "West Bengal": {"lat": 22.5726, "lon": 88.3639}
}

def fetch_weather_for_all_india(start_date="20240101", end_date="20250101"):

    all_state_dfs = []
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    
    print(f"Starting bulk fetch for {len(INDIAN_STATES)} states....")

    for state, coords in INDIAN_STATES.items():
        # Parameters for NASA POWER API
        params = {
            "parameters": "T2M_MAX,T2M_MIN,RH2M,PRECTOTCORR", # Temp, Humidity, Rain
            "community": "SB",
            "longitude": coords['lon'],
            "latitude": coords['lat'],
            "start": start_date,
            "end": end_date,
            "format": "JSON"
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()['properties']['parameter']
                
                # Transforming JSON to a clean Table (DataFrame)
                state_df = pd.DataFrame(data)
                state_df = state_df.reset_index().rename(columns={'index': 'date'})
                
                # Tagging each row with the State name
                state_df['state'] = state
                all_state_dfs.append(state_df)
                print(f"Successfully fetched: {state}")
            else:
                print(f"Failed for {state}: Status {response.status_code}")
                
        except Exception as e:
            print(f"Error fetching {state}: {e}")
            
        time.sleep(0.5) 

    # Combine everything into one giant file
    final_dataset = pd.concat(all_state_dfs, ignore_index=True)
    
    # Save to my 'raw' data folder 
    os.makedirs('data/raw', exist_ok=True)
    final_dataset.to_csv('data/raw/india_weather_2024_2025.csv', index=False)
    
    print("\nALL DONE! Dataset saved to data/raw/india_weather_2024_2025.csv")
    return final_dataset

if __name__ == "__main__":
    fetch_weather_for_all_india()