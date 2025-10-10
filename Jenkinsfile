pipeline {
    agent any

    environment {
        BRANCH_NAME = "dev"
        BASE_URL = "byeong98.xyz"
        DOCKER_IMAGE_NAME = "workinkorea-server"
        DISCORD_WEBHOOK_URL = credentials('discord-webhook-url')
    }

    stages {
        
        stage("Docker build") {
            // 기존 docker 중지 및 삭제
            steps {
                echo "Building.."
                script{
                    sh """
                    docker stop ${env.DOCKER_IMAGE_NAME} || true
                    docker rm ${env.DOCKER_IMAGE_NAME} || true
                    docker rmi ${env.DOCKER_IMAGE_NAME} || true
                    """

                    sh "docker build -t ${env.DOCKER_IMAGE_NAME} ."
                }
                echo "Docker build finished"
            }
        }
        stage("Test") {
            // 테스트 코드 실행
            steps {
                echo "Testing.."
                // 테스트 코드 추가 예정
                echo "Test finished"
            }
        }
        stage("Deploy") {
            // 배포
            steps {
                echo "Deploying...."
                script {
                    sh """
                        docker run -d \
                        --name workinkorea-server \
                        --network core_network \
                        --label 'traefik.enable=true' \
                        --label 'traefik.http.routers.workinkorea-server.rule=Host("arw.${env.BASE_URL}")' \
                        --label 'traefik.http.routers.workinkorea-server.entrypoints=websecure' \
                        --label 'traefik.http.routers.workinkorea-server.tls.certresolver=le' \
                        --label 'traefik.http.services.workinkorea-server.loadbalancer.server.port=${env.PORT}' \
                        workinkorea-server
                        """
                }
                echo "Deploy finished"
            }
        }
        stage("health check") {
            // 배포 후 헬스 체크
            steps {
                echo "Health check..."
                script {
                    def success = false
                    def response = sh """curl -s -o /dev/null -w "%{http_code}\n" https://arw.${env.BASE_URL}/docs"""

                    if (response == '200') {
                        echo "Health check passed"
                        success = true
                    } else {
                        echo "Health check failed"
                        success = false
                    }
                }
                echo "Health check finished"
            }
        }
    }
    // 빌드 결과 디스코드 알림
    post {
        success {
            echo "Build passed"
            sh """
            curl -X POST \ 
            -H 'Content-Type: application/json' \
            --data '{"content": "Build passed"}' \
            ${env.DISCORD_WEBHOOK_URL}
            """
        }
        failure {
            echo "Build failed"
            sh """
            curl -X POST \
            -H 'Content-Type: application/json' \
            --data '{"content": "Build failed"}' \
            ${env.DISCORD_WEBHOOK_URL}
            """
        }
        always {
            echo "Discord notification finished"
        }
    }
}