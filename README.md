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
Content-Length: 298
Server: Werkzeug/0.16.0 Python/3.7.2
Date: Sat, 26 Oct 2019 23:48:39 GMT

{
  "artobjects": [
    {
      "coordinate": {
        "altitude": 0.0, 
        "latitude": 47.484257, 
        "longitude": 19.065508
      }, 
      "description": "Descr3", 
      "id": 1, 
      "imageURL": "http://localhost:7777/api/artobjects/body/1", 
      "title": "Object3"
    }
  ]
}

```



### Download Artobject image data

Endpoint with specified id (could be used ImageURI field from prev request)

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
        "altitude": 0.0, 
        "latitude": 47.484257, 
        "longitude": 19.065508
      }, 
      "description": "Descr3", 
      "id": 2, 
      "title": "Object3"
    }, 
    201
  ]
}

```

### Get all Feedback ids and imageUrls:

```
curl -i -H "Content-Type: application/json" -X GET http://<address>:<port>/api/feedback
```

### Download Feedback image data

```
curl -H GET http://<address>:<port>/api/feedback/body/<id>
```

### Upload new Feedback image to the server

```
curl -F 'image=@<path/to/image>' http://<address>:<port>/api/feedback'
```
