# Define a function to check if the date is within the given range
def is_within_date_range(dt):
    if dt.month > 12 or (dt.month == 12 and dt.day >= 15):
        return True
    elif dt.month < 3 or (dt.month == 3 and dt.day <= 3):
        return True
    elif (dt.month == 7 and dt.day >= 15 and dt.day <= 31):
        return True
    elif (dt.month == 9 and dt.day >= 11 and dt.day <= 30):
        return True
    else:
        return False
    
# Define time categories
time_categories = {
    'mañana': ((5, 0), (11, 59)),
    'tarde': ((12, 0), (18, 59)),
    'noche': ((19, 0), (4, 59))
}

# Create a function to classify the time
def classify_time(timestamp):
    hour = timestamp.hour
    minute = timestamp.minute

    for category, ((start_hour, start_minute), (end_hour, end_minute)) in time_categories.items():
        if category == 'noche':
            if (hour > start_hour or (hour == start_hour and minute >= start_minute)) or \
                    (hour < end_hour or (hour == end_hour and minute <= end_minute)):
                return category
        else:
            if (hour > start_hour or (hour == start_hour and minute >= start_minute)) and \
                    (hour < end_hour or (hour == end_hour and minute <= end_minute)):
                return category
    return None