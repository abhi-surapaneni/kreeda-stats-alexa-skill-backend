import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_model.ui import SimpleCard
from nfl_stats import nfl_stats
from constants import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class BaseNflIntentHandler(AbstractRequestHandler):
    def handle(self, handler_input, stat_type, response_sentence_begin, card_title):
        year = handler_input.request_envelope.request.intent.slots["year"].value
        week = handler_input.request_envelope.request.intent.slots["week"].value
        speech, card_title, card_text = nfl_stats.nfl_get_stat(year, week, stat_type, TOP_N)
        handler_input.response_builder.speak(speech).set_card(SimpleCard(card_title, card_text)).ask(ASK_MESSAGE)
        return handler_input.response_builder.response

class LaunchkreedaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input) or is_intent_name("LaunchkreedaIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In LaunchRequestHandler")
        speech = WELCOME_MESSAGE
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class NflGetTopRusherIntentHandler(BaseNflIntentHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NflGetTopRusherIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In NflGetTopRusherIntent")
        return super().handle(handler_input, 'rushing_yards', RB_RESP_SENTENCE_BEGIN, RB_CARD_TITLE)

class NflGetTopRusherTdIntentHandler(BaseNflIntentHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NflGetTopRusherTdIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In NflGetTopRusherTdIntent")
        return super().handle(handler_input, 'rushing_tds', RB_RESP_SENTENCE_BEGIN, RB_CARD_TITLE)

class NflGetTopPasserIntentHandler(BaseNflIntentHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NflGetTopPasserIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In NflGetTopPasserIntent")
        return super().handle(handler_input, 'passing_yards', QB_RESP_SENTENCE_BEGIN, QB_CARD_TITLE)

class NflGetTopPasserTdIntentHandler(BaseNflIntentHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NflGetTopPasserTdIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In NflGetTopPasserTdIntent")
        return super().handle(handler_input, 'passing_tds', QB_RESP_SENTENCE_BEGIN, QB_CARD_TITLE)

class NflGetTopReceiverIntentHandler(BaseNflIntentHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NflGetTopReceiverIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In NflGetTopReceiverIntent")
        return super().handle(handler_input, 'receiving_yards', WR_RESP_SENTENCE_BEGIN, WR_CARD_TITLE)

class NflGetTopReceiverTdIntentHandler(BaseNflIntentHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NflGetTopReceiverTdIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In NflGetTopReceiverTdIntent")
        return super().handle(handler_input, 'receiving_tds', WR_RESP_SENTENCE_BEGIN, WR_CARD_TITLE)

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In HelpIntentHandler")
        handler_input.response_builder.speak(HELP_MESSAGE).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In CancelOrStopIntentHandler")
        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(FALLBACK_REPROMPT)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)
        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(HELP_REPROMPT)
        return handler_input.response_builder.response

class RequestLogger(AbstractRequestInterceptor):
    def process(self, handler_input):
        logger.debug("Alexa Request: {}".format(handler_input.request_envelope.request))

class ResponseLogger(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        logger.debug("Alexa Response: {}".format(response))