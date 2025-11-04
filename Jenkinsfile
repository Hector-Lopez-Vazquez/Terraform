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
                sh '''
                    echo "=== Levantando contenedores de test ==="
                    docker-compose -f docker-compose.test.yml up --abort-on-container-exit
                '''
            }
            post {
                always {
                    sh '''
                        echo "=== Limpiando entorno de test ==="
                        docker-compose -f docker-compose.test.yml down
                        docker-compose -f docker-compose.test.yml logs --no-color > test_logs.txt 2>&1 || true
                        echo "=== Logs de test guardados ==="
                        tail -50 test_logs.txt
                    '''
                    archiveArtifacts artifacts: 'test_logs.txt', allowEmptyArchive: true
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
                echo "=== Limpiando entorno de desarrollo ==="
                docker-compose -f docker-compose.yml down || true
                docker system prune -f || true
            '''
            cleanWs()
        }
        success {
            echo "🎉 Pipeline COMPLETADO EXITOSAMENTE"
        }
        failure {
            echo "❌ Pipeline FALLÓ - revisar logs de test (ya archivados)"
        }
    }
}






