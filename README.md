This repository demonstrates how to leverage **Kubernetes Event-Driven Autoscaling (KEDA)** to create a dynamically scaling application based on incoming HTTP requests. The project sets up a **Python Flask application** on **Amazon EKS (Elastic Kubernetes Service)**, integrates it with **KEDA** for event-driven scaling, and tests the autoscaling functionality using load testing.

### **Overview**

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

*   **Dockerfile**: Contains instructions for building the Docker image.
    
*   **app.py**: The Python Flask app that serves HTTP requests.
    
*   **deployment.yaml**: Kubernetes deployment manifest for the Flask app.
    
*   **scaledobject.yaml**: KEDA configuration for scaling based on HTTP traffic.
    
*   **http-add-on-service.yaml**: Kubernetes service definition to expose the Flask app.
    
*   **requirements.txt**: Lists Python dependencies for the Flask application.
    

**Step-by-Step Guide**
----------------------

### **1\. Setting Up EKS Cluster**

#### **Create an EKS Cluster**

1.  bashCopy codeeksctl create cluster --name keda-cluster --region \--nodes 3
    
2.  bashCopy codeaws eks --region update-kubeconfig --name keda-cluster
    

### **2\. Installing KEDA on Kubernetes**

KEDA will scale our service based on the HTTP traffic it receives. We will install KEDA using **Helm**.

1.  bashCopy codehelm repo add kedacore https://kedacore.github.io/chartshelm repo update
    
2.  bashCopy codehelm install keda kedacore/keda --namespace keda --create-namespace
    

### **3\. Building and Deploying the Flask Application**

#### **Dockerizing the Flask Application**

1.  DockerfileCopy codeFROM python:3.8-slimWORKDIR /appCOPY requirements.txt .RUN pip install -r requirements.txtCOPY app.py .EXPOSE 8080CMD \["python", "app.py"\]
    
2.  pythonCopy codefrom flask import Flaskapp = Flask(\_\_name\_\_)@app.route('/')def hello(): return "Hello, Kubernetes with KEDA!"if \_\_name\_\_ == '\_\_main\_\_': app.run(host='0.0.0.0', port=8080)
    
3.  txtCopy codeFlask==2.1.1
    

#### **Building and Pushing the Docker Image**

Build the Docker image:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopy codedocker build -t ghcr.io/ibraheemcisse/keda-http-app:v1 .   `

Push the image to **GitHub Container Registry**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopy codedocker push ghcr.io/ibraheemcisse/keda-http-app:v1   `

### **4\. Deploying to Kubernetes**

#### **Kubernetes Deployment Manifest**

The deployment.yaml file defines how the application should be deployed.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   yamlCopy codeapiVersion: apps/v1  kind: Deployment  metadata:    name: http-app    namespace: keda  spec:    replicas: 1    selector:      matchLabels:        app: http-app    template:      metadata:        labels:          app: http-app      spec:        containers:          - name: http-app            image: ghcr.io/ibraheemcisse/keda-http-app:v1            ports:              - containerPort: 8080   `

Deploy the app:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopy codekubectl apply -f deployment.yaml --namespace keda   `

### **5\. Setting Up KEDA Autoscaling**

#### **KEDA ScaledObject Configuration**

The **scaledobject.yaml** file defines how KEDA will scale the application based on HTTP traffic. It triggers scaling when HTTP requests exceed a defined threshold.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   yamlCopy codeapiVersion: keda.k8s.io/v1alpha1  kind: ScaledObject  metadata:    name: http-app-scaler    namespace: keda  spec:    scaleTargetRef:      name: http-app    triggers:      - type: http-add-on        metadata:          httpTarget: "http://localhost:8080"          value: "1000"  # Set desired threshold based on load testing   `

Apply the KEDA configuration:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopy codekubectl apply -f scaledobject.yaml --namespace keda   `

### **6\. Load Testing the Application**

To test the autoscaling functionality, simulate heavy traffic using a **curl** command in a loop.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopy codefor i in {1..1000}; do curl http://localhost:8080; done   `

### **7\. Verifying Pod Scaling**

To observe the scaling of your application, use:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopy codekubectl get pods --namespace=keda   `

You should see the number of pods scale up in response to the load.

**Troubleshooting**
-------------------

Here are some challenges I faced while setting up the system and how they were resolved:

### **1\. Pod Creation Issues**

*   **Problem**: Pods for interceptor, scaler, and operator were in a CreateContainerConfigError state, preventing them from starting.
    
*   **Root Cause**: The issue stemmed from either image accessibility or misconfiguration in Kubernetes manifests.
    
*   **Resolution**: I successfully pulled the images manually using Docker, but the problem persisted until Kubernetes configurations were corrected.
    

### **2\. Docker Image Pulling Issue**

*   **Problem**: Despite pulling the Docker image manually, Kubernetes pods failed to start.
    
*   **Resolution**: The image was accessible, but Kubernetes manifests needed adjustments, such as adding missing configurations in the service.
    

### **3\. Service Manifest Error**

*   **Problem**: The service manifest lacked the name field for ports, leading to an error during deployment.
    
*   **Solution**: Adding the required name for each port in the service definition resolved the error.
    

### **4\. Kubernetes Node Debugging**

*   **Problem**: Debugging Kubernetes nodes using kubectl debug had limited functionality because the debugging container lacked necessary tools (e.g., docker, apk).
    
*   **Solution**: I performed debugging on specific nodes by using the debug pod but faced limited access.
    

**Conclusion**
--------------

This project successfully demonstrates how to set up and configure **KEDA** to autoscale a **Python Flask application** on **Kubernetes** based on HTTP traffic. The autoscaling feature reacts dynamically to load and adjusts the number of application pods accordingly.

*   **KEDA Scaling**: The application scaled up and down based on traffic, proving the effectiveness of KEDA for event-driven scaling.
    
*   **Challenges**: Configuring the Docker image and Kubernetes manifests were some hurdles encountered, but these were resolved through debugging and modifying configurations.
    

**Future Improvements**
-----------------------

*   **Enhanced Scaling**: Implement additional scaling triggers based on other metrics such as CPU usage or memory consumption.
    
*   **Multi-Service Architecture**: Scale different microservices independently based on varying triggers and thresholds.
    

**Contributing**
----------------

Contributions are welcome! Feel free to fork the repository, create issues, and submit pull requests. If you encounter bugs or have feature suggestions, please open an issue.

**License**
-----------

This project is licensed under the MIT License - see the LICENSE file for details.
