* install ubuntu server 14.04 LTS.

* modify ip of ubuntu server
cd ansible
vi host.cfg

* deploy a jenkins machine
ansible-playbook -kK -i host.cfg playbook.yml 

* update jobs
cd ../jjb
jenkins-jobs --conf ./config update test.yml
