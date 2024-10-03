from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, precision_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys
import os


def import_data(path):
    """Load data from csv file."""
    try:
        assert isinstance(path, str), "your path is not valid."
        assert os.path.exists(path), "your file doesn't exist."
        assert os.path.isfile(path), "your 'file' is not a file."
        assert path.lower().endswith(".csv"), "file format is not .csv."
        data = pd.read_csv(path)
        return data

    except AssertionError as msg:
        print(f"Assertion Error: {msg}")


def main():
    c_reset = "\033[0m"
    c_shape = "\033[94m"     # Blue
    c_red = "\033[91m"       # Red

    try:
        assert len(sys.argv) == 3, "1 Usage: python3 Tree.py /path/to/Train_knight.csv /path/to/Test_knight.csv"
        assert sys.argv[1] not in "Train_knight.csv", "2 Usage: python3 Tree.py /path/to/Train_knight.csv /path/to/Test_knight.csv"
        assert sys.argv[2] not in "Test_knight.csv", "3 Usage: python3 Tree.py /path/to/Train_knight.csv /path/to/Test_knight.csv"

        print(f"{c_shape}---------------Load file---------------{c_reset}")
        train_data = import_data(sys.argv[1])
        test_data = import_data(sys.argv[2])

        print(f"{c_shape}---------------Preprocessing data------{c_reset}")
        X = train_data.drop('knight', axis=1)
        Y = train_data.knight

        scaler = StandardScaler()
        X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

        X_train, X_valid, Y_train, Y_valid = train_test_split(X, Y, train_size=0.8, random_state=42)



    except AssertionError as msg:
        print(f"Assertion Error: {msg}")


if __name__ == "__main__":
    main()
