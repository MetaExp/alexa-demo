from flask import Flask, jsonify, request, abort, session
from flask_session import Session
from flask_cors import CORS
import json
import os
import time
import datetime
from flask_ask import Ask, statement, question, session, delegate, elicit_slot
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
    speech_text = "Aspirin wirkt außerdem noch fiebersenkend, infarktvorbeugend und antirheumatisch"
    return question(speech_text).simple_card("Greeting", speech_text)


@ask.intent("ProblemDescription")
def problem_description():
    return question("Erzählt mir von euren verschiedenen Vorlieben.")


@ask.intent("PreferenceDialog")
def preference_dialog(firstPreference, secondPreference):
    dialog_state = get_dialog_state()
    if dialog_state == "STARTED":
        return delegate()
    return statement("Okay, lasst mich euer Problem lösen. Ich bin ein super Streitschlichter."
                    "Glücklicherweise habe ich gerade in meinem Knowledge Graph einen Film gefunden der eure beiden"
                     "Vorlieben {} und {} zufriedenstellt. Der Film heißt Top Gun!" .format(firstPreference, secondPreference))


def get_dialog_state():
    return session['dialogState']


# Self defined intents
@ask.intent('MovieSearch')
def choose_dataset(film, actor):
    speech_text = "Du hast {} und {} gesagt?".format(film, actor)
    return statement(speech_text).simple_card('MovieSearch', speech_text)
