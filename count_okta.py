import requests

def get_count_from_okta(okta_token, okta_url, resource_path):
    """
    Generalized function to retrieve counts for different resources from Okta API.
    Handles pagination to ensure all resources are counted.
    """
    resource_url = f"{okta_url}/api/v1/{resource_path}"
    headers = {
        'Authorization': f"SSWS {okta_token}",
        'Content-Type': 'application/json'
    }
    total_count = 0

    while True:
        response = requests.get(resource_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            total_count += len(data)

            # Check for pagination link
            link_header = response.headers.get('Link', None)
            if link_header:
                links = link_header.split(', ')
                next_url = None
                for link in links:
                    if 'rel="next"' in link:
                        next_url = link[link.find("<")+1:link.find(">")]
                        break
                
                if next_url:
                    resource_url = next_url
                else:
                    break
            else:
                break
        else:
            print(f"Failed to retrieve {resource_path}: {response.status_code} {response.text}")
            break

    return total_count

def count_all_resources(okta_token, okta_url):
    resources = {
        'Groups': 'groups',
        'Applications': 'apps',
        'Group Rules': 'groups/rules',
        'Brands': 'brands',
        # Policy types
        'Access Policies': 'policies?type=ACCESS_POLICY',
        'Identity Provider Policies': 'policies?type=IDP_DISCOVERY',
        'Multifactor Enrollment Policies': 'policies?type=MFA_ENROLL',
        'Okta Sign On Policies': 'policies?type=OKTA_SIGN_ON',
        'Password Policies': 'policies?type=PASSWORD',
        'Profile Enrollment Policies': 'policies?type=PROFILE_ENROLLMENT',
        'Authorization Server Policies': 'authorizationServers/default/policies'
    }

    total_policies_count = 0
    for resource_name, resource_path in resources.items():
        count = get_count_from_okta(okta_token, okta_url, resource_path)
        print(f"{resource_name}: {count}")
        if "Policies" in resource_name:  # Sum up all policy types
            total_policies_count += count
    print(f"Total Policies Count: {total_policies_count}")

# Example usage
if __name__ == "__main__":
    okta_token = "YOUR_OKTA_TOKEN"
    okta_url = "https://YOUR_OKTA_TENANT.okta.com"
    
    count_all_resources(okta_token, okta_url)
