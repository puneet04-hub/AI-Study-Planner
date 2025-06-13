from flask import Flask, render_template, request
import json

app = Flask(__name__)

def save_data(data):
    with open("study_data.json", "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    try:
        with open("study_data.json") as f:
            return json.load(f)
    except:
        return {"subjects": [], "materials": []}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    days = int(request.form['days'])
    subjects = request.form.getlist('subject[]')
    priorities = request.form.getlist('priority[]')
    completion = request.form.getlist('completion[]')

    study_data = {
        "days": days,
        "subjects": []
    }

    for i in range(len(subjects)):
        study_data["subjects"].append({
            "name": subjects[i],
            "priority": int(priorities[i]),
            "completion": int(completion[i])
        })

    total_priority = sum([s['priority'] for s in study_data["subjects"]])
    plan = []

    for day in range(1, days+1):
        today_plan = {"day": day, "tasks": []}
        for subject in study_data["subjects"]:
            time_share = round((subject['priority']/total_priority)*6, 1)
            today_plan["tasks"].append({
                "subject": subject["name"],
                "hours": time_share
            })
        plan.append(today_plan)

    study_data["plan"] = plan
    save_data(study_data)

    return render_template("plan.html", plan=plan)

@app.route('/materials', methods=['GET', 'POST'])
def materials():
    data = load_data()
    if request.method == 'POST':
        subject = request.form['subject']
        title = request.form['title']
        link = request.form['link']
        data['materials'].append({"subject": subject, "title": title, "link": link})
        save_data(data)
    return render_template("materials.html", materials=data['materials'])

if __name__ == '__main__':
    app.run(debug=True)
