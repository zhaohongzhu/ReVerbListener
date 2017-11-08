#
# Copyright IBM Corp. 2014
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Author: Daniel Bolanos
# Date:   2015

import base64  # necessary to encode in base64 according to the RFC2045 standard
# coding=utf-8
import sys  # system calls

# WebSockets
from autobahn.twisted.websocket import connectWS
from stt_watson.config.Config import Config
from stt_watson.utils.Utils import Utils
from stt_watson.watson_client.websocket.WSInterfaceProtocol import WSInterfaceProtocol
from twisted.internet import ssl, reactor
from twisted.python import log
from .websocket.WSInterfaceFactory import WSInterfaceFactory


class Client:
    CONTENT_TYPE = 'audio/l16;rate=16000'

    def __init__(self):
        self.listeners = []
        self.configData = Config.Instance().getWatsonConfig()

    def setListeners(self, listeners):
        self.listeners = listeners

    def getListeners(self):
        return self.listeners

    def startStt(self, audioFd):

        # logging
        log.startLogging(sys.stdout)

        hostname = "stream.watsonplatform.net"
        headers = {}

        # authentication header
        if self.configData["tokenauth"]:
            headers['X-Watson-Authorization-Token'] = Utils.getAuthenticationToken("https://" + hostname,
                                                                                   'speech-to-text',
                                                                                   self.configData["user"],
                                                                                   self.configData["password"])
        else:
            string = self.configData["user"] + ":" + self.configData["password"]
            headers["Authorization"] = "Basic " + base64.b64encode(bytes(string, 'utf_8')).decode('utf_8')

        # create a WS server factory with our protocol
        url = "wss://" + hostname + "/speech-to-text/api/v1/recognize?model=" + self.configData["model"]
        summary = {}
        factory = WSInterfaceFactory(audioFd,
                                     summary,
                                     self.CONTENT_TYPE,
                                     self.configData["model"],
                                     url,
                                     headers,
                                     debug=False)
        factory.setListeners(self.listeners)
        factory.protocol = WSInterfaceProtocol

        if factory.isSecure:
            contextFactory = ssl.ClientContextFactory()
        else:
            contextFactory = None
        connectWS(factory, contextFactory)

        reactor.run(installSignalHandlers=0)
        #reactor.run()
