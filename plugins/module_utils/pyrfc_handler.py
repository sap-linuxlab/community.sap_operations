#!/usr/bin/env python

import pyrfc


def get_connection(module, conn_params):
  module.warn('Connecting ... %s' % conn_params['ashost'])
  if "saprouter" in conn_params:
    module.warn("...via SAPRouter to SAP System")
  elif "gwhost" in conn_params:
    module.warn("...via Gateway to SAP System")
  else:
    module.warn("...direct to SAP System")

  conn = pyrfc.Connection(**conn_params)

  module.warn("Verifying connection is open/alive: %s" % conn.alive)
  return conn
