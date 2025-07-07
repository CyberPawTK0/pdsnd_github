import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Make sure the csv files are in the same location of the python program

def bicycle_song():
    """
    Easter egg function that plays the Bicycle song lyrics.
    """
    print("\nBicycle, bicycle, bicycle")
    print("I want to ride my bicycle, bicycle, bicycle")
    print("I want to ride my bicycle")
    print("I want to ride my bike")
    print("I want to ride my bicycle")
    print("I want to ride it where I like\n")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

# get user input for city (chicago, new york city, washington)
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington? Or type "bicycle"\n').lower().strip()
        if city == 'bicycle':
            bicycle_song()
        elif city in cities:
            break
        else:
            print('Invalid input. Please enter Chicago, New York City, or Washington.')

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('\nWould you like to filter by month? Enter a month (January through June) or "all" for no filter:\n').lower().strip()
        if month in months:
            break
        else:
            print('Invalid input. Please enter a valid month (January-June) or "all".')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('\nWould you like to filter by day? Enter a day of the week or "all" for no filter:\n').lower().strip()
        if day in days:
            break
        else:
            print('Invalid input. Please enter a valid day of the week or "all".')

    print('-'*69)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print(f'Most Common Month: {months[common_month-1]}')

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f'Most Common Day of Week: {common_day}')

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f'Most Common Start Hour: {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*69)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f'Most Common Start Station: {common_start_station}')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'Most Common End Station: {common_end_station}')

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['trip'].mode()[0]
    print(f'Most Common Trip: {common_trip}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*69)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_travel_time} seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Average Travel Time: {mean_travel_time:.2f} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*69)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Type Counts:')
    for user_type, count in user_types.items():
        print(f'{user_type}: {count}')

    # Display counts of gender (only available for NYC and Chicago)
    if 'Gender' in df.columns:
        print('\nGender Counts:')
        gender_counts = df['Gender'].value_counts()
        for gender, count in gender_counts.items():
            print(f'{gender}: {count}')
    else:
        print('\nGender data not available for this city.')

    # Display earliest, most recent, and most common year of birth (only available for NYC and Chicago)
    if 'Birth Year' in df.columns:
        print('\nBirth Year Statistics:')
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f'Earliest Birth Year: {earliest_year}')
        print(f'Most Recent Birth Year: {most_recent_year}')
        print(f'Most Common Birth Year: {common_year}')
    else:
        print('\nBirth year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*69)


def display_raw_data(df):
    """
    Displays 5 rows of raw data at a time based on user input.
    """
    start_row = 0
    while True:
        view_data = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n').lower().strip()
        if view_data == 'yes':
            print(df.iloc[start_row:start_row + 5])
            start_row += 5
            if start_row >= len(df):
                print('\nNo more data to display.')
                break
        elif view_data == 'no':
            break
        else:
            print('Invalid input. Please enter yes or no.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Ask if user wants to see raw data
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()