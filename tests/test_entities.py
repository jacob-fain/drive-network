"""Tests for domain entities."""
import pytest
from src.entities import Partner, Company, Employee, Contact, Network


class TestPartner:
    """Tests for Partner class."""

    def test_create_partner(self):
        """Test creating a partner."""
        partner = Partner("Alice")
        assert partner.name == "Alice"

    def test_partner_repr(self):
        """Test partner string representation."""
        partner = Partner("Alice")
        assert repr(partner) == "Partner('Alice')"


class TestCompany:
    """Tests for Company class."""

    def test_create_company(self):
        """Test creating a company."""
        company = Company("Acme")
        assert company.name == "Acme"

    def test_company_repr(self):
        """Test company string representation."""
        company = Company("Acme")
        assert repr(company) == "Company('Acme')"


class TestEmployee:
    """Tests for Employee class."""

    def test_create_employee(self):
        """Test creating an employee."""
        employee = Employee("Bob", "Acme")
        assert employee.name == "Bob"
        assert employee.company_name == "Acme"

    def test_employee_repr(self):
        """Test employee string representation."""
        employee = Employee("Bob", "Acme")
        assert repr(employee) == "Employee('Bob', 'Acme')"


class TestContact:
    """Tests for Contact class."""

    def test_create_contact(self):
        """Test creating a contact."""
        contact = Contact("Bob", "Alice", "email")
        assert contact.employee_name == "Bob"
        assert contact.partner_name == "Alice"
        assert contact.contact_type == "email"

    def test_contact_repr(self):
        """Test contact string representation."""
        contact = Contact("Bob", "Alice", "email")
        assert repr(contact) == "Contact('Bob', 'Alice', 'email')"


class TestNetwork:
    """Tests for Network class."""

    def test_create_empty_network(self):
        """Test creating an empty network."""
        network = Network()
        assert len(network.partners) == 0
        assert len(network.companies) == 0
        assert len(network.employees) == 0
        assert len(network.contacts) == 0

    def test_add_partner(self):
        """Test adding a partner."""
        network = Network()
        network.add_partner("Alice")
        assert "Alice" in network.partners
        assert network.partners["Alice"].name == "Alice"

    def test_add_duplicate_partner(self):
        """Test that adding duplicate partner raises error."""
        network = Network()
        network.add_partner("Alice")
        with pytest.raises(ValueError, match="Partner 'Alice' already exists"):
            network.add_partner("Alice")

    def test_add_company(self):
        """Test adding a company."""
        network = Network()
        network.add_company("Acme")
        assert "Acme" in network.companies
        assert network.companies["Acme"].name == "Acme"

    def test_add_duplicate_company(self):
        """Test that adding duplicate company raises error."""
        network = Network()
        network.add_company("Acme")
        with pytest.raises(ValueError, match="Company 'Acme' already exists"):
            network.add_company("Acme")

    def test_add_employee(self):
        """Test adding an employee."""
        network = Network()
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        assert "Bob" in network.employees
        assert network.employees["Bob"].name == "Bob"
        assert network.employees["Bob"].company_name == "Acme"

    def test_add_employee_without_company(self):
        """Test that adding employee without company raises error."""
        network = Network()
        with pytest.raises(ValueError, match="Company 'Acme' does not exist"):
            network.add_employee("Bob", "Acme")

    def test_add_duplicate_employee(self):
        """Test that adding duplicate employee raises error."""
        network = Network()
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        with pytest.raises(ValueError, match="Employee 'Bob' already exists"):
            network.add_employee("Bob", "Acme")

    def test_add_contact(self):
        """Test adding a contact."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        network.add_contact("Bob", "Alice", "email")

        assert len(network.contacts) == 1
        contact = network.contacts[0]
        assert contact.employee_name == "Bob"
        assert contact.partner_name == "Alice"
        assert contact.contact_type == "email"

    def test_add_contact_without_employee(self):
        """Test that adding contact without employee raises error."""
        network = Network()
        network.add_partner("Alice")
        with pytest.raises(ValueError, match="Employee 'Bob' does not exist"):
            network.add_contact("Bob", "Alice", "email")

    def test_add_contact_without_partner(self):
        """Test that adding contact without partner raises error."""
        network = Network()
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        with pytest.raises(ValueError, match="Partner 'Alice' does not exist"):
            network.add_contact("Bob", "Alice", "email")

    def test_add_contact_invalid_type(self):
        """Test that invalid contact type raises error."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        with pytest.raises(ValueError, match="Invalid contact type 'meeting'"):
            network.add_contact("Bob", "Alice", "meeting")

    def test_add_contact_case_insensitive_type(self):
        """Test that contact types are case-insensitive."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")

        network.add_contact("Bob", "Alice", "Email")
        network.add_contact("Bob", "Alice", "CALL")
        network.add_contact("Bob", "Alice", "Coffee")

        assert len(network.contacts) == 3
        assert network.contacts[0].contact_type == "email"
        assert network.contacts[1].contact_type == "call"
        assert network.contacts[2].contact_type == "coffee"

    def test_multiple_contacts_same_pair(self):
        """Test that multiple contacts between same employee/partner are allowed."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")

        network.add_contact("Bob", "Alice", "email")
        network.add_contact("Bob", "Alice", "call")
        network.add_contact("Bob", "Alice", "email")

        assert len(network.contacts) == 3

    def test_get_contacts(self):
        """Test retrieving all contacts."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        network.add_contact("Bob", "Alice", "email")
        network.add_contact("Bob", "Alice", "call")

        contacts = network.get_contacts()
        assert len(contacts) == 2
        assert all(isinstance(c, Contact) for c in contacts)

    def test_complex_network(self):
        """Test a more complex network with multiple entities."""
        network = Network()

        # Add partners
        network.add_partner("Alice")
        network.add_partner("Bob")
        network.add_partner("Charlie")

        # Add companies
        network.add_company("Acme")
        network.add_company("Globex")

        # Add employees
        network.add_employee("Dave", "Acme")
        network.add_employee("Eve", "Acme")
        network.add_employee("Frank", "Globex")

        # Add contacts
        network.add_contact("Dave", "Alice", "email")
        network.add_contact("Dave", "Bob", "call")
        network.add_contact("Eve", "Alice", "coffee")
        network.add_contact("Frank", "Charlie", "email")

        assert len(network.partners) == 3
        assert len(network.companies) == 2
        assert len(network.employees) == 3
        assert len(network.contacts) == 4
