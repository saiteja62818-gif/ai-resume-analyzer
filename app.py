import streamlit as st
import PyPDF2

# Skill list
skills_list = [
    "python", "java", "sql", "aws", "machine learning", "excel",
    "cloud", "salesforce", "linux", "html", "css", "javascript",
    "react", "node", "git", "github", "data analysis", "power bi",
    "tableau", "testing", "automation", "selenium"
]

# Extract text from PDF
def extract_text(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text.lower()

# Extract skills
def extract_skills(text):
    found_skills = set()
    for skill in skills_list:
        if skill in text:
            found_skills.add(skill)
    return list(found_skills)

# Match score
def match_score(resume_skills, job_skills):
    if len(job_skills) == 0:
        return 0
    match = len(set(resume_skills) & set(job_skills))
    return round((match / len(job_skills)) * 100, 2)

# UI
st.title("🚀 AI Resume Analyzer")
st.markdown("### Analyze your resume and match with job roles instantly")
st.markdown("---")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_role = st.text_input("Enter Job Role (e.g., python developer, data analyst)")

if uploaded_file and job_role:
    text = extract_text(uploaded_file)

    if not text:
        st.error("Unable to read resume. Try another PDF.")
        st.stop()

    resume_skills = extract_skills(text)

    job_skills_map = {
        "python developer": ["python", "sql", "aws"],
        "data analyst": ["excel", "sql", "python"],
        "cloud engineer": ["aws", "cloud", "linux"],
        "java developer": ["java", "sql"],
        "salesforce developer": ["salesforce", "apex", "soql"],
        "software tester": ["testing", "sql"]
    }

    job_skills = job_skills_map.get(job_role.lower().strip(), [])
    if not job_skills:
       st.error("⚠️ Job role not found. Please enter a valid role like 'python developer'")
       st.stop()

    score = match_score(resume_skills, job_skills)
    missing = set(job_skills) - set(resume_skills)

    # Results
    st.markdown("## 📌 Results")

    st.markdown("### ✅ Extracted Skills")
    st.success(", ".join(resume_skills) if resume_skills else "No skills detected")

    st.markdown("### 📊 Match Score")
    st.info(str(score) + "%")

    if score >= 80:
        st.success("🔥 Excellent match! You are job ready.")
    elif score >= 50:
        st.warning("⚡ Average match. Improve missing skills.")
    else:
        st.error("❌ Low match. You need to upskill.")

    st.markdown("### ❌ Missing Skills")
    st.warning(", ".join(missing) if missing else "No missing skills 🎉")

    if missing:
        st.markdown("### 💡 Suggestions")
        st.write("You should learn:", ", ".join(missing))
    else:
        st.success("Your profile is a strong match!")

st.markdown("---")
st.markdown("Made by Sai Teja 🚀")