from .base_settings import *
from .local_settings import *

STATIC_ROOT = os.path.join(BASE_DIR, "collected_static")

# For various emails (might be sent to users)
DEFAULT_FROM_EMAIL = "no.relpy@ifx.oglam.hasadna.org.il"

# For emails sent to admins:
# Default **from** address:
SERVER_EMAIL = "admin@ifx.oglam.hasadna.org.il"
# Subject-line prefix. Make sure to include the trailing space.
EMAIL_SUBJECT_PREFIX = "[IFX] "