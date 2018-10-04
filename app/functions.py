import watson_developer_cloud

def watsonConnection(message, context, categoria):
    user = 'fe0ed9e8-fd96-405b-baee-3a0e8e6e95b1'
    pw = 'TPKMPYH21L3Q'
    wk = ''
    if(categoria == 'st'):
        wk = '85a2b90e-4d6c-42ef-9787-e269d38f2aad'
    else:
        wk = 'fc9f117a-f372-4f93-b932-bade81508504'
    assistant = watson_developer_cloud.AssistantV1(
        username=user,
        password=pw,
        version='2018-09-25'
    )

    response = assistant.message(
        workspace_id=wk,
        encoding='utf-8',
        input={
            'text': message
        },
		context= eval(context)
    ).get_result()

    return response
