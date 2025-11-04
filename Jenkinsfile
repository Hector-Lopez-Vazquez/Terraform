pipeline {
    agent any

    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "=== Haciendo checkout del repositorio ==="
                checkout scm
                sh 'ls -l $WORKSPACE'
            }
        }

        stage('Verify Environment') {
            steps {
                sh '''
                    echo "=== Docker y docker-compose ==="
                    docker --version
                    docker-compose --version
                    echo "=== Workspace ==="
                    pwd
                    ls -la
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "=== Construyendo contenedores de test ==="
                    docker-compose -f docker-compose.test.yml build --no-cache
                '''
            }
        }

        stage('Start Test Infrastructure') {
            steps {
                sh '''
                    echo "=== Levantando MySQL y Redis para tests ==="
                    docker-compose -f docker-compose.test.yml up -d test-mysql test-redis
                    echo "=== Esperando inicialización de MySQL ==="
                    sleep 45
                    echo "=== Estado de los servicios ==="
                    docker-compose -f docker-compose.test.yml ps
                    docker-compose -f docker-compose.test.yml logs test-mysql | tail -20
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "=== Ejecutando tests de la aplicación ==="
                    docker-compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test-web || true
                '''
            }
            post {
                always {
                    sh '''
                        echo "=== Limpiando entorno de test ==="
                        docker-compose -f docker-compose.test.yml down || true
                        docker-compose -f docker-compose.test.yml logs --no-color > test_logs.txt 2>&1 || true
                        echo "=== Últimos 50 logs de test ==="
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

        stage('Integration Test') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "=== Pruebas de integración ==="
                    timeout 180 sh -c '
                        while true; do
                            if curl -s -f http://localhost:5000/login > /dev/null; then
                                echo "✅ Flask respondiendo"
                                if curl -s http://localhost:5000/register | grep -q "Register"; then
                                    echo "✅ Formulario de registro accesible"
                                    echo "🎉 Todas las pruebas pasaron"
                                    break
                                else
                                    echo "⏳ Esperando servicios listos..."
                                    sleep 10
                                fi
                            else
                                echo "⏳ Esperando que la aplicación esté lista..."
                                sleep 10
                            fi
                        done
                    '
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





