# nova-log-parser
Task to parse nova logs using functional programming style and Python

LOGGING FORMATTERS
Format string to use for log messages with context. (string value)
logging_context_format_string=%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(request_id)s %(user_identity)s] %(instance)s%(message)s

Format string to use for log messages when context is undefined. (string
value)
logging_default_format_string=%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s

Additional data to append to log message when logging level for the message is
DEBUG. (string value)
logging_debug_format_suffix=%(funcName)s %(pathname)s:%(lineno)d

Prefix each line of exception output with this format. (string value)
logging_exception_prefix=%(asctime)s.%(msecs)03d %(process)d ERROR %(name)s %(instance)s

Defines the format string for %(user_identity)s that is used in
logging_context_format_string. (string value)
logging_user_identity_format=%(user)s %(tenant)s %(domain)s %(user_domain)s %(project_domain)s