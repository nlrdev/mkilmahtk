pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'cp ./_prod/nginx.conf ./nginx/nginx.conf'
                sh 'docker-compose -f production.yml down'
                sh 'docker volume rm mkilmahtk_website_data'
                sh 'docker-compose -f production.yml build --no-cache'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose -f production.yml up -d --force-recreate'
            }
        }
    }
}
