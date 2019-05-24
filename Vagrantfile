# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |nms|
  nms.vm.box = "ubuntu/xenial64"
  nms.vm.network "private_network", ip: "192.10.1.10", auto_config: false
  nms.vm.network "forwarded_port", guest: 8888, host: 9999

  nms.vm.provider "virtualbox" do |vb|
     vb.gui = false
     vb.memory = "1024"
     vb.cpus = "1"
     vb.name = "AnsibleServer"
  end
end
