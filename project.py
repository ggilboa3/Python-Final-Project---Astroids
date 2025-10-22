#Data refinement and preparation phase
"""
____________________________________________________________________________________________
Stage 1: Load CSV File
____________________________________________________________________________________________
Loads asteroid data from a CSV file into a Pandas DataFrame.

Args:
    filename (str): CSV file path.
Returns:
    pandas.DataFrame or None: DataFrame if successful, None if an error occurs.
Raises:
    FileNotFoundError: File not found.
    pd.errors.EmptyDataError: File is empty.
    pd.errors.ParserError: Invalid CSV format.
    Exception: Any unexpected error.

Notes:
    The CSV must be properly formatted.
    Errors are printed to the console.
Example:
    data = NASADataProcessor.load_data("nasa.csv")
"""

def load_data(filename):
    try:
        df = pd.read_csv(filename)
        return df  #Return the DataFrame - (if successful)
    except FileNotFoundError:  #Missing file error
        print("Error: The file was not found.")
    except pd.errors.EmptyDataError:  #Empty file error
        print("Error: The file is empty.")
    except pd.errors.ParserError:  #Parsing errors
        print("Error: Failed to parse the file. Please check its format.")
    except Exception as unexpected:  #Catch any other unexpected errors
        print(f"Error: An unexpected error occurred - {unexpected}")

    return None  #Return None - an error occurred

"""
____________________________________________________________________________________________
Stage 2 :Filter & Prepare Data
____________________________________________________________________________________________
Filters the DataFrame to include only asteroids with a Close Approach Date from the year 2000 onwards.
Args : 
    df (pandas.DataFrame): The input DataFrame containing asteroid information.
Returns :
    pandas.DataFrame: A filtered DataFrame including only asteroids from the year 2000 and onwards.
 Notes:
    - Assumes the presence "Close Approach Date" column with date values in a recognizable date format.
    - the function converts this column to datetime format to ensure accurate filtering.
    - If the required column is not found, an error message is displayed, and the original DataFrame will be returned unchanged.

Example:
    filtered_df = mask_data(nasa_file)
"""

def extract_year(date_str):
    try:
        parts = date_str.split('-')
        if len(parts) == 3: #A flag for good return of date
            return int(parts[0])
        return None
    except ValueError:
        return None

def mask_data(df):
    df['year'] = df['Close Approach Date'].apply(extract_year)
    df = df[df['year'] >= 2000].drop(columns='year') #Makes the updated date
    return df
"""
_____________________________________________________________________________________________
Stage 3: Analyze Data
_____________________________________________________________________________________________
cleans the dataframe to make it be more sorted and handle less storage.
by removing specific columns and returns dataist details.

Args:
    df (pandas.DataFrame): The original DataFrame containing asteroid data.
Returns:
    tuple: A tuple containing:
        int: Total number of rows in the resulting DataFrame.
        int: Total number of columns after removing specified ones.
        list: List of names of the columns that remain.

Notes:
    Drops the columns: "Orbiting Body","Equinox" and "Neo Reference ID".
    If any of those columns are not present, the function proceeds without raising an error.

Example:
    num_rows, num_cols, column_names = data_details(filtered_nasa_file)

"""

def data_details(df):
    df.drop(columns=['Orbiting Body', 'Neo Reference ID', 'Equinox'], inplace=True, errors='ignore') #Mention the column to be removed
    num_rows = df.shape[0] #Get the numbers of rows
    num_cols = df.shape[1] #Get the numbers of columns
    titles = df.columns.tolist() #Get the list of remaining column names 
    return num_rows, num_cols, titles #Return a tuple with datadet details

#Data analysis phase

"""
_____________________________________________________________________________________________
Stage 4: Pretty Output - maximum absolute magnitude value 
_____________________________________________________________________________________________
Identifies the asteroid that has the highest absolute (maximum) magnitude value.

Args:
    df (pandas.DataFrame): DataFrame containing asteroid data, including "Name" and "Absolute Magnitude" columns.

Returns:
    tuple: (asteroid_name, max_value) where:
        asteroid_name (str): The name of the asteroid with the greatest absolute (maximum) magnitude.
        max_value (numeric): The highest absolute (maximum) magnitude found in the dataset.

"""

def max_absolute_magnitude(df):
    max_index = df['Absolute Magnitude'].idxmax() #Find the highest absolute magnitude value
    return int(df.loc[max_index, 'Name']), float(df.loc[max_index, 'Absolute Magnitude']) #Get the mentioned and corresponding asteroid name

"""
_____________________________________________________________________________________________
Stage 5: Pretty Output - ateroid with closest approach to earth (kilometers) 
_____________________________________________________________________________________________
Determines the asteroid that made the closest approach to Earth based on miss distance in kilometers.

Args:
    df (pandas.DataFrame): DataFrame containing asteroid data with "Name" and "Miss Dist.(kilometers)" columns.
Returns:
    str: The name of the asteroid with the smallest miss distance from Earth.

"""

def closest_to_earth(df):
    min_index = df['Miss Dist.(kilometers)'].idxmin() #Find the minimum miss distance value
    #Get the name of the asteroid corresponding to the minimum miss distance
    return int(df.loc[min_index, 'Name'])

"""
_____________________________________________________________________________________________
Stage 6: Pretty Output - ateroid with Orbit ID and return result as dictionary 
_____________________________________________________________________________________________
Calculates the number of asteroids associated with each Orbit ID and returns the results as a dictionary.

Args:
    df (pandas.DataFrame): DataFrame containing asteroid data with the "Orbit ID" column.
Returns:
    dict: A dictionary mapping each Orbit ID to the count of asteroids assigned to it.

"""

def common_orbit(df):
    return df['Orbit ID'].value_counts() #Count occurrences of each Orbit ID and convert to dictionary

"""
_____________________________________________________________________________________________
Stage 7: Pretty Output - ateroid with Orbit ID and return result as dictionary 
_____________________________________________________________________________________________
Counts how many asteroids have a maximum estimated diameter ("Est Dia in KM(max)")
greater than the average maximum diameter of all asteroids in the DataFrame.

Args:
    df (pandas.DataFrame): DataFrame containing asteroid data with the "Est Dia in KM(max)" column.
Returns:
    int: The number of asteroids whose maximum estimated diameter exceeds the overall average.

"""

def min_max_diameter(df):
    mean_val = df['Est Dia in KM(min)'].mean() #Calculate the average maximum diameter
    return df[df['Est Dia in KM(min)'] > mean_val].shape[0] #Count rows with diameter above average

#Data presentation phase
"""
_____________________________________________________________________________________________
Stage 8: visualisation - Executes a series of analytical operations on an asteroid dataset and prints the results.
_____________________________________________________________________________________________
Prints basic information about the dataset (shape and column names).
Identifies and prints the asteroid with the highest absolute magnitude.
Finds and prints the asteroid that made the closest approach to Earth.
Calculates and prints the frequency of asteroids by Orbit ID.
Counts and prints how many asteroids have a maximum estimated diameter above the dataset's average.

Args:
    df (pandas.DataFrame): The input DataFrame containing asteroid data. 
        Expected to include the following columns:
            "Name"
            "Absolute Magnitude"
            "Miss Dist.(kilometers)"
            "Orbit ID"
            "Est Dia in KM(min)"
            "Est Dia in KM(max)"
Returns:
    None
"""

def run_analysis_and_print(df):
     #Print basic dataset info
    print("Saving mock_asteroid_data.csv to mock_asteroid_data.csv")
    print(f"Data shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print("Table Column Headers:") # Print column headers
    for col in df.columns:
        print(f"  {col}")

    max_name, max_val = max_absolute_magnitude(df) #Find and print asteroid with the highest absolute magnitude
 
    print("Max absolute magnitude:")
    print(f"  ({max_name}, {max_val})")

    closest_name = closest_to_earth(df) #Find and print the closest asteroid to Earth
    print("Closest to Earth asteroid:")
    print(f"  {closest_name}")

    print("Orbit frequency:") #Count and print asteroids by Orbit ID
    for orbit_id, count in common_orbit(df).items():
        print(f"  {orbit_id}: {count}")

    above_mean = min_max_diameter(df) #Count and print asteroids with diameter above the average
    print("Asteroids above mean diameter:")
    print(f"  {above_mean}")

"""
_____________________________________________________________________________________________
Stage 9: visualisation - histogram chart for distribution of ateroids (average estimated diameter(km))
_____________________________________________________________________________________________
Displays a histogram showing the distribution of asteroids by their average estimated diameter in kilometers.
The average diameter for each asteroid is calculated as the mean of the minimum and maximum
estimated diameters in kilometers:
    average = (Est Dia in KM(min) + Est Dia in KM(max)) / 2

Args:
    df (pandas.DataFrame): DataFrame containing asteroid data.
        (Note: This DataFrame must include the columns 
        "Est Dia in KM(min)" and "Est Dia in KM(max)". 
        If not, modify the column names accordingly.)

    The histogram is generated using 100 continuous bins.
"""

# Check that the required columns exist
def plt_hist_diameter_improved(df, bins=30, color='blue', show_grid=True):
    # Compute the average diameter for each asteroid
    avg_diameter = df[['Est Dia in KM(min)', 'Est Dia in KM(max)']].mean(axis=1)
    
    plt.figure(figsize=(10, 6))  # Create a new figure with dimensions 10x6 inches
    plt.hist(avg_diameter, bins=bins, color=color, edgecolor='black')
    plt.title('Distribution of Average Asteroid Diameters')
    plt.xlabel('Average Diameter (KM)')
    plt.ylabel('Number of Asteroids')

    if show_grid: #Optionally show grid on plot
        plt.grid(True, linestyle='--', alpha=0.6)
        
    # Get min and max of average diameter
    min_val = avg_diameter.min() 
    max_val = avg_diameter.max()
    # Determine tick step based on number of unique orbits
    orbit_count = df['Orbit ID'].nunique()
    if orbit_count > 100:
        tick_step = 0.2
    else:
        tick_step = (max_val - min_val) / 14 # Generate x-axis ticks

    x_ticks = np.arange(min_val, max_val + tick_step, tick_step).round(2)
    
    plt.xticks(ticks=x_ticks) # Display the plot
    plt.tight_layout()
    plt.show()

"""
_____________________________________________________________________________________________
Stage 10: visualisation - histogram chart representing the number of asteroids based on Minimum Orbit Intersection values.
_____________________________________________________________________________________________
The histogram uses 10 continuous bins ranging from the minimum to the maximum 
values found in the 'Minimum Orbit Intersection' column.

Args:
    df (pandas.DataFrame): DataFrame containing asteroid data with the 
    'Minimum Orbit Intersection' column.
"""

def plt_hist_common_orbit(df):
    plt.figure(figsize=(10, 5))  #Create the plot
    #Plot the histogram with 10 bins over the specified range, set colors and add a label
    df['Minimum Orbit Intersection'].plot(kind='hist', bins=10, color='gray')
    plt.title('Minimum Orbit Intersection')     #Set the title and labels for the axes
    plt.xlabel('Orbit Distance') #Set the title and labels for the axes
    plt.ylabel('Frequency')
    plt.grid(True, linestyle='--', alpha=0.6) #Display the legend and add gridlines
    plt.xlim(df['Minimum Orbit Intersection'].min(), df['Minimum Orbit Intersection'].max())
    plt.tight_layout() #Adjusts the layout so that all plot elements
    plt.show() #Renders and displays the final plot in a window or inline
"""
_____________________________________________________________________________________________
Stage 11: visualisation - pie chart representing the number of asteroids based on Minimum Orbit Intersection values.
_____________________________________________________________________________________________
Displays a pie chart illustrating the proportion of hazardous vs. non-hazardous asteroids 
based on the 'Hazardous' column in the DataFrame.

Args:
    df (pandas.DataFrame): DataFrame containing asteroid data with a 'Hazardous' column 
                       (expected to be boolean or numeric, where 1 indicates hazardous and 0 indicates non-hazardous).
"""

def plt_pie_hazard(df):
    counts = df['Hazardous'].value_counts()
    labels = ['Hazardous' if val == 1 else 'Non-Hazardous' for val in counts.index]
    colors = ['red', 'green']  #Dis[lay by  the signs : red for dangerous and green for non-dangerous
    explode = [0.1 if label == 'Hazardous' else 0 for label in labels]  #Reflects and emphesize for dangerous
    
    plt.figure(figsize=(10, 6)) #Create the new plot
    plt.pie(
        counts,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        explode=explode,
        startangle=140,
        shadow=True
    )
    plt.title('Percentage of Hazardous and Non-Hazardous Asteroids')
    plt.legend(labels, loc='upper right')
    plt.tight_layout()
    plt.show()

"""
_____________________________________________________________________________________________
Stage 12: visualisation - scatter plot chart representing the relationship
between an asteroid’s miss distance from Earth (km).
_____________________________________________________________________________________________
Displays a scatter plot with a simple linear regression line to explore the relationship 
between an asteroid’s miss distance from Earth (in kilometers) and its speed (in miles per hour).

Args:
    df (pandas.DataFrame): DataFrame containing asteroid data with the columns 
                         "Miss Dist.(kilometers)" and "Miles per hour".
Returns:
    None

My Answer:
    Based on the regression analysis shown in the plot,
    there does not appear to be a strong linear correlation between miss distance and asteroid speed.
    I believe this outcome could vary with different datasets or value distributions.

"""

def plt_linear_motion_magnitude(df):
    x = df['Miles per hour']
    y = df['Absolute Magnitude']
    slope, intercept, r, p, stderr = np.linregress(x, y) #Compute the linear regression coefficients
    #Create the plot
    plt.scatter(x, y) #Plot the actual data points
    plt.plot(x, slope * x + intercept, color='red') #Plot the regression line
    plt.title('Absolute Magnitude vs Speed')
    plt.xlabel('Speed (mph)')
    plt.ylabel('Magnitude')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

"""
_______________________________________
Stage 13 : Run All Steps
_______________________________________
"""

# Load and filter the data
df = load_data() 
df = mask_data(df)

# Select only relevant columns
df = df[[ 
    'Name', 'Close Approach Date', 'Absolute Magnitude',
    'Miss Dist.(kilometers)', 'Orbit ID',
    'Est Dia in KM(min)', 'Est Dia in KM(max)',
    'Minimum Orbit Intersection', 'Miles per hour', 'Hazardous',
    'Orbiting Body', 'Neo Reference ID', 'Equinox'
]]

#Run core analysis and plots
run_analysis_and_print(df)
plt_hist_diameter_improved(df)
plt_hist_common_orbit(df)
plt_pie_hazard(df)
plt_linear_motion_magnitude(df)
