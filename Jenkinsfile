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
                   dvc remote add origin s3://dvc
                   dvc remote modify origin endpointurl https://dagshub.com/benjamin.lopezl/proyecto_mlops.s3
                '''
                sh("dvc remote modify origin --local access_key_id $DH_S3_KEY")
                sh("dvc remote modify origin --local secret_access_key $DH_S3_KEY")
                sh("dvc pull -r origin")
            }
        }
    }
}