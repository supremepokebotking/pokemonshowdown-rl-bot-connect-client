import numpy as np
import math
import os

from showdown_mine.server import *  # noqa: F401

print(get_host("showdown"))
print(generate_ws_url(get_host("showdown")))
print(generate_action_url(get_host("showdown")))
#quit()
#https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from math import inf
from client import *
from local_model import *


def get_model():
    action_space = 14
    model = Model(num_actions=action_space)

    prediction = model(SAMPLE_OBS[None, :])
    print('prediction', prediction)
    model.load_weights('./showdown_a2c_weights_4b07b6d7-19a2-4534-b9b1-ab53d0c89957.h5')

    return model

model_to_use = get_model()

#sim3.psim.us:8000
#ws://sim3.psim.us:8000/showdown/906/rfwopjis/websocket
#https://play.pokemonshowdown.com/~~sim3.psim.us:8000/action.php
#http://raw-showdown-test.herokuapp.com-80.psim.us
#ws://raw-showdown-test.herokuapp.com-80.psim.us:8000/showdown/906/rfwopjis/websocket

def handle_exception(loop, context):
    print('csadasasassa')
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
#    logging.error(f"Caught exception: {msg}")
#    logging.info("Shutting down...")
    print('crashing')
    asyncio.create_task(shutdown(loop))

@asyncio.coroutine
def handle_exception():
    try:
        yield from on_receive()
    except Exception:
        print("exception consumed")
        asyncio.create_task(shutdown(loop, signal=s))

username, password = 'username', 'password'

def main():

    queue = asyncio.Queue()

    client = ChallengeClient(queue, name=username, password=password)
    client.model = model_to_use

    # schedule the consumer
    consumer = asyncio.ensure_future(client.consume_system_message(queue))

    client.reset()
    client.start()
    # May want to catch other signals too
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    loop = asyncio.get_event_loop()
    #loop.create_task(client.on_receive())
    asyncio.ensure_future(handle_exception())
    #loop.add_signal_handler(
    #    s, lambda s=s: asyncio.create_task(shutdown(loop, signal=s)))
    #loop.set_exception_handler(handle_exception)
    loop.run_forever()

main()
