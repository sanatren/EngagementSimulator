import random
import pandas as pd
from faker import Faker

fake = Faker()

# Parameters for simulation
post_types = ["carousel", "reel", "static_image", "video"]
platforms = ["Instagram", "Facebook", "YouTube", "TikTok", "Twitter"]

# Top countries with major global impacts and rich cultures
countries = [
    # North America
    "United States", "Canada",
    # Europe
    "United Kingdom", "Germany", "France", "Italy", "Spain",
    # Asia
    "India", "China", "Japan", "South Korea", "Indonesia",
    # Latin America
    "Brazil", "Mexico",
    # Oceania
    "Australia",
    # Middle East
    "United Arab Emirates", "Saudi Arabia",
    # Africa
    "South Africa", "Egypt",
    # Cultural Heritage
    "Greece", "Turkey"
]

# Urban and rural classifications for each country
regions_by_country = {
    "United States": ["Urban", "Rural"],
    "Canada": ["Urban", "Rural"],
    "United Kingdom": ["Urban"],
    "Germany": ["Urban", "Rural"],
    "France": ["Urban", "Rural"],
    "Italy": ["Urban", "Rural"],
    "Spain": ["Urban", "Rural"],
    "India": ["Urban", "Rural"],
    "China": ["Urban", "Rural"],
    "Japan": ["Urban"],
    "South Korea": ["Urban"],
    "Indonesia": ["Urban", "Rural"],
    "Brazil": ["Urban", "Rural"],
    "Mexico": ["Urban", "Rural"],
    "Australia": ["Urban", "Rural"],
    "United Arab Emirates": ["Urban"],
    "Saudi Arabia": ["Urban", "Rural"],
    "South Africa": ["Urban", "Rural"],
    "Egypt": ["Urban", "Rural"],
    "Greece": ["Urban", "Rural"],
    "Turkey": ["Urban", "Rural"]
}

# Languages based on regions
languages_by_country = {
    "United States": ["English"],
    "Canada": ["English", "French"],
    "United Kingdom": ["English"],
    "Germany": ["German"],
    "France": ["French"],
    "Italy": ["Italian"],
    "Spain": ["Spanish"],
    "India": ["Hindi", "English", "Bengali", "Tamil"],
    "China": ["Mandarin"],
    "Japan": ["Japanese"],
    "South Korea": ["Korean"],
    "Indonesia": ["Indonesian"],
    "Brazil": ["Portuguese"],
    "Mexico": ["Spanish"],
    "Australia": ["English"],
    "United Arab Emirates": ["Arabic", "English"],
    "Saudi Arabia": ["Arabic"],
    "South Africa": ["English", "Zulu", "Afrikaans"],
    "Egypt": ["Arabic"],
    "Greece": ["Greek"],
    "Turkey": ["Turkish"]
}

categories = [
    "Entertainment", "Education", "Food", "Travel", "Sports", "Technology",
    "Politics", "Finance", "Fashion", "Gaming", "Health", "Music", "Movies", "Social Issues"
]
age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]

# Major global events and festivals by country
festivals_by_country = {
    "United States": ["Thanksgiving", "Independence Day", "Halloween"],
    "India": ["Diwali", "Holi", "Eid"],
    "China": ["Chinese New Year", "Mid-Autumn Festival"],
    "Brazil": ["Carnival"],
    "United Kingdom": ["Christmas", "Easter", "Bonfire Night"],
    "Japan": ["Cherry Blossom Festival", "Obon"],
    "South Korea": ["Chuseok", "Seollal"],
    "Mexico": ["Day of the Dead", "Cinco de Mayo"],
    "France": ["Bastille Day"],
    "Germany": ["Oktoberfest"],
    "Spain": ["La Tomatina", "Running of the Bulls"],
    "Italy": ["Venice Carnival", "Easter"],
    "South Africa": ["Heritage Day"],
    "Australia": ["Australia Day", "Melbourne Cup"],
    "United Arab Emirates": ["National Day", "Dubai Shopping Festival"],
    "Saudi Arabia": ["Eid al-Fitr", "Eid al-Adha"],
    "Egypt": ["Ramadan", "Eid al-Fitr"],
    "Greece": ["Easter", "Carnival"],
    "Turkey": ["Republic Day", "Ramadan"]
}

# Platform restrictions by country
banned_platforms = {
    "China": ["Instagram", "Facebook", "YouTube", "Twitter"],
    "India": ["TikTok"],
    "United Arab Emirates": [],
    "Saudi Arabia": [],
    "United States": [],
    "Indonesia": ["TikTok"]
}

def get_relevant_festivals(country):
    return ", ".join(festivals_by_country.get(country, []))

def generate_dataset(num_posts):
    data = []
    for i in range(num_posts):
        # Randomly select country and associated attributes
        country = random.choice(countries)
        region = random.choice(regions_by_country[country])
        language = random.choice(languages_by_country[country])

        # Generate timestamp
        timestamp = fake.date_time_this_year()
        
        # Determine platform availability
        platform = random.choice(platforms)
        if platform in banned_platforms.get(country, []):
            likes, shares, comments, views = 0, 0, 0, 0
            engagement_rate, ctr = 0, 0
        else:
            # Randomly assign engagement metrics
            base_likes = random.randint(50, 5000)
            base_shares = random.randint(10, 1000)
            base_comments = random.randint(5, 500)
            base_views = random.randint(100, 10000)

            # Calculate engagement multiplier based on festivals
            has_festival = "Yes" if random.random() < 0.3 else "No"
            engagement_multiplier = 1.5 if has_festival == "Yes" else 1.0

            likes = int(base_likes * engagement_multiplier)
            shares = int(base_shares * engagement_multiplier)
            comments = int(base_comments * engagement_multiplier)
            views = int(base_views * engagement_multiplier)

            # Calculate engagement metrics
            engagement_rate = round((likes + shares + comments) / views, 2)
            ctr = round(shares / views, 2)

        post = {
            "post_id": i + 1,
            "post_type": random.choice(post_types),
            "platform": platform,
            "category": random.choice(categories),
            "likes": likes,
            "shares": shares,
            "comments": comments,
            "views": views,
            "engagement_rate": engagement_rate,
            "ctr": ctr,
            "country": country,
            "region": region,
            "language": language,
            "festival_relevance": "Yes" if likes > 0 and random.random() < 0.3 else "No",
            "relevant_festivals": get_relevant_festivals(country) if likes > 0 else "None",
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "month": timestamp.strftime("%B"),
            "day_of_week": timestamp.strftime("%A"),
            "ad_spend": round(random.uniform(0, 5000), 2) if likes > 0 else 0,
            "post_reach": int(views * random.uniform(0.6, 0.9)) if views > 0 else 0,
            "age_group": random.choice(age_groups),
            "gender": random.choice(["Male", "Female", "Other"]),
          }
        data.append(post)

    return pd.DataFrame(data)

# Generate dataset
df = generate_dataset(1000)

# Save to CSV
df.to_csv("global_social_media_engagement.csv", index=False)

# Configure display options
pd.set_option('display.max_rows', 10)  # Limit rows to 10 for display
pd.set_option('display.max_columns', None)

# Display dataset preview
print("\nDataset Preview:")
print(df.head())

# Display dataset info
print("\nDataset Info:")
print(df.info())

# Display unique values in key columns
print("\nUnique values in key columns:")
print("Countries:", len(df['country'].unique()))
print("Regions:", df['region'].unique())
print("Languages:", len(df['language'].unique()))
print("Categories:", df['category'].unique())

# Check for duplicate rows
duplicate_rows = df[df.duplicated()]
print(f"\nNumber of duplicate rows: {len(duplicate_rows)}")
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

# Fix unrealistic rows by ensuring likes >= max(shares, comments)
df.loc[df['likes'] < df[['shares', 'comments']].max(axis=1), 'likes'] = \
    df[['shares', 'comments']].max(axis=1) + random.randint(10, 50)

# Check if likes are always greater than shares or comments
unrealistic_data = df[df['likes'] < df[['shares', 'comments']].max(axis=1)]
print(f"\nUnrealistic data rows after fixing: {len(unrealistic_data)}")

# Plot engagement rate distribution
df['engagement_rate'].hist(bins=50)

# Display average engagement metrics by platform
print("\nAverage engagement metrics by platform:")
print(df.groupby('platform')[['likes', 'shares', 'comments', 'views', 'ctr']].mean())
     
print(df.head(5))
