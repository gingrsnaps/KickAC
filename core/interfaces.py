import time
import random
import string

class MockEmailProvider:
    """Simulates interaction with a temp email service."""
    @staticmethod
    def get_email():
        # Simulates fetching a fresh inbox
        domains = ["internxt-mock.com", "temp-sim.org"]
        prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{prefix}@{random.choice(domains)}"

class MockTarget:
    """
    Simulates the target platform (Kick).
    NO REAL REQUESTS ARE SENT.
    """
    @staticmethod
    def check_availability(username):
        """Simulates an API check for username availability."""
        time.sleep(random.uniform(0.2, 0.6)) # Simulate network RTT
        # 20% chance the username is 'taken' to test retry logic
        return random.random() > 0.2

    @staticmethod
    def register(email, username, password, user_agent):
        """Simulates the registration POST request."""
        # Simulate processing time and Cloudflare challenge
        time.sleep(random.uniform(1.5, 3.0)) 
        return True