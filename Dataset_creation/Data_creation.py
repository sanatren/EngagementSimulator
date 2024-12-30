import random
import pandas as pd
from faker import Faker

# Initialize Faker for generating fake data
fake = Faker()

# Parameters for simulation
post_types = ["carousel", "reel", "static_image", "video"]
platforms = ["Instagram", "Facebook", "YouTube"]

# Enhanced regions with urban/rural classifications
regions = [
    "Mumbai Urban", "Delhi Urban", "Bengaluru Urban", "Chennai Urban", "Kolkata Urban", "Hyderabad Urban",
    "Mumbai Suburban", "Pune Urban", "Rural Maharashtra West", "Rural Maharashtra East", "Rural Maharashtra North",
    "Delhi NCR Urban", "Gurgaon Urban", "Noida Urban", "Rural NCR",
    "Bengaluru Suburban", "Mysuru Urban", "Rural Karnataka North", "Rural Karnataka South",
    "Chennai Suburban", "Coimbatore Urban", "Rural Tamil Nadu North", "Rural Tamil Nadu South",
    "Rural UP East", "Rural UP West", "Rural Bihar", "Rural Gujarat", "Rural Rajasthan",
    "Rural Punjab", "Rural West Bengal"
]

# Enhanced languages with regional variations
languages = [
    "English", "Hindi", "Hinglish",
    "Marathi", "Gujarati",
    "Tamil", "Telugu", "Kannada", "Malayalam",
    "Bengali", "Odia",
    "Punjabi", "Bhojpuri",
    "Urdu"
]



categories = ["Entertainment", "Education", "Food", "Travel", "Sports", "Technology", "Politics", "Finance", "Fashion", "Gaming", "Health", "Music", "Movies", "Social Issues"]
age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]

# Festival data by month
festivals_by_month = {
    1: ["Lohri", "Pongal", "Republic Day"],
    2: ["Vasant Panchami"],
    3: ["Holi", "Maha Shivaratri"],
    4: ["Baisakhi", "Ram Navami"],
    5: ["Buddha Purnima", "Eid al-Fitr"],
    6: ["Rath Yatra"],
    7: ["Eid al-Adha"],
    8: ["Independence Day", "Raksha Bandhan", "Janmashtami", "Onam"],
    9: ["Ganesh Chaturthi"],
    10: ["Navratri", "Durga Puja", "Dussehra"],
    11: ["Diwali", "Bhai Dooj"],
    12: ["Christmas", "New Year's Eve"]
}

supported_post_types = {
    "Instagram": ["carousel", "reel", "static_image", "video"],
    "Facebook": ["carousel", "reel", "static_image", "video"],
    "YouTube": ["static_image", "video"],  # Exclude "reel"
    "TikTok": ["video", "reel"],
    "Twitter": ["static_image", "video"]  # Exclude "reel"
}

def get_relevant_festivals(month):
    return ", ".join(festivals_by_month.get(month, []))

def generate_dataset(num_posts):
    data = []
    for i in range(num_posts):
        # Generate timestamp first to determine festival relevance
        timestamp = fake.date_time_this_year()
        month = timestamp.month
        
        # Determine festival relevance based on month
        has_festival = "Yes" if month in [8, 10, 11] else "No"
        if has_festival == "No":
            has_festival = random.choice(["Yes", "No", "No", "No"])
        
        # Adjust engagement metrics based on festival season
        engagement_multiplier = 1.5 if month in [8, 10, 11] else (1.2 if month in [1, 3, 4] else 1.0)
        
        base_likes = random.randint(50, 5000)
        base_shares = random.randint(10, 1000)
        base_comments = random.randint(5, 500)
        base_views = random.randint(100, 10000)
        platform = random.choice(platforms)
        post_type = random.choice(supported_post_types[platform])
        post = {
            "post_id": i + 1,
            "post_type": post_type,
            "platform": platform,
            "category": random.choice(categories),
            "likes": int(base_likes * engagement_multiplier),
            "shares": int(base_shares * engagement_multiplier),
            "comments": int(base_comments * engagement_multiplier),
            "views": int(base_views * engagement_multiplier),
            "engagement_rate": round(random.uniform(0.01, 0.3) * engagement_multiplier, 2),
            "region": random.choice(regions),
            "language": random.choice(languages),
            "festival_relevance": has_festival,
            "festival_season": "High" if month in [8, 10, 11] else ("Medium" if month in [1, 3, 4] else "Low"),
            "relevant_festivals": get_relevant_festivals(month),
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "month": timestamp.strftime("%B"),
            "day_of_week": timestamp.strftime("%A"),
            "ad_spend": round(random.uniform(0, 5000), 2),
            "age_group": random.choice(age_groups),
            "gender": random.choice(["Male", "Female", "Other"]),
        }
        data.append(post)

    return pd.DataFrame(data)

# Generate dataset
df = generate_dataset(1000)

# Save to CSV
df.to_csv("social_media_engagement_india.csv", index=False)

# Configure display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Display a preview of the dataset
print("\nDataset Preview:")
print(df.head())

# Display dataset info
print("\nDataset Info:")
print(df.info())

# Display unique values in key columns
print("\nUnique values in key columns:")
print("Regions:", len(df['region'].unique()))
print("Languages:", len(df['language'].unique()))
print("Festival Seasons:", df['festival_season'].unique())

# Check for duplicate rows
duplicate_rows = df[df.duplicated()]
print(f"Number of duplicate rows: {len(duplicate_rows)}")
if not duplicate_rows.empty:
    print(duplicate_rows)

# Check for unique post_ids
if df['post_id'].is_unique:
    print("All post_ids are unique.")
else:
    print("Duplicate post_ids found!")

# Check for missing values
print("\nMissing values in columns:")
print(df.isnull().sum())

# Validate ranges of numeric columns
print("\nSummary statistics for numeric columns:")
print(df.describe())

# Check for invalid engagement rates
invalid_engagement_rate = df[(df['engagement_rate'] < 0) | (df['engagement_rate'] > 1)]
print(f"Invalid engagement rates: {len(invalid_engagement_rate)}")

# Fix unrealistic rows by ensuring likes >= max(shares, comments)
df.loc[df['likes'] < df[['shares', 'comments']].max(axis=1), 'likes'] = \
    df[['shares', 'comments']].max(axis=1) + random.randint(10, 50)

# Check if likes are always greater than shares or comments
unrealistic_data = df[df['likes'] < df[['shares', 'comments']].max(axis=1)]
print(f"Unrealistic data rows after fixing: {len(unrealistic_data)}")

# Recalculate engagement rate and add new metrics
df['engagement_rate'] = ((df['likes'] + df['shares'] + df['comments']) / df['views']).clip(upper=1).round(2)
df['post_reach'] = (df['views'] * random.uniform(0.6, 0.9)).astype(int)
df['ClickTroughRate'] = (df['shares'] / df['views']).clip(upper=1).round(2)

# Plot engagement rate distribution
df['engagement_rate'].hist(bins=50)

# Display average engagement metrics by platform
print("\nAverage engagement metrics by platform:")
print(df.groupby('platform')[['likes', 'shares', 'comments']].mean())

print(df.head(5))