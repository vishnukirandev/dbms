pipeline {
    agent any
    stages {
        stage('Install dependencies') {
            steps {
                bat '''
                cd C:/workspace/dbms/dbms
                pip install -r requirements.txt
                '''
            }
        }
        stage('Stop Flask') {
            steps {
                bat '''
                taskkill /F /IM python.exe || echo "No process running"
                '''
            }
        }
        stage('Run Flask') {
            steps {
                bat '''
                cd C:/workspace/dbms/dbms
                python app.py
                '''
            }
        }
    }
}
