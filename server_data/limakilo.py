from datetime import datetime, timedelta


def parse_lk(data_dict: dict) -> dict:
	if data_dict is None:
		return {'exception': 'Server offline'}

	seconds_to_restart = timedelta(seconds=int(data_dict['restartPeriod']) - int(data_dict['modelTime']))

	return {'player_count': f"{int(data_dict['players']['current']) - 1} player(s) online",
			'players': [i['name'] for i in data_dict['players']['list']],
			'restart': f"restart <t:{round((datetime.fromisoformat(data_dict['date']) + seconds_to_restart).timestamp())}:R>"}
