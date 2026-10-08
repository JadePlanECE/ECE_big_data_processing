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
