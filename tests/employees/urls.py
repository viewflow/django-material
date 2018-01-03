from material import Application, Icon

from . import views


class Employees(Application):
    title = 'Employees'
    icon = Icon('people')

    employee_viewset = views.EmployeeViewset()
    department_viewset = views.DepartmentViewset()
