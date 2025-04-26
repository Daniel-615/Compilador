class interCodeGenerator:
    def __init__(self):
        self.temp_counter=0
        self.code=[]
        self.label_counter=0
    def new_temp(self):
        temp=f"t{self.temp_counter}"
        self.temp_counter+=1
        return temp
    def emit(self,instruction):
        print(f" [EMIT] {instruction}")
        self.code.append(instruction)
    def get_code(self):
        return self.code
    def new_label(self):
       label = f"L{self.label_counter}"
       self.label_counter += 1
       return label