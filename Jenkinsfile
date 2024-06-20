pipeline {
    agent {
        dockerfile true
    }
    environment {
        DH_S3_KEY = credentials('dagshub_token')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Get dataset and models') {
            steps {
                sh '''
                   dvc version
                   dvc remote modify origin --local access_key_id ${DH_S3_KEY}
                   dvc remote modify origin --local secret_access_key ${DH_S3_KEY}
                   dvc pull -r origin
                '''
            }
        }
    }
}