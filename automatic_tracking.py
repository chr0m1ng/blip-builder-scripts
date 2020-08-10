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


def is_automatic_tracking(action):
    return action['$title'] == BASE_TRACKING['$title']


def has_input_bypass(state):
    return '$contentActions' in state and\
        'input' in state['$contentActions'][-1] and\
        'bypass' in state['$contentActions'][-1]['input'] and\
        state['$contentActions'][-1]['input']['bypass']


if len(sys.argv) < 2:
    print('usage: python add_tracking.py <file>')
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
