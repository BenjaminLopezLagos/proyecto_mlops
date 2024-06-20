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
                   docker exec dind git clone https://${GITHUB_KEY}@github.com/BenjaminLopezLagos/proyecto_mlops.git
                '''
            }
        }
        stage('Build from image') {
            steps {
                sh '''
                   docker exec dind docker build -t potato-detector-dev .
                   docker exec dind docker run -d --name potato-container potato-detector-dev
                '''
            }
        }
        stage('Get dataset and models') {
            steps {
                sh '''
                   docker exec dind dvc version
                   docker exec dind dvc remote modify origin --local access_key_id ${DH_S3_KEY}
                   docker exec dind dvc remote modify origin --local secret_access_key ${DH_S3_KEY}
                   docker exec dind dvc pull -r origin
                '''
            }
        }
    }
}