# helloworld

Demo project using Docker and Kubernetes.

## Local Development (Docker Compose)

```bash
docker-compose -f compose/hello-world.yml up --build
```

Visit: http://localhost:8080
Visit: http://localhost:8081


## Kubernetes Deployment (Minikube)

```bash
# Build the docker images
docker build -t apache-hello-world:local ./docker/specs/apache-hello-world
docker build -t python-hello-world:local ./docker/specs/python-hello-world

# Start Minikube under the profile k8s-hello-world, with 2 nodes
minikube start --profile k8s-hello-world --nodes 2 --kubernetes-version=v1.33.1 --driver=docker

# Load the docker images into Minikube
minikube image load --profile k8s-hello-world apache-hello-world:local
minikube image load --profile k8s-hello-world python-hello-world:local

# Check the status of Minikube
minikube status --profile k8s-hello-world

# Install the monitoring stack (Prometheus, Alertmanager, Grafana, some exporters and ServiceMonitors to monitor the K8s cluster)
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set grafana.enabled=true \
  --kube-context k8s-hello-world

# Check the kube-prometheus-stack status
kubectl --namespace monitoring get pods -l "release=monitoring"

# Check the sevices under the namespace monitoring
kubectl get svc -n monitoring


# Apply the Manifest
kubectl --context=k8s-hello-world apply -f ./k8s/macOS_minikube/yaml/hello-world.yaml

# Start forwarding the ports between in&out of the cluster
./utils/mykubectl --context=k8s-hello-world start port-forward service/apache-hello-world 8080:80
./utils/mykubectl --context=k8s-hello-world start port-forward service/python-hello-world 8081:80
./utils/mykubectl --context=k8s-hello-world start  port-forward service/nginx-python-lb 8082:80
# Start forwarding port for Grafana 
./utils/mykubectl --context=k8s-hello-world start port-forward -n monitoring svc/monitoring-grafana 3000:80
./utils/mykubectl --context=k8s-hello-world start port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090

# Some status of the Cluster
kubectl --context=k8s-hello-world get deployments
kubectl --context=k8s-hello-world get services
kubectl --context=k8s-hello-world get pods

# Reach the services
curl http://localhost:8080
curl http://localhost:8081
curl http://localhost:8082


# Retrieve the Grafana 'admin' user password
kubectl --namespace monitoring get secrets monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo
# Reach Grafana
curl http://localhost:3000

# Go to Prometheus portal and query nginx_connections_accepted
curl http://localhost:9090
# nginx_connections_accepted
# nginx_connections_accepted{container="nginx-exporter", endpoint="metrics", instance="10.244.0.6:9113", job="nginx-python-lb-metrics", namespace="default", pod="nginx-python-lb-5d45ff878f-rj9q9", service="nginx-python-lb-metrics"}	14
# nginx_connections_accepted{container="nginx-exporter", endpoint="metrics", instance="10.244.1.13:9113", job="nginx-python-lb-metrics", namespace="default", pod="nginx-python-lb-5d45ff878f-wj24k", service="nginx-python-lb-metrics"}	2



# Stop forwarding the ports between in&out of the cluster
./utils/mykubectl --context=k8s-hello-world stop port-forward service/apache-hello-world
./utils/mykubectl --context=k8s-hello-world stop port-forward service/python-hello-world
./utils/mykubectl --context=k8s-hello-world stop port-forward service/nginx-python-lb
./utils/mykubectl --context=k8s-hello-world stop port-forward -n monitoring svc/monitoring-grafana
./utils/mykubectl --context=k8s-hello-world stop port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus

# Stop Minikube
minikube stop --profile k8s-hello-world

# Delete Minikube
minikube delete --profile k8s-hello-world

# Check the Status
minikube status --profile k8s-hello-world
```
