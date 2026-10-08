# Lab 6.3

## Setup

We start minikube
```
minikube start
```
```
minikube image pull python:3.13-slim
```
We create namespace
```
kubectl create namespace lab-job-cronjob
```
```
cd .\lab6.3\
```

## Part 1

After creating `job-simple.yaml`, we run
```
kubectl apply -f job-simple.yaml
```
```
kubectl -n lab-job-cronjob get job
```
```
kubectl -n lab-job-cronjob wait --for=condition=complete job/data-import-job --timeout=60s
```
```
kubectl -n lab-job-cronjob logs -l job-name=data-import-job
```

## Part 2

We create `job-with-retry.yaml`
```
kubectl apply -f job-with-retry.yaml
```
```
kubectl -n lab-job-cronjob get pods -l job-name=data-transform-job -w
```
```
kubectl -n lab-job-cronjob describe job data-transform-job
```
4 pods were created (1 attempt + 3 retries).
Failed pods are kept so we can inspect their logs.

In `describe` output, the failure reason is BackoffLimitExceeded.

After changing `activeDeadlineSeconds`: from 300 to 10, deleting and re-applying the Jobs, the reason becomes `DeadlineExceeded`.

## Part 3

We create `cronjob-pipeline.yaml`
```
kubectl apply -f cronjob-pipeline.yaml
```
```
kubectl -n lab-job-cronjob get cronjob
```
```
kubectl -n lab-job-cronjob get jobs -w
```
```
kubectl -n lab-job-cronjob logs job/bronze-to-silver-pipeline-29858352
```
Then we create `cronjob-backup.yaml`
```
kubectl apply -f cronjob-backup.yaml
```

## Part 4

```
# List all Jobs
kubectl -n lab-job-cronjob get jobs

# View Job status and events
kubectl -n lab-job-cronjob describe job data-import-job

# View logs from Job Pod
kubectl -n lab-job-cronjob logs -l job-name=data-import-job

# Suspend/resume a CronJob
kubectl -n lab-job-cronjob patch cronjob bronze-to-silver-pipeline -p '{"spec":{"suspend":true}}'
kubectl -n lab-job-cronjob patch cronjob bronze-to-silver-pipeline -p '{"spec":{"suspend":false}}'
```

## Part 5

```
kubectl -n lab-job-cronjob create configmap etl-config --from-literal=BATCH_SIZE=1000 --from-literal=SOURCE_LAYER=bronze --from-literal=TARGET_LAYER=silver
```
Then we create `cronjob-etl.yaml`
```
kubectl apply -f cronjob-etl.yaml
```
```
kubectl get cronjob -n lab-job-cronjob
```
```
kubectl get jobs -n lab-job-cronjob -w
```
To test the CronJob without waiting for its schedule
```
kubectl -n lab-job-cronjob create job etl-manual-run --from=cronjob/etl-bronze-to-silver
```
```
kubectl -n lab-job-cronjob wait --for=condition=complete job/etl-manual-run --timeout=60s
```
```
kubectl -n lab-job-cronjob logs job/etl-manual-run
```

## Teardown

```
# Delete all Jobs and CronJobs in the namespace
kubectl -n lab-job-cronjob delete job --all
kubectl -n lab-job-cronjob delete cronjob --all

# Delete the namespace
kubectl delete namespace lab-job-cronjob

# Verify deletion
kubectl get namespace lab-job-cronjob  # Should show "not found"

# Remove lab directory
cd .. && rm -r lab-job-cronjob
```