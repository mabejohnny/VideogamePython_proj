import collections
import json
from random import random

import requests

from types import SimpleNamespace

from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint

from datatracker.Models.game import Game

from datatracker.Models.platform import Platform

from datatracker.Models.publisher import Publisher


bp = Blueprint('modules.videogames', __name__)


# @bp.route('/postform)
# def post_search_by_game_title():

@bp.route('/gamedetails', methods=('GET', 'POST'))
def gamedetails():
    if request.method == 'POST':
        game_title = request.form['details_button']
        error = None

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
    allgames = json.loads(response.content, object_hook=Game.game_decoder)
    unique_games = []

    def getKey(game):
        return game.rank

    sorted_games = sorted(allgames, key=getKey)

    for game in allgames:
        if game.name not in unique_games:
            unique_games.append(game)

    return render_template('games.html', allgames=allgames, unique_games=sorted_games)

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
    colors = []

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

    for platform in platforms:
        for game in platform.games:
            if game.year is not None and game.year <= 1989:
                platform.sales85_89 += game.globalSales
                platform.totalSales += game.globalSales
            elif game.year is not None and game.year > 1989 and game.year <= 1994:
                platform.sales90_94 += game.globalSales
                platform.totalSales += game.globalSales
            elif game.year is not None and game.year > 1994 and game.year <= 1999:
                platform.sales95_99 += game.globalSales
                platform.totalSales += game.globalSales
            elif game.year is not None and game.year > 1999 and game.year <= 2004:
                platform.sales00_04 += game.globalSales
                platform.totalSales += game.globalSales
            elif game.year is not None and game.year > 2004 and game.year <= 2009:
                platform.sales05_09 += game.globalSales
                platform.totalSales += game.globalSales
            elif game.year is not None and game.year > 2009 and game.year <= 2014:
                platform.sales10_14 += game.globalSales
                platform.totalSales += game.globalSales
            elif game.year is not None and game.year > 2014 and game.year <= 2019:
                platform.sales15_19 += game.globalSales
                platform.totalSales += game.globalSales
            elif game.year is None:
                platform.totalSales += game.globalSales

    return render_template('platforms.html', platforms=platforms, colors=colors)

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
                platform.totalSales += game.globalSales

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
    collection_of_publishers = []

    #Create a list of Unique Publishers
    for game in games:
        if game.publisher in publishers:
            continue
        else:
            publishers.append(game.publisher)

    #Creates a list of all platforms
    for game in games:
        if game.platform in platforms:
            continue
        else:
            platforms.append(game.platform)

    #Creates a collection of Publisher Objects
    for publisher in publishers:
        publisher = Publisher.publisher_decoder(publisher)
        collection_of_publishers.append(publisher)

    for publisher in collection_of_publishers:
        for platform in platforms:
            platform = Platform.platform_decoder(platform)
            publisher.platforms.append(platform)

    for publisher in collection_of_publishers:
        for platform in publisher.platforms:
            for game in games:
                if game.platform == platform.name and game.publisher == publisher.name:
                    platform.totalSales += game.globalSales

    return render_template('publishers.html', collection_of_publishers=collection_of_publishers)

@bp.route('/bonus', methods=['GET'])
def bonus():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=Game.game_decoder)
    publishers = []
    platforms = []
    collection_of_platforms = []

    #Create a list of Unique Publishers
    for game in games:
        if game.publisher in publishers:
            continue
        else:
            publishers.append(game.publisher)

    #Creates a list of all platforms
    for game in games:
        if game.platform in platforms:
            continue
        else:
            platforms.append(game.platform)

    #Creates a collection of Platform Objects
    for platform in platforms:
        platform = Platform.platform_decoder(platform)
        collection_of_platforms.append(platform)

    for platform in collection_of_platforms:
        for game in games:
            if game.platform == platform.name:
                platform.games.append(game)

    for platform in collection_of_platforms:
        for publisher in publishers:
            for game in platform.games:
                if game.publisher == publisher:
                    new = Publisher.publisher_decoder(game.publisher)
                    platform.publishers.append(new)

    for platform in collection_of_platforms:
        for game in platform.games:
            for publisher in platform.publishers:
                if game.publisher == publisher.name:
                    publisher.sales += game.globalSales

    return render_template('bonus.html', collection_of_platforms=collection_of_platforms)