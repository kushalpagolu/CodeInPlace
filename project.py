"""
A Data Science program to analyse and visualize COVID-19 data using .csv file and api to get latest case data. 
To accomplish this python has libraries like "PLOTLY", which gives us tools like maps, bar, figures etc.
"""
import pandas as pd
import plotly.express as px
import requests
import json
import sys


def main():
    print('Welcome to Covid 19 Data and Vaccination Visualisation Project')
    data2 = pd.read_csv('sortedbytotalvaccines.csv')
    data4 = pd.read_csv('worldcovidcases.csv')
    df = data2[["vaccines", "country"]]
    df.head()
    dict_ = {}
    for vaccine in df.vaccines.unique():
        dict_[vaccine] = [df["country"][j] for j in df[df["vaccines"] == vaccine].index]
    vaccines = {}
    for key, value in dict_.items():
        vaccines[key] = set(value)

    print("Enter 1 to display Total Vaccinations by Country")
    print("Enter 2 to display Vaccination Manufacturers used by Country")
    print("Enter 3 to display visualisation of Total Covid-19 Cases Worldwide ")
    print("Enter 4 to display Total Covid-19 Cases by Country in a BAR diagram")
    print("Enter 5 to display visualisation of Live Total Covid-19 Cases by Country ")

    option = input("Please select from the available options to visualize data: ")
    while option not in ['1', '2', '3', '4', '5']:
        print("Enter 1 to display Total Vaccinations by Country")
        print("Enter 2 to display Vaccination Manufacturers used by Country")
        print("Enter 3 to display visualisation of Total Covid-19 Cases Worldwide ")
        print("Enter 4 to display Total Covid-19 Cases by Country in a BAR diagram")
        print("Enter 5 to display visualisation of Live Total Covid-19 Cases by Country ")
        option = input("Please select a valid option from the list to visualize data: ")

    """
    In a choropleth map, each row of `data_frame` is represented by a
    colored region mark on a map.
    """
    if option == '1':
        vaccine_map = px.choropleth(data2, locations='iso_code', color='total_vaccinations')
        vaccine_map.update_layout(height=500, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        vaccine_map.show()
    if option == '2':
        vaccine_map = px.choropleth(data2, locations='iso_code', color='vaccines')
        vaccine_map.update_layout(height=500, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        vaccine_map.show()
    if option == '3':
        vaccine_map = px.choropleth(data4, title='Total Covid Cases World Wide', locations='iso_code',
                                    hover_name="Country", range_color=(1000, 10000000), color='Total_Cases',
                                    color_continuous_scale='Viridis')
        vaccine_map.update_layout(height=500, title="Total Covid 19 World Wide Cases",
                                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
        vaccine_map.update_layout(title="Total Covid 19 World Wide Cases")
        vaccine_map.show()
    """    
    In a bar plot, each row of `data_frame` is represented as a rectangular mark.
    """
    if option == '4':
        fig = px.bar(data4, title='Total Covid-19 Cases', x='Total_Cases', y='Country', hover_name='Country',
                     color='Country', color_discrete_sequence=px.colors.qualitative.Prism, facet_row_spacing=0.9)
        fig.show()
    if option == '5':
        country = input("Enter a country name to see latest COVID-19 details(eg- spain): ")
        url = "https://covid-19-data.p.rapidapi.com/country"
        querystring = {"name": str(country)}
        headers = {
            'x-rapidapi-key': "431a9d91famsh03249337403e0d5p1ca757jsn20736c1461a3",
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            parse_json = json.loads(response.text)
            """
            "loads" function from json class converts types - (a ``str``, ``bytes`` or ``bytearray`` instance
            containing a JSON document) to a Python object.
            """
            x = [int(parse_json[0]['confirmed'])]
            y = [int(parse_json[0]['deaths'])]
            country_map = px.choropleth(parse_json, locations='country', color='country',
                                    color_discrete_sequence=px.colors.qualitative.Vivid, locationmode="country names",
                                    hover_name='country', hover_data=['confirmed', 'recovered', 'deaths'])
            country_map.update_layout(height=500, title='Total Covid 19 Country Wide Data',
                                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
            country_map.add_bar(x=x, y=y, offset=-10, hovertext='Confirmed Cases/Total Deaths', text='Total Cases')
            country_map.show()
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Please try other options this time around :)")
        


if __name__ == '__main__':
    main()
