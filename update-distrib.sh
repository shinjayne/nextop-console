#!/bin/bash
# mac 에서 실행하는 방법 : chmod 755 update-distrib.sh  로 권한 변경 후 실행

# avocado 란 이름의 azure docker machine 과 원격 연결 환경 구성 (환경변수 설정)
eval $(docker-machine env nextop)
# avocado docker machine (/home/shinjayne) 으로 현재 컴퓨터(/Users/shinjayne/gdrive/dev/avocado-project/host-docker-machine-file/) 의 파일을 업데이트
# docker-compose 에서 volume 을 docker-machine 의 디렉토리에서 조회하기 때문에 변경사항 반영하려면 파일 업데이트 필수
docker-machine scp -r /Users/shinjayne/gdrive/dev/avocado-project/host-docker-machine-file/ nextop:/home/shinjayne/host-docker-machine-file/
# 호스트 머신에서 docker contalsiners 동시 실행 --> 서비스 재실행
docker-compose --file docker-compose-distrib.yml up -d --build --force-recreate

# 다른 명령어들..
# 1
# docker-machine ssh nextop
# -> 머신 쉘 접속
# 2
# docker-compose --file docker-compose-distrib.yml run web bash
# -> web 컨테이너 쉘 접속