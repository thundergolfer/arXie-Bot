## Kubernetes Stuff

#### Create secrets file

1. `cp secrets.yaml.template secrets.yaml`
2. Fill in secrets in `secrets.yaml` (base64 encoded. eg. `echo stuffstuff | base64`)
2. `kubectl create -f ./secret.yaml`

#### Deploying to Kube

> From: https://codelabs.developers.google.com/codelabs/cloud-slack-bot/index.html

1. Push the docker image to gcloud: `gcloud docker -- push gcr.io/${PROJECT_ID}/arxie-bot:<VERSION>`
2. Create cluster: `gcloud container clusters create arxie-bot-cluster --num-nodes=2 --zone=us-central1-f --machine-type n1-standard-1`
3. Create secrets file (see above)
4. Create deployment: `kubectl create -f slack-codelab-deployment.yaml --record`
5. keep checking status until it says COMPLETE `kubectl get pods`
