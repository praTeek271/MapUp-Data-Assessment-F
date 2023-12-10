import pandas as pd


def generate_car_matrix(df) -> pd.DataFrame:
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[[range(len(car_matrix))]*2] = 0  # Setting diagonal values to 0
    return car_matrix


def get_type_count(df) -> dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_count = df['car_type'].value_counts().to_dict()
    return dict(sorted(type_count.items()))


def get_bus_indexes(df) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.sort_values().tolist()
    return bus_indexes


def filter_routes(df) -> list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    avg_truck_routes = df.groupby('route')['truck'].mean()
    selected_routes = avg_truck_routes[avg_truck_routes > 7].index.sort_values().tolist()
    return selected_routes


def multiply_matrix(matrix) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    return modified_matrix.round(1)

def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period.

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')
    
    # Useing list instead of tuple to select multiple columns in groupby
    grouped_data = df.groupby(['id', 'id_2']).agg({'start_datetime': 'min', 'end_datetime': 'max'}).reset_index()
    
    grouped_data['time_span'] = (grouped_data['end_datetime'] - grouped_data['start_datetime']).dt.total_seconds()
    grouped_data['full_24_hours'] = (grouped_data['time_span'] == 24 * 60 * 60)
    grouped_data['full_week'] = (
        (grouped_data['start_datetime'].dt.day_name() == 'Monday') &
        (grouped_data['end_datetime'].dt.day_name() == 'Sunday')
    )
    return grouped_data[['id', 'id_2', 'full_24_hours', 'full_week']]

