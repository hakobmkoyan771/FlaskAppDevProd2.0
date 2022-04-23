pipeline {
  agent any
  
  options {
    timeout(unit: 'MINUTES', time: 2) 
  }
  
  triggers {
    GenericTrigger(causeString: 'Generic Trigger', 
                   genericVariables: [[key: 'prerelease', value: '$.release.prerelease'],
                                      [key: 'release_tag', value: '$.release.tag_name'],
                                      [key: 'git_username', value: '$.sender.login']])
  }
  
  stages {
    stage("Build application image") {
      steps {
        script {
          try {
            docker.build("${git_username}/flaskapp:${release_tag}", "-f ./app/Dockerfile .")
          }
          catch(Exception err) {
            error("error making image of application") 
          }
        }
      }
    }
    
    stage("Start Dev application container") {
      when {
        expression {
          prerelease == 'true'  
        }
      }
      steps {
        sh "cd ./app; APP_IMAGE=${git_username}/flaskapp:${release_tag} APP_NAME=dev_app DEBUG_VAR=True docker-compose up"
      }
    }
    
    stage("Start Prod application container") {
      when {
        expression {
          prerelease == 'false'  
        }
      }
      steps {
        sh "cd ./app; APP_IMAGE=${git_username}/flaskapp:${release_tag} APP_NAME=prod_app DEBUG_VAR=False docker-compose up"
      }
    }
  }
  
  post {
    always {
      sh "docker container rm -f dev_app || true"
      sh "docker container rm -f prod_app || true"
    }
  }
}
