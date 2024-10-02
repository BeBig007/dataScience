from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import pandas as pd
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


def plot_decision_tree(clf_object):
    """Plot the decision tree."""
    plt.figure(figsize=(15, 10))
    plot_tree(clf_object, filled=True, rounded=True)
    plt.title("Decision tree trained on al Knights features")
    plt.show()


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

        print(f"{c_shape}---------------Training Tree-----------{c_reset}")
        model = DecisionTreeClassifier(random_state = 42)
        model.fit(X_train, Y_train)

        print(f"{c_shape}---------------Prediction--------------{c_reset}")
        Y_pred = model.predict(X_valid)
        print(f"{c_red}Report on validation data\n{c_reset}")
        print(classification_report(Y_valid, Y_pred))


        print(f"{c_shape}---------------Test data---------------{c_reset}")
        Y_test = model.predict(test_data)
        with open('Tree.txt', 'w') as f:
            for line in Y_test:
                f.write(f"{line}\n")

        print(f"{c_shape}---------------Plot decision tree------{c_reset}")
        plot_decision_tree(model)

    except AssertionError as msg:
        print(f"Assertion Error: {msg}")


if __name__ == "__main__":
    main()
