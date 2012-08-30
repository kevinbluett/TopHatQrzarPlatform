import MySQLdb as mdb
from mapper import Mapp
from qrzargamemapper import QRzarGameMapper
from deferredcollection import DeferredCollection

class TeamMapper(Mapp):

	def __init__(self):
		super(TeamMapper, self).__init__()

	def targetClass(self):
		return "Team"

	def tableName(self):
		return "teams"
		
	def _doCreateObject(self, data):
		"""Builds the game object given the draw data returned from the database query"""
		from Model.team import Team
		
		team = Team(data["id"])

		# game reference
		GM = QRzarGameMapper()
		game = GM.find(data["game_id"])
		team.setGame(game)

		# rest of the vars
		team.setName(data["name"])

		return team

	def _doInsert(self, obj):
		# build query
		# id, name, game_id
		query = "INSERT INTO teams VALUES(NULL, %s, %s)"

		# convert boolean value to int bool
		params = (obj.getName(), obj.getGame().getId())

		# run the query
		cursor = self.db.getCursor()
		rowsAffected = cursor.execute(query, params)

		# get insert id
		id_ = cursor.lastrowid
		obj.setId(id_)

		cursor.close()

		# only if rows were changed return a success response
		if rowsAffected > 0:
			return True
		else:
			return False

	def _doUpdate(self, obj):
		# build the query
		query = "UPDATE teams SET name = %s, game_id = %s WHERE id = %s LIMIT 1"
		params = (obj.getName(), obj.getGame().getId(), obj.getId())

		# run the query
		cursor = self.db.getCursor()
		rowsAffected = cursor.execute(query, params)
		cursor.close()

		if rowsAffected > 0:
			return True
		else:
			return False

	def getByGame(self, game, start=0, number=50):
		if start < 0:
			raise mdb.ProgrammingError("The start point must be a positive int")

		if number > 50:
			raise mdb.ProgrammingError("You cannot select more than 50 rows at one time")

		query = "SELECT * FROM teams WHERE game_id = %s LIMIT %s, %s"
		params = (game.getId(), start, start+number)

		return DeferredCollection(self, query, params)