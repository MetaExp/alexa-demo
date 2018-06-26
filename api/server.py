from flask import Flask, jsonify, request, abort, session
from flask_session import Session
from flask_cors import CORS
import json
import os
import time
import datetime
from flask_ask import Ask, statement
import logging
from typing import Dict

import embeddings.meta2vec
from util.config import *
from active_learning.active_learner import UncertaintySamplingAlgorithm
from explanation.explanation import SimilarityScore, Explanation
from api.redis_own import Redis
from util.metapaths_database_importer import RedisImporter


app = Flask(__name__)
ask = Ask(app, '/alexa')
set_up_logger()
logger = logging.getLogger('MetaExp.Server')

CORS(app, supports_credentials=True, resources={r"/*": {
    "origins": ["https://hpi.de/mueller/metaexp-demo-api/", "http://172.20.14.22:3000", "http://localhost",
                "http://localhost:3000", "http://metaexp.herokuapp.com"]}})


def run(port, hostname, debug_mode):
    app.run(host=hostname, port=port, debug=debug_mode, threaded=True)

@ask.launch
def start():
    speech_text = "Willkommen bei MetaExp. Einer interaktiven Graphexplorationssoftware. Bitte sage deine erste Auswahl"
    return statement(speech_text).simple_card("Greeting", speech_text)

# Self defined intents
@ask.intent('MovieSearch')
def choose_dataset(film, actor):
    speech_text = "Du hast {} und {} gesagt?".format(film, actor)
    return statement(speech_text).simple_card('MovieSearch', speech_text)

@ask.intent('SearchProducer')
def rate_metapath():
    raise NotImplementedError()


@ask.intent('ExcludeEdgeType')
def exclude_edge_type():
    raise NotImplementedError()


@ask.intent('ExcludeNodeType')
def exclude_node_type():
    raise NotImplementedError()


@ask.intent('ShowMoreMetapaths')
def show_more_metapaths():
    raise NotImplementedError()


@ask.intent('ShowResults')
def show_results():
    raise NotImplementedError()


# Built-in intents
@ask.intent('AMAZON.CancelIntent')
def cancel():
    raise NotImplementedError()


@ask.intent('AMAZON.HelpIntent')
def help():
    raise NotImplementedError()


@ask.intent('AMAZON.StopIntent')
def stop():
    raise NotImplementedError()


@ask.intent('AMAZON.MoreIntent')
def more():
    raise NotImplementedError()


@ask.intent('AMAZON.NavigateHomeIntent')
def navigate_home():
    raise NotImplementedError()


@ask.intent('AMAZON.NavigateSettingsIntent')
def navigate_settings():
    raise NotImplementedError()


@ask.intent('AMAZON.NextIntent')
def next():
    raise NotImplementedError()


@ask.intent('AMAZON.PageUpIntent')
def page_up():
    raise NotImplementedError()


@ask.intent('AMAZON.PageDownIntent')
def page_down():
    raise NotImplementedError()


@ask.intent('AMAZON.PreviousIntent')
def previous():
    raise NotImplementedError()


@ask.intent('AMAZON.ScrollRighIntent')
def scroll_right():
    raise NotImplementedError()


@ask.intent('AMAZON.ScrollDownIntent')
def scroll_down():
    raise NotImplementedError()


@ask.intent('AMAZON.ScrollLeftIntent')
def scroll_left():
    raise NotImplementedError()


@ask.intent('AMAZON.ScrollUpIntent')
def scroll_up():
    raise NotImplementedError()


if __name__ == '__main__':
    app.run(port=API_PORT, threaded=True, debug=True)
