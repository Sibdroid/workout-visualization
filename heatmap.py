from typing import List, Union, T
import matplotlib.pyplot as plt
import matplotlib.colors as cls
from matplotlib.colors import LinearSegmentedColormap as LinearCmap
import seaborn as sns
import pandas as pd
import numpy as np
import random
import math
def split_list(list_: List[T],
               length: int) -> List[List[T]]:
    return [list_[i:i+length] for i in range(0, len(list_), length)]
def values_to_df(values: List[int],
                 row_length: int,
                 fill_empty: float = np.nan) -> pd.DataFrame:
    values = split_list(values, row_length)
    values[-1] = values[-1] + [fill_empty] * (row_length - len(values[-1]))
    df = pd.DataFrame(values)
    return df
def create_heatmap(values: List[int],
                   cmap: LinearCmap,
                   title: str,
                   ax: plt.Axes) -> plt.Axes:
    if len(values) == 28:
        values += [0.5]
    df = values_to_df(values, 7, 0.5)
    annot = values_to_df([i for i in range(1, 36)], 7, 0)
    ax = sns.heatmap(df, cmap = cmap, linewidth = 1, annot = annot,
                     linecolor = "white", cbar = False,
                     square = True, ax = ax)
    for text in ax.texts:
        if len(values) == 29:
            text.set_visible(int(text.get_text()) <= len(values)-1)
        else:
            text.set_visible(int(text.get_text()) <= len(values))
    ax.axis("off")
    ax.set_title(title)
    return ax
def main():
    fig, axes = plt.subplots(4, 3, figsize=(11.25, 10))
    data = pd.read_excel("workouts.xlsx")
    colors = [[0, "#A39594"],
              [0.5, "#FFFFFF"],
              [1, "#55D6BE"]]
    cmap = LinearCmap.from_list("", colors)
    for index, ax in enumerate(fig.axes):
        values = data.iloc[[index]].values.flatten().tolist()
        title = values[0]
        values = [i for i in values[1:] if not pd.isna(i)]
        create_heatmap(values, cmap, title, ax)
    fig.subplots_adjust(wspace=0)
    plt.savefig("heatmap.png")
if __name__ == "__main__":
    main()
