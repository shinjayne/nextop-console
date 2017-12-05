#!/bin/bash

# avocado 란 이름의 azure docker machine 과 원격 연결 환경 구성 (환경변수 설정)
eval $(docker-machine env avocado)
# avocado docker machine (/home/shinjayne) 으로 현재 컴퓨터(/Users/shinjayne/gdrive/dev/avocado-project/host-docker-machine-file/) 의 파일을 업데이트
# docker-compose 에서 volume 을 docker-machine 의 디렉토리에서 조회하기 때문에 변경사항 반영하려면 파일 업데이트 필수
docker-machine scp -r /Users/shinjayne/gdrive/dev/avocado-project/host-docker-machine-file/ avocado:/home/shinjayne/host-docker-machine-file/
# 호스트 머신에서 docker containers 동시 실행 --> 서비스 재실행
docker-compose --file docker-compose-distrib.yml up -d --build --force-recreate