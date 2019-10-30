from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import json
import jsonpickle

app = Flask(__name__, static_url_path="")
api = Api(app)


class Tarefas:
	def __init__(self, nome, nivel):
		self.nome = nome
		self.nivel = nivel

t1 = Tarefas("limpar", 1)
t2 = Tarefas("cozinhar", 2)
t3 = Tarefas("brincar", 0)

tarefas_dict = {
	0: t1,
	1: t2

}


def addToDict(tarefa):
	key = 0
	while(1):
		if key in tarefas_dict:
			key +=1
		else:
			tarefas_dict[key] = tarefa
			break
	return


def DictOFObjectsToJSON(tarefas):
	new_dict = {}
	for key in tarefas:
		tarefa = tarefas[key].__dict__
		new_dict[key] = tarefa
	return new_dict


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

	def get(self):
		response_dict = DictOFObjectsToJSON(tarefas_dict)
		return {'tasks': response_dict}, 200

	def post(self):
		args = self.reqparse.parse_args()
		tarefa = Tarefas(args['nome'], args['nivel'])
		addToDict(tarefa)
		response_dict = DictOFObjectsToJSON(tarefas_dict)
		return {'tasks': response_dict}, 200


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

	def get(self, tarefa_id):
		if tarefa_id not in tarefas_dict:
			print("ERRO")
			abort(404)
		tarefa = tarefas_dict[tarefa_id]

		return {'task': vars(tarefa)}

	def put(self, tarefa_id):
		if tarefa_id not in tarefas_dict:
			abort(404)
		tarefa = tarefas_dict[tarefa_id]
		args = self.reqparse.parse_args()
		for k, v in args.items():
			if v is not None:
				tarefas_dict[tarefa_id].k = v
		response_dict = DictOFObjectsToJSON(tarefas_dict)
		return {'tasks': response_dict}, 200

	def delete(self, tarefa_id):
		if tarefa_id not in tarefas_dict:
			abort(404)
		del tarefas_dict[tarefa_id]
		response_dict = DictOFObjectsToJSON(tarefas_dict)
		return {'tasks': response_dict}, 200

class HealthCheck(Resource):

	def __init__(self):
		super(HealthCheck, self).__init__()

	def get(self):
		return {}, 200

api.add_resource(TarefaListAPI, '/Tarefa', endpoint='tasks')
api.add_resource(TarefaAPI, '/Tarefa/<int:tarefa_id>', endpoint='task')
api.add_resource(HealthCheck, '/healthcheck', endpoint='healthcheck')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

#tarefa = tarefas_dict[key]
#thisdict["color"] = "red"