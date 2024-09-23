# Kubernetes Pod Cleanup Solution
 
## Overview
 
This project provides two approaches to clean up Kubernetes pods that are in a bad state (not running or older than 5 minutes). The script periodically checks the second namespace and deletes pods meeting the criteria. The cleanup script is run from a pod deployed in the first namespace.
 
## Approaches
 
1. **Docker-based Approach**: 
   - Uses a Docker container to run the cleanup Python script inside a pod.
   - The pod runs in `first-namespace`, and the script deletes pods in `second-namespace`.
 
2. **ConfigMap-based Approach**:
   - Uses a ConfigMap to store the cleanup script and mounts it to the pod.
   - The pod runs in `first-namespace`, and the script deletes pods in `second-namespace`.
 
## Files
 
### Kubernetes Manifests
 
1. **01-namespace.yml**: 
   - Defines the namespaces `first-namespace` and `second-namespace`.
 
2. **02-serviceacc.yml**: 
   - Creates a ServiceAccount in `first-namespace` named `pod-cleaner-sa`.
 
3. **03-role-rolebinding.yml**: 
   - Defines a Role in `second-namespace` with permissions to list and delete pods.
   - Creates a RoleBinding to bind the ServiceAccount to the Role.
 
4. **04-pod.yml** (Docker-based Approach): 
   - Defines a pod deployment in `first-namespace` that runs the cleanup script using a Docker container.
 
5. **05-secondpod.yml**: 
   - Defines a regular pod in `second-namespace` and an error pod (with an incorrect image) to simulate the cleanup scenario.
 
### Docker-Based Approach
 
- **cleanup.py**: 
   - Python script to delete failed or pending pods older than 5 minutes.
- **Dockerfile**: 
   - Dockerfile for building the image that runs the Python cleanup script.
 
### ConfigMap-Based Approach
 
- **config.yml**: 
   - ConfigMap that stores the cleanup script for the pod to use in `first-namespace`.
 
- **pod.yml** (ConfigMap-Based Approach): 
   - Defines a pod in `first-namespace` that mounts the ConfigMap and runs the cleanup script.
 
## Usage
 
1. **Docker-based Approach**:
   - Build the Docker image and deploy the pod in `first-namespace`.
 
2. **ConfigMap-based Approach**:
   - Deploy the ConfigMap and the pod in `first-namespace` to run the script.
 
3. **Test**:
   - Use `05-secondpod.yml` to create a regular pod and an error pod in `second-namespace`.
   - The pod in `first-namespace` should clean up the error pod based on the criteria.
 
## Conclusion
 
This solution ensures that pods in a bad state in `second-namespace` are automatically cleaned up by a pod running in `first-namespace`, keeping the cluster healthy.
