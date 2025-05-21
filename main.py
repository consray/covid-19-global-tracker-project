import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_dataset(filepath):
    try:
        df = pd.read_csv(filepath, parse_dates=['date'])
        print("Dataset loaded successfully.")
        return df
    except FileNotFoundError:
        print("Error: File not found. Check the file path.")
    except Exception as e:
        print("Error loading dataset:", e)
    return None

def explore_data(df):
    print("\nFirst 5 rows of the dataset:")
    print(df.head())

    print("\nData types and non-null counts:")
    print(df.info())

    print("\nMissing values in key columns:")
    print(df.isnull().sum().sort_values(ascending=False).head(10))

    # Drop rows missing values in important numerical columns for analysis
    df_cleaned = df.dropna(subset=['total_cases', 'total_deaths', 'new_cases', 'new_deaths'])
    print("\nDropped rows with missing values in key columns.")
    return df_cleaned

def analyze_data(df):
    print("\nBasic statistics for numerical columns:")
    print(df[['total_cases', 'total_deaths', 'new_cases', 'new_deaths']].describe())

    print("\nMean total cases and deaths by continent:")
    continent_means = df.groupby('continent')[['total_cases', 'total_deaths']].mean().dropna()
    print(continent_means)
    return continent_means

def create_visualizations(df, continent_means):
    # Filter countries with enough data for meaningful trend analysis
    countries = ['United States', 'India', 'Brazil', 'Russia', 'United Kingdom']
    df_countries = df[df['location'].isin(countries)]

    # Line Chart: Total COVID-19 Cases Over Time
    plt.figure(figsize=(10, 6))
    for country in countries:
        country_data = df_countries[df_countries['location'] == country]
        plt.plot(country_data['date'], country_data['total_cases'], label=country)
    plt.title('Total COVID-19 Cases Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Cases')
    plt.legend(title='Country')
    plt.tight_layout()
    plt.show()

    # Bar Chart: Average Total Deaths by Continent
    plt.figure(figsize=(8, 5))
    continent_means['total_deaths'].plot(kind='bar', color='firebrick')
    plt.title('Average Total Deaths by Continent')
    plt.xlabel('Continent')
    plt.ylabel('Average Total Deaths')
    plt.tight_layout()
    plt.show()

    # Histogram: Distribution of Daily New Cases
    plt.figure(figsize=(8, 5))
    sns.histplot(df['new_cases'], bins=50, kde=True, color='dodgerblue')
    plt.title('Distribution of Daily New COVID-19 Cases')
    plt.xlabel('New Cases')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

    # Scatter Plot: Total Cases vs Total Deaths by Continent (latest date per country)
    latest_dates = df.groupby('location')['date'].max()
    latest_data = df[df.set_index(['location', 'date']).index.isin(latest_dates.items())]

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='total_cases', y='total_deaths', hue='continent', data=latest_data, palette='Set2')
    plt.title('Total Cases vs Total Deaths by Continent (Latest Data)')
    plt.xlabel('Total Cases')
    plt.ylabel('Total Deaths')
    plt.legend(title='Continent')
    plt.tight_layout()
    plt.show()

def main():
    filepath = 'Surveillance.csv'  # Set your CSV file path here
    df = load_dataset(filepath)

    if df is not None:
        df_cleaned = explore_data(df)
        continent_means = analyze_data(df_cleaned)
        create_visualizations(df_cleaned, continent_means)
    else:
        print("Program exiting due to dataset load failure.")

if __name__ == "__main__":
    main()
