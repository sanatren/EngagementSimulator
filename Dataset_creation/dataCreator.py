import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def get_peak_hours_for_day(day):
    peak_hours = {
        'Monday': ['11:00', '12:00', '15:15', '19:30'],
        'Tuesday': ['07:00', '08:00', '09:00', '10:00', '11:30', '13:30'],
        'Wednesday': ['11:00', '16:30', '17:30'],
        'Thursday': ['07:00', '11:00', '12:00', '14:00', '16:30', '18:30', '21:00'],
        'Friday': ['00:30', '14:00', '14:30', '22:30'],
        'Saturday': ['06:00', '07:00', '15:00', '20:30'],
        'Sunday': ['02:00', '16:00', '17:30', '19:00']
    }
    return peak_hours[day]

def generate_timestamp():
    start_date = datetime.now() - timedelta(days=30)
    random_days = random.randint(0, 29)
    date = start_date + timedelta(days=random_days)
    
    day_name = date.strftime('%A')
    
    if random.random() < 0.7:  # 70% chance of peak hour
        time_str = random.choice(get_peak_hours_for_day(day_name))
        hour, minute = map(int, time_str.split(':'))
    else:
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
    
    return date.replace(hour=hour, minute=minute)

def generate_engagement_metrics(post_type, timestamp, state):
    # Base multipliers for post types
    base_multipliers = {
        'reel': {'likes': 2.0, 'comments': 2.2, 'shares': 2.5},
        'carousel': {'likes': 1.2, 'comments': 1.3, 'shares': 1.1},
        'static_image': {'likes': 1.0, 'comments': 1.0, 'shares': 1.0}
    }
    
    # State-based multiplier (higher for states with more urban population)
    state_multipliers = {
        'Maharashtra': 1.3, 'Delhi': 1.4, 'Karnataka': 1.25, 
        'Tamil Nadu': 1.2, 'Telangana': 1.15, 'Gujarat': 1.2,
        'West Bengal': 1.15, 'Uttar Pradesh': 1.1, 'Kerala': 1.15,
        'Rajasthan': 1.05, 'Madhya Pradesh': 1.0, 'Bihar': 0.95,
        'Punjab': 1.1, 'Haryana': 1.05, 'Assam': 0.95,
        'Odisha': 0.95, 'Jharkhand': 0.9, 'Chhattisgarh': 0.9,
        'Uttarakhand': 0.95, 'Himachal Pradesh': 0.9, 
        'Goa': 1.1, 'Manipur': 0.9, 'Tripura': 0.85,
        'Meghalaya': 0.85, 'Nagaland': 0.85, 'Arunachal Pradesh': 0.85,
        'Mizoram': 0.85, 'Sikkim': 0.85,
        'Andhra Pradesh': 1.1, 'Jammu and Kashmir': 0.95
    }
    
    # Time-based multiplier
    hour = timestamp.hour
    time_multiplier = 1.0
    if 8 <= hour <= 22:  # Daytime bonus
        time_multiplier *= 1.2
    if hour in [11, 12, 15, 19, 20]:  # Peak hours bonus
        time_multiplier *= 1.3
    
    # Base numbers (realistic for medium-sized account)
    base_likes = np.random.normal(500, 100)
    base_comments = np.random.normal(50, 15)
    base_shares = np.random.normal(30, 10)
    
    # Apply multipliers with 15% noise
    multiplier = base_multipliers[post_type]
    noise = np.random.normal(1, 0.15)  # 15% noise
    state_multiplier = state_multipliers.get(state, 1.0)
    
    likes = int(max(0, base_likes * multiplier['likes'] * time_multiplier * noise * state_multiplier))
    comments = int(max(0, base_comments * multiplier['comments'] * time_multiplier * noise * state_multiplier))
    shares = int(max(0, base_shares * multiplier['shares'] * time_multiplier * noise * state_multiplier))
    
    return likes, comments, shares

def generate_location():
    indian_states = [
        'Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Telangana',
        'Gujarat', 'West Bengal', 'Uttar Pradesh', 'Kerala', 'Rajasthan',
        'Madhya Pradesh', 'Bihar', 'Punjab', 'Haryana', 'Assam',
        'Odisha', 'Jharkhand', 'Chhattisgarh', 'Uttarakhand',
        'Himachal Pradesh', 'Goa', 'Manipur', 'Tripura', 'Meghalaya',
        'Nagaland', 'Arunachal Pradesh', 'Mizoram', 'Sikkim',
        'Andhra Pradesh', 'Jammu and Kashmir'
    ]
    
    # Raw weights based on population and digital presence
    raw_weights = [
        0.115, 0.095, 0.085, 0.085, 0.075,  # More urbanized states
        0.075, 0.075, 0.075, 0.065, 0.055,  # Medium-high population
        0.035, 0.035, 0.035, 0.035, 0.025,  # Medium population
        0.015, 0.015, 0.015, 0.015, 0.015,  # Medium-low population
        0.010, 0.010, 0.010, 0.010, 0.010,  # Lower population
        0.005, 0.005, 0.005, 0.015, 0.015   # Remaining states
    ]
    
    # Normalize weights to ensure they sum to 1
    weights = np.array(raw_weights) / sum(raw_weights)
    
    return np.random.choice(indian_states, p=weights)

def generate_dataset(n_rows=2500):
    data = []
    post_types = ['static_image', 'reel', 'carousel']
    post_type_weights = [0.4, 0.3, 0.3]
    
    for _ in range(n_rows):
        state = generate_location()
        post_type = np.random.choice(post_types, p=post_type_weights)
        timestamp = generate_timestamp()
        likes, comments, shares = generate_engagement_metrics(post_type, timestamp, state)
        
        data.append({
            'post_type': post_type,
            'timestamp': timestamp,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'state': state
        })
    
    df = pd.DataFrame(data)
    return df

# Generate the dataset
df = generate_dataset()

# Sort by timestamp
df = df.sort_values('timestamp')

# Save to CSV
df.to_csv('social_media_engagement_data.csv', index=False)

# Print some basic statistics
print("\nDataset Statistics:")
print("\nMean engagement by post type:")
print(df.groupby('post_type')[['likes', 'comments', 'shares']].mean())

print("\nTop 5 states by average engagement:")
print(df.groupby('state')[['likes', 'comments', 'shares']].mean().sort_values('likes', ascending=False).head())