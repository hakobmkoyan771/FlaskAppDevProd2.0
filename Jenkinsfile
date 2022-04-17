pipeline {
  agent any
  
  environment {
    DEBUG = ''
    DOCKERHUB_CREDENTIALS = credentials('docker-repo')
  }
  options {
    timeout(unit: 'MINUTES', time: 2) 
  }
  triggers {
    GenericTrigger(causeString: 'Generic Cause', genericVariables: [[defaultValue: '', key: 'release', regexpFilter: '', value: '$.release.prerelease']], regexpFilterExpression: '', regexpFilterText: '', token: '', tokenCredentialId: '')
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
    stage("Run application") {
      steps {
        script {
          if(release == true) {
            Image.run("-e DEBUG=True", "--name dev-app", "-p 5050:5050", "${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${env.BUILD_ID}") 
          }
          else {
             Image.run("-e DEBUG=False", "--name prod-app", "-p 5050:5050", "${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${env.BUILD_ID}") 
          }
        }
      }
    }/*
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
  }*/
  post {
    always {
      sh "docker container rm -f dev-app || true" 
      sh "docker container rm -f prod-app || true" 
    }
  }
}
