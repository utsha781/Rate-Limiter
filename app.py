
from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)

# Rate limiter configuration
MAX_REQUESTS = 5
TIME_WINDOW = 60

# Hash Map to store user request details
users = {}

# Lock to prevent simultaneous updates
lock = threading.Lock()

def rate_limiter(user_id):

    current_time = time.time()

    with lock:

        # Check if user exists
        if user_id not in users:
            users[user_id] = {
                "count": 0,
                "window_start": current_time
            }

        user = users[user_id]

        # Check whether the time window has expired
        if current_time - user["window_start"] >= TIME_WINDOW:

            user["count"] = 0
            user["window_start"] = current_time

        # Check request limit
        if user["count"] < MAX_REQUESTS:

            user["count"] += 1
            return True, user["count"]

        else:
            return False, user["count"]

@app.route('/api/data', methods=['GET'])
def get_data():

    # Identify the user
    user_id = request.headers.get(
        'X-User-ID',
        request.remote_addr
    )

    allowed, count = rate_limiter(user_id)

    if allowed:

        return jsonify({
            "message": "Request successful!",
            "user": user_id,
            "requests_used": count,
            "remaining_requests": MAX_REQUESTS - count
        }), 200

    else:

        return jsonify({
            "message": "Rate limit exceeded!",
            "user": user_id,
            "limit": MAX_REQUESTS,
            "retry_after": TIME_WINDOW
        }), 429

if __name__ == '__main__':
    app.run(debug=True)