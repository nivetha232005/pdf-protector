A production-ready full-stack PDF management platform that allows users to securely upload, modify, protect, and download PDF files.

## Features

- 🔒 **Password Protection**: Encrypt PDFs with strong AES encryption
- 🔓 **Remove Password**: Unlock password-protected PDFs
- 📚 **Merge PDFs**: Combine multiple PDFs into one document
- ✂️ **Split PDF**: Extract specific pages or page ranges
- 📦 **Compress PDF**: Reduce file size while maintaining quality
- 🔄 **Rotate PDF**: Rotate all or selected pages
- 🌓 **Dark Mode**: Toggle between light and dark themes
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile

## Tech Stack

### Frontend
- React.js
- CSS3 (Pure CSS, no frameworks)
- Axios for API calls
- React Router for navigation

### Backend
- Flask (Python)
- pikepdf for PDF processing
- Flask-CORS for cross-origin requests
- REST API architecture

## Installation

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/441867d4-87f7-4244-8caa-bac3bed665e9" />

