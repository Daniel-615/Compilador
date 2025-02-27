import os
import webbrowser
class errors:
    def __init__(self,error,message):
        self.error = {
            'error': error,
            'message': message
        }

    def get_error(self, error, message):
        self.error['error'] = error
        self.error['message'] = message
        return self.error
    def errorHtml(self):
        """Return lexic and sintactic errors as HTML."""
        html= '<div style="border: 1px solid red; padding: 10px; margin: 10px; background-color: #f8d7da; color: #721c24;">'
        html+= '<strong>Error:</strong> {self.error["error"]}<br>'
        html+= '<strong> Message:</strong> {self.error["message"]}'
        html+= '</div>'

        os.makedirs('templates',exist_ok=True)
        
        file_path=os.path.join('templates',errors.html)
        with open(file_path,'w') as file:
            file.write(html)
        
        webbrowser.open('file://' + os.path.realpath(file_path))
        
        return html