import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to see data for Chicago, New York City or Washington?\n').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('\nInvalid input. Please try again.')
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWould you like to see data for January, February, March, April, May, June, or for all months?\n').lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('\nInvalid input. Please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWould you like to see data for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or for all days?\n').lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('\nInvalid input. Please try again.')

    print()
    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        df = df[df['Month'] == month.title()]
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    print('\nThe most common month was:')
    print(df.mode()['Month'][0])

    # display the most common day of week
    print('\nThe most common day of the week was:')
    print(df.mode()['Day of Week'][0])

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    print('\nThe most common start hour was:')
    print(str(int(df.mode()['Start Hour'][0])) + ':00')

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most commonly used start station was:')
    print(df.mode()['Start Station'][0])

    # display most commonly used end station
    print('\nThe most commonly used end station was:')
    print(df.mode()['End Station'][0])

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    print('\nThe most frequent trip was:')
    print(df.mode()['Trip'][0])

    print('\nThis took %s seconds.\n' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    ttt = df['Travel Time'].sum()
    print('\nTotal travel time was:')
    print('{} day(s), {} hour(s), {} minute(s) and {} second(s)'.format(ttt.components.days, ttt.components.hours, ttt.components.minutes, ttt.components.seconds))
    # display mean travel time
    mtt = df['Travel Time'].mean()
    print('\nMean travel time was:')
    print('{} day(s), {} hour(s), {} minute(s) and {} second(s)'.format(mtt.components.days, mtt.components.hours, mtt.components.minutes, mtt.components.seconds))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        data = df['User Type']
    except KeyError:
        print('\nThere is no data for user type.')
    else:
            if df['User Type'].isnull().any():
                df['User Type'].fillna('Unknown', inplace=True)
            user_types = df['User Type'].value_counts()
            print("\nDisplaying counts of user types:")
            for index, value in user_types.items():
                print('{}: {}'.format(index, value))

    # Display counts of gender
    try:
        data = df['Gender']
    except KeyError:
        print('\nThere is no data for gender.')
    else:
        if df['Gender'].isnull().any():
            df['Gender'].fillna('Unknown', inplace=True)
        genders = df['Gender'].value_counts()
        print("\nDisplaying counts of gender:")
        for index, value in genders.items():
            print('{}: {}'.format(index, value))

    # Display earliest, most recent, and most common year of birth
    try:
        data = df['Birth Year']
    except KeyError:
        print('\nThere is no data for birth year.')
    else:
        print("\nThe earliest year of birth was:")
        print(str(int(df['Birth Year'].min())) + '.')
        print("\nThe most recent year of birth was:")
        print(str(int(df['Birth Year'].max())) + '.')
        print("\nThe most common year of birth was:")
        print(str(int(df.mode()['Birth Year'][0])) + '.')

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def main():
    print('\nHello! Let\'s explore some US bikeshare data!')
    condition = True
    while condition == True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # request user input (for raw data display)
        i = 0
        while True:
            display = input("\nWould you like to see (the next) 5 lines of raw data? Enter 'yes' or 'no'.\n").lower()
            if display == 'no':
                break
            elif display == 'yes':
                print(df.iloc[i: i+5])
                i += 5
            else:
                print('\nInvalid input. Please try again.')

        # request user input (for restart)
        while True:
            restart = input("\nWould you like to restart? Enter 'yes' or 'no'.\n").lower()
            if restart == 'no':
                condition = False
                print('\nThanks for your time and have a nice day! :)')
                break
            elif restart == 'yes':
                break
            else:
                print('\nInvalid input. Please try again.')


if __name__ == "__main__":
	main()
