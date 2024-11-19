import subprocess

def restart_service(service_name):
    try:
        # Stop the service
        print(f"Stopping the service '{service_name}'...")
        subprocess.run(["sc", "stop", service_name], check=True)
        print(f"Service '{service_name}' stopped successfully.")

        # Start the service
        print(f"Starting the service '{service_name}'...")
        subprocess.run(["sc", "start", service_name], check=True)
        print(f"Service '{service_name}' started successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while managing the service '{service_name}': {e}")

if __name__ == "__main__":
    service_name = "cyverver"  # Replace with the exact service name
    restart_service(service_name)
