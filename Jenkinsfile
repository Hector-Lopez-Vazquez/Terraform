pipeline {
    agent any
    
    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                sh '''
                    echo "=== Verificando archivos después del checkout ==="
                    pwd
                    ls -la
                    echo "=== Verificando docker-compose.test.yml ==="
                    if [ -f "docker-compose.test.yml" ]; then
                        echo "✅ docker-compose.test.yml encontrado"
                        cat docker-compose.test.yml | head -20
                    else
                        echo "❌ ERROR: docker-compose.test.yml NO encontrado"
                        echo "Archivos YML disponibles:"
                        find . -name "*.yml" -o -name "*.yaml"
                        exit 1
                    fi
                '''
            }
        }
        
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
                sh 'docker-compose build --no-cache'
            }
        }
        
        stage('Start Test Infrastructure') {
            steps {
                sh '''
                    echo "=== Iniciando solo MySQL y Redis para tests ==="
                    docker-compose -f docker-compose.test.yml up -d test-mysql test-redis
                    echo "=== Esperando 45 segundos para inicialización de MySQL ==="
                    sleep 45
                    echo "=== Verificando estado de los servicios ==="
                    docker-compose -f docker-compose.test.yml ps
                    docker-compose -f docker-compose.test.yml logs test-mysql | tail -20
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    echo "=== Ejecutando tests con aplicación ==="
                    # Iniciar solo el servicio web que ejecutará los tests
                    docker-compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test-web
                '''
            }
            post {
                always {
                    sh '''
                        echo "=== Limpiando entorno de test ==="
                        if [ -f "docker-compose.test.yml" ]; then
                            docker-c







