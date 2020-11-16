import collections
import json

import requests

from types import SimpleNamespace

from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint

from datatracker.Models.game import Game

from datatracker.Models.platform import Platform

from datatracker.Models.publisher import Publisher

bp = Blueprint('modules.videogames', __name__)


# @bp.route('/postform)
# def post_search_by_game_title():


@bp.route('/home', methods=['GET'])
def index():
    response = requests.get('https://api.dccresource.com/api/games')
    games_dict = json.loads(response)
    games = Game.game_decoder(games_dict)
    #games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    return render_template('index.html', games=games)

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