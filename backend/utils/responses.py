from rest_framework.response import Response

class DataResponse(Response):
    def __init__(self, data=None, status=None, error_message=None):
        if status and 400 <= status < 600:
            response_data = {
                'data': data,
                'success': False,
                'errorMessage': error_message or 'An error occurred.',
            }
        else:
            # If it's a success response, only include the data and success fields
            response_data = {
                'data': data,
                'success': True,
            }

        super().__init__(data=response_data, status=status)


def success_response(data=None, status=200):
    return DataResponse(data=data, status=status)

def error_response(error_message=None, status=400):
    return DataResponse(data=[], status=status, error_message=error_message)
