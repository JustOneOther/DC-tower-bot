from datetime import datetime, timedelta
from re import match


def parse_hoggit(data_dict: dict) -> dict:
    # Check data to be processed for unexpected types
    if (type(data_dict['objects']), type(data_dict['players']), type(data_dict['uptime'])) != (list, int, float) \
            or data_dict['updateTime'] == '':
        return {'exception': 'Unexpected data types in server information'}

    seconds_to_restart = timedelta(seconds=14400 - data_dict['uptime'])
    # List comprehension to end all list comprehensions (filters all except enemy air units with non-standard names)
    players = [v['Pilot'] for v in data_dict['objects'] if
               v['Coalition'] == 'Enemies' and v['Type'] in {'Air+FixedWing', 'Air+Rotorcraft'} and not match(
                   r'USA air \d+ unit\d', v['Pilot'])]

    return {'player_count': f"{data_dict['players'] - 1} player(s) online",
            'players': players,
            'metar': f"METAR: `{data_dict['metar']}`",
            'restart': f"restart <t:{round((datetime.fromisoformat(data_dict['updateTime']) + seconds_to_restart).timestamp())}:R>"}
