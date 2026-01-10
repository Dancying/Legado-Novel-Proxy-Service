# Legado-Novel-Proxy-Service

A simple book source proxy project.  


## Installation

You can deploy this project using the automatic installation script or via Podman containerization.  


### Method 1: Automatic Installation Script

Run the following code to deploy this project directly on your system:  

```sh
sudo curl -fsSL "https://raw.githubusercontent.com/Dancying/Legado-Novel-Proxy-Service/refs/heads/main/install.sh" | sudo sh
```


### Method 2: Podman Deployment

If you prefer using containers, follow these steps to build and run the service.  


#### 1. Build the Image

Execute the following command in the project root directory. You can customize the `BASE_URL` and `API_PREFIX` arguments as needed:  

```sh
podman build \
  --build-arg BASE_URL="https://api.dancying.cn" \
  --build-arg API_PREFIX="/legado" \
  -t localhost/novel-service:latest .
```


#### 2. Run the Container

Start the container using the following command:  

```sh
podman run -d \
  --name novel-service \
  -v novel-service:/novel/temp:Z \
  -p 39966:39966 \
  --shm-size=1g \
  --log-opt max-size=20mb \
  --log-opt max-file=3 \
  localhost/novel-service:latest
```

> **Note**: This maps the container's internal port `39966` to the host port `39966`.  


### Nginx Reverse Proxy Setup (Optional)

To expose the service via Nginx, add the following location block to your server configuration:  

```nginx
location /legado/ {
    proxy_pass http://127.0.0.1:39966;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```


## License

This project uses the MIT license.  

```text
MIT License

Copyright (c) 2025 Dancying

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
