import matplotlib.pyplot as plt


def show_data(df, col_name, **indices):
    index1 = indices.get('index1', None)
    index2 = indices.get('index2', None)

    df[index1 : index2].plot(x='Date', y=col_name)
    plt.show()