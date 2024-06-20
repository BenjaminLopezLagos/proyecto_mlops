pipeline {
    agent any
    environment {
        GITHUB_KEY = credentials('github_token')
        DH_S3_KEY = credentials('dagshub_token')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                bat 'docker compose up -d --build'
            }
        }
        stage ('Test API') {
            steps {
                bat 'docker container exec potato_container python -m pytest app/tests/'
            }
        }
        stage('Get dataset and models') {
            steps {
                bat 'docker container exec potato_container dvc version'
                bat 'docker container exec potato_container dvc remote modify origin --local access_key_id ${DH_S3_KEY}'
                bat 'docker container exec potato_container dvc remote modify origin --local secret_access_key ${DH_S3_KEY}'
                bat 'docker container exec potato_container dvc pull -r origin'
            }
        }
        stage('train_test_model') {
            steps {
                bat 'docker container exec potato_container dagshub login --token ${DH_S3_KEY}'
                bat 'docker container exec potato_container dvc exp run'
            }
        }
        stage('convert to onnx'){
            steps {
                bat 'docker container exec potato_container python to_onnx.py'
            }
        }
    }
}