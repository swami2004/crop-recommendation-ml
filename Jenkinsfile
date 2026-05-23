pipeline {
agent any

```
stages {

    stage('Clone') {
        steps {
            git branch: 'main',
            url: 'https://github.com/swami2004/crop-recommendation-ml.git'
        }
    }

    stage('Build Docker Image') {
        steps {
            sh 'docker build -t crop-project .'
        }
    }

    stage('Stop Old Container') {
        steps {
            sh 'docker stop crop-container || true'
            sh 'docker rm crop-container || true'
        }
    }

    stage('Run Container') {
        steps {
            sh 'docker run -d -p 8000:8000 --name crop-container crop-project'
        }
    }
}
```

}

