'''
EN.605.662 Data Visualization Final project
Tony Sheller

A Streamlit based application for Visualizing resources in Kubernetes

'''
from collections import namedtuple
import altair as alt
import math
import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.error import URLError
from kubernetes import client, config


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
    ret = v1.list_pod_for_all_namespaces(watch=False)
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


def get_nodes():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    ret = v1.list_node()
    internalIps = []
    hostnames = []
    for i in ret.items:
        internalIps.append(i.status.addresses[0].address)
        hostnames.append(i.status.addresses[1].address)
    df = pd.DataFrame(data = [hostnames],columns = ["hostname"])
    df['ip'] = internalIps
    return df

st.set_page_config(layout = "wide")

c1,c2 = st.columns(2)

page = st.sidebar.selectbox('Select View',['Start','View of Pods','Node Information','GPU','SR-IOV']) 

st.markdown(
"""
<script>
// Function to scroll to the top of the page
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Scroll to top on page load
window.onload = function() {
    scrollToTop();
};
</script>
""",
unsafe_allow_html=True
)



if page == 'Start':
    c1.subheader('EN.605.662 Data Visualization Final Project')
    c1.subheader('Author: Anthony Sheller')
    c1.markdown(
        """
        **Overview**
        PLANETINA combines GPU acceleration with Network acceleration for containers operating in Kubernetes (K8s).
        The application being viewed is a streamlit application running in K8s.


        **Instructions**

        From the dropdown on the left select the visusalization you would like to view.
    """)
    # https://rickandmorty.fandom.com/wiki/Planetina
    c1.image('images/Planetina.webp',caption='Planetina from Rick and Morty [1]')
    c2.markdown(
        """
        **Nodes In the Cluster**
        """
    )
    data = get_nodes()
    c2.dataframe(data)
    
    c2.markdown(
        """
        **References:**
        1.	"Fandom Contributors." "Planetina." Rick and Morty Wiki, Fandom, https://rickandmorty.fandom.com/wiki/Planetina.
        
        **GitHub Repo**
        [Data Visualization Final Project](https://github.com/acsheller/dv_final)

    """

    )    
    
    


if page == 'View of Pods':
    c1.subheader('EN.605.662 Data Visualization Final Project')
    c1.subheader('View of Pods running in the cluster')
    c1.markdown(
        """
        **Overview**
        This is a simple view of pods running in the cluster.
     
    """)
    data = get_k8s_pods()
    c1.dataframe(data)
    c2.markdown(
        """
        **Something Interesting:**

    """
    )    
    
    
