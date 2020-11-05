#!/bin/bash
# run this in the root of the layer directory
export PKG_DIR="python"

rm -rf ${PKG_DIR} && mkdir -p ${PKG_DIR}
docker run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.8 \
    pip install -r requirements.txt -t ${PKG_DIR}
cp -r peloton ${PKG_DIR}


# docker run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.8 \
#     pip install -r requirements.txt --no-deps -t ${PKG_DIR}
