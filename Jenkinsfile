pipeline {
    agent any
    
    parameters {
        choice(
            name: 'PYTHON_VERSION',
            choices: ['3.9', '3.10', '3.11'],
            description: 'Python version to build with'
        )
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "Checkout du code depuis GitHub"
                git branch: '${CHANGE_BRANCH}', url: 'https://github.com/Hibaaguir/WEATHER-APP.git'
                sh 'git log -1 --oneline'
            }
        }
        
        stage('Setup') {
            steps {
                echo "Configuration de l environnement Python ${params.PYTHON_VERSION}"
                sh """
                    python --version
                    pip --version
                """
            }
        }
        
        stage('Build') {
            steps {
                echo "Construction de l application"
                sh """
                    pip install -r requirements.txt
                    python -m py_compile app/main.py
                """
            }
        }
        
        stage('Run Docker') {
            steps {
                echo "Lancement des conteneurs Docker"
                sh """
                    docker-compose down || true
                    docker-compose up -d --build weather-app
                    sleep 10
                """
            }
        }
        
        stage('Smoke Test') {
            steps {
                echo "Execution des tests smoke"
                sh """
                    docker-compose run --rm smoke-test
                """
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo "Archivage des artefacts"
                archiveArtifacts artifacts: '**/logs/*.log', allowEmptyArchive: true
                junit '**/test-reports/*.xml'
            }
        }
        
        stage('Cleanup') {
            steps {
                echo "Nettoyage des ressources"
                sh """
                    docker-compose down || true
                    docker system prune -f || true
                """
            }
        }
    }
    
    post {
        always {
            echo "Pipeline termine - Resume"
            script {
                currentBuild.description = "PR Build - Python ${params.PYTHON_VERSION}"
            }
        }
        success {
            echo "Pipeline reussi!"
        }
        failure {
            echo "Pipeline echoue!"
        }
    }
}