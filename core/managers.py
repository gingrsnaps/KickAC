import time
import random
import string
import logging
from core.data_resources import VERBS, NOUNS, USER_AGENTS
from core.interfaces import MockEmailProvider, MockTarget

class RateLimiter:
    """
    Enforces the '10 accounts per 30 minutes' rule.
    """
    def __init__(self, limit=10, window_seconds=1800):
        self.limit = limit
        self.window = window_seconds
        self.history = []

    def can_proceed(self):
        now = time.time()
        # Clean old history
        self.history = [t for t in self.history if now - t < self.window]
        
        if len(self.history) < self.limit:
            return True
        return False

    def record_action(self):
        self.history.append(time.time())

    def get_cooldown(self):
        if not self.history: return 0
        # Time remaining until the oldest action expires
        return max(0, self.window - (time.time() - min(self.history)))

class BotManager:
    def __init__(self, task_id, socketio):
        self.task_id = task_id
        self.socketio = socketio
        self.limiter = RateLimiter() # Enforce 10/30m

    def emit(self, msg, type="INFO"):
        print(f"[{type}] {msg}")
        self.socketio.emit('log', {'message': msg, 'type': type})

    def generate_creds(self):
        # Verb + Noun + Random Digits
        username = f"{random.choice(VERBS)}{random.choice(NOUNS)}{random.randint(100, 999)}"
        # Complex Password
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(14))
        return username, password

    def run_batch(self, count):
        self.emit(f"Initializing Batch: {count} accounts.", "SYSTEM")
        
        for i in range(count):
            # 1. Check Rate Limit
            if not self.limiter.can_proceed():
                cooldown = int(self.limiter.get_cooldown())
                self.emit(f"Rate Limit Reached (10/30m). Pausing for {cooldown}s...", "WARN")
                time.sleep(cooldown)

            # 2. Email Acquisition
            email = MockEmailProvider.get_email()
            self.emit(f"Acquired Inbox: {email}", "INFO")

            # 3. Username Generation & Rebound Logic
            attempts = 0
            success = False
            
            while attempts < 3:
                username, password = self.generate_creds()
                self.emit(f"Checking: {username}", "DEBUG")
                
                if MockTarget.check_availability(username):
                    # 4. Registration
                    ua = random.choice(USER_AGENTS)
                    self.emit(f"Registering with UA: {ua[:25]}...", "DEBUG")
                    
                    if MockTarget.register(email, username, password, ua):
                        self.emit(f"SUCCESS: {username} created.", "SUCCESS")
                        self.limiter.record_action()
                        success = True
                        break
                else:
                    self.emit(f"Username '{username}' taken. Rebounding...", "WARN")
                    attempts += 1
            
            if not success:
                self.emit(f"Failed to register account {i+1} after 3 attempts.", "ERROR")

            # Organic Sleep
            time.sleep(random.uniform(2, 5))

        self.emit("Batch Job Completed.", "SYSTEM")