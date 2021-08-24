import pandas as pd

def describe_overarching_change(x,y,ts):
    # assume each x value is distinct and that there are more than one rows
    min_x = ts[x].min()
    y_at_min_x = ts[ts[x] == min_x][y].values[0]

    max_x = ts[x].max()
    y_at_max_x = ts[ts[x] == max_x][y].values[0]

    return describe_change(x,y,(min_x,y_at_min_x),(max_x,y_at_max_x))

def describe_interval_changes(x,y,ts):
    # assume each x value is distinct and that there are more than one rows
    ts = ts.sort_values(by=[x])
    diffs = ts.diff()
    ts['change_y_per_x'] = diffs[y]/diffs[x]

    cap = "Within this " + x.lower() + " range, we were able to capture data at " + str(ts.shape[0]) + " " + x.lower() + "s ("
    cap += stringify(ts[x].to_list()) + "), forming " + str(ts.shape[0] - 1) + " intervals. "
    if (ts[ts['change_y_per_x'] > 0].shape[0] > 0):
        cap += describe_interval_increases(x,y,ts)
    if (ts[ts['change_y_per_x'] < 0].shape[0] > 0):
        cap += describe_interval_decreases(x,y,ts)
    return cap

def describe_max_min(x,y,ts):
    cap = ""
    if (ts[y].max()!=ts[y].min()):
        max_val = ts[y].max()
        max_val_years = ts[ts[y] == max_val][x]
        cap += y + " was at its highest in " + stringify(max_val_years.to_list()) + " at " + str(max_val) + ". "
        min_val = ts[y].min()
        min_val_years = ts[ts[y] == min_val][x]
        cap += y + " was at its lowest in " + stringify(min_val_years.to_list()) + " at " + str(min_val) + ". "
    return cap

### HELPERS
def describe_interval_increases(x,y,ts):
    cap = y + " increased in "
    if ts[ts['change_y_per_x'] > 0].shape[0] == (ts.shape[0] - 1):
        cap += "all"
    else:
        cap += str(ts[ts['change_y_per_x'] > 0].shape[0])
    cap += " of these recorded intervals"
    max_change = ts['change_y_per_x'].max()
    maxes = ts[ts['change_y_per_x'] == max_change]
    ranges = []
    for i in maxes.index:
        stringa = str(ts.iloc[i-1][x].astype('int64')) + "-" + str(ts.iloc[i][x].astype('int64'))
        ranges.append(stringa)
    cap += ", showing the greatest average increase in " + y + " per " + x.lower() + " of " + str(max_change) + " in " + stringify(ranges) + ". "
    return cap

def describe_interval_decreases(x,y,ts):
    cap = y + " decreased in "
    if ts[ts['change_y_per_x'] < 0].shape[0] == (ts.shape[0] - 1):
        cap += "all"
    else:
        cap += str(ts[ts['change_y_per_x'] < 0].shape[0])
    cap += " of these recorded intervals"
    min_change = ts['change_y_per_x'].min()
    mins = ts[ts['change_y_per_x'] == min_change]
    ranges = []
    for i in mins.index:
        stringa = str(ts.iloc[i-1][x].astype('int64')) + "-" + str(ts.iloc[i][x].astype('int64'))
        ranges.append(stringa)
    cap += ", showing the greatest average decrease in " + y + " per " + x.lower() + " of " + str(min_change) + " in " + stringify(ranges) + ". "
    return cap

def inc_dec(a,b):
    if (a < b):
        return "increased"
    elif (a > b):
        return "decreased"
    else:
        return "remained constant"

def from_in_to(a,b,capitalize):
    if capitalize:
        return "From " + str(a[1]) + " in " + str(a[0]) + " to " + str(b[1]) + " in " + str(b[0])
    else:
        return "from " + str(a[1]) + " in " + str(a[0]) + " to " + str(b[1]) + " in " + str(b[0])

def describe_change(x,y,pta,ptb):
    caption = y + " " + inc_dec(pta[1],ptb[1]) + " " + from_in_to(pta,ptb,False) + "."
    return caption

def stringify(a):
    list_str = ""
    for i in range(len(a)):
        if i == len(a) - 1 and len(a)>1:
            list_str += "and "
        list_str += str(a[i])
        if i != len(a) - 1:
            if len(a)>2:
                list_str += ","
            list_str += " "
    return list_str
