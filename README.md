# EKS Simple Panel

Constantly updated

Features
========
* List namespaces (with option to hide namespaces)
* List pods
* List containers

CONFIGURING K8S USER
====================

1) Create IAM user(ex: eks-readonly) with this policy:
```
{
    "Version": "2012-10-17",
    "Statement": {
        "Sid": "45345354354",
        "Effect": "Allow",
        "Action": [
            "eks:DescribeCluster",
            "eks:ListCluster"
        ],
        "Resource": "*"
    }
} 
```

2) Edit aws-auth
```
kubectl edit cm -n kube-system aws-auth
```

3) Add information below inside mapUsers, ex:
```
mapUsers: |
    - userarn: arn:aws:iam::xxx:user/eks-readonly
        username: eks-readonly
```
4) Create cluster role
```
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
name: eks-readonly
rules:
- apiGroups:
- ""
resources:
- '*'
verbs:
- get
- list
- watch
- apiGroups:
- extensions
resources:
- '*'
verbs:
- get
- list
- watch
- apiGroups:
- apps
resources:
- '*'
verbs:
- get
- list
- watch  
```
5) Create cluster role binding    
```
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
name: eks-readonly
subjects:
- kind: User
name: eks-readonly
apiGroup: rbac.authorization.k8s.io
roleRef:
kind: ClusterRole
name: eks-readonly
apiGroup: rbac.authorization.k8s.io    
```

RUNNING ON SEVER
================

    # git clone https://github.com/nopp/k8spanel.git
    # cd k8spanel
    # python main.py

RUNNING ON DOCKER
=================

    # docker container run -d -e CLUSTER_NAME="clusterName" -e AWS_ACCESS_KEY_ID="yourAccessKey" -e AWS_SECRET_ACCESS_KEY="yourSecretKey" -p 9191:9191 nopp/eks-simple-panel:1.0

Screenshot
==========
![Image Alt](https://raw.githubusercontent.com/nopp/eks-simple-panel/master/screenshots/panel-1.png)
![Image Alt](https://raw.githubusercontent.com/nopp/eks-simple-panel/master/screenshots/panel-2.png)
