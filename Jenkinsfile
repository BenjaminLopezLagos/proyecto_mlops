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
            }
        }
        stage ('Test API') {
            agent {
                docker {
                    image 'potato-dev'
                    reuseNode true
                }
            }
            steps {
                sh 'python -m pytest /app/tests/'
            }
        }
        stage('Get_data_and_test_models'){
            agent {
                docker {
                    image 'potato-dev'
                    reuseNode true
                }
            }
            stages{
                stage('Get dataset and models') {
                    steps {
                        sh 'dvc remote modify origin --local access_key_id ${DH_S3_KEY}'
                        sh 'dvc remote modify origin --local secret_access_key ${DH_S3_KEY}'
                        sh 'dvc pull -r origin'
                    }
                }
                stage('train_test_model') {
                    steps {
                        sh 'dagshub login --token ${DH_S3_KEY}'
                        sh 'dvc exp run'
                    }
                }
                stage('convert to onnx'){
                    steps {
                        sh 'python to_onnx.py'
                    }
                }
            }
        }
    }
}