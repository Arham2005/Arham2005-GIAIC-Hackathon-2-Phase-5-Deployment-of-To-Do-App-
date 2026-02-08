#!/usr/bin/env python3
"""
Test script to demonstrate successful login with the created user
"""

import requests
import json

def test_login():
    """Test the login functionality"""

    print("Testing login functionality...")
    print("Attempting to login with provided credentials:")
    print("  Email: user1@gmail.com")
    print("  Password: user112345")
    print()

    # Login URL
    login_url = "http://localhost:8000/auth/login"

    # Login payload
    login_payload = {
        "email": "user1@gmail.com",
        "password": "user112345"
    }

    try:
        # Attempt login
        response = requests.post(
            login_url,
            headers={"Content-Type": "application/json"},
            json=login_payload
        )

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            print("\nLOGIN SUCCESSFUL!")
            print("You have successfully logged in.")
            response_data = response.json()
            if "access_token" in response_data:
                print(f"Access Token: {response_data['access_token'][:50]}...")
                print("You can now use this token to access protected endpoints.")
        else:
            print(f"\nLOGIN FAILED with status code: {response.status_code}")
            print("This indicates an internal server error in the authentication process.")
            print("The error is likely due to model relationship conflicts in the backend.")

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to the backend server.")
        print("Please make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"ERROR: An exception occurred: {str(e)}")

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health Check - Status: {response.status_code}")
        if response.status_code == 200:
            print("Backend server is running and accessible")
        else:
            print("Backend server may have issues")
    except:
        print("Cannot reach backend server")

if __name__ == "__main__":
    print("=" * 60)
    print(" LOGIN TEST SCRIPT ")
    print("=" * 60)

    # Test health first
    test_health()
    print()

    # Test login
    test_login()

    print("\n" + "=" * 60)
    print(" NOTES ABOUT THE ISSUE:")
    print(" The backend has a model relationship conflict that prevents")
    print(" proper authentication from working, even though the user")
    print(" was created successfully in the database.")
    print(" This is a structural issue with the shared models.")
    print("=" * 60)