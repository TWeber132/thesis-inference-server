# HTTP Client Workspace

Workspace for developing an HTTP client python package. 
Included is a simple client for making HTTP requests.

For the usage of the client, refer to the package's README in `src/http_client/README.md`.

## Build

Build the image:

```bash
./build_image.sh
```

Run the container:

```bash
./run_container.sh
```


Navigate to 'src/http_client':

```bash
cd src/http_client
```

Then you can build the package:

```bash
python -m build
```

This will create a `.whl` file in the `dist` directory.

## Install

You can install the package using pip:

```bash
pip install dist/http_client-0.0.1.tar.gz
```

You should also add `/home/$USER/.local/bin` to your PATH. You can also directly do this in your Dockerfile.
```bash
export PATH=$PATH:/home/$USER/.local/bin
```
