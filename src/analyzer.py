"""Relationship strength analysis logic."""
from src.entities import Network


def analyze_network(network: Network, verbose: bool = False) -> str:
    """
    Analyze partner-company relationships and return formatted output.

    For each company, finds the partner with the strongest relationship
    (most total contacts with all employees at that company).

    Args:
        network: Network instance containing all entities and contacts
        verbose: If True, include per-employee contact type breakdowns

    Returns:
        str: Formatted output showing strongest relationships, one company per line,
             sorted alphabetically by company name
    """
    # Count contacts for each (company, partner) pair
    company_partner_counts = {}

    for contact in network.get_contacts():

        # Find which company this employee works at
        employee = network.employees[contact.employee_name]
        company_name = employee.company_name
        partner_name = contact.partner_name

        # Initialize company dict if first time seeing this company
        if company_name not in company_partner_counts:
            company_partner_counts[company_name] = {}

        # Initialize partner count if first time seeing this partner for this company
        if partner_name not in company_partner_counts[company_name]:
            company_partner_counts[company_name][partner_name] = 0

        # Increment the contact count
        company_partner_counts[company_name][partner_name] += 1

    # Build output for each company (sorted alphabetically)
    results = []
    for company_name in sorted(network.companies.keys()):
        if company_name in company_partner_counts:

            # Company has contacts - find the partner with most contacts
            partner_counts = company_partner_counts[company_name]

            # Find the maximum count
            max_count = max(partner_counts.values())

            # Get all partners with the max count (handles ties)
            best_partners = []
            for partner, count in partner_counts.items():
                if count == max_count:
                    best_partners.append(partner)

            # If multiple partners tied, pick first alphabetically
            best_partners.sort()
            best_partner = best_partners[0]

            results.append(f"{company_name}: {best_partner} ({max_count})")

            if verbose:
                # Collect employee/contact-type details for the winning partner
                employee_details = {}
                for contact in network.get_contacts():
                    emp = network.employees[contact.employee_name]
                    if emp.company_name == company_name and contact.partner_name == best_partner:
                        if contact.employee_name not in employee_details:
                            employee_details[contact.employee_name] = {}
                        types = employee_details[contact.employee_name]
                        types[contact.contact_type] = types.get(contact.contact_type, 0) + 1

                for emp_name in sorted(employee_details.keys()):
                    type_counts = employee_details[emp_name]
                    type_parts = [f"{ct} ({type_counts[ct]})" for ct in sorted(type_counts.keys())]
                    results.append(f"  - {emp_name}: {', '.join(type_parts)}")
        else:
            # Company has no contacts
            results.append(f"{company_name}: No current relationship")

    return "\n".join(results)
