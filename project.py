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
    print('Welcome to Covid 19 Data and Vaccination Visualization Project')
    data2 = pd.read_csv('sortedbytotalvaccines.csv')
    # data4 = pd.read_csv('worldcovidcases.csv')
    dataframe = data2[["vaccines", "country"]]
    # fetch the latest data from worldcovidcases api,
    url = "https://covid-19-tracking.p.rapidapi.com/v1"
    headers = {
        'x-rapidapi-key': "431a9d91famsh03249337403e0d5p1ca757jsn20736c1461a3",
        'x-rapidapi-host': "covid-19-tracking.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url, headers=headers)
        print(response.text)
        # parse_json = json.loads(response.text)
        df = pd.read_json(response.text, dtype={"Country_text": str})
        # remove front and ending blank spaces
        df = df.replace({"^\s*|\s*$": ""}, regex=True)
        # if there remained only empty string "", change to 0
        df = df.replace({"N/A": "0", "nan": "0"})
        df["Active Cases_text"] = pd.to_numeric(df["Active Cases_text"].str.replace(',', ''))
        df["New Cases_text"] = pd.to_numeric((df["New Cases_text"]).str.replace(',', ''))
        # df["New Deaths_text"] = pd.to_numeric((df["New Deaths_text"]).str.replace('', ''))
        df["Total Cases_text"] = pd.to_numeric(df["Total Cases_text"].str.replace(',', ''))
        df["Total Deaths_text"] = pd.to_numeric((df["Total Deaths_text"]).str.replace(',', ''))
        df["Total Recovered_text"] = pd.to_numeric((df["Total Recovered_text"]).str.replace(',', ''))
        df1 = df.rename(
            columns={'Country_text': 'Country', 'Total Cases_text': 'Total Cases', 'Total Deaths_text': 'Total Deaths',
                     'Total Recovered_text': 'Total Recovered', 'Active Cases_text': 'Active Cases'}, inplace=False)
        print(df1.head())
        df = df1.iloc[1:223, :]
        # delete world cases row and last row
    except Exception as inst:
        print("Oops!", sys.exc_info()[0], "occurred.", inst)
        print("Please try other options this time around :)")
    dict_ = {}
    for vaccine in dataframe.vaccines.unique():
        dict_[vaccine] = [dataframe["country"][j] for j in dataframe[dataframe["vaccines"] == vaccine].index]
    vaccines = {}
    for key, value in dict_.items():
        vaccines[key] = set(value)

    print("Enter 1 to display Total Vaccinations by Country")
    print("Enter 2 to display Vaccination Manufacturers used by Country")
    print("Enter 3 to display latest visualization of Total Covid-19 Cases Worldwide ")
    print("Enter 4 to display Total Covid-19 Cases by Country in a scatter polar diagram")
    print("Enter 5 to display visualization of Live Total Covid-19 Cases by Country ")

    option = input("Please select from the available options to visualize data: ")
    while option not in ['1', '2', '3', '4', '5']:
        print("Enter 1 to display Total Vaccinations by Country")
        print("Enter 2 to display Vaccination Manufacturers used by Country")
        print("Enter 3 to display latest visualization of Total Covid-19 Cases Worldwide ")
        print("Enter 4 to display Total Covid-19 Cases by Country in a scatter polar diagram")
        print("Enter 5 to display visualization of Live Total Covid-19 Cases by Country ")
        option = input("Please select a valid option from the list to visualize data: ")

    """
    In a choropleth map, each row of `data_frame` is represented by a
    colored region mark on a map.
    """
    if option == '1':
        vaccine_map = px.choropleth(data2, range_color=(10000, 80000000), hover_name='country', locations='iso_code',
                                    color='total_vaccinations', color_discrete_sequence=px.colors.qualitative.Prism,
                                    hover_data=['total_vaccinations', 'people_vaccinated', 'vaccines'])
        vaccine_map.update_layout(title='Total Vaccinations by Country', height=500,
                                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
        vaccine_map.show()
    if option == '2':
        vaccine_map = px.choropleth(data2, locations='iso_code', color='vaccines',
                                    color_discrete_sequence=px.colors.qualitative.Antique, hover_name='country',
                                    hover_data=['total_vaccinations', 'people_vaccinated', 'vaccines'])
        vaccine_map.update_layout(height=500, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        vaccine_map.show()
    if option == '3':
        country_map = px.choropleth(df, locations='Country', color='Total Cases', range_color=(1000, 10000000),
                                    color_discrete_sequence=px.colors.qualitative.Vivid,
                                    locationmode="country names",
                                    hover_name='Country',
                                    hover_data=['Total Cases', 'Total Recovered', 'Active Cases',
                                                'Total Deaths'], color_continuous_scale='Viridis')
        country_map.update_layout(height=500, title='Total Covid 19 Country Wide Data',
                                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
        country_map.show()
    if option == '4':
        """
        In a polar scatter plot, each row of `data_frame` is represented by a
        symbol mark in polar coordinates.
        """
        fig = px.scatter_polar(df, r="Total Cases", theta='Total Deaths', size='Total Cases', hover_name='Country',
                               hover_data=['Total Cases', 'Total Deaths'], color='Total Cases',
                               range_color=(10000, 8000000),
                               color_discrete_sequence=px.colors.qualitative.Prism, direction="clockwise",
                               start_angle=360)
        fig.show()
    if option == '5':
        try:
            country = input("Enter a country name to see latest COVID-19 details(eg- spain): ")
            url = "https://covid-19-data.p.rapidapi.com/country"
            querystring = {"name": str(country)}
            headers = {
                'x-rapidapi-key': "431a9d91famsh03249337403e0d5p1ca757jsn20736c1461a3",
                'x-rapidapi-host': "covid-19-data.p.rapidapi.com"}
            response = requests.request("GET", url, headers=headers, params=querystring)
            parse_json = json.loads(response.text)
            """
            "loads" function from json class converts types - (a ``str``, ``bytes`` or ``bytearray`` instance
            containing a JSON document) to a Python object.
            """
            x = [int(parse_json[0]['confirmed'])]
            y = [int(parse_json[0]['deaths'])]
            country_map = px.choropleth(parse_json, locations='country', color='country',
                                        color_discrete_sequence=px.colors.qualitative.Vivid,
                                        locationmode="country names",
                                        hover_name='country', hover_data=['confirmed', 'recovered', 'deaths'])
            country_map.update_layout(height=500, title='Total Covid 19 Country Wide Data',
                                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
            country_map.add_bar(x=x, y=y, offset=-10, hovertext='Confirmed Cases/Total Deaths', text='Total Cases')
            country_map.show()
        except Exception as inst:
            print("Oops!", sys.exc_info()[0], "occurred.", inst)
            print("Please try other options this time around :)")


if __name__ == '__main__':
    main()
