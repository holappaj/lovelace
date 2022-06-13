def count_series(values):
    return sum(values)
    
def count_parallel(values):
    return 1 / sum([1 / a for a in values])
    
resistors = []
while True:
    value = input("Give a resistance value: ")
    if value:
        try:    
            value = float(value)      
        except ValueError:
            print("Invalid, please try again.")
        else:
            if value > 0:
                resistors.append(value)
            else:
                print("Invalid, please try again.")
    else:
        break

if resistors:
    print("Series resitance:",count_series(resistors))
    print("Parallel resistance:",count_parallel(resistors))
    
else:
    print("You didn't give a single resistor value!")

    