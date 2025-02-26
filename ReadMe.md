# Universal Software Testing Suite

## **Overview**
The Universal Software Testing Suite is a robust, AI-powered test automation framework that supports cross-browser testing, professional reporting, and data-driven test execution. It is built using **Python, Selenium, Flask, React, MySQL, and ExtentReports**, with easy deployment via Docker.

## **Features**
- **Cross-Browser Support**: Works with Chrome, Edge, Firefox, and more.
- **AI-Powered Element Detection**: Ensures robust test execution across layouts.
- **Professional Reports**: Generates HTML/PDF reports with logs and screenshots.
- **File Upload Testing**: Automates validation of file submissions.
- **Portable & Scalable**: Fully Dockerized for deployment flexibility.
- **Web-Based UI for Test Case Management**: Built with React & Flask.
- **Configurable Execution**: Supports CSV, JSON, and database-driven test data.

## **Installation & Setup**
### **Prerequisites**
- Python 3.8+
- Node.js & npm (for the React frontend)
- Docker & Docker Compose
- MySQL

### **Clone the Repository**
```bash
git clone https://github.com/your-username/universal-testing-suite.git
cd universal-testing-suite
```

### **Run Using Docker**
```bash
docker-compose up --build
```
This will start the MySQL database, Flask backend, and React frontend.

### **Providing Database Credentials**
To set the MySQL database password, configure the environment variables in the `.env` file or pass them directly when running the container:
```bash
MYSQL_ROOT_PASSWORD=my-secret-password
MYSQL_USER=test_user
MYSQL_PASSWORD=test_password
MYSQL_DATABASE=testing_db
```
Ensure that these values are used consistently in both the Flask backend and the database configuration.

### **Manual Setup (Without Docker)**
#### **Backend (Flask API)**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
#### **Frontend (React UI)**
```bash
cd frontend
npm install
npm start
```

## **Usage**
1. **Access the Web UI**: Open `http://localhost:3000` in your browser.
2. **Create Test Cases**: Define test scenarios via the UI.
3. **Execute Tests**: Run tests on selected browsers.
4. **View Reports**: Navigate to `/app/reports/` to see test results.

## **Environment Variables**
Configure the following environment variables as needed:
```bash
BROWSER=chrome  # Options: chrome, edge, firefox
TEST_URL=https://example.com  # The target application URL
```

## **Running Tests via CLI**
```bash
python run_tests.py --browser chrome --url https://example.com
```

## **Future Enhancements**
- Parallel test execution
- API testing integration
- AI-based self-healing tests

## **License**
This project is licensed under the MIT License.

## **Contributing**
Contributions are welcome! Please submit a pull request or open an issue.

