from flask import Flask, render_template, request, jsonify
import random
import datetime

app = Flask(__name__)

# Simulated memory and dataset
incident_data = [
    {"id": 1, "title": "Database latency spike", "timestamp": "2025-04-06 10:32", "status": "open", "root_cause": "Unindexed query", "impact": "High latency in user login"},
    {"id": 2, "title": "Pod restart loop in staging", "timestamp": "2025-04-06 09:15", "status": "resolved", "root_cause": "Misconfigured health check", "impact": "Intermittent downtime in staging"},
    {"id": 3, "title": "Memory leak in image processor", "timestamp": "2025-04-05 17:45", "status": "resolved", "root_cause": "Unreleased buffer", "impact": "Increased memory usage"},
    {"id": 4, "title": "Timeouts on payment API", "timestamp": "2025-04-04 12:22", "status": "open", "root_cause": "Slow third-party service", "impact": "Payment failures"}
]

self_healing_logs = [
    {"timestamp": "2025-04-06 09:45", "action": "Restarted service", "status": "Success"},
    {"timestamp": "2025-04-05 13:10", "action": "Rolled back deployment", "status": "Success"}
]

release_notes = [
    {"version": "v3.4", "changes": ["Improved cache performance", "Fixed auth token refresh bug"]},
    {"version": "v3.3", "changes": ["Upgraded PostgreSQL", "Optimized image delivery"]},
    {"version": "v3.2", "changes": ["Introduced feature flags", "Added login audit logs"]}
]

risk_scores = {
    "PR#1221": {"score": 7.8, "reason": "Infra config drift + missing unit tests"},
    "PR#1222": {"score": 3.2, "reason": "Minor UI text changes"},
    "PR#1223": {"score": 6.5, "reason": "New DB index might affect writes"}
}

def simulate_fix():
    fix = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": random.choice(["Restarted service", "Rolled back deployment", "Scaled up replicas", "Purged cache", "Rebuilt container image"]),
        "status": "Success"
    }
    self_healing_logs.append(fix)
    return fix

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').lower()

    if "incident" in user_input:
        return jsonify({"response": f"There are {len(incident_data)} incidents. Use the Incident tab for details or ask for a postmortem."})

    elif "self-heal" in user_input:
        fix = simulate_fix()
        return jsonify({"response": f"✅ Self-healing triggered: {fix['action']} at {fix['timestamp']}"})

    elif "postmortem" in user_input:
        postmortem = f"Incident: {incident_data[0]['title']}\nRoot Cause: {incident_data[0]['root_cause']}\nImpact: {incident_data[0]['impact']}"
        return jsonify({"response": postmortem})

    elif "release note" in user_input:
        latest = release_notes[0]
        return jsonify({"response": f"🚀 Release {latest['version']} includes: {', '.join(latest['changes'])}"})

    elif "risk" in user_input:
        responses = []
        for pr, score in risk_scores.items():
            responses.append(f"⚠️ {pr} Risk Score: {score['score']}/10 – {score['reason']}")
        return jsonify({"response": "\n".join(responses)})

    elif "doc" in user_input or "confluence" in user_input:
        return jsonify({"response": "📝 Generated AI documentation from Jira + Git. Summary: Feature complete, 95% test pass rate, ready for release."})

    elif "test" in user_input:
        return jsonify({"response": "🔬 Smart Test Agent: 3 flaky tests detected, 2 redundant tests skipped. Coverage at 92%."})

    else:
        return jsonify({"response": "🤖 Try asking about incidents, postmortems, self-healing, risks, tests, or docs!"})

@app.route('/incidents')
def incidents():
    return jsonify(incident_data)

@app.route('/self-healing')
def healing():
    return jsonify(self_healing_logs)

@app.route('/release-notes')
def notes():
    return jsonify(release_notes)

@app.route('/risk')
def risk():
    return jsonify(risk_scores)

if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0',port=8058)

