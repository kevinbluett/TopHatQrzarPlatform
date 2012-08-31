from datetime import datetime
from Model.domainobject import DomainObject
from Model.domainexception import DomainException
from Model.teamgame import TeamGame

class Team(DomainObject):

	_name = "Team"
	_game = None
	_players = None

	def __init__(self, id_=None):
		super(Team, self).__init__(id_)

	def getName(self):
		return self._name

	def setName(self, name):
		if len(name) > 255:
			raise DomainException("Name cannot be more than 255 characters")

		self._name = name

	def getGame(self):
		return self._game

	def setGame(self, game):
		if not isinstance(game, TeamGame):
			raise DomainException("Teams can only be part of team games not %s" % str(type(game)))

		self._game = game

	def getPlayers(self):
		if self._players is None:
			# load games data
			from Mapper.qrzarplayermapper import QRzarPlayerMapper
			PM = QRzarPlayerMapper()
			self._players = PM.findByTeam(self)
			
		return self._players

	def dict(self):
		self.getPlayers()		# hit lazy load

		super(Team, self).dict()