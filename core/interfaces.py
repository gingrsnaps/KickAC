import time
import random
import string

class MockEmailProvider:
    """Simulates interaction with a temp email service."""
    
    @staticmethod
    def get_email():
        # Simulates fetching a fresh inbox
        domains = ["internxt-mock.com", "temp-sim.org", "10min-mail.net"]
        prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{prefix}@{random.choice(domains)}"

    @staticmethod
    def get_verification_code(email):
        """
        Simulates polling the inbox for a Kick verification code.
        """
        # Simulate the delay of an email arriving
        time.sleep(random.uniform(2.0, 4.0)) 
        
        # Generate a 6-digit code
        code = str(random.randint(100000, 999999))
        return code

class MockTarget:
    """
    Simulates the target platform (Kick).
    NO REAL REQUESTS ARE SENT.
    """
    @staticmethod
    def check_availability(username):
        time.sleep(random.uniform(0.1, 0.4))
        # 90% chance username is available for this demo
        return random.random() > 0.1

    @staticmethod
    def register(email, username, password, user_agent):
        time.sleep(random.uniform(1.0, 2.0)) 
        return True