class BotDetectedException(Exception):
	def __init__(self):
		msg = 'Bot Has Been detected, Try using a proxy or change the headers'
		super().__init__(msg)

class TranslateNotFound(Exception):
	def __init__(self):
		msg = """The word you are looking for not found in the directory,
		please consider using the online traslator method
		"""
		super().__init__(msg)
