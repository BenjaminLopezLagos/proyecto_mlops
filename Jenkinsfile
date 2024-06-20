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
        stage('Setup Container') {
            steps {
                sh '''
                   docker build -t potato-detector-project .
                   docker run -d --name potato potato-detector-project
                '''
            }
        }
    }
}