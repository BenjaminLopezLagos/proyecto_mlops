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
        stage('Build') {
            steps {
                sh 'docker build -t potato-dev .'
                sh 'docker stop potato_container || true'
                sh 'docker rm potato_container || true'
                // sh 'docker run -d -p 5000:5000 --name potato_container potato-dev'
                // Aquí especificamos que el contenedor debe usar la GPU
                sh 'docker run -d --gpus all -p 5000:5000 --name potato_container potato-dev'
            }
        }
        stage ('Test API') {
            steps {
                sh 'docker container exec potato_container python -m pytest /app/tests/'
            }
        }
        stage('Get dataset and models') {
            steps {
                sh 'docker container exec potato_container dvc version'
                sh 'docker container exec potato_container dvc remote modify origin --local access_key_id ${DH_S3_KEY}'
                sh 'docker container exec potato_container dvc remote modify origin --local secret_access_key ${DH_S3_KEY}'
                sh 'docker container exec potato_container dvc pull -r origin'
            }
        }
        stage('train_test_model') {
            steps {
                sh 'docker container exec potato_container dagshub login --token ${DH_S3_KEY}'
                sh 'docker container exec potato_container dvc exp run'
            }
        }
        stage('convert to onnx'){
            steps {
                sh 'docker container exec potato_container python to_onnx.py'
            }
        }
    }
}