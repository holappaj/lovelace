import csv

def store_sums(sums, fname):
    with open(fname, "w", newline="") as f:
        w = csv.writer(f)
        for row in sums:
            w.writerow(row)