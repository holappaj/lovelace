def store_sums(sums, fname):
    with open(fname, "w") as target:        
        for row in sums:
            target.write(":".join(row) + "\n")