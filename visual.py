import matplotlib.pyplot as plt


# show a plot of df
def show_data(df, col_name, label="", **indices):
    index1 = indices.get('index1', None)
    index2 = indices.get('index2', None)

    try:
        df[index1: index2].plot(x='Date', y=col_name)
    except TypeError:
        print("Out of range?")

    # TODO: add 'Name', e.g. "spy"
    # plt.legend(loc='upper left')

    plt.show()


# show a plot comparing $list1 to $list2 with range given by index1 and index2
def show_data_compare(x_axis, list1, list2, label1="", label2="", **indices):
    plt.cla()

    index1 = indices.get('index1', None)
    index2 = indices.get('index2', None)

    plt.plot(list1, label=label1)
    plt.plot(list2, label=label2)
    plt.xlim([index1, index2])
    plt.legend()
    plt.show()
