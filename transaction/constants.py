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
FRAUDULENT = 'FRUD'  # Error during payment

TRANSACTION_STATES = (
    INIT,
    GATHERING_INFO,
    READY_FOR_PAYMENT,
    PAID,
    PROCESSED,
    CANCELLED,
    FRAUDULENT,
    INVALID
)

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

# Bill Decriptions
EGC_POSTPAID_DESC = 'ECG (electricity)'
GWC_WATER_DESC = 'GWC (water)'
DSTV_DESC = 'DStv'
GOTV_DESC = 'GOtv'
SURFLINE_DESC = 'surfline'
VODAFONE_BROADBAND_DESC = 'Vodafone Broadband'

BILL_2_DESC = {
    EGC_POSTPAID: EGC_POSTPAID_DESC,
    GWC_WATER: GWC_WATER_DESC,
    DSTV: DSTV_DESC,
    GOTV: GOTV_DESC,
    SURFLINE: SURFLINE_DESC,
    VODAFONE_BROADBAND: VODAFONE_BROADBAND_DESC,
}

# Gift Types
CAKE = 'CAKE'
FLOWERS = 'FLOW'
BASKET = 'BASK'
MISC = 'MISC'

GIFTS = (CAKE, FLOWERS, BASKET, MISC)

AIRTIME = 'AIRTIME'
BILL = 'BILL'
SCHOOL = 'SCHOOL'
GIFT = 'GIFT'
VALET = 'VALET'

AIRTIME_MODEL = 'AirtimeTopup'
BILL_MODEL = 'BillPayment'
SCHOOL_MODEL = 'SchoolFeePayment'
GIFT_MODEL = 'Gift'
VALET_MODEL = 'ValetTransaction'

TRANSACTION_MODELS = (
    AIRTIME_MODEL,
    BILL_MODEL,
    SCHOOL_MODEL,
    GIFT_MODEL,
    VALET_MODEL
)

INSTANT_PAYMENTS = (BILL, AIRTIME)
INSTANT_PAYMENT_MODELS = (BILL_MODEL, AIRTIME_MODEL)

TXN_TYPE_2_MODEL = {
    AIRTIME: AIRTIME_MODEL,
    BILL: BILL_MODEL,
    SCHOOL: SCHOOL_MODEL,
    GIFT: GIFT_MODEL,
    VALET: VALET_MODEL
}
