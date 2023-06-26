import csv, numpy as np

if __name__ == "__main__":
    with open("points.txt", "r") as file:
        file_as_csv = csv.reader(file, delimiter=",")
        aw = 0
        for row in file_as_csv:
            if "TERME" in str(row[0]):
                tmp = np.array([float(row[1]), float(row[2])])
                aw += np.linalg.norm(tmp)
                tmp = []
        
        file.seek(0,0)
        print(f"Awareness of terme is: {aw}")
