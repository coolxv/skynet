centos：
    yum install libffi
    yum install libffi-devel
ubuntu：
    apt-get install libffi-dev
    
执行setup.sh时，需要先把setup.sh转换成unix文件，且chmod +x setup.sh
    
根据私有生成证书
openssl req -new -key privkey.pem -out cert.csr