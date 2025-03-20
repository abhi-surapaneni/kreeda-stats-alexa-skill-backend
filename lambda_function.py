# -*- coding: utf-8 -*-
"""Kreeda Stats gives you NFL Stats at this time"""

import logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractExceptionHandler, AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from handlers import (
    LaunchkreedaIntentHandler, NflGetTopRusherIntentHandler, NflGetTopRusherTdIntentHandler,
    NflGetTopPasserIntentHandler, NflGetTopPasserTdIntentHandler, NflGetTopReceiverIntentHandler,
    NflGetTopReceiverTdIntentHandler, HelpIntentHandler, CancelOrStopIntentHandler,
    FallbackIntentHandler, SessionEndedRequestHandler, CatchAllExceptionHandler,
    RequestLogger, ResponseLogger)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Skill Builder object to register the handlers
sb = SkillBuilder()

# Register intent handlers
sb.add_request_handler(LaunchkreedaIntentHandler())
sb.add_request_handler(NflGetTopRusherIntentHandler())
sb.add_request_handler(NflGetTopRusherTdIntentHandler())
sb.add_request_handler(NflGetTopPasserIntentHandler())
sb.add_request_handler(NflGetTopPasserTdIntentHandler())
sb.add_request_handler(NflGetTopReceiverIntentHandler())
sb.add_request_handler(NflGetTopReceiverTdIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Register request and response loggers
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()