from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
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
    c_shape = "\033[94m"  # Blue
    c_red = "\033[91m"  # Red

    try:
        assert len(sys.argv) == 3, "1 Usage: python3 Tree.py /path/to/Train_knight.csv /path/to/Test_knight.csv"
        assert sys.argv[1] not in "Train_knight.csv", "2 Usage: python3 Tree.py /path/to/Train_knight.csv /path/to/Test_knight.csv"
        assert sys.argv[2] not in "Test_knight.csv", "3 Usage: python3 Tree.py /path/to/Train_knight.csv /path/to/Test_knight.csv"

        print(f"{c_shape}---------------Load file---------------{c_reset}")
        train_data = import_data(sys.argv[1])
        test_data = import_data(sys.argv[2])

        print(f"{c_shape}---------------Split data--------------{c_reset}")
        X = train_data.drop('knight', axis=1)
        Y = train_data.knight

        X_train, X_valid, Y_train, Y_valid = train_test_split(X, Y, train_size=0.8, random_state=42)
        
        print(f"{c_shape}---------------Preprocessing data-------{c_reset}")
        scaler = StandardScaler()
        X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
        X_valid = pd.DataFrame(scaler.transform(X_valid), columns=X_valid.columns)

        print(f"{c_shape}---------------KNN------------{c_reset}")
        k_values = [i for i in range (1,31)]
        scores = []

        X = scaler.fit_transform(X)

        for k in k_values:
            knn = KNeighborsClassifier(n_neighbors=k)
            score = cross_val_score(knn, X, Y, cv=5)
            scores.append(np.mean(score))
        
        plt.figure()
        sns.lineplot(x = k_values, y = scores)
        plt.xlabel("k values")
        plt.ylabel("accuracy")
        plt.show()

        print(f"{c_shape}---------------Training KNN------------{c_reset}")
        best_index = np.argmax(scores)
        best_k = k_values[best_index]
        print(f"{c_red}Best k value: {best_k}\n{c_reset}")

        model = KNeighborsClassifier(n_neighbors=best_k)
        model.fit(X_train, Y_train)
        
        print(f"{c_shape}---------------Prediction--------------{c_reset}")
        Y_pred = model.predict(X_valid)
        print(f"{c_red}Report on validation data\n{c_reset}")
        print(classification_report(Y_valid, Y_pred))

        print(f"{c_shape}---------------Test data---------------{c_reset}")
        df_std = pd.DataFrame(scaler.transform(test_data), columns=test_data.columns)
        Y_test = model.predict(df_std)
        with open('KMN.txt', 'w') as f:
            for line in Y_test:
                f.write(f"{line}\n")

    except AssertionError as msg:
        print(f"Assertion Error: {msg}")


if __name__ == "__main__":
    main()
