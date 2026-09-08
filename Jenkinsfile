pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        skipDefaultCheckout()
        timeout(time: 10, unit: 'MINUTES')
    }

    parameters {
        booleanParam(
            name: 'RUN_DIAGNOSTIC',
            defaultValue: true,
            description: '是否执行参数演示阶段'
        )

        choice(
            name: 'TEST_SCOPE',
            choices: ['all', 'smoke', 'user'],
            description: '选择测试范围'
        )

        string(
            name: 'PYTEST_KEYWORD',
            defaultValue: '',
            description: 'pytest -k 关键字过滤，可为空'
        )
    }

    environment {
        PYTHON = 'D:\\Python314\\python.exe'
        REPORT_DIR = 'reports'
        PYTHONUTF8 = '1'
        PYTHONIOENCODING = 'utf-8'
    }

    stages {
        stage('Marker') {
            steps {
                echo 'Loaded from SCM Jenkinsfile'
            }
        }

        stage('Checkout') {
            steps {
                retry(count:3) {
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [[
                            $class: 'CloneOption',
                            depth: 1,
                            noTags: false,
                            reference: '',
                            shallow: true
                        ]],
                        submoduleCfg: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github_token',
                            url: 'https://github.com/NGUN/API_AUTO_TEST.git'
                        ]]
                    ])
                }
            }
        }

        stage('Prepare') {
            steps {
                bat '''
                chcp 65001 >nul
                "%PYTHON%" --version
                if not exist ".jenkins-venv\\Scripts\\python.exe" "%PYTHON%" -m venv .jenkins-venv
                ".jenkins-venv\\Scripts\\python.exe" -m pip install -r requirements.txt
                '''
            }
        }

        stage('Parameter Check') {
            when {
                expression {
                    return params.RUN_DIAGNOSTIC
                }
            }

            steps {
                echo "RUN_DIAGNOSTIC = ${params.RUN_DIAGNOSTIC}"
                echo "TEST_SCOPE = ${params.TEST_SCOPE}"
                echo "PYTEST_KEYWORD = ${params.PYTEST_KEYWORD}"
                echo "Build number = ${env.BUILD_NUMBER}"
            }
        }

        stage('Smoke Check') {
            when {
                expression {
                    return params.TEST_SCOPE == 'smoke'
                }
            }
            steps {
                echo "当前是冒烟测试，关键字：${params.PYTEST_KEYWORD}"
            }
        }

        stage('Smoke Test') {
            when {
                expression {
                    return params.TEST_SCOPE == 'smoke'
                }
            }
            steps {
                echo '主分支的冒烟测试'
            }
        }

        stage('Test') {
            options {
                timeout(time: 1, unit: 'MINUTES')
            }

            steps {
                bat '''
                chcp 65001 >nul
                if not exist reports mkdir reports
                ".jenkins-venv\\Scripts\\python.exe" -X utf8 -m pytest -q ^
                  --junitxml=reports\\junit.xml ^
                  --html=reports\\report.html ^
                  --self-contained-html ^
                  --alluredir=reports\\allure-results ^
                  --clean-alluredir
                '''
            }
        }
    }

    post {
        success {
            echo '构建成功'
        }
        failure {
            echo '构建失败'
        }
        always {
            junit allowEmptyResults: false, testResults: "${env.REPORT_DIR}/junit.xml"
            archiveArtifacts artifacts: "${env.REPORT_DIR}/**", allowEmptyArchive: false
        }
    }
}
