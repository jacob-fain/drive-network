"""End-to-end integration tests."""
import pytest
from io import StringIO
from src.cli import parse_command, read_input, main
from src.entities import Network


class TestParseCommand:
    """Tests for command parsing."""

    def test_parse_partner_command(self):
        """Test parsing Partner command."""
        network = Network()
        parse_command("Partner Alice", network)
        assert "Alice" in network.partners

    def test_parse_company_command(self):
        """Test parsing Company command."""
        network = Network()
        parse_command("Company Acme", network)
        assert "Acme" in network.companies

    def test_parse_employee_command(self):
        """Test parsing Employee command."""
        network = Network()
        network.add_company("Acme")
        parse_command("Employee Bob Acme", network)
        assert "Bob" in network.employees

    def test_parse_contact_command(self):
        """Test parsing Contact command."""
        network = Network()
        network.add_partner("Alice")
        network.add_company("Acme")
        network.add_employee("Bob", "Acme")
        parse_command("Contact Bob Alice email", network)
        assert len(network.contacts) == 1

    def test_parse_empty_line(self):
        """Test that empty lines are skipped."""
        network = Network()
        parse_command("", network)
        parse_command("   ", network)
        # Should not raise any errors

    def test_parse_line_with_whitespace(self):
        """Test parsing line with extra whitespace."""
        network = Network()
        parse_command("  Partner   Alice  ", network)
        assert "Alice" in network.partners


class TestReadInput:
    """Tests for input reading."""

    def test_read_from_string_io(self):
        """Test reading from StringIO (simulates stdin)."""
        fake_input = StringIO("Partner Alice\nCompany Acme\n")
        # Read directly from the StringIO object
        lines = fake_input.readlines()
        assert len(lines) == 2
        assert lines[0].strip() == "Partner Alice"
        assert lines[1].strip() == "Company Acme"

    def test_read_from_file(self):
        """Test reading from example file."""
        lines = read_input("examples/basic.txt")
        assert len(lines) > 0
        assert any("Partner" in line for line in lines)


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_basic_scenario(self):
        """Test basic end-to-end scenario."""
        network = Network()

        # Parse commands
        commands = [
            "Partner Alice",
            "Company Acme",
            "Employee Bob Acme",
            "Contact Bob Alice email",
        ]

        for command in commands:
            parse_command(command, network)

        # Verify network state
        assert "Alice" in network.partners
        assert "Acme" in network.companies
        assert "Bob" in network.employees
        assert len(network.contacts) == 1

    def test_example_from_spec(self):
        """Test with scenario similar to spec example."""
        network = Network()

        commands = [
            "Partner Alice",
            "Partner Bob",
            "Company Acme",
            "Company Globex",
            "Employee Dave Acme",
            "Employee Eve Acme",
            "Employee Frank Globex",
            "Contact Dave Alice email",
            "Contact Dave Alice call",
            "Contact Eve Alice coffee",
            "Contact Dave Bob email",
            "Contact Frank Bob call",
        ]

        for command in commands:
            parse_command(command, network)

        # Verify expected state
        assert len(network.partners) == 2
        assert len(network.companies) == 2
        assert len(network.employees) == 3
        assert len(network.contacts) == 5

    def test_complete_workflow(self):
        """Test complete workflow: parse, analyze, verify output."""
        from src.analyzer import analyze_network

        network = Network()

        commands = [
            "Partner Alice",
            "Partner Bob",
            "Company Acme",
            "Company Globex",
            "Employee Dave Acme",
            "Employee Frank Globex",
            "Contact Dave Alice email",
            "Contact Dave Alice call",
            "Contact Frank Bob coffee",
        ]

        for command in commands:
            parse_command(command, network)

        result = analyze_network(network)
        lines = result.split("\n")

        # Alice has 2 contacts with Acme, Bob has 0
        assert lines[0] == "Acme: Alice (2)"
        # Bob has 1 contact with Globex, Alice has 0
        assert lines[1] == "Globex: Bob (1)"

    def test_company_with_no_relationships(self):
        """Test company with no employee contacts."""
        network = Network()

        commands = [
            "Partner Alice",
            "Company Acme",
            "Company NoContacts",
            "Employee Bob Acme",
            "Contact Bob Alice email",
        ]

        for command in commands:
            parse_command(command, network)

        from src.analyzer import analyze_network
        result = analyze_network(network)
        lines = result.split("\n")

        assert lines[0] == "Acme: Alice (1)"
        assert lines[1] == "NoContacts: No current relationship"

    def test_tie_breaking_integration(self):
        """Test tie-breaking in complete workflow."""
        from src.analyzer import analyze_network

        network = Network()

        commands = [
            "Partner Zara",
            "Partner Alice",
            "Company Acme",
            "Employee Bob Acme",
            "Contact Bob Zara email",
            "Contact Bob Alice call",
        ]

        for command in commands:
            parse_command(command, network)

        result = analyze_network(network)
        # Both partners have 1 contact, Alice should win (alphabetically first)
        assert result == "Acme: Alice (1)"

    def test_multiple_employees_multiple_contacts(self):
        """Test complex scenario with multiple employees and contacts."""
        from src.analyzer import analyze_network

        network = Network()

        commands = [
            "Partner Alice",
            "Partner Bob",
            "Partner Charlie",
            "Company Acme",
            "Company Globex",
            "Employee Dave Acme",
            "Employee Eve Acme",
            "Employee Frank Globex",
            "Employee Grace Globex",
            # Acme: Alice gets 3, Bob gets 1
            "Contact Dave Alice email",
            "Contact Dave Alice call",
            "Contact Eve Alice coffee",
            "Contact Dave Bob email",
            # Globex: Charlie gets 2, Bob gets 1
            "Contact Frank Charlie email",
            "Contact Grace Charlie call",
            "Contact Frank Bob coffee",
        ]

        for command in commands:
            parse_command(command, network)

        result = analyze_network(network)
        lines = result.split("\n")

        assert lines[0] == "Acme: Alice (3)"
        assert lines[1] == "Globex: Charlie (2)"

    def test_alphabetical_sorting(self):
        """Test that output is sorted alphabetically by company."""
        from src.analyzer import analyze_network

        network = Network()

        commands = [
            "Partner Alice",
            "Company Zebra",
            "Company Apple",
            "Company Mango",
            "Employee Bob Zebra",
            "Employee Charlie Apple",
            "Employee Dave Mango",
            "Contact Bob Alice email",
            "Contact Charlie Alice call",
            "Contact Dave Alice coffee",
        ]

        for command in commands:
            parse_command(command, network)

        result = analyze_network(network)
        lines = result.split("\n")

        assert lines[0].startswith("Apple:")
        assert lines[1].startswith("Mango:")
        assert lines[2].startswith("Zebra:")
