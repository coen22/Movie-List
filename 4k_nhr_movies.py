import pandas as pd
import re


# Function to extract year from the title and return cleaned title
def extract_year_and_clean_title(title):
    match = re.search(r'\((\d{4})\)$', title)
    year = int(match.group(1)) if match else None
    cleaned_title = re.sub(r'\(\d{4}\)$', '', title).strip() if match else title.strip()
    return year, cleaned_title.lower()  # Convert title to lowercase


if __name__ == '__main__':
    # Load the first CSV
    df1 = pd.read_csv('4k_hdr.csv')

    # Apply the function to extract year and clean title
    df1[['Year', 'Title']] = df1.apply(lambda x: extract_year_and_clean_title(x['TITLE']), axis=1, result_type='expand')

    # Convert 'Year' to integer, if not null
    df1['Year'] = pd.to_numeric(df1['Year'], errors='coerce').astype('Int64')

    # Load the second CSV
    df2 = pd.read_csv('national_film_registry.csv')
    # Convert 'Year of Release' to integer
    df2['Year of Release'] = pd.to_numeric(df2['Year of Release'], errors='coerce').astype('Int64')
    # Rename the columns for consistency and convert title to lowercase
    df2.rename(columns={'Film Title': 'Title', 'Year of Release': 'Year'}, inplace=True)
    df2['Title'] = df2['Title'].str.lower()  # Convert title to lowercase

    # Join the dataframes on Title and Year
    result = pd.merge(df1, df2, on=['Title', 'Year'])

    # Drop rows where "Native 4k" is not null
    result.dropna(subset=['Native 4K'], inplace=True)

    # Drop rows where HDR is not null
    result.dropna(subset=['HDR'], inplace=True)

    # Print summary
    print('4K/HDR movies: ', len(df1))
    print('National Film Registry: ', len(df2))
    print('Joined movies: ', len(result))

    # remove columns 'Added', 'Upscaled 4K', 'Title'
    result.drop(columns=['Added', 'Upscaled 4K', 'Title'], inplace=True)

    # Save the result to a new CSV file
    result.to_csv('joined_movies.csv', index=False)
