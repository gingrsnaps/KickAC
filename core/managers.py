import time
import random
import string
import logging
from core.data_resources import VERBS, NOUNS, USER_AGENTS
from core.interfaces import MockEmailProvider, MockTarget

class RateLimiter:
    def __init__(self, limit=10, window_seconds=1800):
        self.limit = limit
        self.window = window_seconds
        self.history = []

    def can_proceed(self):
        now = time.time()
        self.history = [t for t in self.history if now - t < self.window]
        return len(self.history) < self.limit

    def record_action(self):
        self.history.append(time.time())

    def get_cooldown(self):
        if not self.history: return 0
        return max(0, self.window - (time.time() - min(self.history)))

class BotManager:
    def __init__(self, task_id, socketio):
        self.task_id = task_id
        self.socketio = socketio
        self.limiter = RateLimiter()

    def emit(self, msg, type="INFO"):
        print(f"[{type}] {msg}")
        self.socketio.emit('log', {'message': msg, 'type': type})

    def generate_creds(self):
        username = f"{random.choice(VERBS)}{random.choice(NOUNS)}{random.randint(100, 999)}"
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(14))
        return username, password

    def run_batch(self, count):
        self.emit(f"Initializing Batch: {count} accounts.", "SYSTEM")
        
        for i in range(count):
            if not self.limiter.can_proceed():
                cooldown = int(self.limiter.get_cooldown())
                self.emit(f"Rate Limit Reached (10/30m). Pausing for {cooldown}s...", "WARN")
                time.sleep(cooldown)

            # 1. Setup
            email = MockEmailProvider.get_email()
            self.emit(f"Inbox Created: {email}", "INFO")

            # 2. Registration Loop
            attempts = 0
            success = False
            
            while attempts < 3:
                username, password = self.generate_creds()
                
                if MockTarget.check_availability(username):
                    ua = random.choice(USER_AGENTS)
                    self.emit(f"Registering {username}...", "DEBUG")
                    
                    if MockTarget.register(email, username, password, ua):
                        self.limiter.record_action()
                        
                        # 3. 2FA Retrieval (Simulated)
                        self.emit("Waiting for verification email...", "INFO")
                        code = MockEmailProvider.get_verification_code(email)
                        
                        # 4. FINAL OUTPUT (The requested clear format)
                        self.emit("------------------------------------------------", "DATA")
                        self.emit(f" ACCOUNT CREATED SUCCESSFULLY [{i+1}/{count}]", "SUCCESS")
                        self.emit(f" EMAIL    : {email}", "DATA")
                        self.emit(f" USERNAME : {username}", "DATA")
                        self.emit(f" PASSWORD : {password}", "DATA")
                        self.emit(f" 2FA CODE : {code}", "Highlight") 
                        self.emit("------------------------------------------------", "DATA")
                        
                        success = True
                        break
                else:
                    self.emit(f"Username '{username}' taken. Rebounding...", "WARN")
                    attempts += 1
            
            if not success:
                self.emit(f"Failed to register account {i+1}.", "ERROR")

            time.sleep(random.uniform(3, 6))

        self.emit("Batch Job Completed.", "SYSTEM")