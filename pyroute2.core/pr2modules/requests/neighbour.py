from socket import AF_INET

from pr2modules.common import get_address_family
from pr2modules.netlink.rtnl.ndmsg import NUD_PERMANENT, ndmsg


class NeighbourFieldFilter:
    def set_index(self, context, value):
        return {'ifindex': value}

    def _state(self, value):
        if isinstance(value, str):
            value = ndmsg.states_a2n(self['state'])
        return {'state': value}

    def set_nud(self, context, value):
        return self._state(value)

    def set_state(self, context, value):
        return self._state(value)

    def finalize_for_iproute(self, context, cmd_context):
        if cmd_context not in ('dump', 'get'):
            if 'state' not in context:
                context['state'] = NUD_PERMANENT
        if 'dst' in context and 'family' not in context:
            context['family'] = get_address_family(context['dst'])
        if 'family' not in context:
            context['family'] = AF_INET
