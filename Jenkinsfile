pipeline {
  agent any
  
  environment {
    DEBUG = ''
    DOCKERHUB_CREDENTIALS = credentials('docker-repo')
  }
  options {
    timeout(unit: 'MINUTES', time: 2) 
  }
  stages {
    stage("Build application image") {
      steps {
        script {
          try {
            docker.build("${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${env.BUILD_ID}", "-f ./app/Dockerfile .")
          }
          catch(Exception e) {
            error("error making image of application") 
          }
        }
      }
    }
    stage("Push application image") {
      steps {
        script {
          try {
            sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
            sh "docker image push ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${env.BUILD_ID}"
          }
          catch(Exception e) {
            error("error pushing image") 
          }
        }
      } 
    }
    stage("Request Git Release API") {
      steps {
        script {
          try {
            RELEASE = sh returnStdout: true, script: '''rel=$(curl https://api.github.com/repos/hakobmkoyan771/FlaskAppDevProd2.0/releases | grep 'prerelease' | awk '{print $2}' | awk 'FNR == 1 {print}'); echo $rel'''
          }
          catch(Exception e) {
            error("Invalid address") 
          }
          for(el in RELEASE) {
            if(el == "t") {
              DEBUG = 'True'
              break;
            }
            else if(el == "f") {
              DEBUG = 'False'
              break;
            }
            else {
              error("Error: link is broken")
              break;
            }
          }
        }
      }
    }
    stage("Running application on dev") {
      when {
        expression {
          DEBUG == "True" 
        }
      }
      steps {
        sh "docker run -e DEBUG=True --name dev-app -p 5050:5050 ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${env.BUILD_ID}"
      }
    }
    stage("Running application on prod") {
      when {
        expression {
          DEBUG == "False" 
        }
      }
      steps {
        sh "docker run -e DEBUG=False --name prod-app -p 5050:5050 ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${env.BUILD_ID}"
      }
    }
  }
  post {
    always {
      sh "docker container rm -f dev-app || true" 
      sh "docker container rm -f prod-app || true" 
    }
  }
}
