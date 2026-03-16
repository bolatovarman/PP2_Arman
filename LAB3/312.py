class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = float(base_salary)
    
    def totai_salary(self):
        return self.base_salary
        
class Manager(Employee):
    def __init__(self, name, base_salary,bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent
    def totai_salary(self):
        return self.base_salary * (1 + float(self.bonus_percent) / 100)
    
class Developer(Employee):
    def __init__(self, name, base_salary,completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects
    def totai_salary(self):
        return self.base_salary + float(self.completed_projects) * 500
    
class Intern(Employee):
    pass
    
data = input().split()
type = data[0]
name = data[1]
base_zp = data[2]
employee = Employee(name,base_zp)

if type == "Manager":
    employee = Manager(name , base_zp , data[3]) #Полиморфизм
    print(f"Name: {employee.name}, Total: {employee.totai_salary():.2f}")
elif type == "Developer":
    employee = Developer(name , base_zp , data[3])
    print(f"Name: {employee.name}, Total: {employee.totai_salary():.2f}")   
elif type == "Intern":
    employee = Intern(name , base_zp)
    print(f"Name: {employee.name}, Total: {employee.totai_salary():.2f}")  
    
         
    
