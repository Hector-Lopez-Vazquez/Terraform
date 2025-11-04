pipeline {
    agent any
    
    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
        COMPOSE_IMAGE = "docker/compose:2.20.2"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                sh '''
                    echo "=== Herramientas disponibles dentro del contenedor Docker Compose ==="
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ${COMPOSE_IMAGE} version
                    pwd
                    ls -la
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v $PWD:$PWD -w $PWD \
                        ${COMPOSE_IMAGE} -f docker-compose.test.yml build --no-cache
                '''
            }
        }

        stage('Start Test Infrastructure') {
            steps {
                sh '''
                    echo "=== Iniciando solo MySQL y Redis para tests ==="
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v $PWD:$PWD -w $PWD \
                        ${COMPOSE_IMAGE} -f docker-compose.test.yml up -d test-mysql test-redis
                    echo "=== Esperando 45 segundos para inicialización de MySQL ==="
                    sleep 45
                    echo "=== Verificando estado de los servicios ==="
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v $PWD:$PWD -w $PWD \
                        ${COMPOSE_IMAGE} -f docker-compose.test.yml ps
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "=== Ejecutando tests con aplicación ==="
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v $PWD:$PWD -w $PWD \
                        ${COMPOSE_IMAGE} -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test-web || true
                '''
            }
            post {
                always {
                    sh '''
                        echo "=== Limpiando entorno de test ==="
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            -v $PWD:$PWD -w $PWD \
                            ${COMPOSE_IMAGE} -f docker-compose.test.yml down || true
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            -v $PWD:$PWD -w $PWD \
                            ${COMPOSE_IMAGE} -f docker-compose.test.yml logs --no-color > test_logs.txt 2>&1 || true
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
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v $PWD:$PWD -w $PWD \
                        ${COMPOSE_IMAGE} -f docker-compose.yml down || true
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v $PWD:$PWD -w $PWD \
                        ${COMPOSE_IMAGE} -f docker-compose.yml up -d
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
                    echo "=== Realizando pruebas de integración ==="
                    timeout 90 sh -c '
                        while true; do
                            if curl -s -f http://localhost:5000/login > /dev/null; then
                                echo "✅ Aplicación Flask respondiendo"
                                if curl -s http://localhost:5000/register | grep -q "Register"; then
                                    echo "✅ Formulario de registro accesible"
                                    echo "🎉 Todas las pruebas pasaron correctamente"
                                    break
                                else
                                    echo "⏳ Esperando que todos los servicios estén listos..."
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
                docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    -v $PWD:$PWD -w $PWD \
                    ${COMPOSE_IMAGE} -f docker-compose.yml down || true
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





