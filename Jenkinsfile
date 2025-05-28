pipeline {
    agent any
    stages {
        stage('Install dependencies') {
            steps {
                bat '''
                cd C:/workspace/dbms/dbms
                python -m pip install -r requirements.txt
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
        stage('Run Flask in Background') {
            steps {
                bat '''
                cd C:/workspace/dbms/dbms
                start "" python app.py
                '''
            }
        }
    }
}
