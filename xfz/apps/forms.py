#定义一个公共的类,用来返回验证表单错误时返回的错误信息
class FormMixin(object):
    # 表单验证失败后返回错误信息
    def get_errors(self):
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            new_errors = {}
            for key, message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors