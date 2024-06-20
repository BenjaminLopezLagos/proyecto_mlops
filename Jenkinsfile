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
                bat 'docker build -t potato-detector-dev .'
                bat 'docker stop potato_container || true'
                bat 'docker rm potato_container || true'
                bat 'docker run -d -p 5000:5000 --name potato_container potato-detector-dev'
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