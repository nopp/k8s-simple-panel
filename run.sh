#!/bin/sh
aws eks update-kubeconfig --name $CLUSTER_NAME
python3 main.py
