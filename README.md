# GQ GMC-500+

Webservice and prometheus exporter for GQ GMC 500+ geiger counters

## Configuration

### Containers

The webservice can be run through containers.

```
docker run --name gmc --rm -v /etc/gq-gmc500plus.json:/etc/gq-gmc500plus.json -p 8500:8500 quay.io/wreiner/gq-gmc500plus:0.1
```

Images can be found here:
- <https://quay.io/repository/wreiner/gq-gmc500plus>
- <https://hub.docker.com/r/wreiner/gq-gmc500plus>

### nginx

```
    server {
        listen       80;
        server_name  192.168.2.32;

        location / {
            proxy_pass   http://127.0.0.1:8500;
        }
    }
```

### GQ GMC-500+

#### Standard values

- Standard URL: www.gmcmap.com
- Standard PAHT: log2.asp

## Examples of requests made of the device

```
192.168.2.136 - - [09/Apr/2023 17:38:05] "GET /u?AID=&GID=&CPM=21&ACPM=21.55&uSV=0.14 HTTP/1.1" 200 -
192.168.2.136 - - [09/Apr/2023 17:43:07] "GET /u?AID=&GID=&CPM=14&ACPM=21.86&uSV=0.09 HTTP/1.1" 200 -
192.168.2.136 - - [09/Apr/2023 17:48:09] "GET /u?AID=&GID=&CPM=31&ACPM=22.10&uSV=0.20 HTTP/1.1" 200 -
192.168.2.136 - - [09/Apr/2023 17:53:11] "GET /u?AID=&GID=&CPM=25&ACPM=22.18&uSV=0.16 HTTP/1.1" 200 -
```

## ToDos

- [X] Forward measurements to gmcmap.com

## Links

- [GMC-500+ User Guide (DE)](http://www.gqelectronicsllc.com/download/GMC-500PlusUserGuideDE.pdf)
- [pygeiger](https://github.com/colon3ltocard/pygeiger)
