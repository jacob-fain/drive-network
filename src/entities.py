"""Domain entities for the network analyzer."""


class Partner:
    """A Drive Capital partner."""

    def __init__(self, name: str):
        """Initialize a partner.

        Args:
            name: Partner's name
        """
        self.name = name

    def __repr__(self):
        return f"Partner('{self.name}')"


class Company:
    """A portfolio or prospect company."""

    def __init__(self, name: str):
        """Initialize a company.

        Args:
            name: Company's name
        """
        self.name = name

    def __repr__(self):
        return f"Company('{self.name}')"


class Employee:
    """An employee at a company."""

    def __init__(self, name: str, company_name: str):
        """Initialize an employee.

        Args:
            name: Employee's name
            company_name: Name of the company where they work
        """
        self.name = name
        self.company_name = company_name

    def __repr__(self):
        return f"Employee('{self.name}', '{self.company_name}')"


class Contact:
    """A contact between an employee and a partner."""

    def __init__(self, employee_name: str, partner_name: str, contact_type: str):
        """Initialize a contact.

        Args:
            employee_name: Name of the employee
            partner_name: Name of the partner
            contact_type: Type of contact (email, call, coffee)
        """
        self.employee_name = employee_name
        self.partner_name = partner_name
        self.contact_type = contact_type

    def __repr__(self):
        return f"Contact('{self.employee_name}', '{self.partner_name}', '{self.contact_type}')"


class Network:
    """Central data structure managing all entities and relationships."""

    def __init__(self):
        """Initialize an empty network."""
        self.partners: dict[str, Partner] = {}
        self.companies: dict[str, Company] = {}
        self.employees: dict[str, Employee] = {}
        self.contacts: list[Contact] = []

    def add_partner(self, name: str) -> None:
        """Add a partner to the network.

        Args:
            name: Partner's name
        """
        if name in self.partners:
            raise ValueError(f"Partner '{name}' already exists")

        partner = Partner(name)    
        self.partners[name]

    def add_company(self, name: str) -> None:
        """Add a company to the network.

        Args:
            name: Company's name
        """
        if name in self.companies:
            raise ValueError(f"Company '{name}' already exists")
        
        company = Company(name)
        self.companies[name] = company

    def add_employee(self, name: str, company_name: str) -> None:
        """Add an employee to the network.

        Args:
            name: Employee's name
            company_name: Name of the company where they work
        """
        if name in self.employees:
            raise ValueError(f"Employee '{name}' already exists")
        if company_name not in self.companies:
            raise ValueError(f"Company '{company_name}' does not exist")

        employee = Employee(name, company_name)
        self.employees[name] = employee

    def add_contact(self, employee_name: str, partner_name: str, contact_type: str) -> None:
        """Record a contact between an employee and a partner.

        Args:
            employee_name: Name of the employee
            partner_name: Name of the partner
            contact_type: Type of contact (email, call, coffee)
        """
        if employee_name not in self.employees:
            raise ValueError(f"Employee '{employee_name}' does not exist")
        if partner_name not in self.partners:
            raise ValueError(f"Partner '{partner_name}' does not exist")

        valid_types = {'email', 'call', 'coffee'}
        if contact_type.lower() not in valid_types:
            raise ValueError(f"Invalid contact type '{contact_type}'. Must be email, call, or coffee")

        contact = Contact(employee_name, partner_name, contact_type.lower())
        self.contacts.append(contact)

    def get_contacts(self) -> list[Contact]:
        """Get all contacts in the network.

        Returns:
            List of all Contact objects
        """
        return self.contacts
