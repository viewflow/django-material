from material import Application, Icon

from . import views


class Employees(Application):
    title = 'Employees'
    icon = Icon('people')
    menu_template_name = 'employees/app_menu.html'

    employee_viewset = views.EmployeeViewset()
    department_viewset = views.DepartmentViewset()
