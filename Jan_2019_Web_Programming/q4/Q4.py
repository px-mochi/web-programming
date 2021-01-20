# Question 3a

from flask import Flask, render_template, request
from flask_api import FlaskAPI, status, exceptions
import requests, csv
import pandas as pd

user_agent = {'User-agent': 'Mozilla/5.0'}
url = "https://raw.githubusercontent.com/jennybc/gapminder/master/data-raw/04_gap-merged.tsv" # Tab seprated file
data = requests.get(url, headers = user_agent)
data_str = data.content.decode("utf-8")
data_csv = csv.reader(data_str.splitlines(), delimiter='\t') 
data_list_raw = list(data_csv) # Used to convert into a python dictionary data model
headers = data_list_raw.pop(0)

data_list = [] # Actual list I am going to be using to insert into my template

line_id = 0
for line in data_list_raw:
    line_dict = {}
    line_dict['lineID'] = line_id
    line_dict['country'] = line[0]
    line_dict['continent'] = line[1]
    line_dict['year'] = int(line[2])
    line_dict['lifeExp'] = float(line[3])
    line_dict['population'] = int(line[4])
    line_dict['gdpPercap'] = float(line[5])
    line_id += 1
    data_list.append(line_dict) # Now I have a list of dicts.    

totalData = len(data_list)

# For sorting purposes
def byCountry(item):
    return item['country']
def byContinent(item):
    return item['continent']
def byYear(item):
    return item['year']
def byLifeExp(item):
    return item['lifeExp']
def byPopulation(item):
    return item['population']
def byGDP(item):
    return item['gdpPercap']

app = Flask(__name__)

# Question 3a)
@app.route("/")
def homepage():
    return render_template("table.html", data_list=data_list, headers=headers)
'''
@app.route("/10")
def dataTable():
    new_list = data_list[:9]
    return render_template("main.html", data_list=new_list, headers=headers)
'''
# Question 3b can be done via client side HTML and javascripting. This method used is server-side.
## Uncomment this section below if the question was intended to be sorting the whole table ##
'''
# Question 3b) and Question 3c) - Sorting the WHOLE table (The question is ambiguous.)
@app.route("/<int:dataKey>/", methods=['GET'])
def next10(dataKey):
    sortMethod = request.args.get('key', '')
    print(sortMethod)
    if sortMethod == "country":
        new_list = sorted(data_list, key=byCountry)
    elif sortMethod == "continent":
        new_list = sorted(data_list, key=byContinent)
    elif sortMethod == "year":
        new_list = sorted(data_list, key=byYear)
    elif sortMethod == "lifeExp":
        new_list = sorted(data_list, key=byLifeExp)
    elif sortMethod == "population":
        new_list = sorted(data_list, key=byPopulation)
    elif sortMethod == "gdpPercap":
        new_list = sorted(data_list, key=byGDP)
    else:
        new_list = data_list

    dataKey = dataKey - 1 # To make this match up to the actual row index
    if dataKey < totalData:
        page_list = new_list[dataKey-9:dataKey+1]
    elif dataKey-9 < totalData:
        page_list = new_list[dataKey-9:totalData]
    else:
        page_list = new_list[totalData-10:totalData]

    return render_template("table.html", data_list=page_list, headers=headers)
'''
## Comment out this section if the question is to sort the whole table ##
# Question 3b) and Question 3c) - Sorting the PAGE table (The question is ambiguous.)
@app.route("/<int:dataKey>/", methods=['GET','DELETE'])
def next10(dataKey):
    dataKey = dataKey - 1 # To make this match up to the actual row index
    if dataKey < totalData:
        page_list = data_list[dataKey-9:dataKey+1]
    elif dataKey-9 < totalData:
        page_list = data_list[dataKey-9:totalData]
    else:
        page_list = data_list[totalData-10:totalData]
        
    sortMethod = request.args.get('key', '')
    print(sortMethod)
    if sortMethod == "country":
        new_list = sorted(page_list, key=byCountry)
    elif sortMethod == "continent":
        new_list = sorted(page_list, key=byContinent)
    elif sortMethod == "year":
        new_list = sorted(page_list, key=byYear)
    elif sortMethod == "lifeExp":
        new_list = sorted(page_list, key=byLifeExp)
    elif sortMethod == "population":
        new_list = sorted(page_list, key=byPopulation)
    elif sortMethod == "gdpPercap":
        new_list = sorted(page_list, key=byGDP)
    else:
        new_list = page_list        
    
    deleteRows = request.args # Gets dict of all checkbox states
    deleteTrue = [] # List to store key values of checked checkboxes
    for key in deleteRows:
        if deleteRows[key] == "true":
            deleteTrue.append(int(key))
    
    print(deleteTrue)
    for line in new_list:
        if line['lineID'] in deleteTrue:  #If the ID of the line is in the deletion list
            #new_list.remove(line)  # Delete it from the listed list
            data_list.remove(line)  # Delete it from the main database
        
    return render_template("table.html", data_list=new_list, headers=headers)


# For Question 4) - passing data to javascript
@app.route("/api", methods=['GET'])
def database():
    byHeader = request.args.get('header', '') #Column to filter
    byContent = request.args.get('by', '') #Filter criteria
    grouping = request.args.get('grouping','') #groupby
    groupAgg = request.args.get('groupAgg','') #Do what with results
    
    
    df = pd.DataFrame(data_list)
    filtered = df

    if byHeader and byContent:
        filtered = df.loc[df[byHeader] == byContent]
    
        if grouping and groupAgg: # If something was returned (i.e. not None)
            filtered = filtered.groupby(['year']).agg({grouping:groupAgg})
    
    country = list(filtered['country'])
    continent = list(filtered['continent'])
    year = filtered['year'].sort_values().drop_duplicates(keep='first')
    year = list(year)
    lifeExp = list(filtered['lifeExp'])
    population = list(filtered['population'])
    gdpPercap = list(filtered['gdpPercap'])
    
    array = {"country":country,\
             "continent":continent,\
             "year":year,\
             "lifeExp":lifeExp,\
             "population":population,\
             "gdpPercap":gdpPercap}
    
    if byHeader not in headers:
        raise exceptions.NotFound
    
    print(array)
    return str(array).replace("'",'"') #JavaScript won't read the string as JSON if it was single quoted somehow


@app.route("/data-chart", methods=['GET'])
def datacharts():
    return render_template("dataChart.html")

@app.route("/stack-chart", methods=['GET'])
def stackcharts():
    return render_template("stackChart.html")

@app.route("/chart-filters", methods=['GET'])
def chartfilters():
    df = pd.DataFrame(data_list)
    continentPicked = request.args.get('picked', '')
    
    first3=[]

    continentDF = df['continent']
    continentList= list(continentDF.drop_duplicates(keep='first'))        
    print(continentList)
    
    countryList = [] # Placeholder for when page is first entered
    if continentPicked:
        countryDF= df.loc[df['continent'] == continentPicked]
        countryDF= df['country']
        countryList= list(countryDF.drop_duplicates(keep='first'))[:3]

        print(countryList)
        
    return render_template("chartFilters.html",continentList=continentList,firstThree=countryList)

if __name__ == "__main__":
    app.run(debug=True)
    