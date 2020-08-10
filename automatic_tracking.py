# coding=utf-8
import sys
import json

BASE_TRACKING = {
    'type': 'TrackEvent',
    '$title': 'TRACKING AUTOMATICO',
    '$invalid': False,
    'conditions': []
}


ROUTER_TRACKING = {
    **BASE_TRACKING,
    'settings': {
        'extras': {
            '#lastStateId': '{{state.previous.id}}',
            '#lastStateName': '{{state.previous.name}}',
            '#input': '{{input.content}}',
            '#contact': '{{contact.serialized}}',
            '#eventDatetime': '{{calendar.datetime}}',
            '#contactIdentity': '{{contact.identity}}',
            '#stateName': '{{state.name}}',
            '#stateId': '{{state.id}}',
            '#messageId': '{{input.message@id}}',
            '#tunnelOriginator': '{{tunnel.originator}}',
            '#tunnelOwner': '{{tunnel.owner}}',
            '#tunnelIdentity': '{{tunnel.identity}}'
        },
        'category': 'flow',
        'action': '{{state.name}} | {{state.id}}'
    }
}

TRACKING = {
    **BASE_TRACKING,
    'settings': {
        'extras': {
            '#lastStateId': '{{state.previous.id}}',
            '#lastStateName': '{{state.previous.name}}',
            '#input': '{{input.content}}',
            '#contact': '{{contact.serialized}}',
            '#eventDatetime': '{{calendar.datetime}}',
            '#contactIdentity': '{{contact.identity}}',
            '#stateName': '{{state.name}}',
            '#stateId': '{{state.id}}',
            '#messageId': '{{input.message@id}}'
        },
        'category': 'flow',
        'action': '{{state.name}} | {{state.id}}'
    }
}

ENTERING_ACTIONS_KEY = '$enteringCustomActions'
LEAVING_ACTIONS_KEY = '$leavingCustomActions'
ACTIONS_KEY = '$contentActions'
TITLE_KEY = '$title'
INPUT_KEY = 'input'
BYPASS_KEY = 'bypass'


def is_automatic_tracking(action):
    return action[TITLE_KEY] == BASE_TRACKING[TITLE_KEY]


def has_input_bypass(state):
    return ACTIONS_KEY in state and\
        INPUT_KEY in state[ACTIONS_KEY][-1] and\
        BYPASS_KEY in state[ACTIONS_KEY][-1][INPUT_KEY] and\
        state[ACTIONS_KEY][-1][INPUT_KEY][BYPASS_KEY]


if len(sys.argv) < 2:
    print('usage: python automatic_tracking.py <file>')
    exit(-1)

flow = []
filename = sys.argv[1]
with open(filename, 'r', encoding='utf-8') as f:
    flow = json.load(f)

for state_id, state in flow.items():
    if not has_input_bypass(state):
        actions = [
            x for x in state[LEAVING_ACTIONS_KEY]
            if not is_automatic_tracking(x)
        ]
        state[LEAVING_ACTIONS_KEY] = actions + [TRACKING]
    else:
        actions = [
            x for x in state[ENTERING_ACTIONS_KEY]
            if not is_automatic_tracking(x)
        ]
        state[ENTERING_ACTIONS_KEY] = [TRACKING] + actions

output_filename = f'{filename.split(".")[0]}-TRACKED.json'

with open(output_filename, 'w') as f:
    json.dump(flow, f, ensure_ascii=False)

print(f'Done! Output file is {output_filename}')
