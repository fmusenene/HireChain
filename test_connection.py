import http.client
import time

def test_connection():
    try:
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Try to connect to the server
        conn = http.client.HTTPConnection('localhost', 8000)
        conn.request('GET', '/')
        response = conn.getresponse()
        print(f"Status: {response.status}")
        print(f"Reason: {response.reason}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection() 