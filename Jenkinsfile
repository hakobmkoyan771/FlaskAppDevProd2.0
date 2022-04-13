pipeline {
  agent any
  options {
    timeout(time: 4, unit: 'MINUTES')
  }
  environment {
    GIT_USERNAME = 'hakobmkoyan771'
    DOCKERHUB_CREDENTIALS = credentials('docker-repo')
  }
  stages {
    stage("Build application image") {
      agent {
        label 'Master' 
      }
      steps {
        script {
          sh "cd ./app/; docker build -t ${DOCKERHUB_CREDENTIALS_USR}/flaskapp ."
        }
      }
    }
    stage("Deploy application image") {
      agent {
        label 'Master' 
      }
      steps {
          sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
          sh "docker image push ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:latest"
      }       //Can be ERRORMESSAGE: Error saving credentials: error storing credentials - err: exit status 1, out: `Cannot autolaunch D-Bus without X11 $DISPLAY`
    }
    stage("Request Git Release API") {
      agent {
        label 'Master'
      }
      steps {
        script {
          try {
            RELEASE = sh returnStdout: true, script: '''rel=$(curl https://api.github.com/repos/hakobmkoyan771/TestRepo/releases | grep 'prerelease' | awk '{print $2}' | awk 'FNR == 1 {print}'); echo $rel'''
          }
          catch(Exception e) {
            error("Invalid address") 
          }
          for(el in RELEASE) {
            if(el == "t") { // if RELEASE variable is true and the first char is 't'
              DEBUG = 'true'
              break;
            }
            else if(el == "f") { // if RELEASE variable is false and the first char is 'f'
              DEBUG = 'false'
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
          DEBUG == "true" 
        }
      }
      agent {
        label 'Slave-1' 
      }
      steps {
        sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
        sh "docker pull ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:latest"
        sh "docker run -d ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:latest --name dev-app"
        sh "docker logs dev-app"
      }
    }
    stage("Running application on prod") {
      when {
        expression {
          DEBUG == "false" 
        }
      }
      agent {
        label 'Slave-2' 
      }
      steps {
        sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
        //sh "docker pull ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:latest"
        //sh "docker run -d ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:latest --name prod-app"
        //sh "docker logs prod-app"
      }
    }
  }
}
