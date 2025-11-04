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

        stage('Levantar y testear') {
            steps {
                echo "🚀 Levantando servicios y ejecutando tests en test-web..."
                sh """
                    # Limpiar cualquier contenedor previo
                    docker-compose -f $COMPOSE_FILE down -v

                    # Levantar los contenedores (test-web correrá pytest al iniciar)
                    docker-compose -f $COMPOSE_FILE up --abort-on-container-exit
                """
            }
        }

        stage('Mostrar logs finales') {
            steps {
                echo "📋 Últimos logs de MySQL y test-web"
                sh "docker-compose -f $COMPOSE_FILE logs test-mysql | tail -30"
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









