#!/bin/bash

set -e

VOLUME_ADDONS="-v $(pwd)/addons:/mnt/extra-addons"
VOLUME_SRC="-v $(pwd):/usr/src"
VOLUME_CONFIG="-v $(pwd)/deploy/purple-drill-demo/config:/etc/odoo"
VOLUMES="$VOLUME_ADDONS $VOLUME_SRC $VOLUME_CONFIG"

LINKS="--link database:db"

DATA="--volumes-from purple-drill-store"

EXPOSE="-p 8069:8069"

CMD="docker run -ti --rm $LINKS $VOLUMES $DATA"

case "$1" in
    cli)
        shift
        exec $CMD purple-drill-demo -- $@
        ;;
    *)
        exec $CMD $EXPOSE purple-drill-demo $@
esac

exit 1
