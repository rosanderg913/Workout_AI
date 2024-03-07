import re

def parse_exercise(exercise_text):
    # Extracts data from a single exercise text string
    match = re.search(r'Exercise (\d+): Sets: ([^,]+), Reps: ([\d\-]+), Rest: ([\d\-]+) minutes?', exercise_text)
    if match:
        return {
            "exercise_number": int(match.group(1)),
            "sets": match.group(2),
            "reps": match.group(3),
            "rest": match.group(4),
        }
    else:
        # Handle cases where the format might not be consistent
        return None
    
def extract_exercise_data(workout_text):
    # Extracts data for all exercises from the response text
    exercises = workout_text.split("\n")[2:]    # Skip focus line and first newline
    exercise_data = []
    for exercise in exercises:
        parsed_data = parse_exercise(exercise)
        if parsed_data:
            exercise_data.append(parsed_data)
        return exercise_data