from flask import Flask , render_template,request,jsonify,redirect,session
import os
import json
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from rag.pdf_reader import read_pdf
from rag.chunker import split_text
from rag.embeddings import get_embeddings
from rag.vector_store import create_index
from rag.vector_store import search
import logging
from rag.llm import generate_answer
from rag.text_analyzer import analyze_text
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.secret_key = "medimind_secret_key"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] =UPLOAD_FOLDER



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            conn.close()
            return "Email already registered!"

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users(name, email, password) VALUES(?, ?, ?)",
            (name, email, hashed_password)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):

            session["user"] = user[1]

            return redirect("/home")

        return "Invalid Email or Password"

    return render_template("login.html")






@app.route("/")
def index():
    return redirect("/login")


@app.route("/home")
def home():

    if "user" not in session:
        return redirect("/login")

    return render_template("home.html")



# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/upload", methods=["POST"])
# def upload_pdf():
#     if "pdf" not in request.files:
#         return "no file uploaded"

@app.route("/upload", methods=["POST"])
def upload_pdf():

    if "user" not in session:
        return redirect("/login")

    if "pdf" not in request.files:
        return "no file uploaded"

    pdf = request.files["pdf"]
    if pdf:

        file_path = os.path.join(app.config["UPLOAD_FOLDER"],pdf.filename)
        pdf.save(file_path)
        # print(file_path)
        logging.info("1 upload started")
        text = read_pdf(file_path)

        logging.info("2 pdf read complete")
        chunks = split_text(text)
        logging.info(" 3 chunks created")

        print("Total chunks : ",len(chunks))
        print(chunks[0])
    
        embeddings = get_embeddings(chunks)

        logging.info("4 embedding created")
        create_index(embeddings,chunks)

        logging.info(" 5 fiass indx created")

        return render_template(
    "home.html",
       message="✓"
  
)
# @app.route("/ask",methods=["POST"])
# def ask_question():
#     print("ask route hit")


@app.route("/ask", methods=["POST"])
def ask_question():

    if "user" not in session:
        return jsonify({"error": "Please login first"})

    print("ask route hit")
    try:
         question = request.form.get("question")
         q_emb= get_embeddings([question])[0]
         result = search(q_emb,k=3)
         
         if not result:
              return "no result"
         
         context = "\n\n".join(result)
         answer = generate_answer(context,question)

         print("llm answer:")
         print(answer)

         structured_answer =analyze_text(answer)
         print("analyzer output")
         print(structured_answer)

         return jsonify({"answer":answer})   #07/2026/////
    
    except Exception as e:
         
         return jsonify ({"error":str(e)})
    
if __name__ =="__main__":
    port = int(os.environ.get("PORT", 5000))
    
    # Crucial: host must be '0.0.0.0'
    app.run(host="0.0.0.0", port=port)
    app.run(debug=True)    
