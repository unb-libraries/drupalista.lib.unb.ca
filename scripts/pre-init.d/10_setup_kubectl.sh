#!/usr/bin/env sh
curl -O https://storage.googleapis.com/kubernetes-release/release/v1.6.1/bin/linux/amd64/kubectl
chmod +x kubectl
./kubectl config set-cluster ${KUBE_CLUSTER_ID} --server=https://${KUBE_NODE}:${KUBE_NODE_PORT}
./kubectl config set clusters.${KUBE_CLUSTER_ID}.certificate-authority-data ${KUBE_NODE_CA_KEY}
./kubectl config set-credentials ${KUBE_SERVICE_ACCOUNT} --token=${KUBE_BEARER_TOKEN}
./kubectl config set-context ${KUBE_SERVICE_ACCOUNT}@${KUBE_CLUSTER_ID} --cluster=${KUBE_CLUSTER_ID} --user=${KUBE_SERVICE_ACCOUNT}
./kubectl config use-context ${KUBE_SERVICE_ACCOUNT}@${KUBE_CLUSTER_ID}
