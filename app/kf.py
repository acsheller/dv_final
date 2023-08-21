'''
Python script that will get resources
in a Kubernetes Cluster
'''

from kubernetes import client, config
import pandas as pd
import nvsmi


def set_config():
    '''
    Return it from one spot so only 
    need to change it in one spot.
    '''
    #config.load_incluster_config()
    config.load_kube_config()


def get_nodes():
    set_config()
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

def get_nodes_for_sriov():
    set_config()
    v1 = client.CoreV1Api()
    ret = v1.list_node()
    nodes = {}
    allocatable={}
    
    for i in ret.items:
        key = i.status.addresses[1].address
        for j in i.status.allocatable.keys():
            allocatable[j]= i.status.allocatable[j]
        nodes[key]= allocatable
        allocatable = {}

    df = pd.DataFrame(nodes)
    return df



def get_k8s_pods():
    '''
    # Get the pods
    '''
    # When outside of K8s
    config.load_kube_config()

    # Because we are in teh cluster
    #config.load_incluster_config()

    v1 = client.CoreV1Api()
    #print("Listing pods with their IPs:")
    pd_ct = []
    ret = v1.list_pod_for_all_namespaces()
    pod_ips = []
    namespaces = []
    names = []
    for i in ret.items:
        #print(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")
        pod_ips.append(i.status.pod_ip)
        namespaces.append(i.metadata.namespace)
        names.append(i.metadata.name)
    df = pd.DataFrame(data= pod_ips,columns=['pod_ip'])
    df['namespace'] = namespaces
    df['name'] = names
    return df


def get_resource_types():
 
    # When outside of K8s
    config.load_kube_config()

    # Because we are in teh cluster
    #config.load_incluster_config()

    v1 = client.CoreV1Api()
    ret = v1.get_api_resources()
    resource_types = []
    for i in ret.resources:
        #if '/' not in i.name:
        resource_types.append(i.name)
    df = pd.DataFrame(data= resource_types,columns=['resource types'])
    return df



def get_gpu_info():
 
    ab = nvsmi.get_gpus()
    
    uuids = []
    names = []
    ids = []
    gpu_util = []
    mem_util = []
    mem_used = []
    mem_free = []
    mem_total = []

    for i in ab:
        uuids.append(i.uuid)
        names.append(i.name)
        ids.append(i.id)
        gpu_util.append(i.gpu_util)
        mem_util.append(i.mem_util)
        mem_used.append(i.mem_used)
        mem_free.append(i.mem_free)
        mem_total.append(i.mem_total)

        
    df = pd.DataFrame(data= uuids,columns=['uuid'])
    df['name'] = names
    df['ids'] = ids
    df['gpu_util'] = gpu_util
    df['mem_util'] = mem_util
    df['mem_used'] = mem_used
    df['mem_free'] = mem_free
    df['mem_total'] = mem_total

    return df

if __name__ == "__main__":
    nodes = get_nodes_for_sriov()
    print("{}".format(nodes))
