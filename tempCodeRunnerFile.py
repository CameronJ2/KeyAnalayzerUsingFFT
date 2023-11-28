    # Check if the last four values are the same
    prev_values.append(max_amplitude_freq)
    if len(prev_values) == 4 and all(val == prev_values[0] for val in prev_values):
        print(f"The last four values are the same: {prev_values[0]}")

    # Remove the oldest value if more than four values are stored
    if len(prev_values) > 4:
        prev_values.pop(0)