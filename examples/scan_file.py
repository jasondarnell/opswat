
from opswat import MetaDefenderApi

if __name__ == "__main__":

    md = MetaDefenderApi(ip="10.26.50.15", port=8008)

    results = md.scan_file("foo.txt")

    print(results)