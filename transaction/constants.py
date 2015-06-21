# Error Messages
INVALID_PARAMETERS = '0'
PRICING_EXPIRED = '1'
PROFILE_INCOMPLETE = '2'

# Transaction States
INIT = 'INIT'  # Initialized by sender
GATHERING_INFO = 'INFO'  # Additional info required
READY_FOR_PAYMENT = 'REDY'  # Payment link sent
PAID = 'PAID'  # Paid by sender
PROCESSED = 'PROC'  # Fulfillment completed by Beam
CANCELLED = 'CANC'  # Could not be completed
INVALID = 'INVD'  # Error during payment

# Telco Providers
VODAFONE = 'VOD'
AIRTEL = 'AIR'
MTN = 'MTN'
TIGO = 'TIG'


# Payment Processors
STRIPE = 'STRP'
PAYPAL = 'PAYP'
WEPAY = 'WPAY'
