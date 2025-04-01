import requests
from datetime import datetime, timedelta

# API Configuration
BASE_URL = 'http://localhost:8000/api'
USERNAME = 'admin'  # Replace with your username
PASSWORD = 'admin'  # Replace with your password

# Create a session to maintain authentication
session = requests.Session()
session.auth = (USERNAME, PASSWORD)

def print_response(response, title):
    """Helper function to print API responses"""
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(response.json())

def jobs_api_examples():
    """Examples of using the Jobs API endpoints"""
    
    # 1. List all jobs
    response = session.get(f'{BASE_URL}/jobs/')
    print_response(response, "List All Jobs")
    
    # 2. Create a new job
    new_job = {
        'title': 'Senior Software Engineer',
        'description': 'Looking for an experienced software engineer',
        'category': 'IT',
        'job_type': 'full_time',
        'job_level': 'senior',
        'experience': '5_years',
        'qualification': 'bachelors',
        'gender': 'any',
        'min_salary': 80000,
        'max_salary': 120000,
        'address': '123 Tech Street',
        'country': 'USA',
        'city': 'San Francisco',
        'contact': 'hr@company.com',
        'location': 'San Francisco, CA',
        'required_skills': 'Python, Django, React',
        'expired_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'status': 'active'
    }
    response = session.post(f'{BASE_URL}/jobs/', json=new_job)
    print_response(response, "Create New Job")
    
    if response.status_code == 201:
        job_id = response.json()['id']
        
        # 3. Get specific job
        response = session.get(f'{BASE_URL}/jobs/{job_id}/')
        print_response(response, "Get Specific Job")
        
        # 4. Update job
        update_data = {'max_salary': 130000}
        response = session.patch(f'{BASE_URL}/jobs/{job_id}/', json=update_data)
        print_response(response, "Update Job")
        
        # 5. Close job
        response = session.post(f'{BASE_URL}/jobs/{job_id}/close_job/')
        print_response(response, "Close Job")
        
        # 6. List active jobs
        response = session.get(f'{BASE_URL}/jobs/active_jobs/')
        print_response(response, "List Active Jobs")
        
        # 7. Delete job
        response = session.delete(f'{BASE_URL}/jobs/{job_id}/')
        print_response(response, "Delete Job")

def applications_api_examples():
    """Examples of using the Job Applications API endpoints"""
    
    # 1. List all applications
    response = session.get(f'{BASE_URL}/applications/')
    print_response(response, "List All Applications")
    
    # 2. Create a new application
    new_application = {
        'full_name': 'John Doe',
        'email': 'john@example.com',
        'phone': '+1234567890',
        'position_applied': 'Senior Software Engineer',
        'cover_letter': 'I am interested in this position...',
        'status': 'pending'
    }
    response = session.post(f'{BASE_URL}/applications/', json=new_application)
    print_response(response, "Create New Application")
    
    if response.status_code == 201:
        application_id = response.json()['id']
        
        # 3. Get specific application
        response = session.get(f'{BASE_URL}/applications/{application_id}/')
        print_response(response, "Get Specific Application")
        
        # 4. Update application status
        response = session.post(
            f'{BASE_URL}/applications/{application_id}/update_status/',
            json={'status': 'reviewed'}
        )
        print_response(response, "Update Application Status")
        
        # 5. Delete application
        response = session.delete(f'{BASE_URL}/applications/{application_id}/')
        print_response(response, "Delete Application")

def candidates_api_examples():
    """Examples of using the Candidates API endpoints"""
    
    # 1. List all candidates
    response = session.get(f'{BASE_URL}/candidates/')
    print_response(response, "List All Candidates")
    
    # 2. Create a new candidate
    new_candidate = {
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'phone': '+1987654321',
        'applied_role': 'Software Engineer',
        'status': 'new'
    }
    response = session.post(f'{BASE_URL}/candidates/', json=new_candidate)
    print_response(response, "Create New Candidate")
    
    if response.status_code == 201:
        candidate_id = response.json()['id']
        
        # 3. Get specific candidate
        response = session.get(f'{BASE_URL}/candidates/{candidate_id}/')
        print_response(response, "Get Specific Candidate")
        
        # 4. Update candidate status
        response = session.post(
            f'{BASE_URL}/candidates/{candidate_id}/update_status/',
            json={'status': 'interviewed'}
        )
        print_response(response, "Update Candidate Status")
        
        # 5. Delete candidate
        response = session.delete(f'{BASE_URL}/candidates/{candidate_id}/')
        print_response(response, "Delete Candidate")

def main():
    """Run all API examples"""
    print("Starting API Examples...")
    
    # Jobs API examples
    print("\n=== Jobs API Examples ===")
    jobs_api_examples()
    
    # Applications API examples
    print("\n=== Applications API Examples ===")
    applications_api_examples()
    
    # Candidates API examples
    print("\n=== Candidates API Examples ===")
    candidates_api_examples()
    
    print("\nAPI Examples completed!")

if __name__ == '__main__':
    main() 