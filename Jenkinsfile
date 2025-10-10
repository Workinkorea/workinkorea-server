pipeline {
    agent any

    environment {
        BRANCH_NAME = "dev"
        BASE_URL = "byeong98.xyz"
        DOCKER_IMAGE_NAME = "workinkorea-server"
        PORT = 8000
        DISCORD_WEBHOOK_URL = credentials('discord-webhook-url')

        // 환경변수 .env 설정
        COOKIE_DOMAIN = credentials('cookie-domain')
        CLIENT_URL = credentials('client-url')

        DATABASE_SYNC_URL = credentials('database-sync-url')
        DATABASE_ASYNC_URL = credentials('database-async-url')

        GOOGLE_CLIENT_ID = credentials('google-client-id')
        GOOGLE_CLIENT_SECRET = credentials('google-client-secret')
        GOOGLE_REDIRECT_URI = credentials('google-redirect-uri')
        GOOGLE_AUTHORIZATION_URL = credentials('google-authorization-url')
        GOOGLE_TOKEN_URL = credentials('google-token-url')
        GOOGLE_USER_INFO_URL = credentials('google-user-info-url')

        JWT_SECRET = credentials('jwt-secret')
        JWT_ALGORITHM = credentials('jwt-algorithm')
        ACCESS_TOKEN_EXPIRE_MINUTES = credentials('access-token-expire-minutes')
        REFRESH_TOKEN_EXPIRE_MINUTES = credentials('refresh-token-expire-minutes')
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
                        --label 'traefik.http.routers.workinkorea-server.rule=Host(\"arw.${env.BASE_URL}\")' \
                        --label 'traefik.http.routers.workinkorea-server.entrypoints=websecure' \
                        --label 'traefik.http.routers.workinkorea-server.tls.certresolver=le' \
                        --label 'traefik.http.services.workinkorea-server.loadbalancer.server.port=${env.PORT}' \
                        -e COOKIE_DOMAIN=${env.COOKIE_DOMAIN} \
                        -e CLIENT_URL=${env.CLIENT_URL} \
                        -e DATABASE_SYNC_URL=${env.DATABASE_SYNC_URL} \
                        -e DATABASE_ASYNC_URL=${env.DATABASE_ASYNC_URL} \
                        -e GOOGLE_CLIENT_ID=${env.GOOGLE_CLIENT_ID} \
                        -e GOOGLE_CLIENT_SECRET=${env.GOOGLE_CLIENT_SECRET} \
                        -e GOOGLE_REDIRECT_URI=${env.GOOGLE_REDIRECT_URI} \
                        -e GOOGLE_AUTHORIZATION_URL=${env.GOOGLE_AUTHORIZATION_URL} \
                        -e GOOGLE_TOKEN_URL=${env.GOOGLE_TOKEN_URL} \
                        -e GOOGLE_USER_INFO_URL=${env.GOOGLE_USER_INFO_URL} \
                        -e JWT_SECRET=${env.JWT_SECRET} \
                        -e JWT_ALGORITHM=${env.JWT_ALGORITHM} \
                        -e ACCESS_TOKEN_EXPIRE_MINUTES=${env.ACCESS_TOKEN_EXPIRE_MINUTES} \
                        -e REFRESH_TOKEN_EXPIRE_MINUTES=${env.REFRESH_TOKEN_EXPIRE_MINUTES} \
                        workinkorea-server
                        """
                }
                echo "Deploy finished"
            }
        }
        
    }
    // 빌드 결과 디스코드 알림
    post {
        success {
            echo "Build passed"
            script {
                sh '''
                curl -X POST \
                  -H "Content-Type: application/json" \
                  -d "{\\"content\\": \\"Build passed - WorkInKorea Server\\"}" \
                  "${DISCORD_WEBHOOK_URL}"
                '''
            }
        }
        failure {
            echo "Build failed"
            script {
                sh '''
                curl -X POST \
                  -H "Content-Type: application/json" \
                  -d "{\\"content\\": \\"Build failed - WorkInKorea Server\\"}" \
                  "${DISCORD_WEBHOOK_URL}"
                '''
            }
        }
        always {
            echo "Discord notification finished"
        }
    }
}