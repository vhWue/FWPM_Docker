Install `kubectl`, `ctlptl`, `kind`, and optionally `k9s`

Setup the cluster:
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

Delete PVC so MariaDB config changes are updated (WARNING: ALL PVCs ARE DELETED!!!):
`kubectl delete pvc --all`

For testing, port forward service by going into services in k9s and forwarding port.