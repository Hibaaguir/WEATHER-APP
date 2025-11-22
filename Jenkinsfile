pipeline {
    agent any
    
    parameters {
        choice(
            name: 'PYTHON_VERSION',
            choices: ['3.9', '3.10', '3.11'],
            description: 'Python version to build with'
        )
        string(
            name: 'BRANCH_NAME',
            defaultValue: 'dev',
            description: 'Branch to build'
        )
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "Checkout du code depuis GitHub"
                git branch: params.BRANCH_NAME, url: 'https://github.com/Hibaaguir/WEATHER-APP.git'
                bat 'git log -1 --oneline'
            }
        }
        
        stage('Setup') {
            steps {
                echo "Configuration de l environnement Python ${params.PYTHON_VERSION}"
                bat """
                    python --version
                    pip --version
                """
            }
        }
        
        stage('Build') {
            steps {
                echo "Construction de l application"
                bat """
                    pip install -r requirements.txt
                    python -m py_compile app/main.py
                """
            }
        }
        
        stage('Run Docker') {
            steps {
                echo "Lancement des conteneurs Docker"
                bat """
                    docker-compose down
                    docker-compose up -d --build weather-app
                    timeout /t 10 /nobreak
                """
            }
        }
        
        stage('Smoke Test') {
            steps {
                echo "Execution des tests smoke"
                bat """
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
                bat """
                    docker-compose down
                    docker system prune -f
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