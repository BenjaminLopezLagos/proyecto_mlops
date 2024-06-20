pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh '''
                   python3 -m venv venv
                   . venv/bin/activate
                   pip install --upgrade pip
                   pip install --no-cache-dir -r requirements.txt
                '''
            }
        }
    }
}