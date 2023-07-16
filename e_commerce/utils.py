from kavenegar import *

def send_otp_code(phone, code):
    try:
        api = KavenegarAPI('374E53487A574D682B4E71754553704265346A6C6B39766B2F454D76646F7379484B41473570547A414A4D3D')
        params = {
            'receptor': phone,
            'template': 'Otp',
            'token': code
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)