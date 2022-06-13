def calculate_catheti(h):
    return h / (2 ** 0.5)

hypo = float(input(": "))
print(":", round(calculate_catheti(hypo), 4))