#!/usr/bin/env groovy

node {
    def installed = fileExists 'env/bin/activate'

    if (!installed) {
        stage("Install Python Virtual Enviroment") {
            sh 'virtualenv -p python3 env'
        }
    }

    // The stage below is attempting to get the latest version of our application code.
    // Since this is a multi-branch project the 'checkout scm' command is used. If you're working with a standard
    // pipeline project then you can replace this with the regular 'git url:' pipeline command.
    // The 'checkout scm' command will automatically pull down the code from the appropriate branch that triggered this build.
    stage ("Get Latest Code") {
        checkout scm
    }

    stage ("Install Application Dependencies") {
        sh '''
            source env/bin/activate
            pip install -r requirements.txt
            deactivate
           '''
    }

    stage ("Collect Static files") {
        sh '''
            source env/bin/activate
            python manage.py collectstatic --noinput
            deactivate
           '''
    }

    stage ("Run Unit/Integration Tests") {
        def testsError = null
        try {
            sh '''
                source env/bin/activate
                python manage.py jenkins
                deactivate
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
