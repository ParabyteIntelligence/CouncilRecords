#!/bin/bash

## Source: https://gist.github.com/ricardo-rossi/8265589463915837429d

### USAGE
###
### ./ElasticSearch.sh 1.7 will install Elasticsearch 1.7
### ./ElasticSearch.sh will fail because no version was specified (exit code 1)
###
### CLI options Contributed by @janpieper
### Check http://www.elasticsearch.org/download/ for latest version of ElasticSearch

### ElasticSearch version
if [ -z "$1" ]; then
  echo ""
  echo "  Please specify the Elasticsearch version you want to install!"
  echo ""
  echo "    $ $0 1.7"
  echo ""
  exit 1
fi

ELASTICSEARCH_VERSION=$1

if [[ ! "${ELASTICSEARCH_VERSION}" =~ ^[0-9]+\.[0-9]+ ]]; then
  echo ""
  echo "  The specified Elasticsearch version isn't valid!"
  echo ""
  echo "    $ $0 1.7"
  echo ""
  exit 2
fi

### Install Java 8
cd ~
sudo apt-get install python-software-properties -y
sleep 1
sudo add-apt-repository ppa:webupd8team/java -y
sleep 1
sudo apt-get update
sleep 1
sudo apt-get install oracle-java8-installer -y

### Download and install the Public Signing Key
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

### Setup Repository
echo "deb http://packages.elastic.co/elasticsearch/${ELASTICSEARCH_VERSION}/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elk.list

### Install Elasticsearch
sudo apt-get update && sudo apt-get install elasticsearch -y

### Start ElasticSearch
sudo service elasticsearch start

### Lets wait a little while ElasticSearch starts
sleep 5

### Make sure service is running
curl http://localhost:9200

### Should return something like this:
# {
#  "status" : 200,
#  "name" : "Storm",
#  "version" : {
#    "number" : "1.3.1",
#    "build_hash" : "2de6dc5268c32fb49b205233c138d93aaf772015",
#    "build_timestamp" : "2014-07-28T14:45:15Z",
#    "build_snapshot" : false,
#    "lucene_version" : "4.9"
#  },
#  "tagline" : "You Know, for Search"
# }
