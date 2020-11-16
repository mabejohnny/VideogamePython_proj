import collections
import json

import requests

from types import SimpleNamespace

from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint

from datatracker.Models.game import Game

from datatracker.Models.platform import Platform

from datatracker.Models.publisher import Publisher

from datatracker.Models.game_collection import Game_Collection

bp = Blueprint('modules.videogames', __name__)


# @bp.route('/postform)
# def post_search_by_game_title():

@bp.route('/gamedetails', methods=('GET', 'POST'))
def gamedetails():
    game_title = "Grand Theft Auto V"
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=Game.game_decoder)
    legend = 'Sales by Platform'
    game_list = []

    for game in games:
        if game.name == game_title:
            game_list.append(game)

    return render_template('gamedetails.html', game_list=game_list, game_title=game_title, legend=legend)


@bp.route('/games', methods=('GET', 'POST'))
def games():
    response = requests.get('https://api.dccresource.com/api/games')
    allgames = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    unique_games = []

    for game in allgames:
        if game.name not in unique_games:
            unique_games.append(game.name)

    return render_template('games.html', allgames=allgames, unique_games=unique_games)

@bp.route('/', methods=('GET', 'POST'))
def index():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    unique_games = []
    search_results = []

    if request.method == 'POST':
        page_title = request.form['title']
        error = None

        if not page_title:
            error = 'You must enter a title'

        for game in games:
            if game.name not in unique_games:
                unique_games.append(game.name)

        for game in unique_games:
            if request.form['title'] in game:
                search_results.append(game)

        return render_template('searchresults.html', games=games, search_results=search_results, unique_games=unique_games)


    return render_template('index.html', games=games, search_results=search_results)

@bp.route('/home', methods=['GET'])
def platform():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=Game.game_decoder)
    platform_names = []
    platforms = []

    #Creates a list of all platforms
    for game in games:
        if game.platform in platform_names:
            continue
        else:
            platform_names.append(game.platform)

    #Creates a Collection of Platform Objects
    for platform in platform_names:
        new_system = Platform.platform_decoder(platform)
        platforms.append(new_system)

    for platform in platforms:
        for game in games:
            if game.platform == platform.name:
                platform.games.append(game)

    return render_template('platform.html', games=games)

@bp.route('/sales', methods=['GET'])
def sales():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=Game.game_decoder)
    recent_games = []
    platforms = []
    recent_platforms = []
    collection_of_platforms = []
    publishers = []
    null_year = []
    collection_of_publishers = []
 
    #Creates a list of Games released since 2013   - recent_games
    for game in games:
        if game.year is not None and game.year >= 2013:
            recent_games.append(game)

    #List of Recent Unique Platforms since 2013  - recent_platforms
    for game in recent_games:
        if game.platform in recent_platforms:
            continue
        else:
            recent_platforms.append(game.platform)

    #Creates a list of all platforms
    for game in games:
        if game.platform in platforms:
            continue
        else:
            platforms.append(game.platform)


    #Creates a Collection of Platform Objects
    for system in platforms:
        new_system = Platform.platform_decoder(system)
        collection_of_platforms.append(new_system)

    #Adds up sales since 2013 for each Platform
    for platform in collection_of_platforms:
        for game in recent_games:
            if game.platform == platform.name:
                platform.sales += game.globalSales

    #Creates a list of games without a release year
    for game in games:
        if game.year is None:
            null_year.append(game)

    #Create a list of Unique Publishers
    for game in games:
        if game.publisher in publishers:
            continue
        else:
            publishers.append(game.publisher)

    #Creates a collection of Publisher Objects
    for publisher in publishers:
        publisher = Publisher.publisher_decoder(publisher)
        collection_of_publishers.append(publisher)

    #Populates the games list for each publisher in collection_of_publishers
    for publisher in collection_of_publishers:
        for game in games:
            if game.publisher == publisher.name:
                publisher.games.append(game)

    for publisher in collection_of_publishers:
        for game in publisher.games:
            for platform in publisher.platforms:
                if game.platform == platform.name:
                    continue
                else:
                    publisher.platforms.append(Platform.platform_decoder(game.platform))

    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]

    return render_template('sales.html', legend=legend, labels=labels, values=values, games=games, results=recent_games, platforms=platforms, collection_of_platforms=collection_of_platforms, null_year=null_year, publishers=publishers, collection_of_publishers=collection_of_publishers)

@bp.route('/publishers', methods=['GET'])
def publishers():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=Game.game_decoder)
    publishers = []
    platforms = []
    collection_of_platforms = []
    collection_of_publishers = []

    #Creates a list of all platforms
    for game in games:
        if game.platform in platforms:
            continue
        else:
            platforms.append(game.platform)


    #Creates a Collection of Platform Objects
    for system in platforms:
        new_system = Platform.platform_decoder(system)
        collection_of_platforms.append(new_system)


    #Create a list of Unique Publishers
    for game in games:
        if game.publisher in publishers:
            continue
        else:
            publishers.append(game.publisher)

    #Creates a collection of Publisher Objects
    for publisher in publishers:
        publisher = Publisher.publisher_decoder(publisher)
        collection_of_publishers.append(publisher)

    #Populates the games list for each publisher in collection_of_publishers
    for publisher in collection_of_publishers:
        for game in games:
            if game.publisher == publisher.name:
                publisher.games.append(game)
                platforms = []
                if game.platform in platforms:
                    continue
                else:
                    platforms.append(game.platform)
            for platform in platforms:
                publisher.platforms.append(Platform.platform_decoder(platform))

    for publisher in collection_of_publishers:
        for game in publisher.games:
            for platform in publisher.platforms:
                if game.publisher == publisher.name and game.platform == platform.name:
                    platform.sales += game.globalSales


    return render_template('publishers.html', games=games, collection_of_publishers=collection_of_publishers)