# 🤖 R&D Proposal Auto-Evaluator

An AI-powered screening tool built with Streamlit and Google's Gemini API to automate the initial evaluation of research and development proposals. This project was developed for the Smart India Hackathon (SIH) to address the challenges of manual, time-intensive, and subjective proposal reviews.

![App Screenshot](https://github.com/Dev-A-17/R-D-Proposal-Auto-Evaluator/blob/64a75e3cf83662341cab800b446bbcce39580971/App_Scr.jpeg)

---

## ## 📋 Description

This application serves as a proof-of-concept for an intelligent evaluation system designed to assist organizations like NaCCER (the R&D arm of CIL). It ingests R&D proposals in PDF format and performs a multi-faceted analysis, providing a comprehensive initial screening report in seconds. The goal is to reduce manual effort, eliminate bias, and accelerate the decision-making process for funding high-potential research.

---

## ## ✨ Features

* **AI-Powered Evaluation:** Leverages a large language model with a detailed, rubric-based prompt to score proposals on **Clarity**, **Novelty**, and **Feasibility**.
* **Objective Justification:** The AI provides not just scores, but also detailed textual justifications for its ratings, along with a summary of the proposal's key strengths and weaknesses.
* **Interactive Dashboard:** A clean, professional user interface built with Streamlit, featuring a dashboard layout with columns and bordered containers.
* **Score Visualization:** Automatically generates a bar chart for an at-a-glance understanding of the proposal's evaluation scores.
* **Database-Driven Novelty Check:** Implements an advanced novelty check by converting proposals into vector embeddings and comparing them against a local database of past projects to calculate an originality score.
* **Secure API Key Management:** Uses a `.env` file to securely manage the Google API key, keeping it separate from the source code.

---

## ## ⚙️ Setup and Installation

Follow these steps to set up the project locally.

### ### 1. Prerequisites

* [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.
* Python 3.9+

### ### 2. Installation Steps

1.  **Clone the repository (or download the source code):**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and activate the Conda environment:**
    ```bash
    conda create --name sih_env python=3.9 -y
    conda activate sih_env
    ```

3.  **Install the required packages:**
    The following command uses the full path to the Python interpreter within the environment to ensure packages are installed correctly, which is recommended for some system configurations.
    ```bash
    # For macOS/Linux
    /opt/anaconda3/envs/sih_env/bin/python -m pip install -r requirements.txt

    # For most systems, a simpler command may also work:
    # python -m pip install -r requirements.txt
    ```

---

## ## 🔑 Configuration

Before running the application, you need to configure your API key and set up the local database.

### ### 1. API Key Setup

1.  Create a file named `.env` in the root of the project folder.
2.  Add your Google AI Studio API key to this file in the following format:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
3.  The project's `.gitignore` file should include `.env` to prevent your secret key from being committed to version control.

### ### 2. Database Setup

1.  Create a folder named `database` in the root of the project folder.
2.  Place one or more sample R&D proposals (in PDF format) inside this `database` folder. These will be used as the baseline for the novelty check.

---

## ## 🚀 How to Run

1.  Make sure your Conda environment is active:
    ```bash
    conda activate sih_env
    ```

2.  Run the Streamlit application using the full-path command:
    ```bash
    # For macOS/Linux
    /opt/anaconda3/envs/sih_env/bin/python -m streamlit run app.py

    # Or the simpler version for most systems:
    # streamlit run app.py
    ```

3.  The application will open in a new tab in your web browser.

---

## ## 📁 Project Structure

```
R-D-Evaluator/
├── 📂 database/
│   └── 📜 Sample1.pdf
├── 📜 .env
├── 📜 .gitignore
├── 📜 app.py
├── 📜 evaluator.py
├── 📜 novelty_checker.py
├── 📜 pdf_reader.py
├── 📜 requirements.txt
└── 📜 README.md
```
