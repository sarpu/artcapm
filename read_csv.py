import csv, os, sys
from operator import itemgetter
from numpy import median

def create_dict():
    my_dict = {"10": dict(), "20": dict(), "30": dict(), "40": dict(), "50": dict(), "60": dict()}
    return my_dict

def create_year_dict():
    my_dict = {"early": dict(), "late": dict()}
    return my_dict

def height_extract(my_col):
    #print my_col
    my_list = my_col.split(" ")
    #print my_list
    if len(my_list) > 1:
        return float(my_list[1])
    return 0

def top_twenty(rows):
    my_dict = dict()
    for row in rows:
        if row[0]:
            if row[0] in my_dict:
                my_dict[row[0]]["freq"] += 1
                my_dict[row[0]]["rows"].append(row)
            else:
                my_dict[row[0]] = {"freq": 1, "rows":[row]}
    return my_dict

def art_year(year):
    if year:
        year = year.replace("Circa", "")
        year = year.replace("Before", "")
        if "-" in year:
            year = year.split("-")[1].strip()
        year = year.replace(" ","")

        return year
    return 0

def year_range(years):
    my_list = []
    for year in years:
        #print year
        if year:
            year = year.replace("Circa", "")
            year = year.replace("Before", "")
            if "-" in year:
                year = year.split("-")[1].strip()
            year = year.replace(" ","")

            my_list.append(int(year))
    my_list = sorted(my_list)
    #print my_list
    my_median = median(my_list)
    return int(my_median)

def artist_dict():
    with open(os.path.join(sys.path[0], 'Sothebys.csv'), 'rU') as csvfile:
        my_file = csv.reader(csvfile, delimiter=',')
        artist_dict = dict()

        my_dict = top_twenty(my_file)
        #print my_dict
        my_list = []
        for item in my_dict:
            my_list.append((item, my_dict[item]["freq"]))

        sorted_list = sorted(my_list, key=itemgetter(1), reverse=True)
        twenty = sorted_list[:20]
        for artist in twenty:
            print artist[0]
            my_year = year_range([row[4] for row in my_dict[artist[0]]["rows"]])
            #print my_year
            for row in my_dict[artist[0]]["rows"]:
                if row[0] in artist_dict:
                    my_height=height_extract(row[5])
                    if my_height > 0:
                        for h in sorted(artist_dict[row[0]].keys()):
                            if my_height <= int(h):
        # if year is non-existent, we take it as zero, this needs to be fixed.
                                if int(art_year(row[4])) <= my_year:
                                    #print art_year(row[4])
                                    artist_dict[row[0]][h]["early"][row[1]] = {"price": row[14], "sale": row[9]}
                                else:
                                    artist_dict[row[0]][h]["late"][row[1]] = {"price": row[14], "sale": row[9]}

                else:
                    artist_dict[row[0]] = create_dict()
                    for item in artist_dict[row[0]]:
                        artist_dict[row[0]][item] = create_year_dict()

        return artist_dict


my_dict = artist_dict()
print my_dict
