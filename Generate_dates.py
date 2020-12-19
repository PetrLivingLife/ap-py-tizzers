import datetime as dt
 
"""" "g:\\temporary indement files\\dates.txt" """
 
 
def generate_dates(filename):
    date_range = 4000
    start_date = dt.date.today() - dt.timedelta(days=date_range)
    date_list = [start_date + dt.timedelta(days=x) for x in range(0, date_range)]
 
    with open(filename, 'w') as f:
        f.write("fromDate,toDate\n")
        for item in date_list:
            f.write("{},{}".format(item.strftime("%Y-%m-%d"), (item+dt.timedelta(days=1)).strftime("%Y-%m-%d")))
            f.write('\n')


generate_dates(r"d:\temporary indement files\dates.csv")
