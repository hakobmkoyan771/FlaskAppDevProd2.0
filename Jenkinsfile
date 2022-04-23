pipeline {
  agent any
  
  environment {
    DOCKERHUB_CREDENTIALS = credentials('docker-creds')
  }
  
  options {
    timeout(unit: 'MINUTES', time: 2) 
  }
  
  triggers {
    GenericTrigger(causeString: 'Generic Cause', 
                   genericVariables: [[key: 'prerelease', value: '$.release.prerelease']])
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
    
    stage("Start application container") {
      steps {
        script {
          if(prerelease == 'true') {
            sh "docker run -p 5050:5050 --name dev-app -e DEBUG=True ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${env.BUILD_ID}"
          }
          else if(prerelease == 'false') {
            sh "docker run -p 5050:5050 --name prod-app -e DEBUG=False ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${env.BUILD_ID}"
          }
        }
      }
    }
  }
  
  post {
    always {
      script {
        sh "docker container rm -f dev-app || true"
        sh "docker container rm -f prod-app || true"
      }
    }
  }
}
