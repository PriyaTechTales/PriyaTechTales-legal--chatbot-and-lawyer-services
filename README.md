# ⚖️ Design and Development of Legal Chatbot & Lawyer Services for Rural India

This project is a **full-stack web application** designed to bridge the gap between rural citizens and legal professionals by providing *AI-powered legal assistance* and *lawyer consultation services*. It integrates **Natural Language Processing (NLP)** for understanding user queries and **Django** for managing backend operations efficiently.

> **Tech Stack:** Django | HTML | CSS | JavaScript | NLP | SQLite | scikit-learn

---

## 🚀 Features

* **AI-Powered Legal Chatbot**

  * Answers common legal questions related to civil, criminal, property, and government laws.
  * Uses NLP to understand and respond to user queries intelligently.
  * Provides accurate and easy-to-understand legal information for rural users.

* **Lawyer Services**

  * Allows users to connect with verified lawyers for legal advice.
  * Provides lawyer profiles, availability, and contact options.

* **Multilingual Support**

  * Offers responses in English and regional languages for accessibility.

* **User-Friendly Interface**

  * Simple and responsive design for mobile and desktop users.
  * Built using HTML, CSS, and JavaScript.

* **Secure Backend**

  * Developed using Django for efficient data management and secure communication.
  * Stores chat history, user details, and lawyer information in SQLite database.

---

## 🧠 How It Works

### 1. Legal Chatbot Module

* User types a legal question (e.g., *“How to file an FIR?”*).
* The NLP model processes the query and identifies relevant legal category.
* Chatbot returns a detailed and reliable answer from the trained dataset.

### 2. Lawyer Service Module

* User searches for a lawyer based on *case type* or *location*.
* System displays a list of available lawyers with their contact details.
* User can schedule a consultation or request a callback.

---

## 🛠 Technology Stack

| Layer     | Tools Used                                  |
| --------- | ------------------------------------------- |
| Frontend  | HTML, CSS, JavaScript                       |
| Backend   | Django (v4.x or higher)                     |
| Database  | SQLite                                      |
| NLP Model | scikit-learn / spaCy (for intent detection) |
| Framework | Django REST Framework (for APIs)            |

---

## ⚙️ Steps or Commands to Run the Project

1. **Download** the project ZIP file and extract it.
2. **Open** the extracted folder in VSCode.
3. **Open Terminal** in VSCode.
4. **Navigate** to the project directory using:

   ```bash
   cd legal_chatbot_project
   ```
5. **Run the Django development server:**

   ```bash
   python manage.py runserver
   ```
6. **Open the provided URL** (usually `http://127.0.0.1:8000/`) in a browser to access the application.

---

## 📦 Requirements

### **Python:** 3.10+

### **Django:** 4.x+

### **Python Libraries:**

```bash
numpy>=1.21.0  
pandas>=1.3.0  
scikit-learn>=1.0.0  
joblib>=1.2.0  
nltk>=3.6.0  
spacy>=3.0.0  
django>=4.0.0  
