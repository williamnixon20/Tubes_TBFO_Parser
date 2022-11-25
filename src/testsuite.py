from main import check
import os
import time

if __name__ == "__main__":
    dirs = os.listdir("../test")
    for dir in dirs:
        check("../test/{}".format(dir))
        time.sleep(5)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("file", type=argparse.FileType("r"))
    # args = parser.parse_args()
    # check(args.file.name)
