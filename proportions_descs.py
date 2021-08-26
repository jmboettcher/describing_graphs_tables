import pandas as pd
import timeseries_descs as d

def describe_proportions(group,strat,prop,p):
    p = p.sort_values(by=[strat])
    cap = "Of individuals in the " + group + " group, "
    max_prop = p[prop].max()
    strats_at_max_prop = p[p[prop] == max_prop][strat].values
    max_prop_string = " (" + str(max_prop) + "%)"
    if max_prop > 50:
        cap += "a majority" + max_prop_string + " were classified under " + strats_at_max_prop[0] + ". "
    else:
        cap += "the largest percentage were classified under " + d.stringify(strats_at_max_prop,max_prop_string)
    rest_strats = p[p[prop] != max_prop]
    cap += "The rest were smaller percentages at " + stringify_complex(strat,prop,rest_strats) + "."
    return cap


def stringify_complex(key,value,df):
    list_str = ""
    num_rows = df.shape[0]
    for i in range(num_rows):
        if i == num_rows - 1 and num_rows>1:
            list_str += "and "
        list_str += str(df.iloc[i][key]) + " (" + str(df.iloc[i][value]) + "%)"
        if i != num_rows - 1:
            if num_rows>2:
                list_str += ","
            list_str += " "
    return list_str
