import json
import os
from time import time
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for matplotlib
# This is required for saving plots to files
import matplotlib.pyplot as plt


def save_json_to_file(data, filename):
    """
    Save the given data to a JSON file.
    :param data: The data to save.
    :param
    filename: The name of the file to save to.
    :return: None
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        
def save_plot_of_fitness_values(result, filename):
    """
    Save a plot of the fitness values to a file.
    :param result: The result containing fitness values.
    :param filename: The name of the file to save the plot to.
    :return: None
    """

    y = list(map(lambda x: x["fitness"], result['history']))
    plt.plot(y)
    plt.title('Fitness Values Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness Value')
    plt.savefig(filename)
    plt.close()


def persist_result(result):
    """
    Persist the result to a file and creates a plot of the fitness values.
    :param result: The result to persist.
    :return: None
    """
    now = datetime.now().fromtimestamp(time()).strftime("%Y-%m-%d_%H-%M-%S")
    save_json_to_file(result, f"results/{now}.json")
    save_plot_of_fitness_values(result, f"results/{now}.png")
