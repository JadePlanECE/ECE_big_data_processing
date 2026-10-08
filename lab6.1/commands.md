# Lab 6.1

## Part 1

[link here](https://minikube.sigs.k8s.io/docs/start/)

```
New-Item -Path 'c:\' -Name 'minikube' -ItemType Directory -Force
$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -OutFile 'c:\minikube\minikube.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing
```

```
$oldPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)
if ($oldPath.Split(';') -inotcontains 'C:\minikube'){
  [Environment]::SetEnvironmentVariable('Path', $('{0};C:\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine)
}
```

Start cluster with docker
```
minikube start --driver=docker
```

Verirfy status
```
minikube status
kubectl get nodes
kubectl describe node minikube
```

Activate metrics server and show the resources consumption
```
minikube addons enable metrics-server
```

The command below display the CPU and Memory usage from each Pods.
```
kubectl top pods -A --sort-by cpu --sum=true
```

The command below display the namespave of all the components.
```
kubectl -n kube-system get pods
```

- `coredns-559f6c778d-h5wpb` provides the DNS-based service discovery
- `etcd-minikube` stores Kubernetes cluster state and configuration
- `kindnet-5x6gc` provides networking between Pods and nodes
- `kube-apiserver-minikube` exposes the Kubernetes API
- `kube-controller-manager-minikube` runs the controllers that maintain the desired cluster state
- `kube-proxy-xnvz7` maintains the network rules
- `kube-scheduler-minikube` chooses which node should run new Pods
- `metrics-server-768f9f6999-w444f` collects resources metrics
- `storage-provisioner` provides automatically persistent storage for Pods

## Part 2

```
kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1
```
```
kubectl get pods
```
```
$env:POD_NAME = kubectl get pods -l app=kubernetes-bootcamp -o jsonpath='{.items[0].metadata.name}'
```
```
echo "$POD_NAME"
```
```
kubectl logs $env:POD_NAME
```
```
kubectl describe pod $env:POD_NAME
```
```
kubectl exec $env:POD_NAME -- cat /etc/os-release
```
```
kubectl exec -it $env:POD_NAME -- bash
```
`ls` to find the `server.js` file, then cat it to read it.
`curl localhost:8080` to make sure the web app is responding inside the container.
`exit` to exit the shell.

## Part 3

```
kubectl expose deployments/kubernetes-bootcamp --type="NodePort" --port 8080
```
```
kubectl get services
```
The service has been attach with the port 8080:31340/TCP
```
minikube ip
```
The IP of the minikube node is 192.168.49.2
```
minikube service kubernetes-bootcamp --url 192.168.49.2
```
In a new Terminal (2) (take url from last command):
```
$env:APP_URL = "http://127.0.0.1:62703"
```
```
curl.exe $env:APP_URL
```

## Part 4

```
kubectl scale deployments/kubernetes-bootcamp --replicas=5
```
To make sure we have 5 Pods, we use:
```
kubectl get pods
```
We query 10 times
```
1..10 | ForEach-Object { curl.exe -s $env:APP_URL }
```
We can observe that the name of the Pods rotate

We now downscale the number of Pods to 3, and verify the others are not erunning anymore.
```
kubectl scale deployment/kubernetes-bootcamp --replicas=2
```
```
kubectl get pods
```
The Pods are still running.

## Part 5
In an other Terminal (3) (do not kill the very first one Terminal (1)), start by trying 
```
curl.exe $env:APP_URL
```
If `curl: (2) no URL specified` or another error, then do the command before the next one (the URL should be the one from the very first Terminal (1)):
```
$env:APP_URL = "http://127.0.0.1:62703"
```
If no error:
```
while ($true) { curl.exe -s $env:APP_URL; Start-Sleep -Milliseconds 500 }
```
Go back to the 'old' Terminal (2):
```
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2
```
```
kubectl rollout status deployments/kubernetes-bootcamp
```
The response of the last created Terminal (3) did not changed, the service was not interrupted.
```
kubectl set image deployment/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v3
```
```
kubectl get pods
```
We update the image with v3 even if it doesnt exist, but the Pods of v2 are still ready, so the service still response.

We then rollout do cancel the previous operation, and rollback again to return to v1
```
kubectl rollout undo deployments/kubernetes-bootcamp
```
```
kubectl rollout history deployment/kubernetes-bootcamp
```
```
kubectl rollout undo deployment/kubernetes-bootcamp --to-revision=1
```
Then we stop the loop of the last Terminal (3) with `Ctrl + C`

## Part 6

We start by cleaning up the previous part
```
kubectl delete service kubernetes-bootcamp
kubectl delete deployment kubernetes-bootcamp
```
We move to the good directory
```
cd .\lab6.1\
```
```
kubectl apply -f deployment.yaml
```
But it raise an error from server: "kubernetes-bootcamp" not found.
After filling `TO COMPLETE #1` in `deployment.yaml`, we can re-run the command.
To verify if the Pods are running, we are again running the same command.
```
kubectl get pods
```
After filling the `service.yaml`, we can run the command. 
```
kubectl apply -f service.yaml
```
We go fetch the url, then update it.
```
minikube service kubernetes-bootcamp-service --url
```
```
$env:APP_URL = "http://127.0.0.1:62703"
```
Then we finally querry
```
curl.exe $env:APP_URL
```
After filling `TO COMPLETE #2` in `deployment.yaml` to replicate 3 Pods, we can re-run the commands.
```
kubectl apply -f deployment.yaml
```
```
1..10 | ForEach-Object { curl.exe -s $env:APP_URL }
```

## Part 7

Delete everything and stop minikube. And close all the Terminals.
```
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
minikube stop
```