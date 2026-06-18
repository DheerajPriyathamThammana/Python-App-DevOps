pipeline {
  agent any
  environment {
    DOCKER_HUB_CREDS = credentials('dockerhub-creds')  // Jenkins credential ID
    IMAGE_NAME       = "thammanadheerajpriyatham/devopsapp"
    IMAGE_TAG        = "${env.BUILD_NUMBER}"
    EC2_HOST         = "ec2-user@ec2-23-23-96-253.compute-1.amazonaws.com"
    SSH_KEY          = credentials('ec2-ssh-key')
  }
  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/DheerajPriyathamThammana/Python-App-DevOps.git'
      }
    }
    stage('Build Docker Image') {
      steps {
        sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
        sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
      }
    }
    stage('Push to Docker Hub') {
      steps {
        sh "echo ${DOCKER_HUB_CREDS_PSW} | docker login -u ${DOCKER_HUB_CREDS_USR} --password-stdin"
        sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
        sh "docker push ${IMAGE_NAME}:latest"
      }
    }
    stage('Deploy to EC2 via Helm') {
      steps {
        sshagent(['ec2-ssh-key']) {
          sh """
            ssh -o StrictHostKeyChecking=no ${EC2_HOST} '
              helm upgrade --install devops /home/ec2-user/Python-App-DevOps/helm/devops/ \
                --set image.repository=${IMAGE_NAME} \
                --set image.tag=${IMAGE_TAG} \
                --namespace default
            '
          """
        }
      }
    }
  }
  post {
    always   { sh 'docker logout' }
    success  { echo "Deployed ${IMAGE_TAG} successfully" }
  }
}
