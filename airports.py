import json
from datetime import datetime

import requests
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt
from rich.table import Table
from rich.theme import Theme

console = Console(record=True)

def get_search() -> str:
    """Prompts the user to enter an airport to search

    Returns:
        str: user's chosen airport
    """
    return Prompt.ask("Search for an an airport")

def load_airport_json() -> dict:
    """Opens airport.json file and loads it, to access airport data

    Returns:
        list: List of dictionaries containing airports and information
    """
    f = open('airports.json')

    airportData = json.load(f)
    
    return airportData

def verify_user_airport_choice(possible_matches:list) -> dict:
    """Takes a list of airports, and prompts user to select one from the list, returns one selection

    Args:
        possible_matches (list): List of airport dictionaries

    Returns:
        dict: Airport dictionary 
    """
    airport_choices = [airports['name'] for airports in possible_matches]

    match = None

    user_choice = Prompt.ask("Please select one out of: " + str(airport_choices) + '\n')

    while match == None:
        user_choice = Prompt.ask("Invalid option, please select one of: " + str(airport_choices) + '\n')
        
        for i, airports in enumerate(airport_choices):
            if user_choice.lower() == airports.lower():
                match = possible_matches[i]
                console.print(f'You have selected: {(match["name"])}', style = 'green')
    
    return match           
            

def find_matching_airports_name(name: str, airport_data: list) -> dict:
    """Takes a name, and searches the name key in airport data, returns a single match

    Args:
        name (str): Airport name user entered
        airport_data (list): List containing airport dictionaries

    Returns:
        dict: Airport dictionary
    """
    possible_matches = [airport for airport in airport_data \
                        if name.lower() in airport['name'].lower()]
    
    if len(possible_matches) == 0:
        console.print('Not a valid airport, please try again', style='bold red')
    elif len(possible_matches) == 1:
        console.print(possible_matches[0]['name'], style ='green')
        return possible_matches[0]
    else:
        return verify_user_airport_choice(possible_matches)

def find_matching_airports_iata(iata: str, airport_data: list) -> dict:
    """Takes an Iata, and searches the Iata key in the airport data, returns a single match

    Args:
        iata (str): _description_
        airport_data (list): _description_

    Returns:
        dict: _description_
    """
    for airport in airport_data:
        if iata.upper() == str(airport['iata']).upper():
            return airport
    
    return None


if __name__ == "__main__":
    console.print(" ")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print("Welcome to the Airports Informer Tool")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print(" ")

    airport_data = load_airport_json()

    while 1:
        airport_search=get_search()
        users_selection=find_matching_airports_name(airport_search, airport_data)

