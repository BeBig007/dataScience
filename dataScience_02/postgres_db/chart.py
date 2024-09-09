import pandas as pd
import matplotlib.pyplot as plt


def load(path: str) -> pd.DataFrame:
    """Load a dataset from a CSV file and print its content."""

    try:
        assert isinstance(path, str), "the input must be string"
        data = pd.read_csv(path)
        print(f"Loading {path} dataset of type:\n {data.dtypes}\n")
        return data

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")
    return None


def chart(data: pd.DataFrame):
    """ Create a chart from the data """
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print(data)
        plt.figure()
        plt.plot()
        plt.savefig('first_chart.png')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    data = load("out.csv")
    chart(data)

# psql -U bebigel -d piscineds -h localhost
# 1286102 rows

# docker cp postgres:first_chart.png ex01 && open ex01/first_chart.png