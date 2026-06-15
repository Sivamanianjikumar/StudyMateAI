async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");
    const status = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {
        status.innerText = "Please select a PDF file.";
        return;
    }

    const formData = new FormData();
    formData.append("pdf", fileInput.files[0]);

    try {
        const response = await fetch("/upload-pdf", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            status.innerText =
    data.message +
    " | File: " + data.filename +
    " | Text Length: " + data.text_length +
    " | Chunks: " + data.chunks;
        } else {
            status.innerText = data.error;
        }
    } catch (error) {
        status.innerText = "Upload failed.";
    }
}
async function askQuestion() {

    const question =
        document.getElementById("question").value;

    const mode =
        document.getElementById("mode").value;

    const answerBox =
        document.getElementById("answer");

    if (!question) {
        answerBox.innerText =
            "Please enter a question.";
        return;
    }

    answerBox.innerHTML = `
    <div class="loader"></div>
    <p style="text-align:center;">
    Generating...
    </p>
    `;

    try {

        const response =
            await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question,
                    mode: mode
                })
            });

        const data =
            await response.json();

        if (response.ok) {

            answerBox.innerHTML =
                marked.parse(data.answer);

        } else {

            answerBox.innerText =
                data.error;
        }

    } catch (error) {

        console.error(error);

        answerBox.innerText =
            "Something went wrong.";
    }
}
async function runResearchTask(taskType) {
    const resultBox = document.getElementById("researchResult");

    resultBox.innerHTML = `
<div class="loader"></div>
<p style="text-align:center;">
Generating...
</p>
`;

    try {
        const response = await fetch("/research-task", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                task_type: taskType
            })
        });

        const data = await response.json();

        if (response.ok) {
            resultBox.innerHTML = marked.parse(data.result);
        } else {
            resultBox.innerText = data.error;
        }

    } catch (error) {
        resultBox.innerText = "Something went wrong.";
    }
}

async function runNotesTask(task){

    const resultBox =
        document.getElementById("notesResult");

        resultBox.innerHTML =
        `
        <div class="loader"></div>
        <p>Generating...</p>
        `;

    try{

        const response =
            await fetch("/notes-task",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    task:task
                })
            });

        const data =
            await response.json();

            resultBox.innerHTML = marked.parse(data.result);

    }catch(error){

        resultBox.innerText =
            "Something went wrong.";
    }
}

async function runResumeTask(task){

    const resultBox =
        document.getElementById("resumeResult");

        resultBox.innerHTML = `
        <div class="loader"></div>
        <p style="text-align:center;">
        Generating...
        </p>
        `;

    const response =
        await fetch("/resume-task",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                task:task
            })
        });

    const data =
        await response.json();

        resultBox.innerHTML = marked.parse(data.result);
}
async function generatePlan(){

    const subject =
        document.getElementById("subject").value;

    const days =
        document.getElementById("days").value;

    const hours =
        document.getElementById("hours").value;

    const resultBox =
        document.getElementById("planResult");

    resultBox.innerText =
        "Creating study plan...";

    const response =
        await fetch("/generate-plan",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                subject,
                days,
                hours
            })
        });

    const data =
        await response.json();

        resultBox.innerHTML = marked.parse(data.result);
}

async function registerUser(){

    const username =
        document.getElementById("username").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    const response =
        await fetch("/register",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                username,
                email,
                password
            })
        });

    const data =
        await response.json();

    document.getElementById(
        "signupMessage"
    ).innerText = data.message;
}
async function loginUser(){

    const email =
        document.getElementById(
            "loginEmail"
        ).value;

    const password =
        document.getElementById(
            "loginPassword"
        ).value;

    const response =
        await fetch("/login-user",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                email,
                password
            })
        });


    const data =
        await response.json();

    if(data.success){
        window.location.href="/";
    }else{
        document.getElementById(
            "loginMessage"
        ).innerText = data.message;
    }
}
async function loadHistory(){

    const container =
        document.getElementById(
            "historyContainer"
        );

    const response =
        await fetch("/my-history");

    const data =
        await response.json();

    let html = "";

    data.forEach(chat => {

        html += `
        <div class="history-card">

            <div class="history-date">
                ${new Date(
                    chat.created_at
                ).toLocaleString()}
            </div>

            <div class="history-question">
                ${chat.question}
            </div>

            <div class="history-answer">
                ${chat.answer}
            </div>

        </div>
        `;
    });

    container.innerHTML = html;
}
function filterHistory(){

    const input =
        document.getElementById(
            "historySearch"
        ).value.toLowerCase();

    const cards =
        document.querySelectorAll(
            ".history-card"
        );

    cards.forEach(card => {

        const text =
            card.innerText.toLowerCase();

        card.style.display =
            text.includes(input)
            ? "block"
            : "none";
    });
}
function showLoginPopup(){

    document.getElementById(
        "loginPopup"
    ).style.display="block";
}
function downloadNotes(){

    const content =
        document.getElementById("notesResult").innerText;

    const tempDiv =
        document.createElement("div");

    tempDiv.style.padding = "20px";

    tempDiv.innerHTML = `
        <h1>ScholarAI Notes</h1>
        <pre style="white-space:pre-wrap;font-size:14px;">
${content}
        </pre>
    `;

    html2pdf()
        .from(tempDiv)
        .save("ScholarAI_Notes.pdf");
}
function downloadResearch(){

    const content =
        document.getElementById(
            "researchResult"
        );

    html2pdf()
        .from(content)
        .save(
            "Research_Report.pdf"
        );
}
function downloadResume(){

    const content =
        document.getElementById(
            "resumeResult"
        );

    html2pdf()
        .from(content)
        .save(
            "Resume_Analysis.pdf"
        );
}
function downloadPlan(){

    const content =
        document.getElementById(
            "planResult"
        );

    html2pdf()
        .from(content)
        .save(
            "Study_Plan.pdf"
        );
}
function toggleMenu(){
  const navLinks =
        document.getElementById(
            "navLinks"
        );

    navLinks.classList.toggle(
        "active"
    );
}