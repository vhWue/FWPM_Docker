# Kubernetes setup
Install `kubectl`, `ctlptl`, `kind`, `helm` and optionally `k9s`

Make sure Docker is running, then setup the cluster:
`ctlptl apply -f k8s/cluster.yaml`

Push the Docker image to the repo:
1. Build the docker image with `docker compose build`
2. Tag it with `docker tag fwpm_docker-fastapi:latest localhost:5005/fwpm_docker-fastapi:latest`
3. Push it with `docker push localhost:5005/fwpm_docker-fastapi:latest`

Apply deployment:
`kubectl apply -f deployment.yaml`

Install MariaDB: `helm install -f values.yaml mariadb oci://registry-1.docker.io/bitnamicharts/mariadb`
Remove MariaDB: `helm uninstall mariadb`

The `values.yaml` contains the SQL init script.

If you change something in the `values.yaml`, delete PVC so MariaDB config changes are updated (WARNING: ALL PVCs ARE DELETED!!!):
`kubectl delete pvc --all`

For testing, port forward service by going into services in k9s and forwarding the port.

## Prometheus setup

1. Install Prometheus stack (includes Grafana): `helm install prometheus-stack prometheus-community/kube-prometheus-stack -f prometheus-values.yaml`
2. Start `k9s`, type `:svc` and hit enter to go to services
3. Scroll to `prometheus-operated` (the one with port 9090) and port forward it (Shift-F)
4. Prometheus should now be accessible on http://localhost:9090. Go to [targets](http://localhost:9090/targets), you should find podMonitors there.
5. Port forward the fuba service as well and access some API endpoint, e.g. http://localhost:8000/clubs
6. In your Prometheus GUI, go to [graph](http://localhost:9090/graph) and type in a query, e.g. `http_requests_total` and press enter.
   You should now see your accessed endpoint (e.g. /clubs) with a count of total requests to the right.