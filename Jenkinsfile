pipeline {
    agent any

    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
    }

    stages {
        stage('Verify Environment') {
            steps {
                sh '''
                    echo "=== Herramientas disponibles ==="
                    docker --version
                    docker-compose --version
                    echo "=== Estructura del proyecto ==="
                    pwd
                    ls -la
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'docker-compose -f docker-compose.test.yml build --no-cache'
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Ejecutar tests y capturar exit code sin detener pipeline
                    def testExitCode = sh(script: '''
                        set +e
                        docker-compose -f docker-compose.test.yml up --abort-on-container-exit
                        EXIT_CODE=$?
                        docker-compose -f docker-compose.test.yml down
                        echo $EXIT_CODE
                    ''', returnStdout: true).trim()

                    echo "✅ Código de salida de tests: ${testExitCode}"

                    // Archivar logs de los tests
                    sh '''
                        docker-compose -f docker-compose.test.yml logs --no-color > test_logs.txt 2>&1 || true
                    '''
                    archiveArtifacts artifacts: 'test_logs.txt', allowEmptyArchive: true

                    // Marcar build como UNSTABLE si tests fallaron
                    if (testExitCode != "0") {
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }

        stage('Deploy to Development') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "=== Desplegando entorno de desarrollo ==="
                    docker-compose -f docker-compose.yml down || true
                    docker-compose -f docker-compose.yml up -d
                    sleep 30
                '''
            }
        }
    }

    post {
        always {
            sh '''
                echo "=== Limpiando entorno de desarrollo y test ==="
                docker-compose -f docker-compose.yml down || true
                docker-compose -f docker-compose.test.yml down || true
                docker system prune -f || true
            '''
            cleanWs()
        }
        success {
            echo "🎉 Pipeline COMPLETADO EXITOSAMENTE"
        }
        unstable {
            echo "⚠️ Pipeline COMPLETÓ con tests fallidos - revisar logs archivados"
        }
        failure {
            echo "❌ Pipeline FALLÓ - revisar logs de Jenkins"
        }
    }
}







