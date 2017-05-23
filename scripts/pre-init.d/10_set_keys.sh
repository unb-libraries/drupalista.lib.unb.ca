#!/usr/bin/env sh
mkdir -p /keys
echo "$KUBE_ADMIN_CA_KEY" > /keys/ca.pem
echo "$KUBE_ADMIN_ADMIN_PEM" > /keys/admin.pem
echo "$KUBE_ADMIN_ADMIN_KEY" > /keys/admin-key.pem
