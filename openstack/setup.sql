-- Create databases
create database keystone;
create database glance;
create database nova;
create database neutron;

-- Keystone grants
grant all privileges on keystone.* to 'keystone'@'localhost' identified by 'KEYSTONE_DBPASS';
grant all privileges on keystone.* to 'keystone'@'192.168.200.%' identified by 'KEYSTONE_DBPASS';

-- Glance grants
grant all privileges on glance.* to 'glance'@'localhost' identified by 'GLANCE_DBPASS';
grant all privileges on glance.* to 'glance'@'192.168.200.%' identified by 'GLANCE_DBPASS';

-- Nova grants
grant all privileges on nova.* to 'nova'@'localhost' identified by 'NOVA_DBPASS';
grant all privileges on nova.* to 'nova'@'192.168.200.%' identified by 'NOVA_DBPASS';

-- Neutron grants
grant all privileges on neutron.* to 'neutron'@'localhost' identified by 'NEUTRON_DBPASS';
grant all privileges on neutron.* to 'neutron'@'192.168.200.%' identified by 'NEUTRON_DBPASS';
