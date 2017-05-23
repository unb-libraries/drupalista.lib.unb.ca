#!/usr/bin/env sh
curl -O https://storage.googleapis.com/kubernetes-release/release/v1.6.1/bin/linux/amd64/kubectl
chmod +x kubectl
./kubectl config set-cluster default-cluster --server=https://${KUBE_NODE}:${KUBE_NODE_PORT} --certificate-authority=/keys/ca.pem
./kubectl config set-credentials default-admin --certificate-authority=/keys/ca.pem --client-key=/keys/admin-key.pem --client-certificate=/keys/admin.pem
./kubectl config set-context default-system --cluster=default-cluster --user=default-admin
./kubectl config use-context default-system
