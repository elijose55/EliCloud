#Acessar client do Kubernetes:
# ssh ubuntu@54.226.190.240

#Accesar a dashboard do Kubernetes:
# ssh -L 8002:localhost:8002 ubuntu@54.226.190.240
# kubectl proxy --port 8002 --accept-hosts '.*'
# http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/






