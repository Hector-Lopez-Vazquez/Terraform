pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.test.yml'
    }

    stages {

        stage('Preparar') {
            steps {
                echo "🛠 Deteniendo contenedores antiguos"
                sh "docker-compose -f $COMPOSE_FILE down -v || true"
            }
        }

        stage('Limpiar workspace') {
            steps {
                echo "🧹 Limpiando workspace"
                deleteDir()
            }
        }

        stage('Levantar y testear') {
            steps {
                echo "🚀 Levantando contenedores y ejecutando tests"
                sh """
                    docker-compose -f $COMPOSE_FILE up --abort-on-container-exit
                """
            }
        }

        stage('Últimos logs') {
            steps {
                echo "📄 Últimos logs de MySQL y Web"
                sh """
                    docker-compose -f $COMPOSE_FILE logs test-mysql | tail -30
                    docker-compose -f $COMPOSE_FILE logs test-web   | tail -30
                """
            }
        }
    }

    post {
        always {
            echo "🧹 Borrando contenedores y volúmenes al final"
            sh "docker-compose -f $COMPOSE_FILE down -v || true"
        }
        success {
            echo "✅ Pipeline completado con éxito"
        }
        failure {
            echo "❌ Pipeline FALLÓ - revisar logs de Jenkins"
        }
    }
}









