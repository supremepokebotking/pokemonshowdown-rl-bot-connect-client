#https://github.com/ckw017/showdown.py
#import showdown as showdown
import showdown_mine as showdown
import logging
import asyncio
from pprint import pprint
import enum
import random
import numpy
import uuid
import json
import time

logging.basicConfig(level=logging.INFO)
"""
with open('./examples/data/login.txt', 'rt') as f,\
     open('./examples/data/mono-ghost.txt', 'rt') as team:
    ghost_team = team.read()
    username, password = f.read().strip().splitlines()
"""
player_str = 'p2'

bot_name = 'showdown_chat_bot'
user_id = 'showdown_chat_bot'

class Action(enum.Enum):
  Attack_Slot_1 = 0
  Attack_Slot_2 = 1
  Attack_Slot_3 = 2
  Attack_Slot_4 = 3
  Attack_Dyna_Slot_1 = 10
  Attack_Dyna_Slot_2 = 11
  Attack_Dyna_Slot_3 = 12
  Attack_Dyna_Slot_4 = 13
  Change_Slot_1 = 4
  Change_Slot_2 = 5
  Change_Slot_3 = 6
  Change_Slot_4 = 7
  Change_Slot_5 = 8
  Change_Slot_6 = 9
  Attack_Struggle = 14
  Not_Decided = 15          # position hasn't been decided yet

def get_sample_action(action=None):
  mega_dyna = 'dynamax'
  action = action
  if action == None:
    actions = len(Action)
    action = random.randint(0,actions-1)
  action = Action(action)
  # lazy avoid shifts
  if(action == Action.Attack_Struggle):
      print('Struggle Selected')
  action_text = 'move 1'
  if action == Action.Attack_Slot_1 or action == Action.Attack_Struggle:
    action_text = 'move 1'
  if action == Action.Attack_Slot_2:
    action_text = 'move 2'
  if action == Action.Attack_Slot_3:
    action_text = 'move 3'
  if action == Action.Attack_Slot_4:
    action_text = 'move 4'
  if action == Action.Attack_Dyna_Slot_1:
    action_text = 'move 1 %s' % (mega_dyna,)
  if action == Action.Attack_Dyna_Slot_2:
    action_text = 'move 2 %s' % (mega_dyna,)
  if action == Action.Attack_Dyna_Slot_3:
    action_text = 'move 3 %s' % (mega_dyna,)
  if action == Action.Attack_Dyna_Slot_4:
    action_text = 'move 4 %s' % (mega_dyna,)

  if action == Action.Change_Slot_1:
    action_text = 'switch 1'
  if action == Action.Change_Slot_2:
    action_text = 'switch 2'
  if action == Action.Change_Slot_3:
    action_text = 'switch 3'
  if action == Action.Change_Slot_4:
    action_text = 'switch 4'
  if action == Action.Change_Slot_5:
    action_text = 'switch 5'
  if action == Action.Change_Slot_6:
    action_text = 'switch 6'

  message = '/choose %s' % ( action_text,)
#  move_history.append(message)
  return message

#receives messages from showdown,
# queues and then fires off to parser service
#queue might not be needed
class ChallengeClient(showdown.Client):
    def __init__(self, message_queue, **kwargs):
        showdown.Client.__init__(self, **kwargs)
        self.rooms = {}
        self.rooms_live_states = {}
        self.message_queue = message_queue
        #Save all messages for local replay testing
        self.recorded_messages = []

    def reset(self):
        pass


    async def on_query_response(self, response_type, data):
        print('response_type', response_type)
        print('data', data)

    async def on_receive(self, room_id, inp_type, params):
        print('room_id', room_id)
        print('inp_type', inp_type)
        print('params', params)

        message_event = [room_id, inp_type, params]
        self.recorded_messages.append(message_event)
        #queuing
        inp_type = inp_type.strip()
        if inp_type != 'rawtext' and inp_type != '':
            await self.message_queue.put(message_event)
    #		await self.room_obj.say(action)


    #slows down the rate that the server receives messages
    #consuming
    async def consume_system_message(self, queue):
        while True:
            # wait for an item from the producer
            item = await self.message_queue.get()

            # process the item
            print('consuming {}...'.format(item))

            room_id, inp_type, params = item


            # General messages come here too
            if room_id.strip() == '':
                print('mehhhh')
                queue.task_done()
                continue

            if room_id not in self.rooms:
                queue.task_done()
                continue

            print('asdsadasdsad')
            room = self.rooms[room_id]
            print('asdsadasdsa32232323d')

            bot_name = 'Test Bot 3'
            reward_config = {}
            group_label = 'Parser Group 1'
            session_label = 'Session Quickness'

    #        response = await self.parser_manager.parse_game_session(user_id, room_id, bot_name, inp_type, params, reward_config, group_label, session_label)
    #        action = room.parse_input(inp_type, params)
    #        await self.room_obj.say(action)

            """
            observation['8_singles']['valid_moves']

            action_needed = response['action_needed']
            is_done = response['is_done']
            if is_done:
                print('Sequence Over')
                timestamp = time.time()
                session_id = str(uuid.uuid4())
                inputs_filename = 'session_inputs_%.3f_%s.json' % (timestamp, session_id)
                kifu_dir = './recorded_inputs/'

                with open(kifu_dir+inputs_filename,'w') as outfile_metrics:
                    json.dump(self.recorded_messages, outfile_metrics)

                self.recorded_messages = []
            """
            if inp_type == 'observation':
                print('asking model for help')
                action_needed = False
                observation = json.loads(params[0])
                if 'wait: true' in observation['8_singles']['request_status']:
                    # Notify the queue that the item has been processed
                    queue.task_done()
                    continue
                print('observation keys', observation.keys())
                print('observation singles 8 keys', observation['8_singles'].keys())
                action, target = await self.get_model_step(observation)
                print('action, target', action, target)
                target = 0
                valid_moves = observation['8_singles']['valid_moves']['a']

                print(action)
                print(type(action))
                action = int(action)
                print('valid_moves', valid_moves)
                print('action', action)
                if valid_moves[action] == 1:
                    print('good action')
                    hshshssh = get_sample_action(action)

                    command = hshshssh
                    if command != None:
                        command = command.replace('>p1 ', '/choose ').replace('>p2 ', '/choose ')
                        print('speaking', command)
                        await self.room_obj.say(command)
                        print('done speaking')



                else:
                    print('invalid action, use a random action')


            # Notify the queue that the item has been processed
            queue.task_done()

    async def get_model_step(self, response):
        print('get_model_step, response', response.keys())
        singles_8_data = response['8_singles']
        obs = singles_8_data['observation']
        obs = numpy.asarray(obs)
        reward = singles_8_data['reward']

        valid_moves = singles_8_data['valid_moves']
        valid_moves = numpy.asarray(valid_moves['a'])
        valid_targets = singles_8_data['valid_targets']
        transcript = singles_8_data['transcript']
        print(transcript)
        print('obs shape', obs.shape)
        print('valid_moves shape', valid_moves.shape)
        obs_valid = numpy.concatenate([obs, valid_moves])
        print('len obs', len(obs))
        print('len obs_valid', len(obs_valid))

        return self.model.action_value(obs[None, :], valid_moves)

    async def on_private_message(self, pm):
        if pm.recipient == self:
            await self.cancel_challenge()
            await pm.author.challenge('', 'gen8randombattle')
#            await pm.author.challenge('', 'gen8randomdoublesbattle')
#            self.simulate.stdin.write('>start {"formatid":"gen8randomdoublesbattle"}\n')

    async def on_challenge_update(self, challenge_data):
        incoming = challenge_data.get('challengesFrom', {})
        for user, tier in incoming.items():
            if 'random' in tier:
                await self.accept_challenge(user, 'null')
            if 'gen7monotype' in tier:
                await self.accept_challenge(user, ghost_team)

    async def on_room_init(self, room_obj):
        if room_obj.id.startswith('battle-'):
            self.room_obj = room_obj
            self.rooms[room_obj.id] = {
                'room': room_obj.id,
            }
            session_id = str(uuid.uuid4())
#            self.rooms_live_states[room_obj.id] = LiveShowdownState(room_obj.id, bot_name, state_manager=StateManager(user_id, room_obj.id))
            await asyncio.sleep(3)

#            await room_obj.say('Oh my, look at the time! Gotta go, gg.')
#            await room_obj.forfeit()
#            await room_obj.leave()
