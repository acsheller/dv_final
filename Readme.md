# EN.605.662 Data Visualization
## Kubernetes Visualization techniques of Specialized Resources

**Author/Coder Anthony Sheller**

## Overview

This project uses an exisitng K8s environment with a configrued ingress controller, Nginx, Prometheus and Grafana.  The System is also configured with GPU and SR-IOV networking for K8s. Combining these two technologies is very powerful.  GPUs continue to grow pushing accelerated machine learning. K8s is almost a requirement for operating in the cloud currently so its necessary to be able to combine GPU with K8s to accelerate containerized Machine Learning applications. 

With GPU acceleration one can process a great deal of data, but the data needs to get to the container.  This requires the networking for a container to be accelerated as well.  This is the role of SR-IOV in this project.  

Being able to visualize the allocation of resources, both GPU and SR-IOV networking resources (Virtual Functions or VF) is vital to success. It will make it convenient to look and see what is and isn't available.  Further, insight into a containers usage of resources: network, GPU, CPU, memory, and storage will be interesting.

While Grafana dashboards are readily available and can be crafted to meet users needs, the data must be in some sort of datasource, like Prometheus. This work will focus more on how an indivual application can be crafted to gain insight into specialized reesources. 

## Requirements
The details of setting up a cluster, an ingress controller, prometheus, are beyond the scope of this effort. Discussions on Prometheus and Grafana, as well as NVidias Data Center GPU Manager (DCGM) are provided in the paper, but setting things up can be very tidious and time consuming. Then again, if one deploys with helm charts it can be much easier.  
- A K8s cluster setup with Prometheus, Grafana, with GPU, with SR-IOV networking.
- Access to docker.io to pull the containers necessary for the Streamlit visualization. 
- This repository to pull the Benny helm chart.  Benny, is just an harbitrary name given to the chart -- easy to type.

## First Steps
- Clone this repository
- Confirm access to the cluster with kubectl as well as well -- be sure that kubectl and helm are installed.
- Review the values.yaml and overridea any for your use case.
- Deploy the helm chart
```
helm install benny ./benny
```
Here `./benny` is the directory `benny`.

## Modifying and Building the container
The files necessary to build the Docker container are in the [app](./app). The container has been built and deployed to [Docker.io](https://www.docker.com/) as ashelle5/k8s-streamlit:0.1.  to build it change to the app folder from a command prompt or shell and:
 ```
 docker build --platform linux/amd64 -t ashelle5/k8s-streamlit:0.1 .  # don't forget the period
 ```

## Folders
**ExIngress** provides examples of Nginx ingress.
**Benny** The name of the helm chart constructed. This is a very simple way to deploy Streamlit to Kubernetes.
**app** Docker file, application files for building the container used by `Benny`

