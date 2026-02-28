"""Tests for relationship analyzer."""
import pytest
from src.entities import Network
from src.analyzer import analyze_network


class TestAnalyzeNetwork:
    """Tests for the analyze_network function."""

    def test_single_company_single_partner(self):
        """Test simplest case: one company, one partner, one contact."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        network.add_contact("Bob", "Alice", "email")

        result = analyze_network(network)
        assert result == "Acme: Alice (1)"

    def test_multiple_contacts_same_partner(self):
        """Test that multiple contacts with same partner accumulate."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        network.add_contact("Bob", "Alice", "email")
        network.add_contact("Bob", "Alice", "call")
        network.add_contact("Bob", "Alice", "coffee")

        result = analyze_network(network)
        assert result == "Acme: Alice (3)"

    def test_multiple_employees_contribute_to_strength(self):
        """Test that contacts from different employees at same company count together."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        network.add_employee("Charlie", "Acme")
        network.add_contact("Bob", "Alice", "email")
        network.add_contact("Charlie", "Alice", "call")

        result = analyze_network(network)
        assert result == "Acme: Alice (2)"

    def test_strongest_partner_wins(self):
        """Test that partner with most contacts wins."""
        network = Network()
        network.add_partner("Alice")
        network.add_partner("Bob")
        network.add_company("Acme")
        network.add_employee("Dave", "Acme")
        network.add_contact("Dave", "Alice", "email")
        network.add_contact("Dave", "Alice", "call")
        network.add_contact("Dave", "Bob", "email")

        result = analyze_network(network)
        assert result == "Acme: Alice (2)"

    def test_tie_breaking_alphabetical(self):
        """Test that ties are broken alphabetically (first partner wins)."""
        network = Network()
        network.add_partner("Zara")  # Alphabetically last
        network.add_partner("Alice")  # Alphabetically first
        network.add_partner("Mike")  # Alphabetically middle
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        # All three partners have exactly 1 contact
        network.add_contact("Bob", "Zara", "email")
        network.add_contact("Bob", "Alice", "call")
        network.add_contact("Bob", "Mike", "coffee")

        result = analyze_network(network)
        assert result == "Acme: Alice (1)"

    def test_company_with_no_contacts(self):
        """Test that companies with no contacts show 'No current relationship'."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_company("NoContacts")
        network.add_employee("Bob", "Acme")
        network.add_contact("Bob", "Alice", "email")

        result = analyze_network(network)
        lines = result.split("\n")
        assert lines[0] == "Acme: Alice (1)"
        assert lines[1] == "NoContacts: No current relationship"

    def test_multiple_companies(self):
        """Test analysis with multiple companies."""
        network = Network()
        network.add_partner("Alice")
        network.add_partner("Bob")
        network.add_company("Acme")
        network.add_company("Globex")
        network.add_employee("Dave", "Acme")
        network.add_employee("Eve", "Globex")
        network.add_contact("Dave", "Alice", "email")
        network.add_contact("Eve", "Bob", "call")

        result = analyze_network(network)
        lines = result.split("\n")
        assert len(lines) == 2
        assert lines[0] == "Acme: Alice (1)"
        assert lines[1] == "Globex: Bob (1)"

    def test_alphabetical_company_sorting(self):
        """Test that companies are sorted alphabetically in output."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Zebra")
        network.add_company("Apple")
        network.add_company("Mango")
        network.add_employee("Bob", "Zebra")
        network.add_employee("Charlie", "Apple")
        network.add_employee("Dave", "Mango")
        network.add_contact("Bob", "Alice", "email")
        network.add_contact("Charlie", "Alice", "call")
        network.add_contact("Dave", "Alice", "coffee")

        result = analyze_network(network)
        lines = result.split("\n")
        assert lines[0].startswith("Apple:")
        assert lines[1].startswith("Mango:")
        assert lines[2].startswith("Zebra:")

    def test_empty_network(self):
        """Test network with companies but no employees or contacts."""
        network = Network()
        network.add_company("Acme")
        network.add_company("Globex")

        result = analyze_network(network)
        lines = result.split("\n")
        assert lines[0] == "Acme: No current relationship"
        assert lines[1] == "Globex: No current relationship"

    def test_no_companies(self):
        """Test network with no companies returns empty string."""
        network = Network()
        network.add_partner("Alice")

        result = analyze_network(network)
        assert result == ""

    def test_complex_scenario(self):
        """Test a complex realistic scenario with multiple entities."""
        network = Network()

        # Add partners
        network.add_partner("Alice")
        network.add_partner("Bob")
        network.add_partner("Charlie")

        # Add companies
        network.add_company("Acme")
        network.add_company("Globex")
        network.add_company("Initech")

        # Add employees
        network.add_employee("Dave", "Acme")
        network.add_employee("Eve", "Acme")
        network.add_employee("Frank", "Globex")
        network.add_employee("Grace", "Globex")

        # Acme: Alice has 3 contacts, Bob has 1 - Alice wins
        network.add_contact("Dave", "Alice", "email")
        network.add_contact("Dave", "Alice", "call")
        network.add_contact("Eve", "Alice", "coffee")
        network.add_contact("Dave", "Bob", "email")

        # Globex: Charlie has 2 contacts, Bob has 1 - Charlie wins
        network.add_contact("Frank", "Charlie", "email")
        network.add_contact("Grace", "Charlie", "call")
        network.add_contact("Frank", "Bob", "coffee")

        # Initech: No employees, no contacts

        result = analyze_network(network)
        lines = result.split("\n")
        assert lines[0] == "Acme: Alice (3)"
        assert lines[1] == "Globex: Charlie (2)"
        assert lines[2] == "Initech: No current relationship"


class TestAnalyzeNetworkVerbose:
    """Tests for verbose output in analyze_network."""

    def test_single_employee_single_type(self):
        """Test basic verbose output with one employee and one contact type."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        network.add_contact("Bob", "Alice", "email")

        result = analyze_network(network, verbose=True)
        lines = result.split("\n")
        assert lines[0] == "Acme: Alice (1)"
        assert lines[1] == "  - Bob: email (1)"

    def test_multiple_employees_multiple_types(self):
        """Test verbose output with multiple employees and types, sorted alphabetically."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Dave", "Acme")
        network.add_employee("Bob", "Acme")
        network.add_contact("Dave", "Alice", "call")
        network.add_contact("Dave", "Alice", "email")
        network.add_contact("Bob", "Alice", "coffee")

        result = analyze_network(network, verbose=True)
        lines = result.split("\n")
        assert lines[0] == "Acme: Alice (3)"
        assert lines[1] == "  - Bob: coffee (1)"
        assert lines[2] == "  - Dave: call (1), email (1)"

    def test_no_relationship_no_sublines(self):
        """Test that 'No current relationship' companies get no sub-lines in verbose mode."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_company("Empty")
        network.add_employee("Bob", "Acme")
        network.add_contact("Bob", "Alice", "email")

        result = analyze_network(network, verbose=True)
        lines = result.split("\n")
        assert lines[0] == "Acme: Alice (1)"
        assert lines[1] == "  - Bob: email (1)"
        assert lines[2] == "Empty: No current relationship"
        assert len(lines) == 3

    def test_multiple_companies_verbose(self):
        """Test full verbose output across multiple companies."""
        network = Network()
        network.add_partner("Alice")
        network.add_partner("Bob")
        network.add_company("Acme")
        network.add_company("Globex")
        network.add_employee("Dave", "Acme")
        network.add_employee("Eve", "Acme")
        network.add_employee("Frank", "Globex")
        network.add_contact("Dave", "Alice", "email")
        network.add_contact("Dave", "Alice", "call")
        network.add_contact("Eve", "Alice", "coffee")
        network.add_contact("Frank", "Bob", "call")

        result = analyze_network(network, verbose=True)
        lines = result.split("\n")
        assert lines[0] == "Acme: Alice (3)"
        assert lines[1] == "  - Dave: call (1), email (1)"
        assert lines[2] == "  - Eve: coffee (1)"
        assert lines[3] == "Globex: Bob (1)"
        assert lines[4] == "  - Frank: call (1)"

    def test_only_winning_partner_shown(self):
        """Test that only the winning partner's employee details are shown."""
        network = Network()
        network.add_partner("Alice")
        network.add_partner("Bob")
        network.add_company("Acme")
        network.add_employee("Dave", "Acme")
        network.add_contact("Dave", "Alice", "email")
        network.add_contact("Dave", "Alice", "call")
        network.add_contact("Dave", "Bob", "coffee")

        result = analyze_network(network, verbose=True)
        lines = result.split("\n")
        assert lines[0] == "Acme: Alice (2)"
        assert lines[1] == "  - Dave: call (1), email (1)"
        assert len(lines) == 2

    def test_repeated_contact_types_accumulate(self):
        """Test that repeated contact types have their counts accumulated."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        network.add_contact("Bob", "Alice", "email")
        network.add_contact("Bob", "Alice", "email")
        network.add_contact("Bob", "Alice", "call")

        result = analyze_network(network, verbose=True)
        lines = result.split("\n")
        assert lines[0] == "Acme: Alice (3)"
        assert lines[1] == "  - Bob: call (1), email (2)"

    def test_non_verbose_no_sublines(self):
        """Test that default (non-verbose) call still produces no sub-lines."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Dave", "Acme")
        network.add_employee("Eve", "Acme")
        network.add_contact("Dave", "Alice", "email")
        network.add_contact("Eve", "Alice", "coffee")

        result = analyze_network(network)
        lines = result.split("\n")
        assert len(lines) == 1
        assert lines[0] == "Acme: Alice (2)"
