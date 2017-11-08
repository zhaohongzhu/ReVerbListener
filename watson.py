from stt_watson.SttWatson import SttWatson
from stt_watson.SttWatsonAbstractListener import SttWatsonAbstractListener
import conf
import json
import requests
import storage
import conf
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.watson_developer_cloud_service import WatsonException
import watson_developer_cloud.natural_language_understanding.features.v1 as Features
from pythonosc import osc_message_builder
from pythonosc import udp_client

"""
Example of listener to use data given by stt-watson (stt-watson notify hypothesis to his listeners when he receive it)

Hypothesis format:
{
    'confidence': '0.1' // confidence of the sentence or words if exist
    'transcript': 'the transcription of your voice'
}
"""
class MyListener(SttWatsonAbstractListener):
    def __init__(self):
        pass
    """
    This give hypothesis from watson when your sentence is finished
    """
    def listenHypothesis(self, hypothesis):
        # print "Hypothesis: {0}".format(hypothesis)
        final_result(hypothesis)
        pass

    """
    This give the json received from watson
    """
    def listenPayload(self, payload):
        # print(u"Text message received: {0}".format(payload))
        pass

    """
    This give hypothesis from watson when your sentence is not finished
    """
    def listenInterimHypothesis(self, interimHypothesis):
        # print "Interim hypothesis: {0}".format(interimHypothesis)
        pass

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username=conf.WATSON_NLP_USER,
  password=conf.WATSON_NLP_PASS,
  version="2017-02-27")

sentences = []
verbs = []
client = []

def __init__():
    global output_file
    output_file = open('story.txt', 'w')
    pass


def set_osc_client(_client):
    global client
    client = _client

def start_listening(threading = False):
    global sentences
    global sttWatson
    sentences = []
    myListener = MyListener()
    sttWatson = SttWatson(conf.WATSON_STT_USER, conf.WATSON_STT_PASS)
    sttWatson.addListener(myListener)
    #sttWatson.run()
    sttWatson.start()

def pause_listening():
    sttWatson.pauseRecord()

def resume_listening():
    sttWatson.continuRecord()

def final_result(result):
    struct_result = result
    if (len(struct_result) >= 0):
        sentence_id = len(sentences)
        #print sentences[-1]
        # print(json.dumps(struct_result, indent=2))
        transcript = struct_result[0]['transcript']
        timestamps = struct_result[0]['timestamps']
        # print(transcript)
        # client.send_message('/sentence', [sentence_id, transcript])
        sentences.append(transcript)
        response = []
        try:
            response = natural_language_understanding.analyze(
                text=transcript,
                features=[
                    Features.Keywords(
                        # Keywords options
                        sentiment=True,
                        emotion=True,
                        limit=10
                    ),
                    Features.SemanticRoles(
                        # Semantic Roles options
                    )
                ]
            )
            # verbs = [v['action']['text'] for v in response['semantic_roles']]
            keywords = [v['text'] for v in response['keywords']]
            print(transcript)
            # print(keywords)
            v_ts_result = extract_verb(transcript, verbs, timestamps)
            k_ts_result = extract_keywords(transcript, keywords, timestamps)
            response = []
            response.append(sentence_id)
            response.append(transcript)
            response.append(len(k_ts_result))
            for t in k_ts_result:
                response += t
            print(response)
            # output_file.write(response)
            client.send_message('/sentence_info', response)

        except WatsonException:
            print("Watson Error")
            pass

        except IndexError:
            print("Hesitation appeared. TODO")
            pass

        pass


def get_timestamp(verb, timestamps):
    for t in timestamps:
        if (t[0] == verb):
            return [verb, float(t[1]), float(t[2])]
    return [verb, -1.0, -1.0]


def extract_verb(sentence, verbs, timestamps):
    # print(json.dumps(timestamps, indent=2))
    ts = [get_timestamp(v, timestamps) for v in verbs]
    return ts


def extract_keywords(sentence, keywords, timestamps):
    # print(json.dumps(timestamps, indent=2))
    ts = [match_string(sentence, k, timestamps) for k in keywords]
    return ts


def match_string(sentence, keyword, timestamps):
    keyword_len = len(keyword.split())
    start_point = sentence.find(keyword)
    if (start_point == -1):
        return [keyword, -1.0, -1.0]
    start_place = len(sentence[:start_point].split())
    return [keyword, timestamps[start_place][1], timestamps[start_place + keyword_len - 1][2]]

