"""Handles getting and parsing DCS server data"""
from aiohttp import ClientSession
from asyncio import create_task, sleep
from server_data.comm_checker import check_usernames as check_usernames, log_user
from server_data.hoggit import parse_hoggit
from server_data.limakilo import parse_lk
from sys import modules
from time import time
from types import ModuleType
import logging


class ServerGetter(ModuleType):
	def __init__(self):
		super().__init__(__name__, 'Handles getting and parsing DCS server data')
		self.close = False
		self.gaw = {'exception': 'Getting data'}
		self.pgaw = {'exception': 'Getting data'}
		self.lkeu = {'exception': 'Getting data'}
		self.lkna = {'exception': 'Getting data'}

		self._url_dict = {'gaw': 'https://statecache.hoggitworld.com/gaw', 'pgaw': 'https://statecache.hoggitworld.com/pgaw',
		                 'lkeu': 'https://levant.eu.limakilo.net/status/data', 'lkna': 'https://levant.na.limakilo.net/status/data'}
		self.check_usernames = check_usernames
		self.log_user = log_user

	async def loop(self):
		async with ClientSession() as session:
			while not self.close:
				start = time()
				for name, parse_func in (('gaw', parse_hoggit), ('pgaw', parse_hoggit),
				                                ('lkeu', parse_lk), ('lkna', parse_lk)):
					async with session.get(self._url_dict[name]) as response:
						if response.status != 200:
							logging.warning('Server %s encountered a %s error', name, response.status)
							continue
						self.__setattr__(name, parse_func(await response.json()))
				await sleep(120 - time() + start)
				print(self.gaw, self.pgaw, self.lkna, self.lkeu)


# I like this better than __getattr__ so ¯\_(ツ)_/¯
modules[__name__] = ServerGetter()
