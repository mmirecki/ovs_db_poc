from ovs_db.compatibility.i18n import i18n

# Copied from: oslo_utils.importutils.import_class
import sys
import traceback


def import_class(import_str):
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str,
                           traceback.format_exception(*sys.exc_info())))

# Copied from: oslo_utils.executils.save_and_reraise_exception
import logging
import six


class save_and_reraise_exception(object):

    def __init__(self, reraise=True, logger=None):
        self.reraise = reraise
        if logger is None:
            logger = logging.getLogger()
        self.logger = logger
        self.type_, self.value, self.tb = (None, None, None)

    def force_reraise(self):
        if self.type_ is None and self.value is None:
            raise RuntimeError("There is no (currently) captured exception"
                               " to force the reraising of")
        six.reraise(self.type_, self.value, self.tb)

    def capture(self, check=True):
        (type_, value, tb) = sys.exc_info()
        if check and type_ is None and value is None:
            raise RuntimeError("There is no active exception to capture")
        self.type_, self.value, self.tb = (type_, value, tb)
        return self

    def __enter__(self):
        # TODO(harlowja): perhaps someday in the future turn check here
        # to true, because that is likely the desired intention, and doing
        # so ensures that people are actually using this correctly.
        return self.capture(check=False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if self.reraise:
                self.logger.error('Original exception being dropped: %s',
                                  traceback.format_exception(self.type_,
                                                             self.value,
                                                             self.tb))
            return False
        if self.reraise:
            self.force_reraise()

# Copied from: neutron.agent.common.utils
import os

# TODO: copy the code
if os.name == 'nt':
    from neutron.agent.windows import utils
else:
    from neutron.agent.linux import utils

execute = utils.execute

#########################################
# Copied from: oslo_utils.encodeutils

_getfilesystemencoding = sys.getfilesystemencoding


def safe_decode(text, incoming=None, errors='strict'):
    if not isinstance(text, (six.string_types, six.binary_type)):
        raise TypeError("%s can't be decoded" % type(text))

    if isinstance(text, six.text_type):
        return text

    if not incoming:
        incoming = (sys.stdin.encoding or
                    sys.getdefaultencoding())

    try:
        return text.decode(incoming, errors)
    except UnicodeDecodeError:
        return text.decode('utf-8', errors)


# Copied from: oslo_serialization.jsonutils
# TODO: only used in impl_vsctl, remove if we don't
import json


def loads(s, encoding='utf-8', **kwargs):
    return json.loads(safe_decode_json(s, encoding), **kwargs)


def safe_decode_json(text, incoming=None, errors='strict'):
    """Decodes incoming text/bytes string using `incoming` if they're not
       already unicode.

    :param incoming: Text's current encoding
    :param errors: Errors handling policy. See here for valid
        values http://docs.python.org/2/library/codecs.html
    :returns: text or a unicode `incoming` encoded
                representation of it.
    :raises TypeError: If text is not an instance of str
    """
    if not isinstance(text, (six.string_types, six.binary_type)):
        raise TypeError("%s can't be decoded" % type(text))

    if isinstance(text, six.text_type):
        return text

    if not incoming:
        incoming = (sys.stdin.encoding or
                    sys.getdefaultencoding())

    try:
        return text.decode(incoming, errors)
    except UnicodeDecodeError:
        # Note(flaper87) If we get here, it means that
        # sys.stdin.encoding / sys.getdefaultencoding
        # didn't return a suitable encoding to decode
        # text. This happens mostly when global LANG
        # var is not set correctly and there's no
        # default encoding. In this case, most likely
        # python will use ASCII or ANSI encoders as
        # default encodings but they won't be capable
        # of decoding non-ASCII characters.
        #
        # Also, UTF-8 is being used since it's an ASCII
        # extension.
        return text.decode('utf-8', errors)


# Copied from: oslo_utils.uuidutils
import uuid


# TODO: inline
def generate_uuid(self):
    return str(uuid.uuid4())


# Copied from: neutron_lib.exceptions
class NeutronException(Exception):

    message = i18n.translate("An unknown exception occurred.")

    def __init__(self, **kwargs):
        try:
            super(NeutronException, self).__init__(self.message % kwargs)
            self.msg = self.message % kwargs
        except Exception:
            with save_and_reraise_exception() as ctxt:
                if not self.use_fatal_exceptions():
                    ctxt.reraise = False
                    # at least get the core message out if something happened
                    super(NeutronException, self).__init__(self.message)

    if six.PY2:
        def __unicode__(self):
            return unicode(self.msg)

    def __str__(self):
        return self.msg

    def use_fatal_exceptions(self):
        """Is the instance using fatal exceptions.

        :returns: Always returns False.
        """
        return False


# Copied from: networking_ovn.common.utils
def ovn_name(id):
    # The name of the OVN entry will be neutron-<UUID>
    # This is due to the fact that the OVN application checks if the name
    # is a UUID. If so then there will be no matches.
    # We prefix the UUID to enable us to use the Neutron UUID when
    # updating, deleting etc.
    return 'neutron-%s' % id


# Copied from: neutron_lib.exceptions
class ServiceUnavailable(NeutronException):
    """A generic service unavailable exception."""
    message = i18n.translate("The service is unavailable.")


# Copied from: neutron_lib.helpers
def parse_mappings(mapping_list, unique_values=True, unique_keys=True):
    """Parse a list of mapping strings into a dictionary.

    :param mapping_list: A list of strings of the form '<key>:<value>'.
    :param unique_values: Values must be unique if True.
    :param unique_keys: Keys must be unique if True, else implies that keys
    and values are not unique.
    :returns: A dict mapping keys to values or to list of values.
    :raises ValueError: Upon malformed data or duplicate keys.
    """
    mappings = {}
    for mapping in mapping_list:
        mapping = mapping.strip()
        if not mapping:
            continue
        split_result = mapping.split(':')
        if len(split_result) != 2:
            raise ValueError(i18n.translate("Invalid mapping: '%s'") % mapping)
        key = split_result[0].strip()
        if not key:
            raise ValueError(i18n.translate("Missing key in mapping: '%s'") %
                             mapping)
        value = split_result[1].strip()
        if not value:
            raise ValueError(i18n.translate("Missing value in mapping: '%s'")
                             % mapping)
        if unique_keys:
            if key in mappings:
                raise ValueError(i18n.translate("Key %(key)s in mapping: "
                                                "'%(mapping)s' not unique") %
                                 {'key': key, 'mapping': mapping})
            if unique_values and value in mappings.values():
                raise ValueError(i18n.translate("Value %(value)s in mapping: "
                                                "'%(mapping)s' not unique") %
                                 {'value': value, 'mapping': mapping})
            mappings[key] = value
        else:
            mappings.setdefault(key, [])
            if value not in mappings[key]:
                mappings[key].append(value)
    return mappings
