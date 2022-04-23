pipeline {
  agent any
  
  options {
    timeout(unit: 'MINUTES', time: 2) 
  }
  
  triggers {
    GenericTrigger(causeString: 'PreRelease', 
                   genericVariables: [[key: 'prerelease', value: '$.release.prerelease'],
                                      [key: 'release_tag', value: '$.release.tag_name']])
  }
  
  stages {
    stage("Build application image") {
      steps {
        script {
          try {
            docker.build("${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${release_tag}", "-f ./app/Dockerfile .")
          }
          catch(Exception e) {
            error("error making image of application") 
          }
        }
      }
    }
    
/*    stage("Start application container") {
      steps {
        script {
          if(prerelease == 'true') {
            sh "docker run -p 5050:5050 --name dev-app -e DEBUG=True ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${release_tag}"
          }
          else if(prerelease == 'false') {
            sh "docker run -p 5050:5050 --name prod-app -e DEBUG=False ${DOCKERHUB_CREDENTIALS_USR}/flaskapp:${release_tag}"
          }
        }
      }
    }*/
    
    stage("Start Dev application container") {
      when {
        expression {
          prerelease == 'true'  
        }
      }
      steps {
        echo "true" 
      }
    }
    
    stage("Start Prod application container") {
      when {
        expression {
          prerelease == 'false'  
        }
      }
      steps {
        echo "false" 
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
