pipeline {
    agent any

    environment {
        COMPOSE_FILE = "docker-compose.test.yml"
    }

    stages {
        stage('Preparar') {
            steps {
                echo "🛠 Deteniendo contenedores antiguos y limpiando volúmenes temporales"
                sh "docker-compose -f $COMPOSE_FILE down -v || true"
            }
        }

        stage('Limpiar workspace') {
            steps {
                echo "🧹 Limpiando workspace"
                deleteDir()  // Workspace limpio solo después de down
            }
        }

        stage('Levantar servicios de prueba') {
            steps {
                echo "🚀 Levantando contenedores de prueba"
                sh "docker-compose -f $COMPOSE_FILE up -d"
            }
        }

        stage('Ejecutar tests') {
            steps {
                echo "🔬 Ejecutando tests"
                sh "docker-compose -f $COMPOSE_FILE run --rm test-web"
            }
        }

        stage('Finalizar') {
            steps {
                echo "🛑 Apagando contenedores de prueba"
                sh "docker-compose -f $COMPOSE_FILE down -v"
            }
        }
    }

    post {
        always {
            echo "🧹 Limpiando workspace al final"
            deleteDir()
        }
    }
}








