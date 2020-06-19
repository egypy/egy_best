class BotDetectedException(Exception):
	""" raise when your ip is detected as a bot """
	def __init__(self):
		msg = 'Bot Has Been detected, Try using a proxy or change the headers'
		super().__init__(msg)

class TranslateNotFound(Exception):
	""" raise when no such keywords found in the trasnlation dict """
	def __init__(self):
		msg = """The word you are looking for not found in the directory,
		please consider using the online traslator method
		"""
		super().__init__(msg)
