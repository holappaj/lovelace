import urllib.request

with urllib.request.urlopen("http://enk.kapsi.fi") as f:
    print(f.read(100).decode("utf-8"))


