**KEDA HTTP Add-On with Autoscaling on Kubernetes (EKS)**
=========================================================

This repository demonstrates how to leverage **Kubernetes Event-Driven Autoscaling (KEDA)** to create a dynamically scaling application based on incoming HTTP requests. The project sets up a **Python Flask application** on **Amazon EKS (Elastic Kubernetes Service)**, integrates it with **KEDA** for event-driven scaling, and tests the autoscaling functionality using load testing.

**Overview**
------------

*   **Objective**: Deploy a Python-based HTTP service on **Kubernetes** (using **EKS**), and configure **KEDA** to autoscale the service pods based on incoming HTTP traffic.
    
*   **Key Components**:
    
    *   **Python Flask Application**: A lightweight HTTP service.
        
    *   **KEDA**: A Kubernetes-based scaler that reacts to HTTP traffic to adjust the number of pods.
        
    *   **AWS EKS**: Managed Kubernetes cluster to deploy and run the app.
        
    *   **Load Testing**: Simulate high traffic to test scaling behavior.
        

**Technologies and Tools**
--------------------------

*   **Kubernetes**: For container orchestration, using **Amazon EKS**.
    
*   **KEDA**: Scalable event-driven autoscaling for Kubernetes.
    
*   **AWS CloudShell**: CLI tool to manage resources within AWS.
    
*   **Docker**: To containerize the Python Flask application.
    
*   **Helm**: Package manager for Kubernetes used to deploy KEDA.
    
*   **Flask**: Python web framework for creating the HTTP service.
    
*   **GitHub Container Registry (GHCR)**: Used to store and distribute Docker images.
    

**Project Structure**
---------------------

*   **Dockerfile**: Instructions for building the Docker image.
    
*   **app.py**: The Python Flask app that serves HTTP requests.
    
*   **deployment.yaml**: Kubernetes deployment manifest for the Flask app.
    
*   **scaledobject.yaml**: KEDA configuration for scaling based on HTTP traffic.
    
*   **http-add-on-service.yaml**: Kubernetes service definition to expose the Flask app.
    
*   **requirements.txt**: Lists Python dependencies for the Flask application.
    

**Step-by-Step Guide**
----------------------

### **1\. Setting Up EKS Cluster**

1.  Create an EKS cluster using eksctl with 3 nodes and configure kubectl to interact with the cluster.
    

### **2\. Installing KEDA on Kubernetes**

1.  Add KEDA's Helm repository and install KEDA into the keda namespace using Helm.
    

### **3\. Building and Deploying the Flask Application**

1.  Use the Dockerfile to build a Docker image for the Flask app.
    
2.  Push the built image to **GitHub Container Registry (GHCR)**.
    
3.  Deploy the Flask app using the deployment.yaml file.
    

### **4\. Setting Up KEDA Autoscaling**

1.  Configure KEDA with the scaledobject.yaml file to scale the application based on HTTP traffic.
    
2.  Apply the configuration to the Kubernetes cluster.
    

### **5\. Load Testing the Application**

Simulate HTTP traffic using a script or a simple loop to test the autoscaling functionality of the app.

**Troubleshooting**
-------------------

Here is a detailed breakdown of the issues faced and their resolutions:

1.  **Pod Creation Issues**:
    
    *   **Problem**: Pods were in a CreateContainerConfigError state due to missing configurations or image accessibility issues.
        
    *   **Resolution**: Manually pulled Docker images and corrected Kubernetes manifests.
        
2.  **Service Manifest Error**:
    
    *   **Problem**: Missing name field for ports in the service manifest.
        
    *   **Resolution**: Added unique name fields to the http-add-on-service.yaml file.
        
3.  **Node Debugging**:
    
    *   **Problem**: Debugging pods lacked necessary tools (docker, apk) for troubleshooting.
        
    *   **Resolution**: Used available Kubernetes debugging tools and logs to identify and resolve issues.
        

**Future Improvements**
-----------------------

*   Implement additional scaling triggers based on CPU usage, memory, or other metrics.
    
*   Extend the project to support a multi-service architecture with independent scaling for each microservice.
    

**Contributing**
----------------

Contributions are welcome! Fork the repository, create issues, and submit pull requests. Open an issue for bugs or feature suggestions.

**License**
-----------

This project is licensed under the MIT License. See the LICENSE file for details.
