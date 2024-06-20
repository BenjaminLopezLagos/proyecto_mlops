pipeline {
    agent any
    environment {
        GITHUB_KEY = credentials('github_token')
        DH_S3_KEY = credentials('dagshub_token')
    }
    stages {
        stage('Checkout') {
            steps {
                sh '''
                   git clone https://${GITHUB_KEY}@github.com/BenjaminLopezLagos/proyecto_mlops.git
                   docker build -t potato-detector-dev .
                   docker run -d -p 5000:5000 --name potato_container potato-detector-dev
                '''
            }
        }
        stage('Get dataset and models') {
            steps {
                sh '''
                   docker container exec potato_container dvc version
                   docker container exec potato_container dvc remote modify origin --local access_key_id ${DH_S3_KEY}
                   docker container exec potato_container dvc remote modify origin --local secret_access_key ${DH_S3_KEY}
                   docker container exec potato_container dvc pull -r origin
                '''
            }
        }
        stage('train_test_model') {
            steps {
                sh '''
                   docker container exec potato_container dagshub login --token ${DH_S3_KEY}
                   docker container exec potato_container dvc exp run
                '''
            }
        }
        stage('convert to onnx'){
            steps {
                sh '''
                   docker container exec potato_container python to_onnx.py
                '''
            }
        }
    }
}