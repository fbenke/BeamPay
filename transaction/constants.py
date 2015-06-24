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

# Bill Types
EGC_POSTPAID = 'ECG'
GWC_WATER = 'GWC'
DSTV = 'DST'
GOTV = 'GOT'
SURFLINE = 'SRF'
VODAFONE_BROADBAND = 'VOB'

# Gift Types
CAKE = 'CAKE'
FLOWERS = 'FLOW'
BASKET = 'BASK'
MISC = 'MISC'

GIFTS = (CAKE, FLOWERS, BASKET, MISC)

BILL = 'BILL'
AIRTIME = 'AIRTIME'

INSTANT_PAYMENTS = (BILL, AIRTIME)

TXN_TYPE_2_MODEL = {
    BILL: 'BillPayment',
    AIRTIME: 'AirtimeTopup'
}
