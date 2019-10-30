from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import json
import jsonpickle
import requests

app = Flask(__name__, static_url_path="")
api = Api(app)
url = "http://127.0.0.1:8000/Tarefa"


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

	def get(self):	#Listar Tarefas
		r = requests.get(url)
		text = r.text
		#r = r.text
		#response_dict = DictOFObjectsToJSON(tarefas_dict)
		print(text)
		text = json.loads(text)
		return text, 200

	def post(self): #Adicionar Tarefa
		args = self.reqparse.parse_args()
		payload = {'nome': args['nome'], 'nivel': args['nivel']}
		r = requests.post(url, json=payload)
		text = json.loads(r.text)
		return {'tasks': text}, 200


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
		par_url = url + '/' + str(tarefa_id)
		r = requests.get(par_url)
		text = json.loads(r.text)
		return {'task': text}, 200

	def delete(self, tarefa_id): #Remover Tarefa
		par_url = url + '/' + str(tarefa_id)
		r = requests.delete(par_url)
		text = json.loads(r.text)
		return {'task': text}, 200

class HealthCheck(Resource):

	def __init__(self):
		super(HealthCheck, self).__init__()

	def get(self):
		return {}, 200

api.add_resource(TarefaListAPI, '/Tarefa', endpoint='tasks')
api.add_resource(TarefaAPI, '/Tarefa/<int:tarefa_id>', endpoint='task')
api.add_resource(HealthCheck, '/healthcheck', endpoint='healthcheck')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port = 5000)

#tarefa = tarefas_dict[key]
#thisdict["color"] = "red"