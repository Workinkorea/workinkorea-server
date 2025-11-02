// Jenkinsfile
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

        MAIL_USERNAME = credentials('mail-username')
        MAIL_PASSWORD = credentials('mail-password')
        MAIL_FROM = credentials('mail-from')
        MAIL_PORT = credentials('mail-port')
        MAIL_SERVER = credentials('mail-server')

        DATABASE_SYNC_URL = credentials('database-sync-url')
        DATABASE_ASYNC_URL = credentials('database-async-url')

        REDIS_HOST = credentials('redis-host')
        REDIS_PORT = credentials('redis-port')
        REDIS_DB = credentials('redis-db')

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

        // TRAEFIK_BASIC_AUTH_USERS = credentials('traefik-basic-auth-users')
    }

    stages {
        stage("Determine Colors") {
            // 색상 결정
            steps {
                echo "Determining colors.."
                script {

                    def blueRunning = sh(
                        script: "docker ps -q -f 'name=workinkorea-server-blue'",
                        returnStdout: true
                    ).trim()

                    def greenRunning = sh(
                        script: "docker ps -q -f 'name=workinkorea-server-green'",
                        returnStdout: true
                    ).trim()
                    
                    if (blueRunning) {
                        env.COLOR = "blue"
                        env.NEW_COLOR = "green"
                    } else if (greenRunning) {
                        env.COLOR = "green"
                        env.NEW_COLOR = "blue"
                    } else {
                        // 처음 배포하는 경우
                        env.COLOR = "none"
                        env.NEW_COLOR = "blue"
                    }

                    echo "Color ${env.COLOR} and ${env.NEW_COLOR} determined"
                }
            }
        }
        stage("Docker build") {
            // 도커 이미지 빌드
            steps {
                echo "Building.."
                script{
                    // clean up docker
                    sh "docker build -f Dockerfile -t ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR} ."
                }
                echo "Docker build finished"
            }
        }
        stage("Docker run") {
            // 도커 실행
            steps {
                echo "Running.."
                script {
                    sh """docker run -d \
                        --name ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR} \
                        --network core_network \
                        --label 'traefik.enable=false' \
                        --label 'traefik.http.routers.${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}.rule=Host(\"arw.${env.BASE_URL}\")' \
                        --label 'traefik.http.routers.${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}.entrypoints=websecure' \
                        --label 'traefik.http.routers.${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}.tls.certresolver=le' \
                        --label 'traefik.http.services.${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}.loadbalancer.server.port=${env.PORT}' \
                        -e COOKIE_DOMAIN=${env.COOKIE_DOMAIN} \
                        -e CLIENT_URL=${env.CLIENT_URL} \
                        -e DATABASE_SYNC_URL=${env.DATABASE_SYNC_URL} \
                        -e DATABASE_ASYNC_URL=${env.DATABASE_ASYNC_URL} \
                        -e REDIS_HOST=${env.REDIS_HOST} \
                        -e REDIS_PORT=${env.REDIS_PORT} \
                        -e REDIS_DB=${env.REDIS_DB} \
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
                        -e MAIL_USERNAME=${env.MAIL_USERNAME} \
                        -e MAIL_PASSWORD="${env.MAIL_PASSWORD}" \
                        -e MAIL_FROM=${env.MAIL_FROM} \
                        -e MAIL_PORT=${env.MAIL_PORT} \
                        -e MAIL_SERVER=${env.MAIL_SERVER} \
                        ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}
                    """
                }
                echo "Docker run finished"
            }
        }
        stage("Docker health check and switch traefik") {
            // 도커 헬스 체크 및 traefik 설정 스위치
            steps {
                echo "Health checking.."
                script {        
                    def healthCheck = sh(
                        script: "docker inspect -f '{{.State.Running}}' ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}",
                        returnStdout: true
                    ).trim()

                    if (healthCheck == "true") {
                        script {
                            sh """
                            docker stop ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}
                            docker rm ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}
                            docker run -d \
                                --name ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR} \
                                --network core_network \
                                --label 'traefik.enable=true' \
                                --label 'traefik.http.routers.${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}.rule=Host(\"arw.${env.BASE_URL}\")' \
                                --label 'traefik.http.routers.${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}.entrypoints=websecure' \
                                --label 'traefik.http.routers.${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}.tls.certresolver=le' \
                                --label 'traefik.http.services.${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}.loadbalancer.server.port=${env.PORT}' \
                                -e COOKIE_DOMAIN=${env.COOKIE_DOMAIN} \
                                -e CLIENT_URL=${env.CLIENT_URL} \
                                -e DATABASE_SYNC_URL=${env.DATABASE_SYNC_URL} \
                                -e DATABASE_ASYNC_URL=${env.DATABASE_ASYNC_URL} \
                                -e REDIS_HOST=${env.REDIS_HOST} \
                                -e REDIS_PORT=${env.REDIS_PORT} \
                                -e REDIS_DB=${env.REDIS_DB} \
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
                                -e MAIL_USERNAME=${env.MAIL_USERNAME} \
                                -e MAIL_PASSWORD="${env.MAIL_PASSWORD}" \
                                -e MAIL_FROM=${env.MAIL_FROM} \
                                -e MAIL_PORT=${env.MAIL_PORT} \
                                -e MAIL_SERVER=${env.MAIL_SERVER} \
                                ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}
                            """

                            sleep 5
                             if (env.COLOR != "none") {
                                sh "docker stop ${env.DOCKER_IMAGE_NAME}-${env.COLOR} || true"
                             }
                        }
                    } else {
                        error "Health check failed : workinkorea-server-${env.NEW_COLOR} is not running"
                    }
                }
                
                echo "Health check finished"
            }
        }
        stage("Traefik test") {
            // traefik 설정 테스트
            steps {
                echo "Traefik test.."
                script {
                    
                    // def traefikTest = sh(
                    //         script: "curl -s -o /dev/null -w '%{http_code}' https://arw.${env.BASE_URL}/docs",
                    //         returnStdout: true
                    //     ).trim()
                    
                    // 개발 환경에서 테스트
                    def traefikTest = sh(
                        script: """docker run --rm --network core_network curlimages/curl:latest curl -s -o /dev/null -w '%{http_code}' -H 'Host: arw.${env.BASE_URL}' http://${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR}:${env.PORT}/docs""",
                        returnStdout: true
                    ).trim()
                    
                    echo "Traefik test passed. HTTP Status: ${traefikTest}"
                    if (traefikTest != "200") {
                        error("Traefik test failed. HTTP Status: ${traefikTest}")
                    }
                    
                }
                echo "Traefik test finished"
            }
        }    
    }
    post {
        success {
            echo "success"
            script {
                sh """
                    docker stop ${env.DOCKER_IMAGE_NAME}-${env.COLOR} || true
                    docker rm ${env.DOCKER_IMAGE_NAME}-${env.COLOR} || true
                    docker rmi ${env.DOCKER_IMAGE_NAME}-${env.COLOR} || true
                    """
            }
            discordSend description: "${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR} deployed successfully",
                  title: "Success : Workinkorea-Server", 
                  webhookURL: "${env.DISCORD_WEBHOOK_URL}"
            echo "old container : ${env.DOCKER_IMAGE_NAME}-${env.COLOR} stopped"
        }
        failure {
            error "rollback to ${env.COLOR} container"
            script {
                sh """
                    docker stop ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR} || true
                    docker rm ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR} || true
                    docker rmi ${env.DOCKER_IMAGE_NAME}-${env.NEW_COLOR} || true
                    """
                sleep 5
                sh """
                    docker rm ${env.DOCKER_IMAGE_NAME}-${env.COLOR} || true
                    docker run -d \
                    --name ${env.DOCKER_IMAGE_NAME}-${env.COLOR} \
                    --network core_network \
                    --label 'traefik.enable=true' \
                    --label 'traefik.http.routers.${env.DOCKER_IMAGE_NAME}-${env.COLOR}.rule=Host(\"arw.${env.BASE_URL}\")' \
                    --label 'traefik.http.routers.${env.DOCKER_IMAGE_NAME}-${env.COLOR}.entrypoints=websecure' \
                    --label 'traefik.http.routers.${env.DOCKER_IMAGE_NAME}-${env.COLOR}.tls.certresolver=le' \
                    --label 'traefik.http.services.${env.DOCKER_IMAGE_NAME}-${env.COLOR}.loadbalancer.server.port=${env.PORT}' \
                    -e COOKIE_DOMAIN=${env.COOKIE_DOMAIN} \
                    -e CLIENT_URL=${env.CLIENT_URL} \
                    -e DATABASE_SYNC_URL=${env.DATABASE_SYNC_URL} \
                    -e DATABASE_ASYNC_URL=${env.DATABASE_ASYNC_URL} \
                    -e REDIS_HOST=${env.REDIS_HOST} \
                    -e REDIS_PORT=${env.REDIS_PORT} \
                    -e REDIS_DB=${env.REDIS_DB} \
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
                    -e MAIL_USERNAME=${env.MAIL_USERNAME} \
                    -e MAIL_PASSWORD="${env.MAIL_PASSWORD}" \
                    -e MAIL_FROM=${env.MAIL_FROM} \
                    -e MAIL_PORT=${env.MAIL_PORT} \
                    -e MAIL_SERVER=${env.MAIL_SERVER} \
                    ${env.DOCKER_IMAGE_NAME}-${env.COLOR}
                """
            }
            discordSend description: "${env.DOCKER_IMAGE_NAME}-${env.COLOR} rolled back",
                  title: "Failure : Workinkorea-Server", 
                  webhookURL: "${env.DISCORD_WEBHOOK_URL}"
            echo "Rolled back to ${env.COLOR} container"
        }
    }
}

