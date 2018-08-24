
from opswat import MetaDefenderApi

if __name__ == "__main__":

    md = MetaDefenderApi(ip="10.26.50.15", port=8008)

    #dir = "files"
    dir = "C:\\Users\\10694\\dev"
    results = md.scan_directory(dir)


    print(results)