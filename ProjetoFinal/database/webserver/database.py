from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import json
import jsonpickle
import pymysql


def connect_db(host='localhost',user='root',password='123',database='TAREFAS_DB'):
	conn = pymysql.connect(
		host='localhost',
		user='root',
		password='123',
		database='TAREFAS_DB')
	return conn

def adiciona_tarefa(tarefa):
	conn = connect_db()
	with conn.cursor() as cursor:
		cursor.execute('INSERT INTO tarefas (nome, nivel) VALUES (%s, %s)', (tarefa.nome, tarefa.nivel))
		cursor.execute('''COMMIT''')
	conn.close()


def remove_tarefa(tarefa_id):
	conn = connect_db()
	with conn.cursor() as cursor:
		cursor.execute('DELETE FROM tarefas WHERE id=%s', (tarefa_id))
		cursor.execute('''COMMIT''')
	conn.close()

def atualiza_tarefa(tarefa_id, tarefa):
	conn = connect_db()
	with conn.cursor() as cursor:
		cursor.execute('UPDATE tarefas SET nome = %s, nivel = %s WHERE id=%s', (tarefa.nome, tarefa.nivel, tarefa_id))
		cursor.execute('''COMMIT''')
	conn.close()

def acha_tarefa(tarefa_id):
	conn = connect_db()
	with conn.cursor() as cursor:
		cursor.execute('SELECT * FROM tarefas WHERE id = %s', (tarefa_id))
		res = cursor.fetchone()
		print("TAREFAS:", res)
		if res:
			return res
		else:
			return None

def lista_tarefas():
	conn = connect_db()
	with conn.cursor() as cursor:
		cursor.execute('SELECT * FROM tarefas')
		res = cursor.fetchall()
		#tarefas = tuple(x[0] for x in res)
		print("TAREFAS:", res)
		return res


app = Flask(__name__, static_url_path="")
api = Api(app)


class Tarefas:
	def __init__(self, nome, nivel):
		self.nome = nome
		self.nivel = nivel


class TarefaListAPI(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('nome', type=str, required=True,
								   help='Nome da tarefa nao definido',
								   location='json')
		self.reqparse.add_argument('nivel', type=str, required=True, 
									help='Nivel da tarefa nao definido',
								   location='json')
		super(TarefaListAPI, self).__init__()

	def get(self): #Listar Tarefas
		tarefas = lista_tarefas()
		return {'tarefa (id, nome, nivel)': tarefas}, 200

	def post(self): #Adicionar Tarefa
		args = self.reqparse.parse_args()
		tarefa = Tarefas(args['nome'], args['nivel'])
		print(adiciona_tarefa(tarefa))
		return {'status': "done"}, 200


class TarefaAPI(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('nome', type=str, required=False,
								   help='Nome da tarefa nao definido',
								   location='json')
		self.reqparse.add_argument('nivel', type=str, required=False, 
									help='Nivel da tarefa nao definido',
								   location='json')
		super(TarefaAPI, self).__init__()

	def get(self, tarefa_id): #Listar uma Tarefa
		tarefa = acha_tarefa(tarefa_id)
		return {'tarefa (id, nome, nivel)': tarefa}


	def delete(self, tarefa_id): #Remover Tarefa
		remove_tarefa(tarefa_id)
		return {'status': "done"}, 200

class HealthCheck(Resource):

	def __init__(self):
		super(HealthCheck, self).__init__()

	def get(self):
		return {}, 200

api.add_resource(TarefaListAPI, '/Tarefa', endpoint='tasks')
api.add_resource(TarefaAPI, '/Tarefa/<int:tarefa_id>', endpoint='task')
api.add_resource(HealthCheck, '/healthcheck', endpoint='healthcheck')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port= 8000)