#!/bin/bash

set -e

case "$1" in
    cli)
        shift
        exec docker run -ti --rm \
            -v $(pwd)/addons:/mnt/extra-addons \
            -v $(pwd)/deploy/purple-drill-demo/config:/etc/odoo \
            --link database:db \
            --volumes-from purple-drill-store \
            purple-drill-demo -- $@
        ;;
    *)
        exec docker run -ti --rm -p 8069:8069 \
            -v $(pwd)/addons:/mnt/extra-addons \
            -v $(pwd)/deploy/purple-drill-demo/config:/etc/odoo \
            --link database:db \
            --volumes-from purple-drill-store \
            purple-drill-demo $@
esac

exit 1
