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


def chart_bar_frequency(data: pd.DataFrame):
    """ Create a chart from the data """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print(data)
        plt.figure()
        n, bins, patches = plt.hist(data['total_order'], bins=5)
        for patch in patches:
            patch.set_width(0.99 * (bins[1] - bins[0]))
        x_ticks = [0, 10, 20, 30]
        x_ticks_labels = ['0', '10', '20', '30']
        plt.xticks(ticks=x_ticks, labels=x_ticks_labels)
        plt.xlabel('frequency')
        plt.ylabel('customers')
        plt.tick_params(length=0)
        plt.savefig('frequency_chart.png')
        print('Histogram created !\n')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


def chart_bar_monetary(data: pd.DataFrame):
    """ Create a chart from the data """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print(data)
        plt.figure()
        n, bins, patches = plt.hist(data['total_price'], bins=5)
        for patch in patches:
            patch.set_width(0.99 * (bins[1] - bins[0]))
        x_ticks = [0, 50, 100, 150, 200]
        x_ticks_labels = ['0', '50', '100', '150', '200']
        plt.xticks(ticks=x_ticks, labels=x_ticks_labels)
        plt.xlabel('monetary value in ₳')
        plt.ylabel('customers')
        plt.tick_params(length=0)
        plt.savefig('monetary_value_chart.png')
        print('Histogram created !\n')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    data = load("out_freq.csv")
    chart_bar_frequency(data)

    monetary_value = load("out_monetary.csv")
    chart_bar_monetary(monetary_value)


# docker cp postgres:frequency_chart.png ex03 && docker cp postgres:monetary_value_chart.png ex03
