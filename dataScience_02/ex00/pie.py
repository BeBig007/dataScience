import pandas as pd
import matplotlib.pyplot as plt


def load(path: str) -> pd.DataFrame:
    """Load a dataset from a CSV file and print its content."""

    try:
        assert isinstance(path, str), "the input must be string"
        data = pd.read_csv(path)
        print(f"Loading {path} dataset of type:\n{data.dtypes}\n")
        return data

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")
    return None


def pie_chart(data: pd.DataFrame):
    """ Create a pie chart from the data """
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print(data)
        plt.figure()
        plt.pie(data['count'],
                labels=data['event_type'], 
                autopct='%1.1f%%',
                explode=[0.008, 0.008, 0.008, 0.008]
                )
        plt.savefig('pie_chart.png')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    data = load("out.csv")
    pie_chart(data)

# psql -U bebigel -d piscineds -h localhost

# docker cp postgres:pie_chart.png ex00 && open ex00/pie_chart.png