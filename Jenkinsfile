pipeline {
    agent any
    environment {
        DH_S3_KEY = credentials('dagshub_token')
    }
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
        stage('Get dataset and models') {
            steps {
                sh '''
                   . venv/bin/activate
                   dvc version
                   dvc remote modify origin --local access_key_id ${DH_S3_KEY}
                   dvc remote modify origin --local secret_access_key ${DH_S3_KEY}
                   dvc pull -r origin
                '''
            }
        }
        stage('train_test_model') {
            steps {
                sh '''
                   . venv/bin/activate
                   dvc exp run
                '''
            }
        }
        stage('convert to onnx'){
            steps {
                sh '''
                   . venv/bin/activate
                   python to_onnx.py
                '''
            }
        }
    }
}