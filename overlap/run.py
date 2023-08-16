import argparse
from detector import Lesion
import os

def main(lesion_path, planes_path):
    name = lesion_path.split("/")[-1].split(".")[0]
    l = Lesion(lesion_path, planes_path)
    res, info = l.overlap_detection()
    print(f"name: {name}\nres: {res}\ninfo: {info}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Overlap Detector",
        description="find most overlaped tracts"
    )
    
    parser.add_argument("-l", "--lesion", dest="lesion_path")
    parser.add_argument("-p", "--planes", dest="planes_path")

    args = parser.parse_args()
    
    if os.path.isdir(args.lesion_path):
        dirs = os.listdir(args.lesion_path)
        for file in dirs:
            lesion_path = os.path.join(args.lesion_path, file)
            main(lesion_path, args.planes_path)
    else:
        main(args.lesion_path, args.planes_path)
