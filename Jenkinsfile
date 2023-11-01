pipeline {
    agent any

    options {
        withFolderProperties()
    }

    stages {
        stage('Deploy') {
            steps {
                withCredentials([string(credentialsId: 'CONNECTION_STRING', variable: 'CONNECTION_STRING'), string(credentialsId: 'JWT_SECRET_KEY', variable: 'JWT_SECRET_KEY'), string(credentialsId: 'REDIS_HOST', variable: 'REDIS_HOST'), string(credentialsId: 'REDIS_PASSWORD', variable: 'REDIS_PASSWORD')]) {
                    sh 'docker stop risk-api || true && docker rm risk-api || true'
                    sh 'docker rmi risk-api-image || true'
                    sh 'docker build -t risk-api-image .'
                    sh "docker create --name risk-api -p 8090:8000 -e CONNECTION_STRING='$CONNECTION_STRING' -e JWT_SECRET_KEY='$JWT_SECRET_KEY' -e REDIS_HOST='$REDIS_HOST' -e REDIS_PASSWORD='$REDIS_PASSWORD' risk-api-image"
                    sh 'docker start risk-api'
                }
            }
        }
    }
    post {
        failure {
            emailext body: 'Test Complete Build failed', recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], subject: "Build failed: ${currentBuild.fullDisplayName}"
        }
    }
}
