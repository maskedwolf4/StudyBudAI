# 🎧 StudyBud AI - AI-Powered Quiz Generator & LLMOps Pipeline

StudyBud AI is an interactive, LLM-powered educational platform designed to automatically generate customized quizzes (Multiple Choice Questions and Fill-in-the-blank) based on any topic, difficulty level, and question count. Built with **Streamlit**, **LangChain**, and the **Groq API**, it features a complete automated **CI/CD and GitOps deployment pipeline** leveraging **Docker**, **Jenkins**, **Kubernetes**, and **ArgoCD**.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [Application Architecture](#-application-architecture)
- [Getting Started (Local Development)](#-getting-started-local-development)
  - [Prerequisites](#prerequisites)
  - [Installation & Execution](#installation--execution)
  - [Environment Variables](#environment-variables)
- [🐳 Docker Setup](#-docker-setup)
- [☸️ Kubernetes Infrastructure](#️-kubernetes-infrastructure)
- [🚀 Comprehensive Deployment Guide (CI/CD & GitOps)](#-comprehensive-deployment-guide-cicd--gitops)
  - [Deployment Workflow Overview](#deployment-workflow-overview)
  - [Jenkins Pipeline Breakdown](#jenkins-pipeline-breakdown)
  - [ArgoCD GitOps Sync](#argocd-gitops-sync)
  - [Required Jenkins Credentials](#required-jenkins-credentials)
- [🛠️ Troubleshooting & Notes](#️-troubleshooting--notes)

---

## ✨ Features

- **Dynamic Quiz Generation**: Generate quizzes on any subject (e.g., Science, History, Programming) in seconds.
- **Multiple Question Types**:
  - **Multiple Choice Questions (MCQs)** with 4 options and validated correct answers.
  - **Fill in the Blank Questions** with structured validation.
- **Customizable Parameters**: Select difficulty level (Easy, Medium, Hard) and question quantity (1–10).
- **Interactive Quiz Interface**: Clean Streamlit UI for attempting questions with real-time state management.
- **Automated Grading & Detailed Analysis**: Instant score calculation percentage and question-by-question breakdown of correct vs. incorrect answers.
- **CSV Export**: Export and download quiz results with timestamps for record-keeping.
- **Production-Ready CI/CD & GitOps**: Automated container building, Docker Hub pushing, manifest versioning, and ArgoCD deployment sync.

---

## 🛠️ Tech Stack

### Application Layer
- **UI Framework**: [Streamlit](https://streamlit.io/)
- **LLM Integration & Prompts**: [LangChain](https://www.langchain.com/) & [LangChain-Groq](https://python.langchain.com/docs/integrations/chat/groq/)
- **LLM Provider**: [Groq API](https://groq.com/) (High-speed inference models)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/) (`BaseModel`, `PydanticOutputParser`)
- **Data Processing**: [Pandas](https://pandas.pydata.org/)
- **Logging & Error Handling**: Custom Python logger and custom exception handlers

### DevOps & Deployment Layer
- **Containerization**: [Docker](https://www.docker.com/)
- **Orchestration**: [Kubernetes](https://kubernetes.io/) (Deployments & Services)
- **Continuous Integration**: [Jenkins](https://www.jenkins.io/) (Declarative Pipeline)
- **Continuous Deployment / GitOps**: [ArgoCD](https://argo-cd.readthedocs.io/)
- **Image Registry**: [Docker Hub](https://hub.docker.com/)

---

## 📁 Repository Structure

```text
StudyBudAI/
├── application.py            # Streamlit web application entry point & session management
├── Dockerfile                # Multi-stage/slim Docker container build definition
├── jenkinsfile               # Jenkins CI/CD automation pipeline script
├── setup.py                  # Package installation script
├── requiremnets.txt          # Python dependencies specification
├── README.md                 # Project documentation
├── manifests/                # Kubernetes deployment configuration files
│   ├── deployment.yaml       # K8s Deployment specification (2 replicas, secret mounting)
│   └── service.yaml          # K8s Service specification (NodePort routing port 80 -> 8501)
└── src/                      # Core application source code
    ├── common/
    │   ├── custom_exception.py  # Structured traceback & exception formatting
    │   └── logger.py            # File logging system (logs/ directory output)
    ├── config/
    │   └── settings.py          # Centralized configuration loader for env variables
    ├── generator/
    │   └── question_generator.py # Core Quiz generator with retry logic & Pydantic parsing
    ├── llm/
    │   └── groq_client.py       # Groq LLM initialization wrapper via LangChain
    ├── models/
    │   └── question_schema.py   # Pydantic data schemas for MCQ and Fill-in-the-blank
    ├── prompts/
    │   └── templates.py         # Prompt templates enforcing JSON responses
    └── utils/
        └── helpers.py           # QuizManager class for state management, grading & CSV export
```

---

## 🏗️ Application Architecture

The application operates as a modular, object-oriented Streamlit web application:

```mermaid
flowchart TD
    User([User Streamlit UI]) -->|1. Selects Topic & Difficulty| Application[application.py]
    Application -->|2. Calls generate_questions| QuizManager[QuizManager - src/utils/helpers.py]
    QuizManager -->|3. Invokes| Generator[QuestionGenerator - src/generator/question_generator.py]
    Generator -->|4. Formats Prompt| PromptTemplates[Prompt Templates - src/prompts/templates.py]
    Generator -->|5. Queries LLM| GroqClient[Groq LLM Client - src/llm/groq_client.py]
    GroqClient -->|6. API Request| GroqAPI[Groq API Services]
    GroqAPI -->|7. JSON Response| Generator
    Generator -->|8. Validates with Pydantic| Schemas[Schemas - src/models/question_schema.py]
    Schemas -->|9. Parsed Object| QuizManager
    QuizManager -->|10. Render & Grade| Application
    Application -->|11. Export CSV| CSV[results/quiz_results_*.csv]
```

### Key Execution Highlights
1. **Retry Mechanism**: `QuestionGenerator` includes automated retries (`MAX_RETRIES`) if LLM outputs fail Pydantic validation or JSON parsing.
2. **Schema Enforcement**:
   - `MCQQuestion`: Ensures exactly 4 options exist and `correct_answer` is present in options.
   - `FillBlankQuestion`: Ensures `___` placeholder exists in the generated question text.
3. **Session State Handling**: `QuizManager` preserves current quiz questions, user choices, submission status, and evaluation results across Streamlit rerun cycles.

---

## ⚙️ Getting Started (Local Development)

### Prerequisites
- Python 3.10 or higher
- A valid **Groq API Key** (Get one at [console.groq.com](https://console.groq.com/))

### Installation & Execution

1. **Clone the repository**:
   ```bash
   git clone https://github.com/maskedwolf4/StudyBudAI.git
   cd StudyBudAI
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requiremnets.txt
   pip install -e .
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   MODEL_NAME=llama-3.3-70b-versatile
   TEMPERATURE=0.7
   MAX_RETRIES=3
   ```

5. **Launch the Streamlit Application**:
   ```bash
   streamlit run application.py
   ```
   Open your browser and navigate to `http://localhost:8501`.

---

## 🐳 Docker Setup

The application is containerized using a lightweight Debian-based Python image (`python:3.10-slim-bookworm`).

### Building the Image Locally
```bash
docker build -t studybudai:local .
```

### Running the Container Locally
```bash
docker run -d \
  -p 8501:8501 \
  -e GROQ_API_KEY="your_groq_api_key" \
  -e MODEL_NAME="llama-3.3-70b-versatile" \
  -e TEMPERATURE="0.7" \
  -e MAX_RETRIES="3" \
  --name studybudai-app \
  studybudai:local
```
Access the application at `http://localhost:8501`.

---

## ☸️ Kubernetes Infrastructure

The application deployment is fully defined using declarative Kubernetes manifests located in `manifests/`.

### 1. Deployment (`manifests/deployment.yaml`)
- **Replicas**: 2 pods for high availability.
- **Port**: Container listens on port `8501`.
- **Secret Integration**: Secret `groq-api-secret` injects `GROQ_API_KEY` into the container environment.

### 2. Service (`manifests/service.yaml`)
- **Type**: `NodePort`
- **Port Mapping**: Exposes internal container port `8501` through service port `80`.

### Manual Kubernetes Deployment Setup

1. **Create the Kubernetes Secret for Groq API**:
   ```bash
   kubectl create secret generic groq-api-secret \
     --from-literal=GROQ_API_KEY="your_actual_groq_api_key"
   ```

2. **Apply Manifests to Cluster**:
   ```bash
   kubectl apply -f manifests/deployment.yaml
   kubectl apply -f manifests/service.yaml
   ```

3. **Verify Deployment**:
   ```bash
   kubectl get pods -l app=llmops-app
   kubectl get svc llmops-service
   ```

---

## 🚀 Comprehensive Deployment Guide (CI/CD & GitOps)

StudyBud AI implements an automated **CI/CD and GitOps deployment pipeline**. Code pushes to the `main` branch automatically build new container images, update Kubernetes deployment specifications, commit changes to Git, and trigger **ArgoCD** to synchronize the cluster.

### Deployment Workflow Overview

```mermaid
flowchart LR
    A[Developer Push to GitHub] -->|Triggers Pipeline| B[Jenkins CI Server]
    B -->|Stage 1: Checkout| C[GitHub Repository]
    B -->|Stage 2: Build Image| D[Docker Build]
    B -->|Stage 3: Push Image| E[Docker Hub Registry]
    B -->|Stage 4: Update Tag| F[manifests/deployment.yaml]
    B -->|Stage 5: Git Commit & Push| C
    B -->|Stage 6 & 7: Trigger Sync| G[ArgoCD Controller]
    G -->|Pulls updated manifest| C
    G -->|Applies Deployment| H[Kubernetes Cluster]
```

---

### Jenkins Pipeline Breakdown (`jenkinsfile`)

The `jenkinsfile` defines a 7-stage automated pipeline:

#### **Stage 1: Checkout Github**
Clones the latest code from `https://github.com/maskedwolf4/StudyBudAI.git` on branch `main` using Jenkins credentials `github-token`.

#### **Stage 2: Build Docker Image**
Builds the Docker container image tagged dynamically using the Jenkins build number (`v${BUILD_NUMBER}`):
```groovy
dockerImage = docker.build("maskedwol4/studybudai:v${BUILD_NUMBER}")
```

#### **Stage 3: Push Image to DockerHub**
Authenticates against Docker Hub using `dockerhub-token` credentials and pushes the newly built image version:
```groovy
docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-token') {
    dockerImage.push("v${BUILD_NUMBER}")
}
```

#### **Stage 4: Update Deployment YAML with New Tag**
Modifies the container image tag inside `manifests/deployment.yaml` in-place using `sed`:
```bash
sed -i 's|image: maskedwol4/studybudai:.*|image: maskedwol4/studybudai:v${BUILD_NUMBER}|' manifests/deployment.yaml
```

#### **Stage 5: Commit & Push Updated Manifest (GitOps Pattern)**
Configures Git identity, commits the updated `manifests/deployment.yaml`, and pushes the updated manifest back to the GitHub repository. This ensures the Git repo remains the single source of truth:
```bash
git config user.name "maskedwolf"
git config user.email "meetwadekar7@gmail.com"
git add manifests/deployment.yaml
git commit -m "Update image tag to v${BUILD_NUMBER}"
git push https://${GIT_USER}:${GIT_PASS}@github.com/maskedwolf4/StudyBudAI.git HEAD:main
```

#### **Stage 6: CLI Tool Setup (`kubectl` & `argocd`)**
Downloads and installs the required `kubectl` and `argocd` command-line binaries on the Jenkins worker node if not present.

#### **Stage 7: Apply & Sync App with ArgoCD**
Connects to the target Kubernetes cluster using the `kubeconfig` Jenkins credential, logs into ArgoCD, and executes a sync operation on the `study` ArgoCD application:
```bash
argocd login 34.45.193.5:31704 --username admin --password $(kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d) --insecure
argocd app sync study
```

---

### ArgoCD GitOps Sync

**ArgoCD** continuously monitors the `manifests/` folder in the GitHub repository `maskedwolf4/StudyBudAI`.
- **Application Name**: `study`
- **Target Namespace**: Default cluster namespace (or custom defined)
- When Jenkins commits the new image tag to `manifests/deployment.yaml`, ArgoCD detects out-of-sync status and automatically (or via `argocd app sync study`) performs a zero-downtime rolling update on the Kubernetes cluster.

---

### Required Jenkins Credentials

To run the pipeline successfully, configure the following credentials in **Jenkins -> Manage Jenkins -> Credentials**:

| Credential ID | Type | Description |
| :--- | :--- | :--- |
| `dockerhub-token` | Username with Password / Secret Text | Docker Hub access token or password for pushing images |
| `github-token` | Username with Password / Personal Access Token | GitHub PAT with repo write permissions to commit updated manifests |
| `kubeconfig` | Kubeconfig file / Secret text | Access configuration for the target Kubernetes cluster |

---

## 📋 Environment Variables Reference

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | *(Required)* | API key for authentication with Groq Cloud services |
| `MODEL_NAME` | `llama-3.3-70b-versatile` | LLM model identifier on Groq |
| `TEMPERATURE` | `0.7` | Sampling temperature for LLM generation randomness |
| `MAX_RETRIES` | `3` | Maximum retry attempts for failed parsing/schema validations |

---

## 🛠️ Troubleshooting & Notes

1. **Kubernetes Secret Missing**:
   If the app fails to start in Kubernetes with `CreateContainerConfigError`, ensure the secret `groq-api-secret` exists in the cluster before deployment.

2. **Jenkins Git Push Errors**:
   If Stage 5 fails during `git push`, verify that the GitHub token associated with `github-token` in Jenkins has `repo` write permissions and workflows access.

3. **ArgoCD Login Failures**:
   Ensure the IP `34.45.193.5:31704` specified in `jenkinsfile` is reachable from the Jenkins worker node and that ArgoCD initial admin credentials are valid.

