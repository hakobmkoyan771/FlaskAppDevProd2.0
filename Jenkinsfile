pipeline {
  agent any
  
  environment {
    DEBUG = ''
    DOCKERHUB_CREDENTIALS = credentials('docker-repo')
  }

  stages {
    stage("Build application image") {
      steps {
        script {
          //sh "cd ./app/; docker build -t ${DOCKERHUB_CREDENTIALS_USR}/flaskapp ."
          docker.build("hakobmkoyan771/flaskapp:${env.BUILD_ID} -f /bitnami/jenkins/home/workspace/$JOB_NAME/app/Dockerfile")
        }
      }
    }/*
    stage("Deploy application image") {
      steps {
          sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
          sh "docker image push ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:latest"
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
            if(el == "t") { // if RELEASE variable is true and the first char is 't'
              DEBUG = 'True'
              break;
            }
            else if(el == "f") { // if RELEASE variable is false and the first char is 'f'
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
        sh "docker pull ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:latest"
        sh "docker run -d -e DEBUG=True --name dev-app -p 5040:5050 ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:latest"
        sh 'sleep 300'
        sh "docker container rm -f dev-app"
      }
    }
    stage("Running application on prod") {
      when {
        expression {
          DEBUG == "False" 
        }
      }
      steps {
        sh "docker pull ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:latest"
        sh "docker run -d  -e DEBUG=False --name prod-app -p 5050:5050 ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:latest"
        sh 'sleep 300'
        sh "docker container rm -f prod-app"
      }
    }*/
  }
}
