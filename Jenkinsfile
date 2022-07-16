pipeline {
  agent {
    node {
      label 'Git-Clone'
    }

  }
  stages {
    stage('Git Clone') {
      steps {
        git(url: 'https://github.com/ddsperera/COVID19-Tracker..git', credentialsId: 'Git_Hub_Credentials')
      }
    }

  }
}