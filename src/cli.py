"""Command-line interface for the network analyzer."""
import sys
from src.entities import Network
from src.analyzer import analyze_network


def parse_command(line: str, network: Network) -> None:
    """
    Parse and execute a single command line.

    Supported commands:
    - Partner <Name>
    - Company <Name>
    - Employee <Name> <CompanyName>
    - Contact <EmployeeName> <PartnerName> <ContactType>

    Args:
        line: Command string to parse
        network: Network instance to update
    """
    # Skip empty lines
    line = line.strip()
    if not line:
        return

    # Split command into parts and then process the command
    parts = line.split()
    command = parts[0]

    if command == "Partner":
        name = parts[1]
        network.add_partner(name)

    elif command == "Company":
        name = parts[1]
        network.add_company(name)

    elif command == "Employee":
        name = parts[1]
        company_name = parts[2]
        network.add_employee(name, company_name)

    elif command == "Contact":
        employee_name = parts[1]
        partner_name = parts[2]
        contact_type = parts[3]
        network.add_contact(employee_name, partner_name, contact_type)


def read_input(source) -> list[str]:
    """
    Read input lines from file or stdin.

    Args:
        source: File path string or None for stdin

    Returns:
        list[str]: Lines of input
    """
    if source is None:
        # Read from stdin
        return sys.stdin.readlines()
    else:
        # Read from file path
        with open(source, 'r') as f:
            return f.readlines()


def main() -> None:
    """Entry point for the CLI."""
    
    # Parse flags and determine input source
    args = sys.argv[1:]
    verbose = "--verbose" in args
    if verbose:
        args.remove("--verbose")
    input_source = args[0] if args else None

    # Read input
    lines = read_input(input_source)

    # Build network by parsing lines in the input
    network = Network()
    for line in lines:
        parse_command(line, network)

    # Analyze and print results
    result = analyze_network(network, verbose=verbose)
    print(result)


if __name__ == "__main__":
    main()
