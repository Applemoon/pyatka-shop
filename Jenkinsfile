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
        sh './env/bin/pip install -r requirements.txt'
    }

    stage ("Collect Static files") {
        sh './env/bin/python manage.py collectstatic --noinput'
    }

    stage ("Run Unit/Integration Tests") {
        def testsError = null
        try {
            sh './env/bin/python manage.py jenkins'
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

    stage ("Deploy dev") {
        sh '''
        . ./env/bin/activate
        ./manage.py makemigrations api
        ./manage.py migrate
        #./manage.py createsuperuser --noinput --username test --email 'test@mail.ru'
        ./manage.py loaddata categories_fixtures.json
        npm install
        npm run build
        deactivate
        '''
    }
}
