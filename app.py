import gradio as gr
import PyPDF2

def analyze_resume_and_jd(resume_file, jd_file):
    if resume_file is None or jd_file is None:
        return {}, "Please upload both files.", ""

    # Extract text from resume PDF
    try:
        pdf_reader = PyPDF2.PdfReader(resume_file)
        resume_text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
    except Exception as e:
        return {}, f"Error reading resume: {str(e)}", ""

    # Extract text from job description TXT file
    try:
        with open(jd_file, 'r', encoding='utf-8') as f:
            jd_text = f.read()
    except Exception as e:
        return {}, f"Error reading job description: {str(e)}", ""

    # Simple word overlap similarity
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    common_words = resume_words & jd_words
    similarity = len(common_words) / len(jd_words) * 100 if jd_words else 0

    extracted_entities = {
        "Skills Mentioned": list(common_words)[:10]
    }

    return extracted_entities, f"{similarity:.2f}%", jd_text[:300] + ("..." if len(jd_text) > 300 else "")

iface = gr.Interface(
    fn=analyze_resume_and_jd,
    inputs=[
        gr.File(label="Upload Resume (PDF)", type="filepath"),
        gr.File(label="Upload Job Description (TXT)", type="filepath")
    ],
    outputs=[
        gr.JSON(label="Extracted Entities"),
        gr.Textbox(label="Resume and Job Description Similarity"),
        gr.Textbox(label="Job Description Text")
    ],
    title="Resume and Job Description Analyzer",
    description="Upload your PDF resume and TXT job description to calculate similarity."
)

iface.launch()