pipeline {
    agent any

    environment {
        COMPOSE_FILE = "docker-compose.test.yml"
    }

    stages {
        stage('Preparar') {
            steps {
                echo "🛠 Limpiando workspace..."
                deleteDir()
            }
        }

        stage('Levantar servicios') {
            steps {
                echo "🚀 Levantando contenedores de test..."
                sh """
                    docker-compose -f $COMPOSE_FILE down -v
                    docker-compose -f $COMPOSE_FILE up -d
                """
            }
        }

        stage('Esperar servicios') {
            steps {
                echo "⏳ Esperando que MySQL y Redis estén listos..."
                sh """
                    # Esperar MySQL
                    docker-compose -f $COMPOSE_FILE exec -T test-mysql \
                        bash -c 'until mysqladmin ping -h localhost --silent; do sleep 2; done'
                    
                    # Esperar Redis
                    docker-compose -f $COMPOSE_FILE exec -T test-redis \
                        bash -c 'until redis-cli ping | grep PONG; do sleep 2; done'
                """
            }
        }

        stage('Ejecutar tests') {
            steps {
                echo "🧪 Ejecutando tests de Flask..."
                sh """
                    docker-compose -f $COMPOSE_FILE exec -T test-web \
                        python -m pytest tests/ -v
                """
            }
        }

        stage('Logs finales') {
            steps {
                echo "📋 Últimos logs de MySQL"
                sh "docker-compose -f $COMPOSE_FILE logs test-mysql | tail -30"

                echo "📋 Últimos logs de Test Web"
                sh "docker-compose -f $COMPOSE_FILE logs test-web | tail -30"
            }
        }
    }

    post {
        always {
            echo "🧹 Limpiando contenedores..."
            sh "docker-compose -f $COMPOSE_FILE down -v"
        }

        success {
            echo "✅ Pipeline completado exitosamente"
        }

        failure {
            echo "❌ Pipeline FALLÓ - revisar logs"
        }
    }
}








