class BotDetectedException(Exception):
	def __init__(self):
		msg = 'Bot Has Been detected, Try using a proxy or change the headers'
		super().__init__(msg)
