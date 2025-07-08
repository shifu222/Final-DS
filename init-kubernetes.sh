# !/bin/bash


#activar minikube como un contenedor de docker
eval $(minikube docker-env)


#crear las imagenes

docker build -t product-service:latest ./src/serviceB/.

docker build -t user-service:latest ./src/serviceA/.


#configmaps

kubectl apply -f ./K8s/configmap/db-env/configmap.yaml
kubectl apply -f ./K8s/configmap/db-env/secret.yaml



#deploy

kubectl apply -f ./K8s/db.yaml
kubectl apply -f ./K8s/product_service.yaml
kubectl apply -f ./K8s/user_service.yaml


#ingress

minikube addons enable ingress
kubectl apply -f ./K8s/ingress/services-ingress.yaml