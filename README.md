# Restful API server for ARtherapy project

## Getting Started

Server provides following API:

### Get all Artobjects without images:

```
curl -i -H "Content-Type: application/json" -X GET http://<address>:<port>/api/artobjects
```

Result:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 352
Server: Werkzeug/0.16.0 Python/3.7.2
Date: Sat, 26 Oct 2019 17:56:05 GMT

{
  "artobjects": [
    {
      "coordinate": {
        "ArtObject": [
          1
        ], 
        "altitude": 0.23, 
        "id": 1, 
        "latitude": 12.1, 
        "longitude": 42.2
      }, 
      "description": "Desct", 
      "id": 1, 
      "title": "Object1", 
      "uri": "http://192.168.0.248:7777/api/artobjects/body/1"
    }
  ]
}

```



### Download Artobject image data

Endpoint with specified id (could be used uri field from prev request)

```
curl -H GET http://<address>:<port>/api/artobjects/body/<id>
```

Result:

raw binary data file

### Upload new Artobject to the server

```
curl -F 'image=@<path/to/image>' -F 'metadata=@<path/to/json> http://<address>:<port>/api/artobjects'
```

Result:

```
{
  "artobject": [
    {
      "coordinate": {
        "ArtObject": [
          1
        ], 
        "altitude": 0.23, 
        "id": 1, 
        "latitude": 12.1, 
        "longitude": 42.2
      }, 
      "description": "Desct", 
      "id": 1, 
      "title": "Object1"
    }, 
    201
  ]
}
```
