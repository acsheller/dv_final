'''
Python script that will get resources
in a Kubernetes Cluster
'''

from kubernetes import client, config
import pandas as pd

def get_nodes():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    ret = v1.list_node()
    internalIps = []
    hostnames = []
    for i in ret.items:
        internalIps.append(i.status.addresses[0].address)
        hostnames.append(i.status.addresses[1].address)
        #print(f" loading nodes {i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")
    df = pd.DataFrame(data = [hostnames],columns = ["hostname"])
    df['ip'] = internalIps
    return df



if __name__ == "__main__":
    nodes = get_nodes()
    print("{}".format(nodes))
