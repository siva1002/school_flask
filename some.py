def somefun():

    lst = ["data", "data2", "data3", "data4"]

    data = []

    somevalues = "data3"

    for i in lst:

        data.append(i)

        if i == somevalues:

            break

    return data


somefun()
