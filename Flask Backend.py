from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import logging
import pdfkit
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/test_suite'
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(filename='test_execution.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

class TestStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_case.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    selector_type = db.Column(db.String(50), nullable=False)
    selector_value = db.Column(db.String(255), nullable=False)
    input_data = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, nullable=False)

db.create_all()

@app.route('/test_cases', methods=['POST'])
def create_test_case():
    data = request.json
    test_case = TestCase(name=data['name'], description=data.get('description'))
    db.session.add(test_case)
    db.session.commit()
    logging.info(f"Created test case: {test_case.name}")
    return jsonify({'message': 'Test case created', 'id': test_case.id})

@app.route('/test_cases', methods=['GET'])
def get_test_cases():
    cases = TestCase.query.all()
    return jsonify([{'id': case.id, 'name': case.name, 'description': case.description} for case in cases])

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    logging.info(f"File uploaded: {file_path}")
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path})

@app.route('/execute/<int:test_case_id>', methods=['POST'])
def execute_test_case(test_case_id):
    test_case = TestCase.query.get(test_case_id)
    if not test_case:
        return jsonify({'error': 'Test case not found'}), 404
    
    steps = TestStep.query.filter_by(test_case_id=test_case_id).order_by(TestStep.order).all()
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(options=options)
    driver.maximize_window()
    
    logging.info(f"Executing test case: {test_case.name}")
    execution_log = []
    
    try:
        for step in steps:
            if step.action == 'click':
                element = driver.find_element(getattr(By, step.selector_type.upper()), step.selector_value)
                element.click()
                message = f"Clicked element: {step.selector_value}"
            elif step.action == 'input':
                element = driver.find_element(getattr(By, step.selector_type.upper()), step.selector_value)
                element.send_keys(step.input_data)
                message = f"Entered input: {step.input_data} into {step.selector_value}"
            elif step.action == 'upload':
                element = driver.find_element(getattr(By, step.selector_type.upper()), step.selector_value)
                element.send_keys(step.file_path)
                message = f"Uploaded file: {step.file_path} to {step.selector_value}"
            else:
                message = f"Unknown action: {step.action}"
            
            logging.info(message)
            execution_log.append(message)
        
        report_path = generate_report(test_case.name, execution_log)
        return jsonify({'message': 'Test executed successfully', 'report': report_path})
    except Exception as e:
        error_message = f"Test execution failed: {str(e)}"
        logging.error(error_message)
        return jsonify({'error': error_message})
    finally:
        driver.quit()
        logging.info("Test execution completed")


def generate_report(test_case_name, execution_log):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_html = f"""
    <html>
    <head><title>Test Report - {test_case_name}</title></head>
    <body>
    <h1>Test Report - {test_case_name}</h1>
    <p>Execution Time: {timestamp}</p>
    <ul>
    {''.join(f'<li>{log}</li>' for log in execution_log)}
    </ul>
    </body>
    </html>
    """
    
    report_html_path = f"reports/{test_case_name}_{timestamp}.html"
    os.makedirs('reports', exist_ok=True)
    with open(report_html_path, 'w') as report_file:
        report_file.write(report_html)
    
    report_pdf_path = report_html_path.replace('.html', '.pdf')
    pdfkit.from_file(report_html_path, report_pdf_path)
    return report_pdf_path

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    app.run(debug=True)
