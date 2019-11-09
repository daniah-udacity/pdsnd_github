import pandas as pd
import numpy as np
import time

CITY_DATA = {'chicago':'chicago.csv','washington':'washington.csv','new_york':'new_york_city.csv'}


def get_filters():
    
    print("Hello! Let's explore some US bikeshare data! ")
    print("Which city you want to see data for Chicago, New York, or Washington?")

    city = input()
    city_name = city.lower().replace(' ','_')

    while city_name not in CITY_DATA:
        print("Your entered city %s is invalid, enter a valid city " % (city_name))
        city = input()
        city_name = city.lower().replace(' ','_')


    print("Would you like to filter data by month, day, both, or not at all? Type 'none' for no time filter")
    choice_data = ['month','day','both','none']
    data_choice = input()
    choice = data_choice.lower()
    
    while choice not in choice_data:
        print("Your entered choice %s is invalid " % (choice))

    if choice == 'month':
        print("Which month? January, February, March, April, May, or June")
        month = input()
        month = month.lower()
        day_of_week = 'all'
        
    elif choice == 'day':
        print("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday ")
        day_of_week = input()
        month = 'all'
    elif choice == 'both':
        print("Which month? January, February, March, April, May, or June")
        month = input()
        month = month.lower()
        print("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday ")
        day_of_week = input()
    else:
        """ If Selected Choice is none """
        month = 'all'
        day_of_week = 'all'

    print('-'*100)
    return city_name,month,day_of_week

def load_data(city,month,day):
   
    df = pd.read_csv(CITY_DATA[city])
    """ To load the selected city csv file """
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month)+1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    print('-'*100)
    return df

def time_stats(df):

    print("Calculating the Most Frequent Time's of travel")
    start_time = time.time()

    frequent_month = df['Start Time'].dt.month.mode()[0]
    frequent_day = df['Start Time'].dt.weekday_name.mode()[0]
    frequent_hour = df['Start Time'].dt.hour.mode()[0]

    print("The Most Frequent Month is %s " % (frequent_month))
    print("The Most Frequent Day is %s " % (frequent_day))
    print("Most Frequent Hour is %s " % (frequent_hour))

    print("This took %s seconds" % (time.time() - start_time))
    print('-'*100)

def station_stats(df):

    print("Calculating the Most Frequent Station's of travel")
    start_time = time.time()

    frequent_start_station = df['Start Station'].mode()[0]

    frequent_end_station = df['End Station'].mode()[0]

    trip_with_counts = df.groupby(['Start Station','End Station']).size().reset_index(name = 'trips')

    sort_trips = trip_with_counts.sort_values('trips', ascending = False)

    start_trip = sort_trips['Start Station'].iloc[0]

    end_trip = sort_trips['End Station'].iloc[0]

    print("Most Frequent Start Station is %s " % (frequent_start_station))
    print("Most Frequent End Station is %s " % (frequent_end_station))
    print("Most popular trip is from %s to %s " % (start_trip,end_trip))

    print("This took %s seconds" % (time.time() - start_time))
    print('-'*100)

def trip_duration_stats(df):

    print("Calculating Trip Duration...!")
    start_time = time.time()

    total_trip_time = df['Trip Duration'].sum()

    mean_trip_time = df['Trip Duration'].mean()

    print("Total Travel Time is %s in seconds " % (total_trip_time))
    print("Mean Travel Time is %s in seconds " % (mean_trip_time))

    print("This took %s seconds" % (time.time() - start_time))
    print('-'*100)

def user_stats(df,city):

    print("Calculating User stats..!")
    start_time = time.time()

    print("Count's of User Type's ")

    if 'User Type' in df.columns:
        print(df['User Type'].value_counts())
    else:
        print("Oops..! for %s User Type data is not available " % (city))


    print("Count's of Gender ")

    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print("Oops..! for %s Gender data is not available " % (city))

    print(" Stats regarding Birth Year data ")
    
    if 'Birth Year' in df.columns:
        max_birth_year = df['Birth Year'].max()

        print("Most Recent Birth Year is %s " % (max_birth_year))

        min_birth_year = df['Birth Year'].min()

        print("Most Earliest Birth Year is %s " % (min_birth_year))

        frequent_birth_year = df['Birth Year'].mode()[0]

        print("Most Frequent Birth Year is %s " % (frequent_birth_year))
    else:
        print("Oops..! for %s Birth Year data is not available " % (city))
    print('-'*100)

def main():
    while True:
        city,month,day = get_filters()
        df = load_data(city,month,day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        print("Would you like see five rows of data ?? Enter yes or no ")
        display_data = input()
        display_data = display_data.lower()

        i = 5
        while display_data == 'yes':
            print(df[:i])
            print("Would you like to see five more rows of data ?? Enter yes or no ")
            i *= 2
            display_data = input()
            display_data = display_data.lower()

        restart = input('\nWould you like to restart? Type "yes" or "no."\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()