#!/usr/bin/env groovy

node {
    def installed = fileExists 'env/bin/activate'

    if (!installed) {
        stage("Install Python Virtual Enviroment") {
            sh 'virtualenv -p python3 env'
        }
    }

    stage ("Get Latest Code") {
        checkout scm
    }

    stage ("Install Application Dependencies") {
        sh '''
            ./env/bin/pip install -r requirements.txt
           '''
    }

    stage ("Collect Static files") {
        sh '''
            ./env/bin/python manage.py collectstatic --noinput
           '''
    }

    stage ("Run Unit/Integration Tests") {
        def testsError = null
        try {
            sh '''
                ./env/bin/python manage.py jenkins
               '''
        }
        catch(err) {
            testsError = err
            currentBuild.result = 'FAILURE'
        }
        finally {
            junit 'reports/junit.xml'

            if (testsError) {
                throw testsError
            }
        }
    }
}
