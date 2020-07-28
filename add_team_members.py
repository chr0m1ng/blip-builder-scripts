from requests import Session
from uuid import uuid4
from json import load
import sys


if len(sys.argv) < 2:
    print('uso: python add_team_members.py <configs_json>')
    exit(-1)

config_json = load(open(sys.argv[1], 'r', encoding='utf8'))

if 'members' not in config_json or 'bots' not in config_json:
    print(
        'configs_json must have members (string list) and bots (obj [identity, name and authorization] list)'
    )
    exit(-1)

TEAM_MEMBERS = config_json['members']

BOTS = config_json['bots']

COMMANDS_URL = 'https://http.msging.net/commands'
SET_METHOD = 'set'

ADMIN_PERMISSIONS = [
    {
        'id': 'team',
        'permissionAction': 3,
        'permissionClaim': 112
    },
    {
        'id': 'payments',
        'permissionAction': 3,
        'permissionClaim': 101
    },
    {
        'id': 'ai-providers',
        'permissionAction': 3,
        'permissionClaim': 102
    },
    {
        'id': 'ai-model',
        'permissionAction': 3,
        'permissionClaim': 103
    },
    {
        'id': 'ai-enhancement',
        'permissionAction': 3,
        'permissionClaim': 104
    },
    {
        'id': 'channels',
        'permissionAction': 3,
        'permissionClaim': 105
    },
    {
        'id': 'desk',
        'permissionAction': 3,
        'permissionClaim': 106
    },
    {
        'id': 'users',
        'permissionAction': 3,
        'permissionClaim': 107
    },
    {
        'id': 'scheduler',
        'permissionAction': 3,
        'permissionClaim': 108
    },
    {
        'id': 'config-basicConfigurations',
        'permissionAction': 3,
        'permissionClaim': 109
    },
    {
        'id': 'config-connectionInformation',
        'permissionAction': 3,
        'permissionClaim': 110
    },
    {
        'id': 'resources',
        'permissionAction': 3,
        'permissionClaim': 111
    },
    {
        'id': 'logMessages',
        'permissionAction': 3,
        'permissionClaim': 113
    },
    {
        'id': 'builder',
        'permissionAction': 3,
        'permissionClaim': 114
    },
    {
        'id': 'analysis',
        'permissionAction': 3,
        'permissionClaim': 115
    }
]


def create_set_member_command(member_email, permissions, bot_identity, bot_name):
    return {
        'id': str(uuid4()),
        'method': SET_METHOD,
        'to': 'postmaster@portal.blip.ai',
        'uri': '/auth-permissions',
        'type': 'application/vnd.iris.portal.guest-user+json',
        'resource': {
            'applicationName': bot_name,
            'returnUrl': f'https://portal.blip.ai/application/detail/{bot_identity}/home',
            'shortName': bot_identity,
            'userCulture': 'en',
            'userEmail': member_email,
            'userFullName': member_email,
            'permissions': permissions
        }
    }


if __name__ == "__main__":
    print(f'Found {len(BOTS)} bots')
    for bot in BOTS:
        print(f'Starting session for {bot["name"]}...')
        session = Session()
        session.headers = {
            'Authorization': bot['authorization']
        }
        for member in TEAM_MEMBERS:
            print(f'Adding member {member} to {bot["name"]}')
            command_body = create_set_member_command(
                member,
                ADMIN_PERMISSIONS,
                bot['identity'],
                bot['name']
            )

            command_res = session.post(COMMANDS_URL, json=command_body)

            if command_res.status_code == 200:
                command_res_json = command_res.json()
                if command_res_json['status'] == 'success':
                    print(f'[SUCCESS] Added {member} to {bot["name"]}')
                else:
                    print(f'[ERROR] Could not add {member} to {bot["name"]}')
                    print(
                        f'[ERROR {member} to {bot["name"]}] Reason: {command_res_json["reason"]["description"]}'
                    )
        print(f'Done adding to {bot["name"]}')
    print('Done')
