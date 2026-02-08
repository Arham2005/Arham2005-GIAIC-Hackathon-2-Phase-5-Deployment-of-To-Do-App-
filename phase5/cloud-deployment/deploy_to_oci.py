#!/usr/bin/env python3
"""
Automated Deployment Script for Oracle Cloud
================================================
This script automates the deployment process for the Todo Application to Oracle Cloud Infrastructure (OCI).
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, desc=""):
    """Run a command and handle errors"""
    print(f"\n📝 {desc}")
    print(f"Command: {cmd}")

    try:
        # Use shell=True for Windows compatibility
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()[:200]}...")  # Show first 200 chars
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print(" 🚀 TODO APP PHASE 5 AUTOMATED DEPLOYMENT TO ORACLE CLOUD")
    print("=" * 60)
    print("\nThis script will guide you through the deployment process.")
    print("Before continuing, please ensure you have:")
    print("  ✅ Oracle Cloud account with free tier access")
    print("  ✅ OCI CLI installed and configured")
    print("  ✅ kubectl installed and connected to OKE")
    print("  ✅ Docker installed and logged into OCIR")
    print("  ✅ PostgreSQL database (Neon or Autonomous DB)")

    response = input("\nDo you want to continue? (y/N): ").strip().lower()
    if response != 'y':
        print("Deployment cancelled.")
        return

    print("\n" + "=" * 60)
    print(" 🔧 STEP 1: BUILDING DOCKER IMAGE")
    print("=" * 60)

    success = run_command(
        "docker build -t todo-phase5-backend:latest -f Dockerfile.unified .",
        "Building Docker image for Phase 5 backend"
    )

    if not success:
        print("\n❌ Docker build failed. Please fix the issues and try again.")
        return

    print("\n" + "=" * 60)
    print(" 📦 STEP 2: TAGGING AND PUSHING TO OCIR")
    print("=" * 60)

    region = input("\nEnter your Oracle Cloud region (e.g., us-ashburn-1): ").strip()
    tenancy = input("Enter your tenancy name: ").strip()

    image_name = f"{region}.ocir.io/{tenancy}/todo-phase5-backend:latest"

    success = run_command(
        f"docker tag todo-phase5-backend:latest {image_name}",
        f"Tagging image for OCIR: {image_name}"
    )

    if not success:
        print("\n❌ Docker tagging failed.")
        return

    success = run_command(
        f"docker push {image_name}",
        "Pushing image to OCIR"
    )

    if not success:
        print("\n❌ Docker push failed. Make sure you're logged in to OCIR.")
        print("Login command: docker login <region>.ocir.io")
        return

    print("\n" + "=" * 60)
    print(" 🚀 STEP 3: DEPLOYING TO KUBERNETES")
    print("=" * 60)

    # Update deployment.yaml with actual values
    print("\n📝 Updating deployment file with your values...")
    try:
        with open('deployment.yaml', 'r') as f:
            deployment_content = f.read()

        # Replace placeholders
        deployment_content = deployment_content.replace('<region>', region)
        deployment_content = deployment_content.replace('<tenancy>', tenancy)

        # Update the image in the deployment
        deployment_content = deployment_content.replace(
            'image: <region>.ocir.io/<tenancy>/todo-phase5-backend:latest',
            f'image: {image_name}'
        )

        with open('temp-deployment.yaml', 'w') as f:
            f.write(deployment_content)

        print("✅ Deployment file updated successfully!")
    except Exception as e:
        print(f"❌ Error updating deployment file: {e}")
        return

    # Apply Kubernetes manifests
    manifests = ['namespace.yaml', 'configmap.yaml', 'temp-deployment.yaml', 'ingress.yaml']

    for manifest in manifests:
        success = run_command(
            f"kubectl apply -f {manifest}",
            f"Applying {manifest}"
        )

        if not success:
            print(f"❌ Failed to apply {manifest}")
            # Clean up temp file
            if os.path.exists('temp-deployment.yaml'):
                os.remove('temp-deployment.yaml')
            return

    print("\n" + "=" * 60)
    print(" ⏳ STEP 4: WAITING FOR DEPLOYMENT TO BE READY")
    print("=" * 60)

    success = run_command(
        "kubectl rollout status deployment/todo-phase5-backend -n todo-app --timeout=300s",
        "Waiting for deployment to be ready"
    )

    if not success:
        print("❌ Deployment rollout failed. Check the logs with: kubectl logs -n todo-app deployment/todo-phase5-backend")
    else:
        print("\n" + "=" * 60)
        print(" 🎉 SUCCESS! DEPLOYMENT COMPLETED")
        print("=" * 60)
        print("\nYour application is now deployed to Oracle Cloud!")
        print("\nTo check the status:")
        print("  kubectl get pods -n todo-app")
        print("  kubectl get services -n todo-app")
        print("  kubectl get ingress -n todo-app")
        print("\nTo access your application:")
        print("  kubectl get svc todo-unified-service -n todo-app")
        print("  Use the EXTERNAL-IP to access your application")

    # Clean up temp file
    if os.path.exists('temp-deployment.yaml'):
        os.remove('temp-deployment.yaml')

if __name__ == "__main__":
    main()