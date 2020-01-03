from kubernetes import client, config

class Panel():

    hideNamespace = ["kube-logging","kube-system","kube-node-lease","kube-public","tiller","prometheus"]

    def connectCluster(self):

        config.load_kube_config()
        v1 = client.CoreV1Api()

        return v1        

    # lista deployments
    # ex list_namespaced_deployment(namespace="pep")
    def appApi(self):

        config.load_kube_config()
        v1 = client.AppsV1Api()

        return v1    

    def listDeployByNamespace(self,ns):

        cluster = self.appApi()

        namespaceInfo = {}
        listNamespace = []

        # List namespaces
        for deploy in cluster.list_namespaced_deployment(namespace=ns).items:
            print(deploy)

        return ""

    def listNamespace(self):

        cluster = self.connectCluster()

        namespaceInfo = {}
        listNamespace = []

        # List namespaces
        for ns in cluster.list_namespace().items:
            # Not show pods from hide namespace
            if ns.metadata.name not in self.hideNamespace:
                namespaceInfo['name'] = ns.metadata.name
                namespaceInfo['labels'] = ns.metadata.labels
                listNamespace.append(namespaceInfo)
                namespaceInfo = {}

        return listNamespace

    def listServiceByNamespace(self,ns):

        cluster = self.connectCluster()

        serviceInfo = {}
        listService = []

        # List services
        for svc in cluster.list_namespaced_service(namespace=ns).items:
            serviceInfo['name'] = svc.metadata.name
            serviceInfo['labels'] = svc.metadata.labels
            serviceInfo['ports'] = svc.spec.ports
            serviceInfo['type'] = svc.spec.type
            listService.append(serviceInfo)
            serviceInfo = {}

        return listService

    def listPodByNamespace(self,ns):

        cluster = self.connectCluster()

        listPod = []
        listContainer = []
        podInfo = {}
        containerInfo = {}

        # List pods inside specific namespace
        for pod in cluster.list_namespaced_pod(namespace=ns).items:
            podInfo['ip'] = pod.status.pod_ip
            podInfo['name'] = pod.metadata.name
            podInfo['namespace'] = pod.metadata.namespace
            if pod.status.container_statuses[0].state.waiting:
                podInfo['status'] = pod.status.container_statuses[0].state.waiting.reason
            else:
                podInfo['status'] = pod.status.phase           
            podInfo['start_time'] = pod.status.start_time
            podInfo['labels'] = pod.metadata.labels
            # List containers inside pod, pod can be one or more containers
            totalContainer = 0
            for container in pod.spec.containers:
                totalContainer = totalContainer+1
                containerInfo['name'] = container.name
                containerInfo['image'] = container.image
                containerInfo['liveness_probe'] = container.liveness_probe
                containerInfo['readiness_probe'] = container.readiness_probe
                listContainer.append(containerInfo)
            podInfo['total_container'] = totalContainer
            podInfo['containers'] = listContainer
            listPod.append(podInfo)
            podInfo = {}
            listContainer = []
            containerInfo = {}

        return listPod

    def listAllPod(self):

        cluster = self.connectCluster()

        listPod = []
        listContainer = []
        podInfo = {}
        containerInfo = {}

        # List all pods
        for pod in cluster.list_pod_for_all_namespaces().items:
            # Not show pods from hide namespace
            if pod.metadata.namespace not in self.hideNamespace:
                podInfo['ip'] = pod.status.pod_ip
                podInfo['name'] = pod.metadata.name
                podInfo['namespace'] = pod.metadata.namespace
                podInfo['status'] = pod.status.phase
                podInfo['start_time'] = pod.status.start_time
                podInfo['labels'] = pod.metadata.labels
                # List containers inside pod, pod can be one or more containers
                totalContainer = 0
                for container in pod.spec.containers:
                    totalContainer = totalContainer+1
                    containerInfo['name'] = container.name
                    containerInfo['image'] = container.image
                    containerInfo['ports'] = container.ports
                    containerInfo['liveness_probe'] = container.liveness_probe
                    containerInfo['readiness_probe'] = container.readiness_probe
                    listContainer.append(containerInfo)
                podInfo['total_container'] = totalContainer
                podInfo['containers'] = listContainer
                listPod.append(podInfo)
            podInfo = {}
            listContainer = []
            containerInfo = {}

        return listPod

    def listNode(self):

        cluster = self.connectCluster()

        listNode = []
        nodeInfo = {}

        # List all nodes
        for node in cluster.list_node().items:
            nodeInfo['name'] = node.metadata.name
            nodeInfo['labels'] = node.metadata.labels
            nodeInfo['node_info'] = node.status.node_info
            nodeInfo['ip'] = node.status.addresses[0].address
            listNode.append(nodeInfo)
            nodeInfo = {}

        return listNode