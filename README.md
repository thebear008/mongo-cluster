# mongo-cluster

# mongod

Tuto to create a cluster of mongo with 1 primary, 1 slave and 1 arbitrer.

Get last binary 3.6.9 in tgz format.

```
cd ~/Téléchargements
curl -L -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-3.6.9.tgz
tar xzvf mongodb-linux-x86_64-rhel70-3.6.9.tgz
```

Start 3 mongo instances on 27017, 27018 and 27019.

```
for i in 7 8 9
do
  mkdir ~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/data${i}/ || echo ok
  ~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/bin/mongod --dbpath ~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/data${i}/ --bind_ip_all --port 2701${i} > /dev/null 2>&1 &
done

openssl rand -base64 756 > ~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/mongo-keyfile
chmod 400 ~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/mongo-keyfile




```

Create admin and db and owner

```
~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/bin/mongo --port 27017
use admin
db.createUser(
  {
    user: "myUserAdmin",
    pwd: "abc123",
    roles: [ "root" ]
  }
)

use test
db.createUser(
  {
    user: "myTester",
    pwd: "xyz123",
    roles: [ { role: "dbOwner", db: "test" } ]
  }
)

```

Then restart `mongod` with replicat set and keyfile.




```
pkill mongod
for i in 7 8 9
do
  ~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/bin/mongod --dbpath ~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/data${i}/ --bind_ip_all --port 2701${i} --auth --keyFile ~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/mongo-keyfile --replSet rs0 > /dev/null 2>&1 &
done
```

Next connect on primary node

```
rs.initiate()
rs.add("sony:27018")
rs.addArb("sony:27019")
```

## connect as users

```
~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/bin/mongo -u "myUserAdmin" -p "abc123" --authenticationDatabase "admin" --port 27017

~/Téléchargements/mongodb-linux-x86_64-rhel70-3.6.9/bin/mongo -u "myTester" -p "xyz123" --authenticationDatabase "test" --port 27017

```

## useful commands

1. run logrotation

```
./mongo --eval "db.adminCommand({logRotate: 1})"
```
