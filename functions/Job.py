from datetime import date, time


class Job:

	def __init__ (self, user: str, command: str, schedule: str):

		self.user = user
		self.command = command
		self.schedule = schedule


	def __repr__ (self):

		return f"< {self.user} | {self.command} | {self.schedule} >"
