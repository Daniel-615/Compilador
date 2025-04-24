class interCodeGenerator:
    def __init__(self):
        self.temp_counter=0
        self.code=[]
    def new_temp(self):
        temp=f"t{self.temp_counter}"
        self.temp_counter+=1
        return temp
    def emit(self,instruction):
        self.code.append(instruction)
    def get_code(self):
        return self.code