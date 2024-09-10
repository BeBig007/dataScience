import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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


def chart_nb_customers(data: pd.DataFrame):
    """ Create a chart from the data """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print(data)
        plt.figure()
        plt.plot(data['date'], data['num_customers'])
        x_ticks = ['2022-10-01', '2022-11-01', '2022-12-01', '2023-01-01', '2023-02-01']
        x_ticks_labels = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb']
        plt.xticks(ticks=x_ticks, labels=x_ticks_labels)
        plt.ylabel('Number of customers')
        plt.margins(x=0, y=0.05)
        plt.tick_params(length=0)
        plt.savefig('nb_customers_chart.png')
        print('Fist plot created !\n')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


def chart_total_sales(data: pd.DataFrame):
    """ Create a chart from the data """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print(data)
        data['month'] = data['month'].astype(str)
        plt.figure()
        plt.bar(data['month'], data['num_sales'])
        x_ticks = ['10', '11', '12', '1', '2']
        x_ticks_labels = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb']
        plt.xticks(ticks=x_ticks, labels=x_ticks_labels)
        plt.ylabel('total sales in million of ₳')
        plt.xlabel('month')
        plt.tick_params(length=0)
        plt.savefig('total_sales_chart.png')
        print('Second plot created !\n')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


def chart_average_spend(data: pd.DataFrame):
    """ Create a chart from the data """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print(data)
        plt.figure()
        plt.plot(data['date'], data['tot_sales'])
        x_ticks = ['2022-10-01', '2022-11-01', '2022-12-01', '2023-01-01', '2023-02-01']
        x_ticks_labels = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb']
        plt.xticks(ticks=x_ticks, labels=x_ticks_labels)
        y_ticks = np.arange(0, data['tot_sales'].max() + 1, 5)
        plt.yticks(y_ticks)
        plt.ylabel('average spend/customers in ₳')
        plt.tick_params(length=0)
        plt.margins(x=0)
        plt.fill_between(data['date'], 0, data['tot_sales'], alpha=0.7)
        plt.savefig('average_spend_chart.png')
        print('Third plot created !\n')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    data = load("out_nb_customers.csv")
    chart_nb_customers(data)
    
    sales = load("out_sales_by_month.csv")
    chart_total_sales(sales)
    
    av_spend = load('out_average_spend.csv')
    chart_average_spend(av_spend)

# 1286102 rows
# docker cp postgres:nb_customers_chart.png dataScience_02/ex01 && docker cp postgres:total_sales_chart.png dataScience_02/ex01 && docker cp postgres:average_spend_chart.png dataScience_02/ex01