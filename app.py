from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect
)
from werkzeug.utils import secure_filename
from modules.pdf_reader import extract_text_from_pdf
import os
from modules.auth import (
    register_user,
    login_user
)
from modules.database import (
    chat_history,
    generated_content
)
from modules.history import save_chat
from modules.study_planner import generate_study_plan
from modules.resume_analyzer import analyze_resume
from modules.notes_generator import generate_notes
from modules.research_explainer import generate_research_response
from modules.chatbot import (
    create_vector_store,
    retrieve_context,
    generate_answer
)

app = Flask(__name__)
app.secret_key = "scholar_ai_secret"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

latest_pdf_text = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/research")
def research():
    return render_template("research.html")

@app.route("/notes")
def notes():
    return render_template("notes.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/planner")
def planner():
    return render_template("planner.html")

@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    global latest_pdf_text

    if "pdf" not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
    file.save(filepath)

    latest_pdf_text = extract_text_from_pdf(filepath)
    
    total_chunks = create_vector_store(latest_pdf_text)
    os.remove(filepath)
    return jsonify({
    "message": "PDF processed successfully",
    "filename": filename,
    "text_length": len(latest_pdf_text),
    "chunks": total_chunks
    })
@app.route("/test-search")
def test_search():

    question = request.args.get("q")

    if not question:
        return jsonify({
            "error": "Please provide a question"
        })

    context = retrieve_context(question)

    return jsonify({
        "question": question,
        "context": context
    })

@app.route("/pdf-text")
def pdf_text():
    return jsonify({
        "text_preview": latest_pdf_text[:5000],
        "text_length": len(latest_pdf_text)
    })
@app.route("/show-text")
def show_text():
    return f"""
    <h2>Extracted PDF Text</h2>
    <p><b>Total Characters:</b> {len(latest_pdf_text)}</p>
    <pre style="white-space: pre-wrap; font-size: 16px;">
    {latest_pdf_text}
    </pre>
    """
@app.route("/ask", methods=["POST"])
def ask():
    if "user_id" not in session:
        return jsonify({
        "error":"Please login first"
        }), 401
   
    data = request.get_json()

    print("Received Data:", data)

    question = data.get("question")
    mode = data.get("mode", "pdf")

    answer = generate_answer(question, mode)
    save_chat(
    session["user_id"],
    question,
    answer
    )
    return jsonify({
        "question": question,
        "mode": mode,
        "answer": answer
    })

@app.route("/research-task", methods=["POST"])
def research_task():
    if "user_id" not in session:
        return jsonify({
        "error":"Please login first"
        }), 401
    
    data = request.get_json()

    print("Received Data:", data)

    task_type = data.get("task_type", "summary")

    print("Task Type:", task_type)

    result = generate_research_response(task_type)
    generated_content.insert_one({
    "user_id": session["user_id"],
    "type":"research",
    "task":task_type,
    "content":result
    })

    return jsonify({
        "task_type": task_type,
        "result": result
    })
@app.route("/notes-task", methods=["POST"])
def notes_task():
    if "user_id" not in session:
        return jsonify({
        "error":"Please login first"
        }), 401
    
    data = request.get_json()

    print("Received Data:", data)

    task = data.get("task")

    print("Task:", task)

    result = generate_notes(task)
    generated_content.insert_one({
    "user_id": session["user_id"],
    "type":"notes",
    "task":task,
    "content":result
    })
    return jsonify({
        "result": result
    })

@app.route("/resume-task", methods=["POST"])
def resume_task():
    if "user_id" not in session:
        return jsonify({
        "error":"Please login first"
        }), 401
    
    data = request.get_json()

    task = data.get("task")

    result = analyze_resume(task)

    return jsonify({
        "result": result
    })

@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    if "user_id" not in session:
        return jsonify({
        "error":"Please login first"
        }), 401
    
    data = request.get_json()

    subject = data.get("subject")
    days = data.get("days")
    hours = data.get("hours")

    result = generate_study_plan(
        subject,
        days,
        hours
    )
    generated_content.insert_one({
    "user_id": session["user_id"],
    "type":"planner",
    "task": subject,
    "content": result
    })
    return jsonify({
        "result": result
    })


@app.route("/history")
def history():

    chats = list(
        chat_history.find(
            {},
            {"_id":0}
        ).sort("created_at",-1)
    )
    return jsonify(chats)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    success, message = register_user(
        data["username"],
        data["email"],
        data["password"]
    )

    return jsonify({
        "success": success,
        "message": message
    })

@app.route("/login-user", methods=["POST"])
def login_route():

    data = request.get_json()

    success, user = login_user(
        data["email"],
        data["password"]
    )

    if success:

        session["user_id"] = str(user["_id"])
        session["username"] = user["username"]

        return jsonify({
            "success": True
        })

    return jsonify({
        "success": False,
        "message": "Invalid Credentials"
    })
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
@app.route("/my-history")
def my_history():

    if "user_id" not in session:
        return jsonify({
            "error":"Please login first"
        }), 401

    chats = list(
        chat_history.find(
            {
                "user_id": session["user_id"]
            },
            {
                "_id":0
            }
        ).sort("created_at",-1)
    )

    return jsonify(chats)
@app.route("/history-page")
def history_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("history.html")

@app.route("/saved-content")
def saved_content():

    if "user_id" not in session:
        return jsonify({
            "error":"Please login first"
        }), 401

    data = list(
        generated_content.find(
            {
                "user_id": session["user_id"]
            },
            {
                "_id":0
            }
        ).sort("created_at",-1)
    )

    return jsonify(data)
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    total_chats = chat_history.count_documents({
        "user_id": user_id
    })

    total_notes = generated_content.count_documents({
        "user_id": user_id,
        "type": "notes"
    })

    total_research = generated_content.count_documents({
        "user_id": user_id,
        "type": "research"
    })

    total_plans = generated_content.count_documents({
        "user_id": user_id,
        "type": "planner"
    })

    return render_template(
        "profile.html",
        username=session["username"],
        email=session.get("email","Not Available"),
        total_chats=total_chats,
        total_notes=total_notes,
        total_research=total_research,
        total_plans=total_plans
    )
if __name__ == "__main__":
    app.run(debug=True)