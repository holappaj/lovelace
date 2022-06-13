def count_series(resistors):
    return sum(resistors)
    
def calculate_voltage(resistors, current):
    voltages = []
    for z in resistors:
        voltages.append(z * current)
    return voltages
    