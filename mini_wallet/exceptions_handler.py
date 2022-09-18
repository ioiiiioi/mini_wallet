from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.data.get("detail", None):
            detail = response.data.pop('detail')
            response.data = {
                "status":"error",
                "data":{
                    "detail":detail
                }
            }
    return response
