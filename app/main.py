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
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import nvsmi
import plotly.graph_objects as go


def set_config():
    '''
    Return it from one spot so only 
    need to change it in one spot.
    '''
    #config.load_incluster_config()
    config.load_kube_config()


def get_k8s_pods():
    '''
    # Get the pods
    '''
    set_config()

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
    set_config()
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

def get_resource_types():
 
    set_config()
    v1 = client.CoreV1Api()
    ret = v1.get_api_resources()
    resource_types = []
    for i in ret.resources:
        if '/' not in i.name:
            resource_types.append(i.name)
    print(resource_types)
    df = pd.DataFrame(data= resource_types,columns=['resource types'])
    return df

def get_resource_by_type(r_type='pod'):
    set_config()

    v1 = client.CoreV1Api()
    ret = v1.get_api_resources()
    resource_types = []
    for i in ret.resources:
        if '/' not in i.name:
            resource_types.append(i.name)
    print("Resource Types {}".format(resource_types))
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
    df['id'] = ids
    df['gpu_util'] = gpu_util
    df['mem_used'] = mem_used
    df['mem_util'] = mem_util
    df['mem_free'] = mem_free
    df['mem_total'] = mem_total

    return df


def create_gauge(value, max_value, label):
    fig, ax = plt.subplots()

    # Create a gauge-like arc
    arc = patches.Arc((0.5, 0.5), width=0.4, height=0.4, angle=0, theta1=0, theta2=value / max_value * 180, color='green')
    ax.add_patch(arc)

    # Create a central circle to mimic a gauge
    circle = plt.Circle((0.5, 0.5), 0.05, color='black')
    ax.add_patch(circle)

    # Set aspect ratio to be equal, remove axes, and set title
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(label)

    # Display the plot
    st.pyplot(fig)

st.set_page_config(layout = "wide")

c1,c2 = st.columns(2)

page = st.sidebar.selectbox('Select View',['Start','View of Pods','Display Resource Types','GPU','SR-IOV']) 

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
    #c1.image('images/Planetina.webp',caption='Planetina from Rick and Morty [1]')
    c2.markdown(
        """
        **Nodes In the Cluster**
        """
    )
    data = get_nodes()
    c2.dataframe(data)
    
    c2.markdown(
        """
        
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
    namespace_list = ['all']+ list(data.namespace.unique())
    data.namespace.unique()
    n_select = st.sidebar.selectbox('Select Namespace',namespace_list) 
    if n_select != 'all':
        data = data[data.namespace == n_select]
    c1.dataframe(data)
    c2.markdown(
        """
        **Something Interesting:**

    """
    )    
    
if page == 'Display Resource Types':
    c1.subheader('EN.605.662 Data Visualization Final Project')
    c1.subheader('Get a Resource Type')
    c1.markdown(
        """
        **Overview**
        Select a Resource Type from the available drop down.
     
    """)
    
    data = get_resource_types()
    print(data)
    #rt_select = st.sidebar.selectbox('Select Resource Type',data) 
    c1.dataframe(data)
    c2.markdown(
        """
        **Something Interesting:**

    """
    )    
    
if page == 'GPU':
    c1.subheader('EN.605.662 Data Visualization Final Project')
    c1.subheader('Display GPU Information')
    c1.markdown(

        """
        **Overview**
        
        Information about GPU. this uses the Python Moduel 
        nvsmi 
     
        """)
    
    data = get_gpu_info()

    if len(data) == 1:
        
        c1.write("A User could insert a GPU intensive application here and then monitor the application as is shown here.")
        c1.write("**{}**".format(data.loc[0]['name']))
        c1.write("Total memory Available: **{} GB**".format(np.round(data.loc[0]['mem_total']/1000,2)))
        c1.write("     Total memory Used: **{} GB**".format(np.round(data.loc[0]['mem_used']/1000,2)))
        c1.write("     Total memory Free: **{} GB**".format(np.round(data.loc[0]['mem_free']/1000,2)))
    #c1.dataframe(data)
    print('data')
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = data.loc[0]['gpu_util'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "GPU Utilization %"},
        gauge = {'axis': {'range': [None,100]},
                 'steps' : [
                    {'range': [0, 75], 'color': "lightgreen"},
                    {'range': [75, 90], 'color': "lightyellow"},
                    {'range': [90, 100], 'color': "lavenderblush"}
                    ]
                 
                 
                 }))
    fig.update_layout(width=300,height=300)
    c2.plotly_chart(fig,use_container_width=False)
    fig2 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = data.loc[0]['mem_util'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "GPU Memory Utilization %"},
        gauge = {'axis': {'range': [None,100]},
                 'steps' : [
                    {'range': [0, 75], 'color': "lightgreen"},
                    {'range': [75, 90], 'color': "lightyellow"},
                    {'range': [90, 100], 'color': "lavenderblush"}
                    ]
                 
                 
                 }))
    fig2.update_layout(width=300,height=300)
    c2.plotly_chart(fig2,use_container_width=False)
    data2 = data[['mem_free','mem_used']]

    data2_melt = data2.melt(var_name='Category', value_name='Amount')
    fig3 = px.bar(data2_melt, x=data2_melt.index, y='Amount',color='Category',
             title='GPU Memory Utilization',
             height=300, width=300)

    # Customize the layout
    #fig3.update_layout(barmode='stack')
    c1.plotly_chart(fig3,use_container_width=False)

    #data2 = data[['']]
    
    #hist = train_mnist_example()
    #c1.plotly_chart(plot_loss(hist))
    #c1.plotly_chart(plot_accuracy(hist))
