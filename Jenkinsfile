pipeline {
    agent any
    stages {
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'playwright install'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest --env=qa --alluredir=reports/allure-results'
            }
        }
        stage('Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
            }
        }
    }
}
