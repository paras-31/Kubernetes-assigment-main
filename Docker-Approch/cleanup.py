from kubernetes import client, config
from datetime import datetime, timedelta
import time
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load kube config for local execution
# config.load_kube_config()
config.load_incluster_config()

# Kubernetes API clients
v1 = client.CoreV1Api()

# Namespace to clean up pods from
TARGET_NAMESPACE = "second-namespace"
CLEANUP_INTERVAL = 300  # Check every 5 minutes

def delete_failed_pods(namespace):
# Get all pods in the namespace
    try:
        pods = v1.list_namespaced_pod(namespace)
        for pod in pods.items:
            pod_name = pod.metadata.name
            pod_status = pod.status.phase
            print(f"pod state: {pod_status}")
            pod_creation_time = pod.metadata.creation_timestamp

            logging.info(f"Checking pod: {pod_name}, status: {pod_status}")

            # Check if the pod is not running (Failed, Pending, or Unknown) and is older than 5 minutes
            if pod_status in ["Failed", "Pending", "Unknown"]:
                print("we")
                age = datetime.utcnow() - pod_creation_time.replace(tzinfo=None)
                print("we are at age")
                if age > timedelta(minutes=2):
                    print("deleteing")
                    # Delete the pod
                    logging.info(f"Deleting pod: {pod_name} (status: {pod_status}, age: {age})")
                    v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
            else:
                logging.info(f"Pod {pod_name} is in state {pod_status} and is not older than 5 minutes.")
    except Exception as e:
        logging.error(f"Error retrieving pods: {e}")

    if __name__ == "__main__":
        while True:
            time.sleep(30)
            try:
                delete_failed_pods(TARGET_NAMESPACE)
                time.sleep(CLEANUP_INTERVAL)
            except KeyboardInterrupt:
                logging.info("Script interrupted by user.")
                sys.exit(0)
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                time.sleep(CLEANUP_INTERVAL)  # Pause before retrying