import logging

class SafeFormatter(logging.Formatter):

    DEFAULTS = {
        "client_ip": "N/A",
        "path": "N/A",
        "method": "N/A",
        "status_code": 0,
        "error_type": "N/A"
    }

    def format(self, record):

        for key, value in self.DEFAULTS.items():
            if not hasattr(record, key):
                setattr(record, key, value)

        return super().format(record)